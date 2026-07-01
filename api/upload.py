from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/upload")


@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File received successfully",
    }
