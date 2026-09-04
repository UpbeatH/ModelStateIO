#!/usr/bin/env python3
import argparse
import json
import os
import selectors
import signal
import subprocess
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--mode", choices=("mmap", "none", "dio"), required=True)
    parser.add_argument("--trial", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = output_dir / f"{args.trial}.stdout.txt"
    stderr_path = output_dir / f"{args.trial}.stderr.txt"
    receipt_path = output_dir / f"{args.trial}.receipt.json"
    cap = 1_048_576
    timeout_s = 120.0
    command = [
        args.binary, "--model", args.model, "--load-mode", args.mode,
        "--single-turn", "--simple-io", "--no-display-prompt",
        "--prompt", "Reply with exactly OK.", "--predict", "1",
        "--seed", "1", "--temp", "0", "--n-gpu-layers", "99",
        "--ctx-size", "256", "--batch-size", "64", "--threads", "4",
        "--threads-batch", "4",
    ]
    environment = os.environ.copy()
    environment["LD_LIBRARY_PATH"] = "/usr/local/cuda-11.6/lib64"
    started_ns = time.monotonic_ns()
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
        start_new_session=True,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    streams = {"stdout": bytearray(), "stderr": bytearray()}
    stdout_pending = bytearray()
    ok_ns = None
    failure = None

    while selector.get_map():
        if (time.monotonic_ns() - started_ns) / 1e9 > timeout_s:
            failure = "timeout"
            os.killpg(process.pid, signal.SIGKILL)
            break
        for key, _ in selector.select(timeout=0.05):
            chunk = os.read(key.fileobj.fileno(), 65536)
            if not chunk:
                selector.unregister(key.fileobj)
                continue
            name = key.data
            streams[name].extend(chunk)
            if len(streams[name]) > cap:
                failure = f"{name}_cap"
                os.killpg(process.pid, signal.SIGKILL)
                break
            if name == "stdout":
                stdout_pending.extend(chunk)
                while b"\n" in stdout_pending:
                    line, _, remainder = stdout_pending.partition(b"\n")
                    stdout_pending = bytearray(remainder)
                    if line.strip() == b"OK" and ok_ns is None:
                        ok_ns = time.monotonic_ns()
        if failure:
            break

    exit_code = process.wait()
    ended_ns = time.monotonic_ns()
    stdout_path.write_bytes(streams["stdout"])
    stderr_path.write_bytes(streams["stderr"])
    stdout_text = streams["stdout"].decode("utf-8", errors="replace")
    exact_ok_count = sum(line.strip() == "OK" for line in stdout_text.splitlines())
    receipt = {
        "trial": args.trial,
        "mode": args.mode,
        "exit_code": exit_code,
        "failure": failure,
        "time_to_ok_s": None if ok_ns is None else (ok_ns - started_ns) / 1e9,
        "time_to_exit_s": (ended_ns - started_ns) / 1e9,
        "exact_ok_count": exact_ok_count,
        "exit_marker": "Exiting..." in stdout_text,
        "stdout_bytes": len(streams["stdout"]),
        "stderr_bytes": len(streams["stderr"]),
    }
    receipt_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
    valid = (
        failure is None and exit_code == 0 and ok_ns is not None
        and exact_ok_count == 1 and receipt["exit_marker"]
        and len(streams["stdout"]) <= cap and len(streams["stderr"]) <= cap
    )
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())

