"""Configuration."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# LLM — any OpenAI-compatible endpoint
LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-noop")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:20128/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instruct")

# Web search — Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# MCP server URL
MCP_HYBRID_RAG_URL = os.getenv("MCP_HYBRID_RAG_URL", "http://127.0.0.1:8765/mcp")

# Retrieval knobs
TOP_K_INTERNAL = 5
TOP_K_WEB = 5
MAX_ROUTING_ITERATIONS = 2
