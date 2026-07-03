from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Split text into chunks using recursive character splitting.

    Args:
        text: The input text to split.
        chunk_size: Maximum size of each chunk (default 500).
        chunk_overlap: Overlap between consecutive chunks (default 50).

    Returns:
        A list of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)
