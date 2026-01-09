import json 
from collections import defaultdict
from typing import Dict

EXPERIMENT_LOG_PATH = "observability/experiment_log.jsonl"


def evaluate_rules() -> Dict[str, dict]:
    """
    Read experiment logs and compute intent-wise averages.
    """

    stats = defaultdict(lambda: {
        "count": 0,
        "total_latency_ms": 0.0,
        "total_chunks": 0,
        "queries" : []
    })

    with open(EXPERIMENT_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            intent = record["intent"]

            stats[intent]["count"] += 1
            stats[intent]["total_latency_ms"] += record["total_latency_ms"]
            stats[intent]["total_chunks"] += record["chunks_retrieved"]
            stats[intent]["queries"].append(record["query"])

    # Compute averages
    results = {}

    for intent, data in stats.items():
        results[intent] = {
            "runs": data["count"],
            "avg_latency_ms": data["total_latency_ms"] / data["count"],
            "avg_chunks": data["total_chunks"] / data["count"],
            "queries": data["queries"] 
        }

    return results

