from langchain_community.vectorstores import FAISS
from services.embeddings import get_embedding_model


def create_vector_store(chunks: list[str]) -> FAISS:
    embeddings = get_embedding_model()
    return FAISS.from_texts(chunks, embeddings)


def save_vector_store(vector_store: FAISS, path: str = "data/vector_store") -> None:
    vector_store.save_local(path)


def load_vector_store(path: str = "data/vector_store") -> FAISS | None:
    try:
        embeddings = get_embedding_model()
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    except Exception:
        return None
