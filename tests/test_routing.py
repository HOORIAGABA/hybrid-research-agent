"""Routing logic tests (mock LLM)."""
from unittest.mock import patch

from src.agents.coordinator import route


def test_route_sufficient():
    with patch("src.agents.coordinator.chat", return_value="SUFFICIENT"):
        assert route("q", "summary") == "SUFFICIENT"


def test_route_web():
    with patch("src.agents.coordinator.chat", return_value="WEB"):
        assert route("q", "summary") == "WEB"


def test_route_verbose():
    with patch("src.agents.coordinator.chat", return_value="Decision: WEB."):
        assert route("q", "summary") == "WEB"
