from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from src.settings import settings

#load_dotenv()

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
    return ChatGoogleGenerativeAI(
            model=settings.judge_model,
            google_api_key=settings.google_api_key,
        )

def build_embedding():
    # Embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )
    return embeddings
