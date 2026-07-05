## chatbot-project
### 프로젝트 과정
| week | 과제 | 진행 |
|:---:|---|:---:|
|5| 다음 단어를 생성하는 Transformer Model을 이용해 챗봇을 구현한다.|✅|
|6| 개인 프로젝트의 바닐라 RAG 시스템을 구현한다. |✅|
|7| 개인 프로젝트의 RAG 시스템을 LangChain 기반으로 구현한다.|✅|
|8| 개인 프로젝트의 RAG 시스템을 LangGraph 기반으로 구현한다.|✅|
### 파일 구조
```
chatbot-project/
├── docs/            회고 기록
├── sian-til/        md 파일 목록
├── src/
│    ├── dataset/
│    │   ├── data_loader.py     Load Documents
│    │   ├── eval_dataset.py    Evaluation Dataset
│    │   └── vector_store.py    Retriever
│    ├── rag/
│    │   ├── chain.py           Lang Chain
│    │   └── graph.py           Lang Graph
│    ├── eval.py                LangSmith Evaluation
│    └── prompts.py             Prompts
├──── main.py                   REST API
├──── test.py                   run test
└──── settings.py               settings
```
---
### 초기 세팅
1. `.env` ← 설정
```
LANGSMITH_TRACING=
LANGSMITH_ENDPOINT=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=

# LLM 선택: google (기본) 또는 ollama
LLM_PROVIDER=google


# google 사용 시 모델명 (선택)
GOOGLE_MODEL=gemini-3.1-flash-lite
GOOGLE_API_KEY=
# ollama 사용 시 설정 (gemma4:e2b-mlx 가 ollama로 서빙되어야 함)
OLLAMA_MODEL=gemma4:e2b-mlx
OLLAMA_BASE_URL=http://localhost:11434
```

2. `uv sync` ← 의존성 설치  
(ollama 사용시)  
3. `ollama serve` ← 서버 띄우기
4. `ollama pull` ← 올라마 모델 다운로드

---
### 실행 방법
> 프로젝트 루트 위치에서 실행하기  

FastAPI 
```
uvicorn main:app ← 스웨거 문서로 확인 http://localhost:8000/docs
```

FastAPI 없이 단일 쿼리 테스트 또는 LangSmith 평가 테스트
```
uv run test.py --mode chain     # LangChain 단일 쿼리 테스트
uv run test.py --mode graph     # LangGraph 단일 쿼리 테스트
uv run test.py --mode smith     # LangSmith 평가 테스트

```