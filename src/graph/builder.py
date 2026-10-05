"""LangGraph wiring."""
from langgraph.graph import END, START, StateGraph

from src.agents.coordinator import route
from src.agents.internal_researcher import internal_research
from src.agents.synthesizer import synthesize
from src.agents.web_researcher import web_research
from src.graph.state import ResearchState


def node_internal(state: ResearchState) -> ResearchState:
    res = internal_research(state["query"])
    return {
        "internal_summary": res["summary"],
        "internal_chunks": res["chunks"],
        "trace": state.get("trace", []) + ["internal_researcher"],
    }


def node_route(state: ResearchState) -> ResearchState:
    decision = route(state["query"], state["internal_summary"])
    return {
        "routing_decision": decision,
        "trace": state.get("trace", []) + [f"router:{decision}"],
    }


def node_web(state: ResearchState) -> ResearchState:
    res = web_research(state["query"])
    return {
        "web_summary": res["summary"],
        "web_results": res["results"],
        "trace": state.get("trace", []) + ["web_researcher"],
    }


def node_synthesize(state: ResearchState) -> ResearchState:
    web_summary = state.get("web_summary") if state.get("routing_decision") == "WEB" else None
    report = synthesize(state["query"], state["internal_summary"], web_summary)
    return {
        "report": report,
        "trace": state.get("trace", []) + ["synthesizer"],
    }


def route_after_decision(state: ResearchState) -> str:
    return "web" if state.get("routing_decision") == "WEB" else "synthesize"


def build_graph():
    g = StateGraph(ResearchState)
    g.add_node("internal", node_internal)
    g.add_node("route", node_route)
    g.add_node("web", node_web)
    g.add_node("synthesize", node_synthesize)

    g.add_edge(START, "internal")
    g.add_edge("internal", "route")
    g.add_conditional_edges(
        "route", route_after_decision,
        {"web": "web", "synthesize": "synthesize"},
    )
    g.add_edge("web", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()
