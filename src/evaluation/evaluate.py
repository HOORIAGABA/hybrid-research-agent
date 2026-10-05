"""Routing accuracy evaluation with saved results."""
import json
from datetime import datetime
from pathlib import Path

from src.graph.builder import build_graph

GOLDEN = Path(__file__).parent / "golden_queries.json"
RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"


def main():
    queries = json.loads(GOLDEN.read_text())["queries"]
    graph = build_graph()

    results = []
    correct = 0

    print("=" * 80)
    print(f"ROUTING ACCURACY EVALUATION ({len(queries)} queries)")
    print("=" * 80)

    for q in queries:
        result = graph.invoke({"query": q["query"], "trace": []})
        actual = result.get("routing_decision", "")
        expected = q["expected_route"]
        ok = actual == expected
        if ok:
            correct += 1

        status = "OK  " if ok else "MISS"
        print(f"[{status}] {q['query'][:70]:<70} expected={expected:<10} actual={actual}")

        results.append({
            "id": q["id"],
            "query": q["query"],
            "category": q.get("category", "unknown"),
            "expected": expected,
            "actual": actual,
            "correct": ok,
        })

    accuracy = correct / len(queries) if queries else 0.0
    print()
    print(f"Routing accuracy: {correct}/{len(queries)} = {accuracy:.1%}")

    # Save human-readable + JSON
    RESULTS_DIR.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")

    txt_path = RESULTS_DIR / f"routing_eval_{date_str}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"ROUTING ACCURACY EVALUATION ({len(queries)} queries)\n")
        f.write("=" * 80 + "\n")
        for r in results:
            status = "OK  " if r["correct"] else "MISS"
            f.write(f"[{status}] {r['query'][:70]:<70} expected={r['expected']:<10} actual={r['actual']}\n")
        f.write("\n")
        f.write(f"Routing accuracy: {correct}/{len(queries)} = {accuracy:.1%}\n")

    json_path = RESULTS_DIR / f"routing_eval_{date_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(queries),
            "correct": correct,
            "accuracy": accuracy,
            "results": results,
        }, f, indent=2)

    print()
    print(f"Saved: {txt_path}")
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
