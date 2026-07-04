## Week8
| # | 과제 | 진행 |
|:---:|---|:---:|
|1| 개인 프로젝트의 랭체인 기반을 랭그래프 기반으로 바꾼다.|✅|
|2| (선택) 기능적으로 RAG 이상의 기능을 추가해보라.|🔜|

---
### 파일 구조
```
chatbot-project/
├── doc/                        회고 기록
├── src/
│    ├── dataset/
│    │   ├── eval_dataset.py    Evaluation Dataset
│    │   └── vector_store.py    Retriever
│    ├── eval.py                LangSmith 평가
│    ├── graph.py
│    └── prompts.py             LangGraph
├──── main.py
└──── settings.py
```
---