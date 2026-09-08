#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
P0 = HERE.parent / "MSIO-CE-D002-TR1-P0-fast-screen"
SOURCE = P0 / "prompts.jsonl"
SOURCE_SHA256 = "04410d017024032c165b57229afd85edfc2cc3ad53b7662fa289bad05f40ad8c"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(encode(row) for row in rows) + "\n", encoding="utf-8")


def build(output: Path = HERE) -> dict:
    if sha(SOURCE) != SOURCE_SHA256:
        raise SystemExit("P0 source hash mismatch")
    prompts = []
    templates = []
    for old in [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines()]:
        row = dict(old)
        row["run_id"] = old["run_id"].replace("D002-TR1-P0-", "D002-TR1-P1-", 1)
        prompts.append(row)
        templates.append({
            "client_build": None, "completed_at": None, "condition": row["condition"],
            "http_status": None, "latency_ms": None, "raw_response_sha256": None,
            "reasoning_effort": "high", "repetition": 1, "request_body_sha256": None,
            "requested_model": "deepseek-v4-pro-0813", "response": None,
            "response_id": None, "returned_model": None, "run_id": row["run_id"],
            "scenario_id": row["scenario_id"], "started_at": None, "status": "NOT_RUN",
            "system_fingerprint": None, "thinking_observed": False, "usage": None,
        })
    output.mkdir(parents=True, exist_ok=True)
    write_jsonl(output / "prompts.jsonl", prompts)
    write_jsonl(output / "prediction-template.jsonl", templates)
    manifest = {
        "experiment_id": "MSIO-CE-D002-TR1-P1",
        "model": "deepseek-v4-pro-0813",
        "planned_invocations": 24,
        "max_tokens": 4096,
        "prompts_sha256": sha(output / "prompts.jsonl"),
        "prediction_template_sha256": sha(output / "prediction-template.jsonl"),
        "source_p0_prompts_sha256": SOURCE_SHA256,
        "only_change_from_p0_request": "max_tokens_900_to_4096",
        "status": "PACKET_FROZEN_BEFORE_OUTPUT",
    }
    (output / "run-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
