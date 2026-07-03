def build_prompt(question: str, context: list[str], history: str = "") -> str:
    """Build a prompt with the given question, retrieved context chunks, and conversation history.

    Args:
        question: The user's question.
        context: A list of relevant text chunks from the vector store.
        history: Formatted conversation history string.

    Returns:
        A formatted prompt string ready for the LLM.
    """
    sections = [
        "You are a helpful AI assistant. Answer the user's question using any relevant "
        "information from the conversation history or document context below."
    ]

    if history:
        sections.append(history)

    joined_context = "\n\n".join(context) if context else ""
    if joined_context:
        sections.append(f"Document context:\n{joined_context}")

    sections.append(f"Question:\n{question}")
    sections.append("Answer:")

    return "\n\n".join(sections)
