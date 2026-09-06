#!/usr/bin/env python3
"""Execute the frozen 100-event prospective BranchDebt material trace."""

import fcntl, hashlib, json, os, signal, subprocess, sys, time, urllib.request
import csv
from collections import Counter
from pathlib import Path

from trace_logic import CANDIDATES, PRIMARY, outcome_blind_view, repair_prompt, route_verifier_classification
from verify_candidate import verify

RUNTIME = Path("/mnt/nvme1/chenhao/modelstateio-runtime")
SERVER = RUNTIME / "build-d230ddd-cuda116-sm70/bin/llama-server"
MODEL_ROOT = RUNTIME / "models/branchdebt-e300"
PROMOTED = RUNTIME / "experiments/MSIO-BD-E300/acquisition/PROMOTED.tsv"
INPUT = RUNTIME / "experiments/MSIO-BD-E300/development.jsonl"
OUTPUT = RUNTIME / "experiments/MSIO-BD-E300/trace"
INPUT_SHA256 = "be203d6e9d2a372a14bd5b3ed5ecab5c43abbc37205f3444db8b210069ba3850"
PORT = 18190
MODEL_PATHS = {
    PRIMARY: MODEL_ROOT / PRIMARY / "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
    CANDIDATES[0]: MODEL_ROOT / CANDIDATES[0] / "qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf",
    CANDIDATES[1]: MODEL_ROOT / CANDIDATES[1] / "qwen2.5-32b-instruct-q5_k_m-00001-of-00006.gguf",
}
MODEL_BYTES = {
    PRIMARY: 4683073632,
    CANDIDATES[0]: 8988110496,
    CANDIDATES[1]: 23262157568,
}

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()

def verify_promoted():
    rows = []
    with PROMOTED.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = Path(row["path"])
            try:
                path.relative_to(MODEL_ROOT)
            except ValueError:
                raise SystemExit("promoted path escapes frozen model root")
            if path.stat().st_size != int(row["bytes"]) or sha256(path) != row["sha256"]:
                raise SystemExit("promoted model identity mismatch: {}".format(path))
            rows.append(row)
    if len(rows) != 11:
        raise SystemExit("expected 11 promoted model shards")

def request(method, route, body=None, timeout=600):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:{}{}".format(PORT, route),
                                 data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

def statuses():
    payload = request("GET", "/models", timeout=10)
    return {item["id"]: item["status"]["value"] for item in payload["data"]}

def loaded_states(state=None):
    state = statuses() if state is None else state
    return sorted(name for name, value in state.items() if value == "loaded")

def wait_status(model, expected="loaded", seconds=600):
    deadline = time.monotonic() + seconds
    last = None
    while time.monotonic() < deadline:
        last = statuses()
        if last.get(model) == expected:
            return last
        time.sleep(0.25)
    raise RuntimeError("model status timeout {}={} last={}".format(model, expected, last))

def load(model):
    before = statuses()
    if before.get(model) != "loaded":
        result = request("POST", "/models/load", {"model": model})
        if not result.get("success"):
            raise RuntimeError("load rejected for {}: {}".format(model, result))
    after = wait_status(model)
    evicted = sorted(name for name, value in before.items()
                     if value == "loaded" and after.get(name) == "unloaded")
    return before, after, evicted

def chat(model, prompt):
    payload = request("POST", "/v1/chat/completions", {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return only the requested Python implementation."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0, "seed": 20260906, "max_tokens": 512,
        "stream": False,
    })
    return payload["choices"][0]["message"]["content"], payload.get("usage", {})

def foreign_gpu_pids(router_pgid):
    gpu_text = subprocess.check_output([
        "nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader,nounits"
    ], universal_newlines=True)
    gpu_pids = {int(line.strip().split(",")[0]) for line in gpu_text.splitlines()
                if line.strip()}
    ps_text = subprocess.check_output(["ps", "-eo", "pid=,pgid="],
                                      universal_newlines=True)
    groups = {int(parts[0]): int(parts[1]) for parts in
              (line.split() for line in ps_text.splitlines()) if len(parts) == 2}
    return sorted(pid for pid in gpu_pids if groups.get(pid) != router_pgid)

def write_jsonl(stream, value):
    stream.write(json.dumps(value, sort_keys=True) + "\n")
    stream.flush(); os.fsync(stream.fileno())

