#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import random
import re
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BASE = Path("/mnt/nvme3n1/chenhao/modelstateio-runtime")
OUT = BASE / "experiments/MSIO-CE-D003R1-EFFECTIVE-STATE-QUOTIENT"
SERVER = BASE / "experiments/MSIO-NI-E004-B0R1/build/bin/llama-server"
MODELS = {
    "qwen05": BASE / "models/qwen2.5-0.5b-instruct-q4_k_m.gguf",
    "qwen7": BASE / "models/qwen2.5-7b-instruct-q4_k_m.gguf",
}
TOTAL_LAYERS = {"qwen05": 25, "qwen7": 29}
PORT = 18332


def configurations(model: str) -> list[dict]:
    full = TOTAL_LAYERS[model]
    half = full // 2
    base = ["--ctx-size", "512", "--batch-size", "512", "--ubatch-size", "512",
            "--flash-attn", "auto", "--cache-type-k", "f16", "--cache-type-v", "f16"]
    def row(name: str, eq: str, *args: str) -> dict:
        return {"name": name, "expected_equivalence": eq, "args": list(args) + base}
    return [
        row("auto_all", "full_mmap_default", "--gpu-layers", "auto", "--load-mode", "auto"),
        row("explicit_all", "full_mmap_default", "--gpu-layers", "all", "--load-mode", "mmap"),
        row("numeric_999", "full_mmap_default", "--gpu-layers", "999", "--load-mode", "mmap"),
        row("numeric_full", "full_mmap_default", "--gpu-layers", str(full), "--load-mode", "mmap"),
        row("numeric_full_plus_one", "full_mmap_default", "--gpu-layers", str(full + 1), "--load-mode", "mmap"),
        row("auto_load", "full_mmap_default", "--gpu-layers", "all", "--load-mode", "auto"),
        {"name": "ubatch_capped_512", "expected_equivalence": "full_mmap_default",
         "args": ["--gpu-layers", "all", "--load-mode", "mmap", "--ctx-size", "512",
                  "--batch-size", "512", "--ubatch-size", "1024", "--flash-attn", "auto",
                  "--cache-type-k", "f16", "--cache-type-v", "f16"]},
        {"name": "batch128_ubatch256", "expected_equivalence": "batch128",
         "args": ["--gpu-layers", "all", "--load-mode", "mmap", "--ctx-size", "512",
                  "--batch-size", "128", "--ubatch-size", "256", "--flash-attn", "auto",
                  "--cache-type-k", "f16", "--cache-type-v", "f16"]},
        {"name": "batch128_ubatch128", "expected_equivalence": "batch128",
         "args": ["--gpu-layers", "all", "--load-mode", "mmap", "--ctx-size", "512",
                  "--batch-size", "128", "--ubatch-size", "128", "--flash-attn", "auto",
                  "--cache-type-k", "f16", "--cache-type-v", "f16"]},
        {"name": "flash_off", "expected_equivalence": "flash_off",
         "args": ["--gpu-layers", "all", "--load-mode", "mmap", "--ctx-size", "512",
                  "--batch-size", "512", "--ubatch-size", "512", "--flash-attn", "off",
                  "--cache-type-k", "f16", "--cache-type-v", "f16"]},
        {"name": "flash_on", "expected_equivalence": "flash_on",
         "args": ["--gpu-layers", "all", "--load-mode", "mmap", "--ctx-size", "512",
                  "--batch-size", "512", "--ubatch-size", "512", "--flash-attn", "on",
                  "--cache-type-k", "f16", "--cache-type-v", "f16"]},
        {"name": "kv_q8", "expected_equivalence": "kv_q8",
         "args": ["--gpu-layers", "all", "--load-mode", "mmap", "--ctx-size", "512",
                  "--batch-size", "512", "--ubatch-size", "512", "--flash-attn", "auto",
                  "--cache-type-k", "q8_0", "--cache-type-v", "q8_0"]},
        row("half_gpu", "half_gpu", "--gpu-layers", str(half), "--load-mode", "mmap"),
        row("cpu_mmap", "cpu_mmap", "--gpu-layers", "0", "--load-mode", "mmap"),
        row("cpu_none", "cpu_none", "--gpu-layers", "0", "--load-mode", "none"),
    ]


def gpu_rows() -> list[str]:
    p = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,used_memory",
                        "--format=csv,noheader,nounits"], text=True, capture_output=True)
    return [x.strip() for x in p.stdout.splitlines() if x.strip()]


def http(path: str, body: dict | None = None, timeout: float = 3) -> dict:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def last(pattern: str, text: str, cast=str):
    values = re.findall(pattern, text, flags=re.MULTILINE)
    return None if not values else cast(values[-1])


def parse_log(text: str) -> dict:
    off = re.findall(r"offloaded\s+(\d+)/(\d+)\s+layers", text)
    kv = re.findall(r"(CUDA\d+|CPU) KV buffer size\s+=\s+([0-9.]+) MiB", text)
    model_buf = re.findall(r"(CUDA\d+|CPU_Mapped|CPU) model buffer size\s+=\s+([0-9.]+) MiB", text)
    flash_status = last(r"^.*llama_context: flash_attn\s+=\s+(\w+)\s*$", text)
    return {
        "load_mode": last(r"load_mode\s*=\s*([a-zA-Z0-9_-]+)", text),
        "offloaded_layers": None if not off else int(off[-1][0]),
        "total_layers": None if not off else int(off[-1][1]),
        "n_ctx": last(r"^.*llama_context: n_ctx\s+=\s+(\d+)\s*$", text, int),
        "n_batch": last(r"^.*llama_context: n_batch\s+=\s+(\d+)\s*$", text, int),
        "n_ubatch": last(r"^.*llama_context: n_ubatch\s+=\s+(\d+)\s*$", text, int),
        "flash_status": flash_status,
        "flash_enabled": flash_status == "enabled",
        "kv_buffers_mib": [[d, float(v)] for d, v in kv],
        "model_buffers_mib": [[d, float(v)] for d, v in model_buf],
    }


