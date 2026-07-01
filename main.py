from fastapi import FastAPI

app = FastAPI(title="Mini AI Assistant", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Mini AI Assistant API is running"}
