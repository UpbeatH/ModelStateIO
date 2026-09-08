#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
FORBIDDEN = {"oracle_decision", "oracle_basis", "implications", "veto", "polarity", "baseline-results"}


def sha(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return h


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def walk_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=HERE)
    args = parser.parse_args()
    manifest = json.loads((args.input_dir / "run-manifest.json").read_text(encoding="utf-8"))
    prompts = load_jsonl(args.input_dir / "prompts.jsonl")
    template = load_jsonl(args.input_dir / "prediction-template.jsonl")
    assert manifest["status"] == "PACKET_FROZEN_MODEL_NOT_RUN"
    assert manifest["model"] == "gpt-5.6-luna"
    assert manifest["reasoning_effort"] == "high"
    assert manifest["planned_invocations"] == 72
    assert manifest["prompts_sha256"] == sha(args.input_dir / "prompts.jsonl")
    assert manifest["prediction_template_sha256"] == sha(args.input_dir / "prediction-template.jsonl")
    assert len(prompts) == len(template) == 72
    assert len({row["run_id"] for row in prompts}) == 72
    assert {row["run_id"] for row in prompts} == {row["run_id"] for row in template}
    counts = Counter((row["condition"], row["scenario_id"]) for row in prompts)
    assert len(counts) == 24 and set(counts.values()) == {3}
    assert all(row["fresh_context_required"] is True for row in prompts)
    assert all(row["model"] == manifest["model"] for row in prompts)
    assert all(row["reasoning_effort"] == manifest["reasoning_effort"] for row in prompts)
    for row in prompts:
        keys = set(walk_keys(row))
        assert not (keys & FORBIDDEN)
        user_payload = json.loads(row["messages"][1]["content"])
        assert not (set(walk_keys(user_payload)) & FORBIDDEN)
        assert user_payload["input"]["scenario_id"] == row["scenario_id"]
    assert all(row["status"] == "NOT_RUN" and row["response"] is None for row in template)
    print(json.dumps({
        "decision": "D002_PACKET_STATIC_VALID",
        "planned_invocations": len(prompts),
        "condition_scenario_groups": len(counts),
        "repetitions_each": 3,
        "model": manifest["model"],
        "reasoning_effort": manifest["reasoning_effort"],
        "outcome_fields_in_prompts": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
