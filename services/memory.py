_MAX_HISTORY = 10
_questions: list[str] = []
_answers: list[str] = []


def add_to_memory(question: str, answer: str) -> None:
    """Store a question-answer pair in memory.

    Args:
        question: The user's question.
        answer: The AI's response.
    """
    _questions.append(question)
    _answers.append(answer)

    if len(_questions) > _MAX_HISTORY:
        _questions.pop(0)
        _answers.pop(0)


def get_history() -> tuple[list[str], list[str]]:
    """Retrieve all stored questions and answers.

    Returns:
        A tuple of (questions, answers) lists.
    """
    return _questions.copy(), _answers.copy()


def clear_history() -> None:
    """Clear all stored conversation history."""
    _questions.clear()
    _answers.clear()