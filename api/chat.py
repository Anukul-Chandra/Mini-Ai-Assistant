import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.llm import generate_response
from services.memory import add_to_memory, get_history
from services.prompt_builder import build_prompt
from services.retrieval import retrieve_context
from services.tools import route_tool

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
    try:
        tool_result = route_tool(body.question)
    except Exception as e:
        logger.warning("Tool routing failed: %s", e)
        tool_result = None

    if tool_result is not None:
        return {
            "source": "tool",
            "answer": tool_result,
        }

    try:
        chunks = retrieve_context(body.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    prompt = build_prompt(body.question, chunks)
    history = _build_history()
    if history:
        prompt = f"{history}\n\n{prompt}"

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