## chatbot-project

### 파일 구조
```
chatbot-project/
├── doc/            회고 기록
├── sian-til/       md 파일 목록
├── src/
│    ├── dataset/
│    │   ├── data_loader.py   
│    │   ├── eval_dataset.py    Evaluation Dataset
│    │   └── vector_store.py    Retriever
│    ├── rag/
│    │   ├── chain.py           Lang Chain
│    │   └── graph.py           Lang Graph
│    ├── eval.py                LangSmith 평가
│    └── prompts.py             LangGraph
├──── main.py
└──── settings.py
```
---
### 실행 방법