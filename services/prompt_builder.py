def build_prompt(question: str, context: list[str]) -> str:
    """Build a RAG prompt with the given question and retrieved context chunks.

    Args:
        question: The user's question.
        context: A list of relevant text chunks from the vector store.

    Returns:
        A formatted prompt string ready for the LLM.
    """
    joined_context = "\n\n".join(context)

    return (
        "You are a helpful AI assistant.\n"
        "\n"
        "Answer the user's question ONLY using the provided context.\n"
        "If the answer is not present in the context, reply exactly:\n"
        '\n'
        '"I couldn\'t find that information in the uploaded documents."\n'
        "\n"
        "Context:\n"
        f"{joined_context}\n"
        "\n"
        "Question:\n"
        f"{question}\n"
        "\n"
        "Answer:"
    )
