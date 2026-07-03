import os

from dotenv import load_dotenv


load_dotenv()


def _generate_with_openai(prompt: str) -> str:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _generate_with_gemini(prompt: str) -> str:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text


def _generate_with_huggingface(prompt: str) -> str:
    from huggingface_hub import InferenceClient

    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        raise ValueError("HF_API_KEY is not set")

    client = InferenceClient(api_key=api_key)
    response = client.chat_completion(
        model="microsoft/Phi-3.5-mini-instruct",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


_PROVIDERS = {
    "openai": _generate_with_openai,
    "gemini": _generate_with_gemini,
    "huggingface": _generate_with_huggingface,
}


def generate_response(prompt: str) -> str:
    """Generate a response from the configured LLM provider.

    Args:
        prompt: The input prompt to send to the LLM.

    Returns:
        The generated text response.

    Raises:
        ValueError: If the provider is unknown or not configured.
    """
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    if not provider:
        raise ValueError(
            "LLM_PROVIDER is not set. Choose 'openai', 'gemini', or 'huggingface'."
        )

    generator = _PROVIDERS.get(provider)
    if generator is None:
        raise ValueError(
            f"Unknown LLM provider '{provider}'. Choose 'openai', 'gemini', or 'huggingface'."
        )

    return generator(prompt)