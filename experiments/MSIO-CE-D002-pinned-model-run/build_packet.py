#!/usr/bin/env python3
"""Build the immutable D002 model-run packet from frozen D001 inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MSIO = HERE.parents[1]
D001 = MSIO / "experiments/MSIO-CE-D001-counterevidence-evaluator"
EXPECTED = {
    "model-inputs-positive-only.jsonl": "598313608a21dbd5ea7719711d75256c1787f560060f352565a72aa0433f6f8c",
    "model-inputs-counterevidence-aware.jsonl": "b8be05a516c4c402592838661a776306d03a330c6707ddf96b67c567be51e89f",
    "scenarios-with-oracles.jsonl": "e74a8dbae366612909862c48070672e305bd87e1726052481c2db3f054cd3545",
}
MODEL = "gpt-5.6-luna"
REASONING_EFFORT = "high"
REPETITIONS = 3
SYSTEM_PROMPT = (
    "You are a conservative decision component for a storage-system tuning study. "
    "Use only the supplied decision contract, context, and evidence. Separate requested, "
    "effective, and physical state. Return exactly one JSON object with no markdown. "
    "Choose only APPLY, PROBE, or ABSTAIN. APPLY requires that the stated objective and "
    "safety constraints are supported in the represented scope. PROBE means a load-bearing "
    "state, scope, or uncertainty field is missing. ABSTAIN means matching evidence is null, "
    "harmful, semantically inconsistent, or explained by a direct fixed defect. Cite only "
    "card_ids present in the supplied evidence."
)
OUTPUT_SCHEMA = {
    "scenario_id": "string_exact_input_id",
    "decision": ["APPLY", "PROBE", "ABSTAIN"],
    "cited_card_ids": ["string_from_supplied_evidence"],
    "effective_state_assessment": ["VERIFIED", "UNVERIFIED", "MISMATCH", "NOT_APPLICABLE"],
    "reason": "string_max_600_characters",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as target:
        for row in rows:
            target.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, expected in EXPECTED.items():
        actual = sha(D001 / name)
        if actual != expected:
            raise SystemExit(f"D001 identity mismatch: {name}: {actual}")

    inputs = {
        "positive_only": load_jsonl(D001 / "model-inputs-positive-only.jsonl"),
        "counterevidence_aware": load_jsonl(D001 / "model-inputs-counterevidence-aware.jsonl"),
    }
    prompts = []
    templates = []
    for mode in ("positive_only", "counterevidence_aware"):
        for item in inputs[mode]:
            for repetition in range(1, REPETITIONS + 1):
                run_id = f"D002-{mode}-{item['scenario_id']}-r{repetition}"
                prompts.append({
                    "run_id": run_id,
                    "condition": mode,
                    "scenario_id": item["scenario_id"],
                    "repetition": repetition,
                    "model": MODEL,
                    "reasoning_effort": REASONING_EFFORT,
                    "fresh_context_required": True,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": json.dumps({"input": item, "output_schema": OUTPUT_SCHEMA}, sort_keys=True, separators=(",", ":"))},
                    ],
                })
                templates.append({
                    "run_id": run_id,
                    "condition": mode,
                    "scenario_id": item["scenario_id"],
                    "repetition": repetition,
                    "requested_model": MODEL,
                    "returned_model": None,
                    "reasoning_effort": REASONING_EFFORT,
                    "client_build": None,
                    "started_at": None,
                    "completed_at": None,
                    "latency_ms": None,
                    "status": "NOT_RUN",
                    "raw_response_sha256": None,
                    "response": None,
                })
    prompts.sort(key=lambda row: row["run_id"])
    templates.sort(key=lambda row: row["run_id"])
    write_jsonl(args.output_dir / "prompts.jsonl", prompts)
    write_jsonl(args.output_dir / "prediction-template.jsonl", templates)
    prompt_hash = sha(args.output_dir / "prompts.jsonl")
    manifest = {
        "experiment_id": "MSIO-CE-D002",
        "status": "PACKET_FROZEN_MODEL_NOT_RUN",
        "model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "temperature": "not_exposed",
        "seed": "not_exposed",
        "repetitions": REPETITIONS,
        "fresh_context_per_invocation": True,
        "conditions": ["positive_only", "counterevidence_aware"],
        "scenarios_per_condition": 12,
        "planned_invocations": len(prompts),
        "d001_inputs": EXPECTED,
        "prompts_sha256": prompt_hash,
        "prediction_template_sha256": sha(args.output_dir / "prediction-template.jsonl"),
        "outcome_exposure": "development_scenarios_known_to_design_team_but_hidden_from_prompts",
        "executor_requirements": [
            "record actual client build and returned model identity",
            "one fresh independent context per run_id",
            "store raw responses outside prompt packet before parsing",
            "no selective retry or prompt repair",
        ],
    }
    (args.output_dir / "run-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": manifest["status"], "planned_invocations": len(prompts), "prompts_sha256": prompt_hash}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
