# source/settings.py
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # settings.py 위치 기준으로 프로젝트 루트 계산

# Pydantic BaseSettings 로 통합 관리 : 실무에서 가장 권장되는 방식
# 민감/비민감 정보를 나누되, 한 군데에서 타입 검증까지 하면서 관리하는 방식
class Settings(BaseSettings):
    # ── 민감 정보 (반드시 .env에서 채워져야 함, 기본값 없음) ──
    
    langsmith_tracing: bool = False
    langsmith_endpoint: str
    langsmith_api_key: str | None = None  # 선택적 (트레이싱 안 쓰면 None)
    langsmith_project: str = "default"

    # ── LLM Provider 선택 ──
    llm_provider: Literal["google", "ollama"] = "google"
    
    # google 설정
    google_model: str = "gemini-3.1-flash-lite"
    google_api_key: str | None = None

    # ollama 설정
    ollama_model: str = "gemma4:e2b-mlx"
    ollama_base_url: str = "http://localhost:11434"

    # indexing 관련 설정
    embedding_model: str = "models/gemini-embedding-001"
    persist_dir: str = "../chroma_db"

    til_collection: str = "sian-til"
    md_path: str = "./sian-til/*.md"
    md_dir_path: str = "./sian-til"

    eval_dataset_name: str = "sian-til-rag-eval"

    # ── 설정 로드 방식 지정 ──
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   # OPENAI_API_KEY, openai_api_key 둘 다 인식
        extra="ignore",         # .env에 정의 안 된 필드는 무시
    )

    @model_validator(mode="after")
    def check_provider_requrements(self) -> "Settings":
        """선택된 provider에 필요한 값이 채워졌는지 검증"""
        if self.llm_provider == "google" and not self.google_api_key:
            raise ValueError(
                "LLM_PROVIDER=google인데 GOOGLE_API_KEY가 설정되지 않았습니다. "
                ".env 파일을 확인하세요."
            )
        # ollama는 로컬 서빙이라 API 키가 필요 없으므로 별도 검증 없음
        return self


# 앱 전체에서 재사용할 싱글턴 인스턴스
settings = Settings()