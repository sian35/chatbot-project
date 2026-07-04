# src/rag/chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough #, RunnableParallel

from src.dataset.vector_store import build_retriever
from src.model import build_llm

#retriever는 문자열을 받아 List[Document]를 돌려주므로, 
# 프롬프트에 넣기 전에 한 덩어리 문자열로 합치는 포맷 함수를 한 번 거쳐야 합니다
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs) # 하나의 긴 문자열로 포맷

def format_docs_with_source(docs):
    return "\n\n".join(f"[source {d.metadata.get('source')}] {d.page_content}" for d in docs)

def format_docs_with_source2(docs):
    lines = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        lines.append(f"[{i}] source={source}\n{doc.page_content}")
    return "\n\n".join(lines)

def build_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system",
        "다음 문서만을 근거로 사용자 질문에 답하세요. "
        "근거가 부족하면 '주어진 자료에서는 확인할 수 없습니다. '라고 답하세요. "
        "답변 끝에는 참고한 출처를 표시하세요. \n\n"
        "{context}"),
        ("human", "{question}"),
    ])
    return prompt

def build_rag_chain():
    print("[INFO] Start RAG Pipeline")
    # ===== 1. 저장된 크로마 디비 가져옴 =====
    #vectorstore = build_vector_store()
    retriever = build_retriever()

    # Augmented Generation을 위한 Prompt 구성
    prompt = build_prompt()

    # 답변 생성 LLM
    llm = build_llm()
    
    # LCEL chain (original)
    rag = (
        {"context": retriever | format_docs_with_source, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    ''' 이해가 필요함
    # 답변 생성용 체인 (docs를 문자열로 합친 뒤 LLM 호출)
    answer_chain = (
        {"context": lambda x: format_docs_with_source(x["docs"]),
         "question": lambda x: x["question"]}
        | prompt
        | llm
        | StrOutputParser()
    )
    # 최종 체인: 문서를 한번만 검색해서 답과 출처에 동시 사용
    rag = RunnableParallel(
        docs=retriever,
        question=RunnablePassthrough(),
    ).assign(answer=answer_chain)
    '''
    print("[INFO] RAG 파이프라인 완료\n")
    return rag

