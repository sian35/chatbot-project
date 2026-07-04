#src/datset/data_loader.py
from dotenv import load_dotenv
from glob import glob

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.settings import settings

#load_dotenv()   # .env 파일을 읽어서 os.environ에 등록

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

# Load Github MD documents
# def load_github_md_docs() -> list[Document]: