"""Internal Researcher — MCP-backed."""
import traceback

from src.mcp_client.hybrid_rag_client import search_financial_docs


def internal_research(query: str, top_k: int = 5) -> dict:
    try:
        chunks = search_financial_docs(query, top_k=top_k)
    except Exception as e:
        print(f"[internal_researcher] ERROR: {e}")
        print(f"[internal_researcher] Traceback:\n{traceback.format_exc()}")
        return {"chunks": [], "summary": f"[internal error: {e}]", "error": str(e)}

    print(f"[internal_researcher] Got {len(chunks)} chunks.")

    if not chunks:
        return {"chunks": [], "summary": "(no internal results)", "error": None}

    lines = [
        f"[{c['source']} p.{c['page']}] {c['content'].strip()[:400]}"
        for c in chunks
    ]
    return {"chunks": chunks, "summary": "\n\n".join(lines), "error": None}
