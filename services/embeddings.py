import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings


_model: HuggingFaceEmbeddings | None = None


def get_embedding_model() -> HuggingFaceEmbeddings:
    global _model

    if _model is None:
        load_dotenv()
        hf_token = os.getenv("HF_TOKEN")
        model_kwargs = {"token": hf_token} if hf_token else {}

        _model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs=model_kwargs,
        )

    return _model
