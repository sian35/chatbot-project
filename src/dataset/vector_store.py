from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough #, RunnableParallel

from dotenv import load_dotenv
import shutil, os
from glob import glob

from source.settings import settings

load_dotenv()   # .env 파일을 읽어서 os.environ에 등록

def chunking(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    split_docs = splitter.split_documents(docs)
    print(f"[INFO] ... Number of chunks: {len(split_docs)}")

    return split_docs

def md_loader():
    md_paths = sorted(glob(settings.md_path))
    md_docs = []
    for p in md_paths:
        md_docs.extend(TextLoader(p, encoding="utf-8").load())
    docs = md_docs
    print(f"[INFO] ... Number of Loaded Documents : {len(docs)}")

    return docs

def dir_loader():

    md_loader = DirectoryLoader(
        path=settings.md_dir_path,
        glob="*.md", # 하위 폴더 포함: "**/*.md"
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    md_docs = md_loader.load()
    print(f"[INFO] ... Number of Loaded Documents : {len(md_docs)}")

    return md_docs

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


def build_embedding():
    # Embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )
    return embeddings

#def build_vector_store():  #기존에 vectorDB반환을 retriever반환으로 수정
def build_retriever():
    # Embedding model
    embeddings = build_embedding()
    
    # ====== 1. Vector DB 존재 확인하고 Indexing 새로 하거나, 기존 Vector DB 로드 ======
    if os.path.exists(os.path.join(settings.persist_dir, "chroma.sqlite3")):
        # ====== Vector DB 존재하면, 기존 인덱스 로드 (from_documents 호출 없이) ======
        print(f"[INFO] ---- 기존 인덱스 {settings.persist_dir} 재로드 ---- ")
        vectorstore = Chroma(
            collection_name=settings.til_collection,
            persist_directory=settings.persist_dir,
            embedding_function=embeddings,  #embedding_function=embeddings는 새 질의를 벡터로 변환할 때 사용할 임베딩 모델
            # 저장된 문서 벡터는 처음 인덱싱할 때 사용한 임베딩 모델 기준으로 만들어졌습니다. 따라서 다시 검색할 때도 같은 임베딩 모델을 사용해야 합니다.
        )
        return vectorstore.as_retriever(search_kwargs={"k":3})

    # ====== Vector DB 존재하지 않으면, Indexing 시작 ======
    print("[INFO] ---- 새 인덱스 생성 ---- ")
    #docs, split_docs = md_loader()
    docs = dir_loader()
    split_docs = chunking(docs)

    # ====== Vector DB 디렉토리 없으면 생성 ======
    if not os.path.exists(settings.persist_dir):
        os.makedirs(settings.persist_dir)

    # ====== 영구 저장 모드 ======
    # from_documents: 생성과 추가 동시에 
    vectorstore = Chroma.from_documents(
        split_docs,
        embeddings,
        collection_name=settings.til_collection,             # 한 persist_directory 안에 여러 컬렉션을 분리 저장할 수 있다
        persist_directory=settings.persist_dir, # Chroma가 해당 폴더에 SQLite 파일로 인덱스를 저장. 프로세스를 다시 시작해도 이 폴더에서 인덱스를 다시 열 수 있다.
    )

    print("[INFO] ... Vector DB 저장 완료. ./chroma_db 폴더에 SQLite 인덱스가 생성되었습니다.")
    print("[INFO] ---- Finish Indexing ---- ")
    return vectorstore.as_retriever(search_kwargs={"k":3})