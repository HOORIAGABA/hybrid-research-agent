"""LLM client — works with any OpenAI-compatible endpoint.

Uses the official `openai` Python SDK pointed at a custom base_url.
This covers Groq, LocalAI, Ollama, LM Studio, vLLM, llama.cpp server,
LiteLLM, and any other OpenAI-compatible API.
"""
from openai import OpenAI

from src.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    return _client


def chat(prompt: str, system: str | None = None, temperature: float = 0.2) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""