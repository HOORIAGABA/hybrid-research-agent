"""End-to-end CLI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.graph.builder import build_graph


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "What was Apple's total net sales in 2023?"
    print(f"Query: {query}\n")

    result = build_graph().invoke({"query": query, "trace": []})

    print("Routing trace:")
    for step in result.get("trace", []):
        print(f"  -> {step}")
    print()

    print("=" * 70)
    print("REPORT")
    print("=" * 70)
    print(result.get("report", "(no report)"))


if __name__ == "__main__":
    main()
