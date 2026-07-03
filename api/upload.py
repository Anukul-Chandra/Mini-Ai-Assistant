from fastapi import APIRouter, UploadFile, File, HTTPException
from services.chunking import split_text
from services.ingestion import validate_file, read_document
from services.vector_store import create_vector_store, save_vector_store

router = APIRouter(prefix="/upload")


@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    try:
        validate_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        text = read_document(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    chunks = split_text(text)
    vector_store = create_vector_store(chunks)
    save_vector_store(vector_store)

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "Document processed and indexed successfully.",
    }