def main():
    if len(sys.argv) != 2 or sys.argv[1] != "RUN-MSIO-BD-E300":
        raise SystemExit("authorization token mismatch")
    if sha256(INPUT) != INPUT_SHA256:
        raise SystemExit("development task identity mismatch")
    verify_promoted()
    if subprocess.check_output(["nvidia-smi", "--query-compute-apps=pid",
                                "--format=csv,noheader"],
                               universal_newlines=True).strip():
        raise SystemExit("GPU has an existing compute process; technical stop")
    for path in MODEL_PATHS.values():
        if not path.is_file():
            raise SystemExit("missing promoted model: {}".format(path))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    lock_stream = (OUTPUT / ".lock").open("w")
    try:
        fcntl.flock(lock_stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("E300 trace runner already active")
    trace_path, raw_path = OUTPUT / "trace.jsonl", OUTPUT / "raw-answers.jsonl"
    if trace_path.exists() or raw_path.exists():
        raise SystemExit("refusing to overwrite existing E300 trace")

    preset = OUTPUT / "models.ini"
    lines = ["version = 1", "", "[*]", "c = 4096", "n-gpu-layers = 999",
             "load-on-startup = false", ""]
    for name, path in MODEL_PATHS.items():
        lines.extend(["[{}]".format(name), "model = {}".format(path), ""])
    preset.write_text("\n".join(lines), encoding="utf-8")
    log = (OUTPUT / "router.log").open("wb")
    env = dict(os.environ); env["CUDA_VISIBLE_DEVICES"] = "0"
    env["LD_LIBRARY_PATH"] = "/usr/local/cuda-11.6/lib64"
    router = subprocess.Popen([
        str(SERVER), "--models-preset", str(preset), "--models-max", "2",
        "--no-models-autoload", "--host", "127.0.0.1", "--port", str(PORT),
        "--no-warmup"], stdout=log, stderr=subprocess.STDOUT, env=env,
        preexec_fn=os.setsid)
    counts = Counter()
    try:
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if router.poll() is not None: raise RuntimeError("router exited before health")
            try: statuses(); break
            except Exception: time.sleep(0.25)
        else: raise RuntimeError("router health timeout")
        tasks = [json.loads(line) for line in INPUT.open(encoding="utf-8")]
        with trace_path.open("x", encoding="utf-8") as trace, raw_path.open("x", encoding="utf-8") as raw:
            for index, task in enumerate(tasks[:100]):
                foreign = foreign_gpu_pids(os.getpgid(router.pid))
                if foreign:
                    raise RuntimeError("foreign GPU process appeared: {}".format(foreign))
                load(PRIMARY)
                initial, primary_usage = chat(PRIMARY, task["prompt"])
                resident_at_notice = loaded_states()
                notice_ns = time.monotonic_ns()
                view = outcome_blind_view(task, initial, resident_at_notice)
                initial_result = verify(task["prompt"], initial)
                branch_resolution_ns = time.monotonic_ns()
                selected = route_verifier_classification(initial_result["classification"])
                arrival_ns = completion_ns = None
                evicted, pre_residency, post_residency = [], resident_at_notice, resident_at_notice
                transition_bytes = 0
                final_result, repair_usage, repair_answer = initial_result, {}, None
                if selected is not None:
                    arrival_ns = time.monotonic_ns()
                    before, after, evicted = load(selected)
                    pre_residency, post_residency = loaded_states(before), loaded_states(after)
                    if before.get(selected) != "loaded": transition_bytes = MODEL_BYTES[selected]
                    repair_answer, repair_usage = chat(
                        selected, repair_prompt(task["prompt"], initial,
                                                initial_result["classification"]))
                    completion_ns = time.monotonic_ns()
                    final_result = verify(task["prompt"], repair_answer)
                event = {
                    "event_id": "e300-{:03d}".format(index), "task_id": task["task_id"],
                    "node_id": "mbpp-repair", "notice_ns": notice_ns,
                    "branch_resolution_ns": branch_resolution_ns,
                    "candidate_state_ids": list(CANDIDATES),
                    "dependency_ids": ["primary-{}".format(task["task_id"])],
                    "selected_state_id": selected, "arrival_ns": arrival_ns,
                    "completion_ns": completion_ns,
                    "branch_outcome": initial_result["classification"],
                    "correctness": final_result["classification"] == "pass",
                    "decision_view": view, "transition_bytes": transition_bytes,
                    "eviction_required": bool(evicted), "evicted_state_ids": evicted,
                    "pre_residency": pre_residency, "post_residency": post_residency,
                    "initial_verifier": initial_result, "final_verifier": final_result,
                }
                write_jsonl(trace, event)
                write_jsonl(raw, {"event_id": event["event_id"], "initial_answer": initial,
                                  "repair_answer": repair_answer,
                                  "primary_usage": primary_usage, "repair_usage": repair_usage})
                counts["no_call" if selected is None else selected] += 1
        summary = {"events": sum(counts.values()), "branches": dict(counts),
                   "trace_sha256": sha256(trace_path), "raw_sha256": sha256(raw_path)}
        (OUTPUT / "SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                                               encoding="utf-8")
        print(json.dumps(summary, sort_keys=True))
        if counts["no_call"] < 10 or any(counts[name] < 10 for name in CANDIDATES):
            raise SystemExit(2)
    finally:
        if router.poll() is None:
            os.killpg(os.getpgid(router.pid), signal.SIGTERM)
            try: router.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(router.pid), signal.SIGKILL); router.wait(timeout=10)
        log.close()

if __name__ == "__main__":
    main()
