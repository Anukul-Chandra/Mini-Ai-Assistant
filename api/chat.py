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
        status = tool_result.get("status", "unknown").capitalize()
        delivery = tool_result.get("estimated_delivery", "N/A")
        answer = f"Order {tool_result['order_id']} is {status}. Estimated delivery: {delivery}."
        add_to_memory(body.question, answer)
        return {
            "type": "order",
            "answer": answer,
            "data": tool_result,
        }

    if intent == "product":
        logger.info("Detected intent: PRODUCT")
        if isinstance(tool_result, list) and len(tool_result) > 0:
            product = tool_result[0]
            name = product.get("name", "Unknown")
            price = product.get("price", 0)
            stock = product.get("stock", 0)
            answer = f"{name} costs ${price} and {stock} units are in stock."
        else:
            answer = "No product found."
        add_to_memory(body.question, answer)
        return {
            "type": "product",
            "answer": answer,
            "data": tool_result if isinstance(tool_result, list) else [tool_result],
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
        "type": "knowledge",
        "answer": answer,
        "retrieved_chunks": chunks,
    }