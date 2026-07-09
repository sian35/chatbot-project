
from langchain_google_genai import ChatGoogleGenerativeAI

from src.settings import settings

#load_dotenv()

def build_embedding():
    print("[INFO] ---- Build Embedding model ---- ")
    # Embedding model
    provider = settings.embedding_provider.lower()
    print(f"[INFO] Embedding Provider: {provider}")
    if settings.embedding_provider == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )
    else:
        from langchain_huggingface import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(
        model_name=settings.hugging_embedding,
        encode_kwargs={"normalize_embeddings": True}
    )

    return embeddings


def build_llm():
    print("[INFO] ---- Build LLM ---- ")
    provider = settings.llm_provider.lower()
    print(f"[INFO] LLM Provider: {provider}")
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
        )

    return ChatGoogleGenerativeAI(
        model=settings.google_model,
        google_api_key=settings.google_api_key,
    )

def build_judge_llm():
    print("[INFO] ---- Build Judge LLM ---- ")
    print(f"[INFO] LLM Judge Provider: {settings.judge_model}")
    return ChatGoogleGenerativeAI(
            model=settings.judge_model,
            google_api_key=settings.google_api_key,
        )


