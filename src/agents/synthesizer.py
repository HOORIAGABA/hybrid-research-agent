"""Synthesizer — cited report from internal + web."""
from src.tools.llm import chat

SYNTH_SYSTEM = """You are a research synthesizer.

You receive a user question, internal document excerpts (SEC filings),
and optionally web search results. Produce a concise research report that:

1. Directly answers the question.
2. Cites every factual claim with either [SEC: <filename> p.<page>] or
   [WEB: <url>].
3. Notes conflicts between sources if any.
4. Does not invent facts not present in the material.

Keep it under 300 words. Plain prose, no headers."""


def synthesize(query: str, internal_summary: str, web_summary: str | None) -> str:
    parts = [f"User question: {query}", "", "Internal (SEC filings):", internal_summary]
    if web_summary:
        parts += ["", "Web results:", web_summary]
    parts += ["", "Write the cited research report:"]
    return chat("\n".join(parts), system=SYNTH_SYSTEM, temperature=0.2)
