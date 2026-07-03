from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.llm import generate_response
from services.prompt_builder import build_prompt
from services.retrieval import retrieve_context
from services.tools import route_tool

router = APIRouter(prefix="/chat")


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(body: QuestionRequest):
    tool_result = route_tool(body.question)
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

    try:
        answer = generate_response(prompt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "question": body.question,
        "answer": answer,
        "retrieved_chunks": len(chunks),
    }