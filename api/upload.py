from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ingestion import validate_file

router = APIRouter(prefix="/upload")


@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    try:
        validate_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File received successfully",
    }
