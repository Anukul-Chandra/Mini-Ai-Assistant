import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.llm import generate_response
from services.memory import add_to_memory, get_history
from services.prompt_builder import build_prompt
from services.retrieval import retrieve_context
from services.tools import detect_intent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat")


class QuestionRequest(BaseModel):
    question: str


def _build_history() -> str:
    questions, answers = get_history()
    if not questions:
        return ""

    lines = ["Previous conversation:"]
    for q, a in zip(questions, answers):
        lines.append(f"User: {q}")
        lines.append(f"Assistant: {a}")

    return "\n".join(lines)


@router.post("/ask")
async def ask_question(body: QuestionRequest):
    history = _build_history()

    intent, tool_result = None, None
    try:
        intent, tool_result = detect_intent(body.question)
    except Exception as e:
        logger.warning("Intent detection failed: %s", e)

    if intent == "order":
        logger.info("Detected intent: ORDER")
        add_to_memory(body.question, str(tool_result))
        return {
            "source": "order_tool",
            "answer": tool_result,
        }

    if intent == "product":
        logger.info("Detected intent: PRODUCT")
        add_to_memory(body.question, str(tool_result))
        return {
            "source": "product_tool",
            "answer": tool_result,
        }

    if history:
        logger.info("Detected intent: MEMORY")

    chunks = []
    try:
        chunks = retrieve_context(body.question)
        if chunks:
            logger.info("Detected intent: KNOWLEDGE")
    except ValueError as e:
        logger.info("No vector store available, proceeding without RAG context: %s", e)

    prompt = build_prompt(body.question, chunks, history)

    try:
        answer = generate_response(prompt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    add_to_memory(body.question, answer)

    return {
        "question": body.question,
        "answer": answer,
        "retrieved_chunks": len(chunks),
    }