#!/usr/bin/env python3
"""Score the one-repetition P0 development screen."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
D001 = HERE.parents[1] / "experiments/MSIO-CE-D001-counterevidence-evaluator"
ALLOWED = {"APPLY", "PROBE", "ABSTAIN"}


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "SCORE.json")
    args = parser.parse_args()
    prompts = load(HERE / "prompts.jsonl")
    prompt_by_id = {row["run_id"]: row for row in prompts}
    rows = load(args.predictions)
    if len(rows) != 24 or {row["run_id"] for row in rows} != set(prompt_by_id):
        raise SystemExit("P0 ledger does not match frozen run IDs")
    oracles = {row["scenario_id"]: row["oracle_decision"] for row in load(D001 / "scenarios-with-oracles.jsonl")}
    summaries = {}
    for condition in ("positive_only", "counterevidence_aware"):
        condition_rows = [row for row in rows if prompt_by_id[row["run_id"]]["condition"] == condition]
        valid = []
        for row in condition_rows:
            prompt = prompt_by_id[row["run_id"]]
            response = row.get("response")
            okay = row.get("status") == "COMPLETED"
            okay = okay and row.get("requested_model") == "deepseek-v4-pro-0813"
            okay = okay and row.get("returned_model") == "deepseek-v4-pro-0813"
            okay = okay and isinstance(row.get("raw_response_sha256"), str)
            okay = okay and re.fullmatch(r"[0-9a-f]{64}", row.get("raw_response_sha256", "")) is not None
            okay = okay and isinstance(response, dict) and response.get("scenario_id") == prompt["scenario_id"]
            okay = okay and response.get("decision") in ALLOWED if isinstance(response, dict) else False
            if okay:
                valid.append((prompt, response))
        exact = sum(response["decision"] == oracles[prompt["scenario_id"]] for prompt, response in valid)
        premature = sum(response["decision"] == "APPLY" and oracles[prompt["scenario_id"]] != "APPLY" for prompt, response in valid)
        summaries[condition] = {"valid_calls": len(valid), "exact": exact, "premature_apply": premature}
    positive = summaries["positive_only"]
    counter = summaries["counterevidence_aware"]
    go = (
        positive["valid_calls"] >= 11
        and counter["valid_calls"] >= 11
        and counter["exact"] >= 10
        and counter["exact"] - positive["exact"] >= 3
        and counter["premature_apply"] == 0
    )
    result = {
        "decision": "P0_GO_TO_REAL_SYSTEM_DESIGN" if go else "P0_NO_GO_TO_PROMPT_EXPANSION",
        "predictions_sha256": hashlib.sha256(args.predictions.read_bytes()).hexdigest(),
        "summaries": summaries,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
