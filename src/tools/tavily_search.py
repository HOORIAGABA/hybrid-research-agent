"""Tavily web search."""
from tavily import TavilyClient

from src.config import TAVILY_API_KEY, TOP_K_WEB

_client = None


def get_client() -> TavilyClient:
    global _client
    if _client is None:
        if not TAVILY_API_KEY:
            raise RuntimeError("TAVILY_API_KEY missing. See .env.example.")
        _client = TavilyClient(api_key=TAVILY_API_KEY)
    return _client


def web_search(query: str, max_results: int = TOP_K_WEB) -> list[dict]:
    resp = get_client().search(query=query, max_results=max_results)
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", ""),
            "score": r.get("score", 0.0),
        }
        for r in resp.get("results", [])
    ]
