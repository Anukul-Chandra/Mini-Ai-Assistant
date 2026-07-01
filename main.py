from fastapi import FastAPI
from api.upload import router as upload_router

app = FastAPI(title="Mini AI Assistant", version="1.0.0")

app.include_router(upload_router)


@app.get("/")
async def root():
    return {"message": "Mini AI Assistant API is running"}
