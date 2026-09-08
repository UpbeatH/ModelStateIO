#!/usr/bin/env python3
"""One-shot TokenRhythm preflight and frozen TR1 executor."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_URL = "https://tokenrhythm.studio/v1"
MODEL = "deepseek-v4-pro-0813"
EFFORT = "high"
DATA_BASE = HERE.parents[2] / "ModelStateIO-data" / "MSIO-CE-D002-TR1"
SMOKE_ROOT = DATA_BASE / "smoke-001"
ATTEMPT_ROOT = DATA_BASE / "attempt-001"
PREFLIGHT = HERE / "PREFLIGHT.json"


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_new(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(value)


def atomic_jsonl(path: Path, values: list[dict]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(b"".join(encode(value) for value in values))
    temporary.replace(path)


def request(key: str, method: str, route: str, body: bytes | None, timeout: int) -> tuple[int, bytes, dict]:
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE_URL + route, data=body, headers=headers, method=method)
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            status = response.status
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as error:
        raw = error.read()
        status = error.code
        response_headers = dict(error.headers.items()) if error.headers else {}
    return status, raw, {"headers": response_headers, "latency_ms": round((time.monotonic() - started) * 1000)}


def request_body(messages: list[dict]) -> bytes:
    return encode({
        "max_tokens": 900,
        "messages": messages,
        "model": MODEL,
        "reasoning_effort": EFFORT,
        "response_format": {"type": "json_object"},
        "stream": False,
        "thinking": {"type": "enabled"},
    })


def parse_receipt(status: int, raw: bytes) -> tuple[dict | None, dict]:
    receipt = {"http_status": status, "raw_response_sha256": sha_bytes(raw)}
    try:
        envelope = json.loads(raw)
    except Exception:
        return None, receipt
    receipt.update({
        "response_id": envelope.get("id"),
        "returned_model": envelope.get("model"),
        "system_fingerprint": envelope.get("system_fingerprint"),
        "usage": envelope.get("usage"),
    })
    try:
        message = envelope["choices"][0]["message"]
        receipt["thinking_observed"] = bool(message.get("reasoning_content"))
        parsed = json.loads(message["content"])
    except Exception:
        return None, receipt
    return parsed, receipt


def qualified(receipt: dict, parsed: dict | None) -> bool:
    return bool(
        receipt.get("http_status") == 200
        and receipt.get("response_id")
        and receipt.get("returned_model") == MODEL
        and receipt.get("system_fingerprint")
        and isinstance(receipt.get("usage"), dict)
        and receipt.get("thinking_observed") is True
        and isinstance(parsed, dict)
    )


def valid_prediction(parsed: dict | None, prompt: dict) -> bool:
    if not isinstance(parsed, dict):
        return False
    if set(parsed) != {
        "scenario_id",
        "decision",
        "cited_card_ids",
        "effective_state_assessment",
        "reason",
    }:
        return False
    if parsed.get("scenario_id") != prompt["scenario_id"]:
        return False
    if parsed.get("decision") not in {"APPLY", "PROBE", "ABSTAIN"}:
        return False
    if parsed.get("effective_state_assessment") not in {
        "VERIFIED",
        "UNVERIFIED",
        "MISMATCH",
        "NOT_APPLICABLE",
    }:
        return False
    if not isinstance(parsed.get("reason"), str) or len(parsed["reason"]) > 600:
        return False
    if not isinstance(parsed.get("cited_card_ids"), list):
        return False
    supplied = {
        card["card_id"]
        for card in json.loads(prompt["messages"][1]["content"])["input"]["evidence"]
    }
    return set(parsed["cited_card_ids"]) <= supplied


def key_or_stop() -> str:
    key = os.environ.get("TOKENRHYTHM_API_KEY", "")
    if not key:
        raise SystemExit("TR1_TECHNICAL_STOP_CREDENTIAL: TOKENRHYTHM_API_KEY is absent")
    return key


def smoke() -> int:
    key = key_or_stop()
    if SMOKE_ROOT.exists() or PREFLIGHT.exists():
        raise SystemExit("TR1 smoke target already exists; refusing overwrite")
    status, models_raw, meta = request(key, "GET", "/models", None, 60)
    if status != 200:
        raise SystemExit(f"TR1_TECHNICAL_STOP_MODEL_UNAVAILABLE: GET /models HTTP {status}")
    try:
        models = json.loads(models_raw)
        available = {item["id"] for item in models["data"]}
    except Exception as error:
        raise SystemExit(f"TR1_TECHNICAL_STOP_MODEL_UNAVAILABLE: invalid model list: {type(error).__name__}")
    if MODEL not in available:
        raise SystemExit(f"TR1_TECHNICAL_STOP_MODEL_UNAVAILABLE: {MODEL} absent")
    SMOKE_ROOT.mkdir(parents=True)
    write_new(SMOKE_ROOT / "TASK-OWNER.json", encode({"task_id": "MSIO-CE-D002-TR1-SMOKE-001"}))
    write_new(SMOKE_ROOT / "models-response.json", models_raw)
    messages = [
        {"role": "system", "content": "Return one JSON object only."},
        {"role": "user", "content": "Return JSON with exactly one field named status whose value is READY."},
    ]
    body = request_body(messages)
    write_new(SMOKE_ROOT / "request.json", body)
    started = now()
    status, raw, call_meta = request(key, "POST", "/chat/completions", body, 900)
    completed = now()
    write_new(SMOKE_ROOT / "response.json", raw)
    parsed, receipt = parse_receipt(status, raw)
    decision = "TR1_GATEWAY_QUALIFIED" if qualified(receipt, parsed) else "TR1_TECHNICAL_STOP_GATEWAY_QUALIFICATION"
    compact = {
        "completed_at": completed,
        "decision": decision,
        "gateway": BASE_URL,
        "model_list_raw_sha256": sha_bytes(models_raw),
        "model_requested": MODEL,
        "reasoning_effort_requested": EFFORT,
        "request_body_sha256": sha_bytes(body),
        "smoke_receipt": receipt,
        "started_at": started,
        "thinking_requested": "enabled",
        "timing": {"models_latency_ms": meta["latency_ms"], "smoke_latency_ms": call_meta["latency_ms"]},
    }
    write_new(PREFLIGHT, json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    print(json.dumps(compact, ensure_ascii=False, sort_keys=True))
    return 0 if decision == "TR1_GATEWAY_QUALIFIED" else 41


def run() -> int:
    key = key_or_stop()
    if ATTEMPT_ROOT.exists() or (HERE / "predictions.jsonl").exists() or (HERE / "SCORE.json").exists():
        raise SystemExit("TR1 attempt target already exists; refusing overwrite")
    if not PREFLIGHT.exists():
        raise SystemExit("TR1_TECHNICAL_STOP_GATEWAY_QUALIFICATION: qualified PREFLIGHT.json absent")
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if preflight.get("decision") != "TR1_GATEWAY_QUALIFIED" or preflight.get("model_requested") != MODEL:
        raise SystemExit("TR1_TECHNICAL_STOP_GATEWAY_QUALIFICATION: preflight not qualified")
    prompts = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
    ledger = [json.loads(line) for line in (HERE / "prediction-template.jsonl").read_text(encoding="utf-8").splitlines()]
    ATTEMPT_ROOT.mkdir(parents=True)
    write_new(ATTEMPT_ROOT / "TASK-OWNER.json", encode({"task_id": "MSIO-CE-D002-TR1-ATTEMPT-001"}))
    ledger_path = ATTEMPT_ROOT / "predictions.jsonl"
    atomic_jsonl(ledger_path, ledger)
    invalid = Counter()
    stopped = None
    for index, (prompt, row) in enumerate(zip(prompts, ledger, strict=True)):
        if invalid[prompt["condition"]] > 3:
            stopped = "D002_TECHNICAL_STOP_INVALID_OUTPUT_RATE"
            break
        body = request_body(prompt["messages"])
        write_new(ATTEMPT_ROOT / "requests" / f"{prompt['run_id']}.json", body)
        row["request_body_sha256"] = sha_bytes(body)
        row["started_at"] = now()
        started = time.monotonic()
        status, raw, _meta = request(key, "POST", "/chat/completions", body, 900)
        row["completed_at"] = now()
        row["latency_ms"] = round((time.monotonic() - started) * 1000)
        write_new(ATTEMPT_ROOT / "responses" / f"{prompt['run_id']}.json", raw)
        parsed, receipt = parse_receipt(status, raw)
        row.update(receipt)
        row["client_build"] = f"python/{platform.python_version()} urllib"
        row["response"] = parsed
        valid_call = qualified(receipt, parsed) and valid_prediction(parsed, prompt)
        row["status"] = "COMPLETED" if valid_call else "INVALID"
        if not valid_call:
            invalid[prompt["condition"]] += 1
        atomic_jsonl(ledger_path, ledger)
    shutil.copyfile(ledger_path, HERE / "predictions.jsonl")
    score_path = HERE / "SCORE.json"
    command = [sys.executable, str(HERE / "score_predictions.py"), str(HERE / "predictions.jsonl"), "--output", str(score_path)]
    scorer = subprocess.run(command, cwd=HERE, capture_output=True, text=True, check=False)
    receipt = {
        "completed_at": now(),
        "decision_before_scoring": stopped or "SCHEDULE_TERMINATED",
        "invalid_by_condition": dict(invalid),
        "model_calls_attempted": sum(row["status"] != "NOT_RUN" for row in ledger),
        "predictions_sha256": hashlib.sha256((HERE / "predictions.jsonl").read_bytes()).hexdigest(),
        "scorer_exit_code": scorer.returncode,
        "scorer_stderr": scorer.stderr[-2000:],
        "scorer_stdout": scorer.stdout[-2000:],
    }
    if score_path.exists():
        receipt["score_sha256"] = hashlib.sha256(score_path.read_bytes()).hexdigest()
    write_new(HERE / "EXECUTION-RECEIPT.json", json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if scorer.returncode == 0 else scorer.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--smoke", action="store_true")
    mode.add_argument("--run", action="store_true")
    args = parser.parse_args()
    return smoke() if args.smoke else run()


if __name__ == "__main__":
    raise SystemExit(main())
