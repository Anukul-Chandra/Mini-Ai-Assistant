from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.retrieval import retrieve_context

router = APIRouter(prefix="/chat")


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(body: QuestionRequest):
    try:
        chunks = retrieve_context(body.question)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "question": body.question,
        "retrieved_chunks": chunks,
        "count": len(chunks),
    }