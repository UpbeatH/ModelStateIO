#!/usr/bin/env python3
"""Build the 24-call P0 screen from frozen TR1 repetition-one rows."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TR1 = HERE.parent / "MSIO-CE-D002-TR1-tokenrhythm"
SOURCE = TR1 / "prompts.jsonl"
SOURCE_SHA256 = "db9cf94880d038b2d75b7a6c6c0a4ff300378d525ee302323f4c19061203e216"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(encode(row) for row in rows) + "\n", encoding="utf-8")


def build(output: Path = HERE) -> dict:
    if sha(SOURCE) != SOURCE_SHA256:
        raise SystemExit("TR1 source hash mismatch")
    source = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines()]
    first = {(row["condition"], row["scenario_id"]): row for row in source if row["repetition"] == 1}
    scenarios = sorted({scenario for _, scenario in first})
    prompts = []
    templates = []
    for index, scenario in enumerate(scenarios):
        order = ["positive_only", "counterevidence_aware"]
        if index % 2:
            order.reverse()
        for condition in order:
            old = first[(condition, scenario)]
            row = dict(old)
            row["run_id"] = old["run_id"].replace("D002-TR1-", "D002-TR1-P0-", 1)
            prompts.append(row)
            templates.append({
                "client_build": None,
                "completed_at": None,
                "condition": condition,
                "http_status": None,
                "latency_ms": None,
                "raw_response_sha256": None,
                "reasoning_effort": "high",
                "repetition": 1,
                "request_body_sha256": None,
                "requested_model": "deepseek-v4-pro-0813",
                "response": None,
                "response_id": None,
                "returned_model": None,
                "run_id": row["run_id"],
                "scenario_id": scenario,
                "started_at": None,
                "status": "NOT_RUN",
                "system_fingerprint": None,
                "thinking_observed": False,
                "usage": None,
            })
    output.mkdir(parents=True, exist_ok=True)
    write_jsonl(output / "prompts.jsonl", prompts)
    write_jsonl(output / "prediction-template.jsonl", templates)
    manifest = {
        "base_url": "https://tokenrhythm.studio/v1",
        "experiment_id": "MSIO-CE-D002-TR1-P0",
        "go_thresholds": {
            "counterevidence_exact_min": 10,
            "counterevidence_premature_apply_max": 0,
            "exact_advantage_min": 3,
            "valid_calls_each_min": 11,
        },
        "model": "deepseek-v4-pro-0813",
        "planned_invocations": 24,
        "prediction_template_sha256": sha(output / "prediction-template.jsonl"),
        "prompts_sha256": sha(output / "prompts.jsonl"),
        "reasoning_effort_requested": "high",
        "source_tr1_prompts_sha256": SOURCE_SHA256,
        "status": "PACKET_FROZEN_AFTER_SMOKE",
        "system_fingerprint_required": False,
        "thinking": "enabled",
    }
    (output / "run-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
