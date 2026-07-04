# source/graph.py
from typing import TypedDict, Annotated
from source.rag import build_retriever, build_llm
from source.prompts import SYSTEM_PROMPT

from langchain_core.documents import Document
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages] # add_messages: reducer- 자동으로 리스트에 새로운 메시지를 append
    context: list[Document] #reducer가 없으므로 노드가 반환하는 값으로 덮어쓰기된다. 매 질문마다 새로 검색한 문서로 교체

def build_rag_graph():
    retriever = build_retriever()
    llm = build_llm()

    def format_docs(ds):# 하나의 긴 문자열로 포맷
        return "\n\n".join(d.page_content for d in ds)
    
    def retrieve(state: State):
        question = state["messages"][-1].content        #대화 이력 중 가장 최신 메시지를 질문으로 설정해서 검색기에 넣는다.
        return {"context": retriever.invoke(question)}  #검색 결과(Document 리스트)를 context에 담아서 반환한다.

    def generate(state: State):
        system_message = SystemMessage(
            content=SYSTEM_PROMPT.format(context=format_docs(state["context"])) #검색된 문서들을 하나의 문자열로 합쳐서(format_docs), 시스템 프롬프트에 context로 끼워넣는다.
        )
        response = llm.invoke([system_message, *state["messages"]])# 시스템 메시지 + 전체 대화 이력을 LLM에 넣어 응답 생성. (멀티턴 대화 맥락 유지)
        return {"messages": [response]} # 이렇게 반환하면 add_messages reducer가 자동으로 대화 이력에 추가한다.
    
    builder = StateGraph(State)
    builder.add_node("retrieve", retrieve)
    builder.add_node("generate", generate)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    # END와 연결하지 않은 이유가 있나? => END 작성 이유: 가독성, 유지보수성
    builder.add_edge("generate", END)

    return builder.compile(checkpointer=MemorySaver())
