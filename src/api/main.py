"""FastAPI backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.graph.builder import build_graph

app = FastAPI(title="Hybrid Research Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


class ResearchRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(req: ResearchRequest):
    result = get_graph().invoke({"query": req.query, "trace": []})
    return {
        "query": req.query,
        "routing_decision": result.get("routing_decision"),
        "trace": result.get("trace", []),
        "internal_chunks": result.get("internal_chunks", []),
        "web_results": result.get("web_results", []),
        "report": result.get("report", ""),
    }
