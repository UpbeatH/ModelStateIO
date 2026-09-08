#!/usr/bin/env python3
"""Validate and score one completed D002 prediction ledger exactly once."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MSIO = HERE.parents[1]
D001 = MSIO / "experiments/MSIO-CE-D001-counterevidence-evaluator"
ALLOWED_DECISIONS = {"APPLY", "PROBE", "ABSTAIN"}
ALLOWED_EFFECTIVE = {"VERIFIED", "UNVERIFIED", "MISMATCH", "NOT_APPLICABLE"}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def majority(values: list[str]) -> str | None:
    if len(values) < 2:
        return None
    decision, count = Counter(values).most_common(1)[0]
    return decision if count >= 2 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "SCORE.json")
    args = parser.parse_args()
    manifest = json.loads((HERE / "run-manifest.json").read_text(encoding="utf-8"))
    prompts = load_jsonl(HERE / "prompts.jsonl")
    scenarios = {row["scenario_id"]: row for row in load_jsonl(D001 / "scenarios-with-oracles.jsonl")}
    prompt_by_id = {row["run_id"]: row for row in prompts}
    rows = load_jsonl(args.predictions)
    if len(rows) != len(prompts) or {row["run_id"] for row in rows} != set(prompt_by_id):
        raise SystemExit("prediction ledger does not match frozen run ids")
    valid_by_key: dict[tuple[str, str], list[str]] = defaultdict(list)
    invalid_by_condition = Counter()
    raw_hashes = []
    for row in rows:
        prompt = prompt_by_id[row["run_id"]]
        valid = True
        if row.get("status") != "COMPLETED":
            valid = False
        if row.get("requested_model") != manifest["model"] or row.get("returned_model") != manifest["model"]:
            valid = False
        response = row.get("response")
        if not isinstance(response, dict):
            valid = False
        else:
            required = {"scenario_id", "decision", "cited_card_ids", "effective_state_assessment", "reason"}
            valid = valid and set(response) == required
            valid = valid and response.get("scenario_id") == prompt["scenario_id"]
            valid = valid and response.get("decision") in ALLOWED_DECISIONS
            valid = valid and response.get("effective_state_assessment") in ALLOWED_EFFECTIVE
            valid = valid and isinstance(response.get("reason"), str) and len(response.get("reason", "")) <= 600
            valid = valid and isinstance(response.get("cited_card_ids"), list)
            supplied = {
                card["card_id"]
                for card in json.loads(prompt["messages"][1]["content"])["input"]["evidence"]
            }
            valid = valid and set(response.get("cited_card_ids", [])) <= supplied
        raw_hash = row.get("raw_response_sha256")
        valid = valid and isinstance(raw_hash, str) and re.fullmatch(r"[0-9a-f]{64}", raw_hash) is not None
        if valid:
            raw_hashes.append(raw_hash)
            valid_by_key[(prompt["condition"], prompt["scenario_id"])].append(response["decision"])
        else:
            invalid_by_condition[prompt["condition"]] += 1

    summaries = {}
    for condition in manifest["conditions"]:
        scenario_predictions = {}
        stable = 0
        for scenario_id in sorted(scenarios):
            values = valid_by_key[(condition, scenario_id)]
            scenario_predictions[scenario_id] = majority(values)
            if len(values) == 3 and len(set(values)) == 1:
                stable += 1
        exact = sum(scenario_predictions[sid] == scenarios[sid]["oracle_decision"] for sid in scenarios)
        premature = sum(
            scenario_predictions[sid] == "APPLY" and scenarios[sid]["oracle_decision"] != "APPLY"
            for sid in scenarios
        )
        missed_abstain = sum(
            scenario_predictions[sid] != "ABSTAIN" and scenarios[sid]["oracle_decision"] == "ABSTAIN"
            for sid in scenarios
        )
        recalls = {}
        for decision in sorted(ALLOWED_DECISIONS):
            population = sum(row["oracle_decision"] == decision for row in scenarios.values())
            hit = sum(
                row["oracle_decision"] == decision and scenario_predictions[sid] == decision
                for sid, row in scenarios.items()
            )
            recalls[decision] = {"correct": hit, "population": population, "recall": hit / population}
        summaries[condition] = {
            "valid_calls": 36 - invalid_by_condition[condition],
            "invalid_calls": invalid_by_condition[condition],
            "majority_exact": exact,
            "stable_3_of_3": stable,
            "premature_apply": premature,
            "missed_abstain": missed_abstain,
            "decision_recall": recalls,
            "majority_predictions": scenario_predictions,
        }
    positive = summaries["positive_only"]
    counter = summaries["counterevidence_aware"]
    technical_stop = any(summary["invalid_calls"] > 3 for summary in summaries.values())
    go = (
        not technical_stop
        and all(summary["valid_calls"] >= 33 for summary in summaries.values())
        and counter["majority_exact"] >= 10
        and counter["decision_recall"]["ABSTAIN"]["correct"] >= 6
        and counter["premature_apply"] == 0
        and counter["stable_3_of_3"] >= 10
        and counter["majority_exact"] - positive["majority_exact"] >= 3
        and counter["decision_recall"]["APPLY"]["recall"] >= positive["decision_recall"]["APPLY"]["recall"]
    )
    decision = (
        "D002_TECHNICAL_STOP_INVALID_OUTPUT_RATE"
        if technical_stop
        else "D002_DEVELOPMENT_MODEL_GO_TO_D003_DESIGN"
        if go
        else "D002_DEVELOPMENT_MODEL_NO_GO"
    )
    result = {
        "experiment_id": "MSIO-CE-D002",
        "decision": decision,
        "development_only": True,
        "model": manifest["model"],
        "reasoning_effort": manifest["reasoning_effort"],
        "predictions_sha256": sha(args.predictions),
        "raw_response_hash_count": len(raw_hashes),
        "raw_response_hash_unique": len(set(raw_hashes)),
        "conditions": summaries,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"decision": decision, "conditions": {key: {"valid": value["valid_calls"], "exact": value["majority_exact"]} for key, value in summaries.items()}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
