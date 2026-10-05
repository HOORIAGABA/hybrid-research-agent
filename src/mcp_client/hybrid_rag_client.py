"""MCP client for the mcp-hybrid-rag server (HTTP transport)."""
import asyncio
import re
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from src.config import MCP_HYBRID_RAG_URL, TOP_K_INTERNAL


async def _call_tool(query: str, top_k: int) -> str:
    async with streamablehttp_client(MCP_HYBRID_RAG_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "search_financial_docs",
                arguments={"query": query, "top_k": top_k},
            )
            texts = [c.text for c in result.content if getattr(c, "type", "") == "text"]
            return "\n".join(texts)


def search_financial_docs(query: str, top_k: int = TOP_K_INTERNAL) -> list[dict[str, Any]]:
    """Synchronous wrapper. Runs the async call in a fresh thread."""
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        raw = pool.submit(lambda: asyncio.run(_call_tool(query, top_k))).result(timeout=300)

    return _parse_chunks(raw)


_HEADER = re.compile(r"^\[(\d+)\]\s+(.+?)\s+p\.(\d+)\s+\(rerank=([\d.]+)\)")


def _parse_chunks(raw: str) -> list[dict[str, Any]]:
    """Parse the server's text output into structured chunks."""
    chunks = []
    current = None
    for line in raw.splitlines():
        m = _HEADER.match(line.strip())
        if m:
            if current:
                chunks.append(current)
            current = {
                "rank": int(m.group(1)),
                "source": m.group(2),
                "page": int(m.group(3)),
                "rerank_score": float(m.group(4)),
                "content": "",
            }
        elif current is not None:
            current["content"] += line + "\n"
    if current:
        chunks.append(current)
    return chunks