def warm(path: Path) -> None:
    with path.open("rb", buffering=0) as source:
        while source.read(16 << 20):
            pass


def run_one(model_id: str, cfg: dict, position: int) -> dict:
    model = MODELS[model_id]
    trial = f"{position:02d}-{model_id}-{cfg['name']}"
    trial_dir = OUT / "raw" / trial
    trial_dir.mkdir(parents=True)
    log_path = trial_dir / "server.log"
    response_path = trial_dir / "response.json"
    cmd = [str(SERVER), "--model", str(model), "--host", "127.0.0.1", "--port", str(PORT),
           "--parallel", "1", "--no-warmup", "--log-verbose"] + cfg["args"]
    env = dict(os.environ, CUDA_VISIBLE_DEVICES="0",
               LD_LIBRARY_PATH="/usr/local/cuda-12.8/lib64")
    started = time.monotonic()
    peak_gpu = 0
    peak_rss = 0
    process = None
    error = None
    response = None
    ready_s = None
    request_s = None
    mapped_lines = 0
    with log_path.open("wb") as log:
        process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                                   stdin=subprocess.DEVNULL, env=env, start_new_session=True)
        try:
            deadline = time.monotonic() + 180
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(f"server_exit_{process.returncode}")
                for row in gpu_rows():
                    fields = [x.strip() for x in row.split(",")]
                    if fields and fields[0] == str(process.pid):
                        peak_gpu = max(peak_gpu, int(fields[1].split()[0]))
                try:
                    status = Path(f"/proc/{process.pid}/status").read_text()
                    match = re.search(r"^VmRSS:\s+(\d+)", status, re.MULTILINE)
                    if match:
                        peak_rss = max(peak_rss, int(match.group(1)))
                    http("/health", timeout=1)
                    ready_s = time.monotonic() - started
                    break
                except Exception:
                    time.sleep(0.1)
            if ready_s is None:
                raise TimeoutError("readiness")
            maps = Path(f"/proc/{process.pid}/maps").read_text(errors="replace")
            mapped_lines = sum(str(model) in line for line in maps.splitlines())
            request_started = time.monotonic()
            response = http("/v1/chat/completions", {
                "messages": [{"role": "user", "content": "Reply with exactly OK."}],
                "temperature": 0, "seed": 3031, "max_tokens": 4,
            }, timeout=120)
            request_s = time.monotonic() - request_started
            response_path.write_text(json.dumps(response, indent=2) + "\n")
        except Exception as exc:
            error = repr(exc)
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(20)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(10)
    text = log_path.read_text(errors="replace")
    plan = parse_log(text)
    content = None
    try:
        content = response["choices"][0]["message"]["content"]
    except Exception:
        pass
    for _ in range(50):
        if not gpu_rows():
            break
        time.sleep(0.1)
    post_gpu = gpu_rows()
    valid = error is None and content is not None and plan["offloaded_layers"] is not None
    return {
        "trial": trial, "position": position, "model": model_id,
        "requested_name": cfg["name"], "expected_equivalence": cfg["expected_equivalence"],
        "requested_args": cfg["args"], "effective_plan": plan,
        "ready_s": ready_s, "request_s": request_s, "content": content,
        "mapped_model_lines": mapped_lines, "peak_gpu_mib": peak_gpu,
        "peak_rss_kib": peak_rss, "error": error, "valid": valid,
        "post_gpu": post_gpu,
        "cleanup_ok": process is not None and process.poll() is not None and not post_gpu,
    }


def main() -> int:
    if sys.argv[1:] != ["RUN-MSIO-CE-D003R1"]:
        raise SystemExit("execution token required")
    if os.uname().nodename != "g127" or subprocess.check_output(["id", "-un"], text=True).strip() != "chenhao":
        raise SystemExit("wrong host or user")
    if OUT.exists() or gpu_rows() or not SERVER.is_file() or any(not p.is_file() for p in MODELS.values()):
        raise SystemExit("preflight refusal")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", PORT))
    OUT.mkdir(parents=True)
    info = {
        "host": os.uname().nodename, "server": str(SERVER),
        "server_version": subprocess.check_output([str(SERVER), "--version"], text=True,
            env=dict(os.environ, LD_LIBRARY_PATH="/usr/local/cuda-12.8/lib64"), stderr=subprocess.STDOUT),
        "models": {k: {"path": str(v), "bytes": v.stat().st_size} for k, v in MODELS.items()},
        "seed": 3031,
    }
    (OUT / "environment.json").write_text(json.dumps(info, indent=2) + "\n")
    for model in MODELS.values():
        warm(model)
    schedule = [(model, cfg) for model in MODELS for cfg in configurations(model)]
    random.Random(3031).shuffle(schedule)
    (OUT / "schedule.json").write_text(json.dumps([
        {"model": m, **c} for m, c in schedule], indent=2) + "\n")
    rows = []
    for position, (model, cfg) in enumerate(schedule, 1):
        row = run_one(model, cfg, position)
        rows.append(row)
        (OUT / "receipts.json").write_text(json.dumps(rows, indent=2) + "\n")
        print(json.dumps({k: row[k] for k in ("trial", "valid", "ready_s", "error")}), flush=True)
        time.sleep(0.5)
    (OUT / "COMPLETE").write_text(f"{len(rows)}\n")
    return 0 if all(r["valid"] and r["cleanup_ok"] for r in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
