## chatbot-project

### 파일 구조
```
chatbot-project/
├── doc/            회고 기록
├── sian-til/       md 파일 목록
├── src/
│    ├── dataset/
│    │   ├── data_loader.py     Load Documents
│    │   ├── eval_dataset.py    Evaluation Dataset
│    │   └── vector_store.py    Retriever
│    ├── rag/
│    │   ├── chain.py           Lang Chain
│    │   └── graph.py           Lang Graph
│    ├── eval.py                LangSmith Evaluation
│    └── prompts.py             LangGraph
├──── main.py
├──── test.py                   run test
└──── settings.py               settings
```
---
### 실행 방법
#### 초기 세팅
1. `.env` 설정
2. `uv sync`
3. `uv run python -m src.dataset.build_vector_store`  ← 벡터 스토어 생성
4. `ollama` ← ollama 실행
4. `uv run main.py`

#### 
```
uvicorn main:app
스웨거 문서로 확인
http://localhost:8000/docs
```