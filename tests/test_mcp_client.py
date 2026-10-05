"""Parse tests for MCP client."""
from src.mcp_client.hybrid_rag_client import _parse_chunks


SAMPLE = """[1] apple_2023_10k.htm p.30 (rerank=0.983)
ed 3% or $11.0 billion during 2023 compared to 2022.

[2] apple_2023_10k.htm p.47 (rerank=0.631)
Total net sales 383,285
"""


def test_parse_chunks():
    chunks = _parse_chunks(SAMPLE)
    assert len(chunks) == 2
    assert chunks[0]["source"] == "apple_2023_10k.htm"
    assert chunks[0]["page"] == 30
    assert chunks[0]["rerank_score"] == 0.983
