#chatbot-project/test.py
import argparse

from src.rag.chain import build_rag_chain
from src.eval import eval_rag

def main():
    print("Hello from rag-project!")
    
    parser = argparse.ArgumentParser(description="LangChain")
    parser.add_argument('--mode', choices=['chaintest','eval'], help='Choose mode: LangChainTest, LangSmithEval')
    args = parser.parse_args()

    if args.mode == "chaintest":
        keyword = input("TIL에서 알고 싶은 개념을 입력하세요: ")
        q = f"{keyword}란 무엇인가요?"
        print(f"Sample Question: {q}\n")
        
        rag = build_rag_chain()
        result = rag.invoke(q)

        print(f"Answer with source: \n{result}")
        print()
        
    elif args.mode == "eval":
        rag = build_rag_chain()
        eval_result = eval_rag(rag)
        print("LangSmith Evaluation")
        print(f"{eval_result}")
    
if __name__ == "__main__":
    main()
