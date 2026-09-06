#!/usr/bin/env python3
"""Qualify native llama.cpp router load/unload status and LRU action surface."""

import hashlib, json, os, signal, subprocess, sys, time, urllib.request
from pathlib import Path

RUNTIME = Path("/mnt/nvme1/chenhao/modelstateio-runtime")
SERVER = RUNTIME / "build-d230ddd-cuda116-sm70/bin/llama-server"
OUTPUT = RUNTIME / "experiments/MSIO-BD-E300/router-smoke"
PORT = 18180
MODELS = [
    ("qwen-0.5b", RUNTIME / "incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf",
     491400032, "74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db"),
    ("qwen-1.5b", RUNTIME / "incoming/qwen2.5-1.5b-instruct-q4_k_m.gguf",
     1117320736, "6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e"),
    ("smollm2-1.7b", RUNTIME / "incoming/smollm2-1.7b-instruct-q4_k_m.gguf",
     1055609536, "decd2598bc2c8ed08c19adc3c8fdd461ee19ed5708679d1c54ef54a5a30d4f33"),
]

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()

def request(method, route, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:{}{}".format(PORT, route),
                                 data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))

def statuses():
    response = request("GET", "/models")
    return {item["id"]: item["status"]["value"] for item in response["data"]}

def wait_status(model, expected, deadline_s=180):
    deadline = time.monotonic() + deadline_s
    last = None
    while time.monotonic() < deadline:
        try:
            last = statuses()
            if last.get(model) == expected:
                return last
        except Exception:
            pass
        time.sleep(0.25)
    raise RuntimeError("status timeout for {}={} last={}".format(model, expected, last))

def main():
    if len(sys.argv) != 2 or sys.argv[1] != "SMOKE-MSIO-BD-E300":
        raise SystemExit("authorization token mismatch")
    gpu = subprocess.check_output(["nvidia-smi", "--query-compute-apps=pid",
                                   "--format=csv,noheader"],
                                  universal_newlines=True).strip()
    if gpu:
        raise SystemExit("GPU has an existing compute process; technical stop")
    for _, path, size, digest in MODELS:
        if path.stat().st_size != size or sha256(path) != digest:
            raise SystemExit("model identity mismatch: {}".format(path))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    preset = OUTPUT / "models.ini"
    lines = ["version = 1", "", "[*]", "c = 512", "n-gpu-layers = 999",
             "load-on-startup = false", ""]
    for name, path, _, _ in MODELS:
        lines.extend(["[{}]".format(name), "model = {}".format(path), ""])
    preset.write_text("\n".join(lines), encoding="utf-8")
    log = (OUTPUT / "router.log").open("wb")
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = "0"
    env["LD_LIBRARY_PATH"] = "/usr/local/cuda-11.6/lib64"
    process = subprocess.Popen([
        str(SERVER), "--models-preset", str(preset), "--models-max", "2",
        "--no-models-autoload", "--host", "127.0.0.1", "--port", str(PORT),
        "--no-warmup"], stdout=log, stderr=subprocess.STDOUT, env=env,
        preexec_fn=os.setsid)
    events = []
    try:
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError("router exited before health")
            try:
                statuses(); break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("router health timeout")
        for name, _, _, _ in MODELS:
            started = time.monotonic_ns()
            result = request("POST", "/models/load", {"model": name})
            state = wait_status(name, "loaded")
            events.append({"model": name, "load_response": result,
                           "elapsed_ms": (time.monotonic_ns() - started) / 1e6,
                           "status_after": state})
        final = statuses()
        expected = {MODELS[0][0]: "unloaded", MODELS[1][0]: "loaded",
                    MODELS[2][0]: "loaded"}
        if any(final.get(name) != value for name, value in expected.items()):
            raise RuntimeError("native LRU readback mismatch: {}".format(final))
        receipt = {"schema_version": "1.0", "experiment_id": "MSIO-BD-E300",
                   "evidence_level": "technical native-router action/readback qualification",
                   "models_max": 2, "autoload": False, "events": events,
                   "final_status": final, "expected_final_status": expected}
        (OUTPUT / "RESULT.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(receipt, sort_keys=True))
    finally:
        if process.poll() is None:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait(timeout=10)
        log.close()

if __name__ == "__main__":
    main()
