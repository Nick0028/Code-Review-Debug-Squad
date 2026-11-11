import os
from langchain_chroma import Chroma
from rag.embeddings import get_embeddings
from rag.document_loader import load_knowledge
_store = None
def _get_store():
    global _store
    if _store is None:
        _store = Chroma(collection_name="code_review_guidelines",
            embedding_function=get_embeddings(),
            persist_directory=os.getenv("CHROMA_DIR","./chroma_db"))
        if _store._collection.count() == 0:
            _store.add_documents(load_knowledge())
    return _store
def retrieve_guidance(query: str) -> str:
    try:
        docs = _get_store().similarity_search(query, k=3)
        return "\n\n".join(d.page_content for d in docs)
    except Exception:
        return "Follow Python best practices, validate edge cases, preserve behavior, and write meaningful tests."
