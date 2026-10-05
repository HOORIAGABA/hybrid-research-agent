"""Web Researcher — Tavily-backed."""
from src.tools.tavily_search import web_search


def web_research(query: str, max_results: int = 5) -> dict:
    try:
        results = web_search(query, max_results=max_results)
    except Exception as e:
        return {"results": [], "summary": f"[web error: {e}]", "error": str(e)}

    if not results:
        return {"results": [], "summary": "(no web results)", "error": None}

    lines = [f"[{r['title']} | {r['url']}] {r['content'][:400]}" for r in results]
    return {"results": results, "summary": "\n\n".join(lines), "error": None}
