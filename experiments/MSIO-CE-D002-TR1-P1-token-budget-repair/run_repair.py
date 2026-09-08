#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
TR1 = HERE.parent / "MSIO-CE-D002-TR1-tokenrhythm"
P0 = HERE.parent / "MSIO-CE-D002-TR1-P0-fast-screen"
ROOT = HERE.parents[2] / "ModelStateIO-data" / "MSIO-CE-D002-TR1-P1" / "attempt-001"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_new(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(value)


def atomic_ledger(path: Path, rows: list[dict]) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_bytes(b"".join(encode(row) for row in rows))
    temp.replace(path)


def request_body(messages: list[dict]) -> bytes:
    return encode({
        "max_tokens": 4096,
        "messages": messages,
        "model": "deepseek-v4-pro-0813",
        "reasoning_effort": "high",
        "response_format": {"type": "json_object"},
        "stream": False,
        "thinking": {"type": "enabled"},
    })


def main() -> int:
    key = os.environ.get("TOKENRHYTHM_API_KEY", "")
    if not key:
        raise SystemExit("P1 credential absent")
    if ROOT.exists() or any((HERE / name).exists() for name in ("predictions.jsonl", "SCORE.json", "EXECUTION-RECEIPT.json")):
        raise SystemExit("P1 one-shot output already exists")
    gateway = load(TR1 / "run_gateway.py", "tr1_gateway")
    p0_runner = load(P0 / "run_pilot.py", "p0_runner")
    prompts = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
    ledger = [json.loads(line) for line in (HERE / "prediction-template.jsonl").read_text(encoding="utf-8").splitlines()]
    ROOT.mkdir(parents=True)
    write_new(ROOT / "TASK-OWNER.json", encode({"task_id": "MSIO-CE-D002-TR1-P1-ATTEMPT-001"}))
    external = ROOT / "predictions.jsonl"
    atomic_ledger(external, ledger)
    invalid = Counter()
    finish_reasons = Counter()
    started_all = now()
    for prompt, row in zip(prompts, ledger, strict=True):
        body = request_body(prompt["messages"])
        write_new(ROOT / "requests" / f"{prompt['run_id']}.json", body)
        row["request_body_sha256"] = hashlib.sha256(body).hexdigest()
        row["started_at"] = now()
        started = time.monotonic()
        status, raw, _meta = gateway.request(key, "POST", "/chat/completions", body, 900)
        row["completed_at"] = now()
        row["latency_ms"] = round((time.monotonic() - started) * 1000)
        write_new(ROOT / "responses" / f"{prompt['run_id']}.json", raw)
        try:
            finish_reasons[json.loads(raw)["choices"][0].get("finish_reason", "missing")] += 1
        except Exception:
            finish_reasons["unparseable_envelope"] += 1
        parsed, receipt = gateway.parse_receipt(status, raw)
        row.update(receipt)
        row["client_build"] = f"python/{platform.python_version()} urllib"
        row["response"] = parsed
        valid = p0_runner.receipt_ok(receipt, parsed) and gateway.valid_prediction(parsed, prompt)
        row["status"] = "COMPLETED" if valid else "INVALID"
        if not valid:
            invalid[prompt["condition"]] += 1
        atomic_ledger(external, ledger)
        print(json.dumps({"run_id": prompt["run_id"], "status": row["status"], "latency_ms": row["latency_ms"]}), flush=True)
    shutil.copyfile(external, HERE / "predictions.jsonl")
    command = [sys.executable, str(HERE / "score_repair.py"), str(HERE / "predictions.jsonl"), "--output", str(HERE / "SCORE.json")]
    scored = subprocess.run(command, cwd=HERE, capture_output=True, text=True, check=False)
    receipt = {
        "completed_at": now(), "finish_reasons": dict(finish_reasons),
        "invalid_by_condition": dict(invalid), "max_tokens": 4096,
        "model_calls": 24,
        "predictions_sha256": hashlib.sha256((HERE / "predictions.jsonl").read_bytes()).hexdigest(),
        "score_sha256": hashlib.sha256((HERE / "SCORE.json").read_bytes()).hexdigest(),
        "scorer_exit_code": scored.returncode, "scorer_stdout": scored.stdout.strip(),
        "started_at": started_all,
    }
    write_new(HERE / "EXECUTION-RECEIPT.json", json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return scored.returncode


if __name__ == "__main__":
    raise SystemExit(main())
