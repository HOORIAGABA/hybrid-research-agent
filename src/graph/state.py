"""LangGraph state schema."""
from typing import TypedDict


class ResearchState(TypedDict, total=False):
    query: str
    internal_summary: str
    internal_chunks: list
    web_summary: str
    web_results: list
    routing_decision: str
    report: str
    trace: list
