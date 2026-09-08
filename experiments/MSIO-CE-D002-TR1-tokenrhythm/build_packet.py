#!/usr/bin/env python3
"""Build the TR1 packet from the frozen D002 messages."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D002 = HERE.parent / "MSIO-CE-D002-pinned-model-run"
SOURCE = D002 / "prompts.jsonl"
SOURCE_SHA256 = "f2800c0863858e00a1c7c1bcc98b39701e36fe20f605e1834a31c30e5d145bc9"
MODEL = "deepseek-v4-pro-0813"
REASONING = "high"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def encode(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(encode(row) for row in rows) + "\n", encoding="utf-8")


def build(output: Path = HERE) -> dict:
    if sha(SOURCE) != SOURCE_SHA256:
        raise SystemExit("frozen D002 prompt source hash mismatch")
    source_rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines()]
    prompts: list[dict] = []
    templates: list[dict] = []
    for source in source_rows:
        run_id = source["run_id"].replace("D002-", "D002-TR1-", 1)
        prompt = {
            "condition": source["condition"],
            "fresh_context_required": True,
            "gateway": "tokenrhythm",
            "messages": source["messages"],
            "model": MODEL,
            "reasoning_effort": REASONING,
            "repetition": source["repetition"],
            "run_id": run_id,
            "scenario_id": source["scenario_id"],
            "thinking": "enabled",
        }
        prompts.append(prompt)
        templates.append({
            "client_build": None,
            "completed_at": None,
            "condition": prompt["condition"],
            "http_status": None,
            "latency_ms": None,
            "raw_response_sha256": None,
            "reasoning_effort": REASONING,
            "repetition": prompt["repetition"],
            "request_body_sha256": None,
            "response": None,
            "response_id": None,
            "returned_model": None,
            "run_id": run_id,
            "scenario_id": prompt["scenario_id"],
            "started_at": None,
            "status": "NOT_RUN",
            "system_fingerprint": None,
            "thinking_observed": False,
            "usage": None,
            "requested_model": MODEL,
        })
    output.mkdir(parents=True, exist_ok=True)
    prompt_path = output / "prompts.jsonl"
    template_path = output / "prediction-template.jsonl"
    write_jsonl(prompt_path, prompts)
    write_jsonl(template_path, templates)
    manifest = {
        "base_url": "https://tokenrhythm.studio/v1",
        "conditions": ["positive_only", "counterevidence_aware"],
        "experiment_id": "MSIO-CE-D002-TR1",
        "fresh_context_per_invocation": True,
        "gateway": "tokenrhythm",
        "json_response_mode": "json_object",
        "model": MODEL,
        "planned_invocations": 72,
        "prediction_template_sha256": sha(template_path),
        "prompts_sha256": sha(prompt_path),
        "reasoning_effective_receipt": "not_exposed_by_gateway_contract",
        "reasoning_effort": REASONING,
        "repetitions": 3,
        "scenarios_per_condition": 12,
        "source_d002_prompts_sha256": SOURCE_SHA256,
        "source_messages_preserved": True,
        "status": "PACKET_FROZEN_CREDENTIAL_NOT_PRESENT",
        "stream": False,
        "thinking": "enabled",
        "tools": "omitted",
    }
    (output / "run-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
