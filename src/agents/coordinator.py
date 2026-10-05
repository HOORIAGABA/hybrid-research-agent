"""Coordinator — routing decision between internal and web."""
from src.tools.llm import chat

ROUTER_SYSTEM = """You are a routing decision assistant.

You receive a user question and the results from an internal retrieval system
over SEC 10-K filings.

Decide whether the internal results are SUFFICIENT to answer the user's question,
or whether the system should ALSO search the web.

Guidelines:
- If the internal results contain the specific information asked for, answer SUFFICIENT.
- If the question asks about current events, market data, industry trends, or
  anything not in financial filings, answer WEB.
- If the internal results are empty or unrelated, answer WEB.

Respond with exactly one word: SUFFICIENT or WEB."""


def route(query: str, internal_summary: str) -> str:
    prompt = f"""User question: {query}

Internal results:
{internal_summary}

Decision (SUFFICIENT or WEB):"""
    decision = chat(prompt, system=ROUTER_SYSTEM, temperature=0.0).strip().upper()
    return "WEB" if "WEB" in decision else "SUFFICIENT"
