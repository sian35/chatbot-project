# src/rag/graph.py
from typing import TypedDict, Annotated
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from src.prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_LOCAL
from src.dataset.vector_store import build_retriever
from src.model import build_llm
from src.settings import settings

class State(TypedDict):
    messages: Annotated[list, add_messages] # add_messages: reducer- 자동으로 리스트에 새로운 메시지를 append
    context: list[Document] #reducer가 없으므로 노드가 반환하는 값으로 덮어쓰기된다. 매 질문마다 새로 검색한 문서로 교체

def build_rag_graph():
    retriever = build_retriever()
    llm = build_llm()
    
    if settings.llm_provider == "ollama":
        prompt = SYSTEM_PROMPT_LOCAL
    else:
        prompt = SYSTEM_PROMPT

    def format_docs(docs):# 여러 개의 Document 객체를 하나의 긴 문자열로 합친다.
        return "\n\n".join(doc.page_content for doc in docs)    # 서로 다른 문서에서 온 내용임을 표시하기 위해 \n\n 사용
    
    def format_docs_src(docs):  # 출처가 포함된 context로 만들어준다.
        return "\n\n".join( # 출처를 받아오는데 경로 전체가 오기 때문에, Path객체로 변환 후 파일명만 추출한다.
            f"[source: {Path(doc.metadata.get('source', 'unknown')).name}]\n{doc.page_content}" for doc in docs
        )
    
    def extract_text(content) -> str:
        # gemini 모델이 응답을 content block으로 반환하기 때문에 llm provider에 구애받지 않고 content를 일관된 문자열로 통일
        if isinstance(content, str):    #이미 str이라면 그대로 반환
            return content
        if isinstance(content, list):
            return "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
        return str(content) #예상 밖의 형태라면 str로 강제로 변환 : 방어선 코드
    
    def retrieve(state: State):
        question = state["messages"][-1].content        #대화 이력 중 가장 최신 메시지를 질문으로 설정해서 검색기에 넣는다.
        return {"context": retriever.invoke(question)}  #검색 결과(Document 리스트)를 context에 담아서 반환한다.

    def generate(state: State):
        docs = state["context"]
        #검색된 문서들을 하나의 문자열로 합쳐서(format_docs), 시스템 프롬프트의 {context}로 끼워넣는다.
        system_message = SystemMessage(
            content=prompt.format(context=format_docs(docs)) 
        )
        # 시스템 메시지 + 전체 대화 이력을 LLM에 넣어 응답 생성. (멀티턴 대화 맥락 유지)
        # 전체 대화 이력: 리스트 그대로가 아닌 리스트 안의 요소들을 하나씩 풀어서 넣는다 (unpacking) # [system_message, HumanMessage("질문1"), AIMessage("답변1"), HumanMessage("질문2")]
        response = llm.invoke([system_message, *state["messages"]])

        # 어떤 응답이든 str로 변환하기
        response_text = extract_text(response.content)

        if settings.llm_provider == "ollama":
            # 출처 직접 추가
            sources = sorted(set(
                Path(doc.metadata.get('source','unknown')).name for doc in docs
            ))
            source_text = "\n\n[출처] " + ",".join(sources) # [출처] 모든 소스들 연결
            response_text += source_text    # response_text의 맨 마지막에 source_text 추가


        response.content = response_text
        return {"messages": [response]} # 새로 생성된 응답 메시지 하나만 반환하면, reducer가 자동으로 기존 이력 뒤에 append
    
    builder = StateGraph(State)
    builder.add_node("retrieve", retrieve)
    builder.add_node("generate", generate)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    # END와 연결하지 않은 이유가 있나? => END 작성 이유: 가독성, 유지보수성
    builder.add_edge("generate", END)

    return builder.compile(checkpointer=MemorySaver())
