#!/usr/bin/env python3
"""One-shot, idle-only online LoRA lifecycle qualification for MSIO-SP-E200."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TASK_ID = "MSIO-SP-E200"
TOKEN = "EXECUTE-MSIO-SP-E200"
PROMPT = "Storage tuning involves optimizing the performance and"


class Stop(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def request(url: str, method: str = "GET", payload: object | None = None) -> object:
    data = None if payload is None else json.dumps(payload, separators=(",", ":")).encode()
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=15) as response:
        if response.status != 200:
            raise Stop(f"HTTP status {response.status} for {method} {url}")
        return json.loads(response.read().decode())


def output_text(payload: object) -> str:
    if not isinstance(payload, dict) or not isinstance(payload.get("content"), str):
        raise Stop("completion response lacks string content")
    return payload["content"]


def ensure_idle(slots: object) -> None:
    def active(value: object) -> bool:
        if isinstance(value, dict):
            if value.get("is_processing") is True or value.get("is_generating") is True:
                return True
            return any(active(child) for child in value.values())
        if isinstance(value, list):
            return any(active(child) for child in value)
        return False

    if active(slots):
        raise Stop("server reports an active slot before transition")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("token")
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--result-root", type=Path, required=True)
    parser.add_argument("--server", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--adapter-a", type=Path, required=True)
    parser.add_argument("--adapter-b", type=Path, required=True)
    parser.add_argument("--port", type=int, default=18181)
    args = parser.parse_args()
    if args.token != TOKEN:
        raise Stop("authorization token mismatch")
    for path in (args.runtime_root, args.server, args.base, args.adapter_a, args.adapter_b):
        if not path.exists():
            raise Stop(f"missing required path: {path}")
    if args.result_root.exists():
        raise Stop(f"result root exists: {args.result_root}")
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", args.port)) == 0:
            raise Stop(f"loopback port occupied: {args.port}")

    args.result_root.mkdir(parents=True, mode=0o700)
    (args.result_root / ".msio-owned").write_text(TASK_ID + "\n")
    logs = args.result_root / "logs"
    raw = args.result_root / "raw"
    logs.mkdir(); raw.mkdir()
    ledger: list[dict[str, object]] = []
    identity = {str(path): {"bytes": path.stat().st_size, "sha256": sha256(path)}
                for path in (args.server, args.base, args.adapter_a, args.adapter_b)}
    (args.result_root / "identity.json").write_text(json.dumps(identity, indent=2) + "\n")
    env = dict(os.environ, LD_LIBRARY_PATH="/usr/local/cuda-11.6/lib64")
    command = [str(args.server), "-m", str(args.base), "--lora", str(args.adapter_a),
               "--lora", str(args.adapter_b), "--lora-init-without-apply", "--host",
               "127.0.0.1", "--port", str(args.port), "-ngl", "99"]
    proc: subprocess.Popen[bytes] | None = None
    try:
        with (logs / "server.log").open("wb") as server_log:
            proc = subprocess.Popen(command, stdout=server_log, stderr=subprocess.STDOUT, env=env)
            base_url = f"http://127.0.0.1:{args.port}"
            for _ in range(60):
                if proc.poll() is not None:
                    raise Stop(f"server exited before ready: {proc.returncode}")
                try:
                    request(base_url + "/health")
                    break
                except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                    time.sleep(1)
            else:
                raise Stop("server health timeout")
            adapters = request(base_url + "/lora-adapters")
            if not isinstance(adapters, list) or len(adapters) != 2:
                raise Stop("expected exactly two loaded adapters")
            ids = [item.get("id") for item in adapters if isinstance(item, dict)]
            if len(ids) != 2 or any(not isinstance(value, int) for value in ids):
                raise Stop("adapter IDs malformed")

            def step(name: str, scales: list[dict[str, float]] | None) -> str:
                slots = request(base_url + "/slots")
                ensure_idle(slots)
                if scales is not None:
                    request(base_url + "/lora-adapters", "POST", scales)
                response = request(base_url + "/completion", "POST", {
                    "prompt": PROMPT, "n_predict": 24, "temperature": 0.0, "seed": 43,
                })
                text = output_text(response)
                record = {"step": name, "slots": slots, "scales": scales, "response": response,
                          "timestamp_ns": time.time_ns()}
                (raw / f"{name}.json").write_text(json.dumps(record, indent=2) + "\n")
                ledger.append({"step": name, "content_sha256": hashlib.sha256(text.encode()).hexdigest()})
                return text

            zero = [{"id": ids[0], "scale": 0.0}, {"id": ids[1], "scale": 0.0}]
            base_0 = step("base_0", zero)
            a = step("adapter_a", [{"id": ids[0], "scale": 1.0}, {"id": ids[1], "scale": 0.0}])
            base_a = step("base_after_a", zero)
            b = step("adapter_b", [{"id": ids[0], "scale": 0.0}, {"id": ids[1], "scale": 1.0}])
            base_b = step("base_after_b", zero)
            if not (base_0 == base_a == base_b):
                raise Stop("base restoration is not byte-identical")
            if a == base_0 or b == base_0:
                raise Stop("an adapter did not alter the frozen response")
            (args.result_root / "result.json").write_text(json.dumps({
                "task_id": TASK_ID, "decision": "TECHNICAL_GO_ONLINE_LIFECYCLE_ONLY",
                "identity": identity, "ledger": ledger,
            }, indent=2) + "\n")
            return 0
    except Exception as exc:
        (args.result_root / "technical-stop.txt").write_text(f"{type(exc).__name__}: {exc}\n")
        return 2
    finally:
        if proc is not None and proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait(timeout=10)
        (args.result_root / "command-ledger.json").write_text(json.dumps(ledger, indent=2) + "\n")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Stop as exc:
        print(f"{TASK_ID}: {exc}", file=sys.stderr)
        raise SystemExit(2)
