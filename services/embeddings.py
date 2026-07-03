import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings


_model = None


def get_embedding_model() -> HuggingFaceEmbeddings:
    global _model

    if _model is None:
        load_dotenv()
        model_kwargs = {}

        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            model_kwargs["token"] = hf_token

        _model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs=model_kwargs,
        )

    return _model
