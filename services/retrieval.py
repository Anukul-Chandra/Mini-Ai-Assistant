from services.vector_store import load_vector_store


def retrieve_context(query: str, k: int = 3) -> list[str]:
    """Load the vector store and retrieve the top k most relevant documents for the given query.

    Args:
        query: The user's query string.
        k: Number of top relevant documents to retrieve (default 3).

    Returns:
        A list of page content strings from the retrieved documents.

    Raises:
        ValueError: If no vector store exists.
    """
    vector_store = load_vector_store()
    if vector_store is None:
        raise ValueError("No vector store found. Please upload a document first.")

    results = vector_store.similarity_search(query, k=k)

    return [doc.page_content for doc in results]