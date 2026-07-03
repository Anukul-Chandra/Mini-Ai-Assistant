from langchain_community.vectorstores import FAISS
from services.embeddings import get_embedding_model


def create_vector_store(chunks: list[str]) -> FAISS:
    """Create a FAISS vector store from a list of text chunks.

    Args:
        chunks: The text chunks to index.

    Returns:
        A new FAISS vector store instance.
    """
    embeddings = get_embedding_model()
    return FAISS.from_texts(chunks, embeddings)


def save_vector_store(vector_store: FAISS, path: str = "data/vector_store") -> None:
    """Persist a FAISS vector store to disk.

    Args:
        vector_store: The vector store to save.
        path: Directory path to save to (default "data/vector_store").
    """
    vector_store.save_local(path)


def load_vector_store(path: str = "data/vector_store") -> FAISS | None:
    """Load a FAISS vector store from disk.

    Args:
        path: Directory path to load from (default "data/vector_store").

    Returns:
        The loaded vector store, or None if it does not exist.
    """
    try:
        embeddings = get_embedding_model()
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    except Exception:
        return None
