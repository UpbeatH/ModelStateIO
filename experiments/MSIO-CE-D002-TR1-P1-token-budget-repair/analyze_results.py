#!/usr/bin/env python3
"""Produce the frozen descriptive P1 error decomposition."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
D001 = HERE.parents[1] / "experiments/MSIO-CE-D001-counterevidence-evaluator"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main() -> int:
    prompts = {row["run_id"]: row for row in load(HERE / "prompts.jsonl")}
    rows = load(HERE / "predictions.jsonl")
    oracles = {row["scenario_id"]: row["oracle_decision"] for row in load(D001 / "scenarios-with-oracles.jsonl")}
    per_scenario = {}
    summaries = {}
    for condition in ("positive_only", "counterevidence_aware"):
        confusion = Counter()
        valid = 0
        exact = 0
        predictions = {}
        for row in rows:
            prompt = prompts[row["run_id"]]
            if prompt["condition"] != condition:
                continue
            oracle = oracles[prompt["scenario_id"]]
            prediction = row.get("response", {}).get("decision") if isinstance(row.get("response"), dict) else None
            is_valid = row.get("status") == "COMPLETED"
            is_exact = is_valid and prediction == oracle
            valid += int(is_valid)
            exact += int(is_exact)
            confusion[(oracle, prediction if is_valid else "INVALID")] += 1
            predictions[prompt["scenario_id"]] = {
                "exact": is_exact,
                "oracle": oracle,
                "prediction": prediction,
                "status": row.get("status"),
            }
        recalls = {}
        for decision in ("APPLY", "PROBE", "ABSTAIN"):
            population = sum(value == decision for value in oracles.values())
            correct = sum(value["exact"] and value["oracle"] == decision for value in predictions.values())
            recalls[decision] = {"correct": correct, "population": population, "recall": correct / population}
        summaries[condition] = {
            "confusion": {f"{oracle}->{prediction}": count for (oracle, prediction), count in sorted(confusion.items())},
            "decision_recall": recalls,
            "exact": exact,
            "exact_rate": exact / 12,
            "valid_calls": valid,
        }
        for scenario, value in predictions.items():
            per_scenario.setdefault(scenario, {})[condition] = value
    paired = {"counter_correct_positive_wrong": 0, "positive_correct_counter_wrong": 0, "both_correct": 0, "both_wrong": 0}
    for values in per_scenario.values():
        counter = values["counterevidence_aware"]["exact"]
        positive = values["positive_only"]["exact"]
        if counter and positive:
            paired["both_correct"] += 1
        elif counter:
            paired["counter_correct_positive_wrong"] += 1
        elif positive:
            paired["positive_correct_counter_wrong"] += 1
        else:
            paired["both_wrong"] += 1
    output = {
        "analysis_class": "prespecified-score-plus-descriptive-error-decomposition",
        "decision": "P1_NO_GO_STOP_API_PROMPT_BRANCH",
        "exact_advantage": summaries["counterevidence_aware"]["exact"] - summaries["positive_only"]["exact"],
        "paired_exact": paired,
        "per_scenario": per_scenario,
        "predictions_sha256": hashlib.sha256((HERE / "predictions.jsonl").read_bytes()).hexdigest(),
        "summaries": summaries,
    }
    (HERE / "ANALYSIS.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
