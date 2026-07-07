#chatbot-project/test.py
import argparse

from langchain_core.messages import HumanMessage

from src.rag.chain import build_rag_chain
from src.rag.graph import build_rag_graph
from src.eval import eval_rag

def main():
    parser = argparse.ArgumentParser(description="LangChain")
    parser.add_argument('--mode', choices=['smith', 'chain', 'graph'], help='Choose mode: LangChain, LangGraph, LangSmith')
    args = parser.parse_args()

    print("Hello from rag-project!")
    print(f"{args.mode} mode selected!")

    if args.mode == "smith":
        rag = build_rag_chain()
        eval_result = eval_rag(rag)
        print("LangSmith Evaluation")
        print(f"{eval_result}")
    
    else:
        keyword = input("TIL에서 알고 싶은 개념을 입력하세요: ")
        q = f"{keyword}란 무엇인가요?"
        print(f"Sample Question: {q}\n")

        if args.mode == "chain":
            rag = build_rag_chain()
            result = rag.invoke(q)

            print(f"Answer:\n{result}")
            print()
            
        elif args.mode == "graph":
            config = {"configurable": {"thread_id":"memory-user-001"}}
            graph = build_rag_graph()
            result = graph.invoke(
                {"messages": [HumanMessage(content=q)]},
                config  # checkpointer 사용중이라 필수
            )
            answer = result["messages"][-1].content

            print(f"Answer:\n{answer}")
            print()
    
if __name__ == "__main__":
    main()
