from observability.rule_evaluation import evaluate_rules


results = evaluate_rules()

print("\n--- Rule Evaluation --- \n")

for intent, stats in results.items():
    print(f"\nIntent: {intent}")
    print(f"Runs: {stats['runs']}")
    print(f"Avg latency (ms): {stats['avg_latency_ms']:.2f}")
    print(f"Avg chunks: {stats['avg_chunks']:.2f}")

    print("Queries:")
    for q in stats["queries"]:
        print(f"  - {q}")
