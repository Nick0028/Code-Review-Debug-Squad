from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
def load_knowledge():
    base = Path("knowledge_base")
    docs = [Document(page_content=p.read_text(encoding="utf-8"), metadata={"source":str(p)})
            for p in base.rglob("*.md")]
    if not docs:
        docs = [Document(page_content="Use descriptive names, validate inputs, handle empty collections and test edge cases.", metadata={"source":"fallback"})]
    return RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100).split_documents(docs)
