#!/usr/bin/env python3
"""Execute the one-shot 24-call P0 screen."""

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
ROOT = HERE.parents[2] / "ModelStateIO-data" / "MSIO-CE-D002-TR1-P0" / "attempt-001"


def load_runner():
    path = TR1 / "run_gateway.py"
    spec = importlib.util.spec_from_file_location("tr1_gateway", path)
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


def receipt_ok(receipt: dict, parsed: dict | None) -> bool:
    return bool(
        receipt.get("http_status") == 200
        and receipt.get("response_id")
        and receipt.get("returned_model") == "deepseek-v4-pro-0813"
        and isinstance(receipt.get("usage"), dict)
        and receipt.get("thinking_observed") is True
        and isinstance(parsed, dict)
    )


def main() -> int:
    key = os.environ.get("TOKENRHYTHM_API_KEY", "")
    if not key:
        raise SystemExit("P0 credential absent")
    if ROOT.exists() or any((HERE / name).exists() for name in ("predictions.jsonl", "SCORE.json", "EXECUTION-RECEIPT.json")):
        raise SystemExit("P0 one-shot output already exists")
    smoke = json.loads((TR1 / "PREFLIGHT.json").read_text(encoding="utf-8"))
    receipt = smoke["smoke_receipt"]
    if not (
        receipt.get("http_status") == 200
        and receipt.get("returned_model") == "deepseek-v4-pro-0813"
        and receipt.get("response_id")
        and receipt.get("thinking_observed") is True
    ):
        raise SystemExit("P0 gateway evidence insufficient")
    gateway = load_runner()
    prompts = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
    ledger = [json.loads(line) for line in (HERE / "prediction-template.jsonl").read_text(encoding="utf-8").splitlines()]
    ROOT.mkdir(parents=True)
    write_new(ROOT / "TASK-OWNER.json", encode({"task_id": "MSIO-CE-D002-TR1-P0-ATTEMPT-001"}))
    external_ledger = ROOT / "predictions.jsonl"
    atomic_ledger(external_ledger, ledger)
    invalid = Counter()
    started_all = now()
    for prompt, row in zip(prompts, ledger, strict=True):
        body = gateway.request_body(prompt["messages"])
        write_new(ROOT / "requests" / f"{prompt['run_id']}.json", body)
        row["request_body_sha256"] = hashlib.sha256(body).hexdigest()
        row["started_at"] = now()
        started = time.monotonic()
        status, raw, _meta = gateway.request(key, "POST", "/chat/completions", body, 900)
        row["completed_at"] = now()
        row["latency_ms"] = round((time.monotonic() - started) * 1000)
        write_new(ROOT / "responses" / f"{prompt['run_id']}.json", raw)
        parsed, call_receipt = gateway.parse_receipt(status, raw)
        row.update(call_receipt)
        row["client_build"] = f"python/{platform.python_version()} urllib"
        row["response"] = parsed
        valid = receipt_ok(call_receipt, parsed) and gateway.valid_prediction(parsed, prompt)
        row["status"] = "COMPLETED" if valid else "INVALID"
        if not valid:
            invalid[prompt["condition"]] += 1
        atomic_ledger(external_ledger, ledger)
        print(json.dumps({"run_id": prompt["run_id"], "status": row["status"], "latency_ms": row["latency_ms"]}), flush=True)
    shutil.copyfile(external_ledger, HERE / "predictions.jsonl")
    command = [sys.executable, str(HERE / "score_pilot.py"), str(HERE / "predictions.jsonl"), "--output", str(HERE / "SCORE.json")]
    scored = subprocess.run(command, cwd=HERE, capture_output=True, text=True, check=False)
    compact = {
        "completed_at": now(),
        "invalid_by_condition": dict(invalid),
        "model_calls": 24,
        "predictions_sha256": hashlib.sha256((HERE / "predictions.jsonl").read_bytes()).hexdigest(),
        "score_sha256": hashlib.sha256((HERE / "SCORE.json").read_bytes()).hexdigest() if (HERE / "SCORE.json").exists() else None,
        "scorer_exit_code": scored.returncode,
        "scorer_stdout": scored.stdout.strip(),
        "started_at": started_all,
        "system_fingerprint_optional": True,
    }
    write_new(HERE / "EXECUTION-RECEIPT.json", json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    print(json.dumps(compact, ensure_ascii=False, sort_keys=True))
    return scored.returncode


if __name__ == "__main__":
    raise SystemExit(main())
