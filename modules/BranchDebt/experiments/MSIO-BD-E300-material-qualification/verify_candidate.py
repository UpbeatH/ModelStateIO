#!/usr/bin/env python3
"""Run an MBPP candidate only inside the frozen E300 Docker sandbox."""

import argparse
import json
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path


IMAGE = "docker.xuanyuan.me/ceph/daemon@sha256:261bbe628f4b438f5bf10de5a8ee05282f2697a5a2cb7ff7668f776b61b9d586"
WRAPPER = r"""
import contextlib, os, sys
path = '/work/candidate.py'
try:
    source = open(path, 'rb').read()
    code = compile(source, path, 'exec')
except (SyntaxError, UnicodeError):
    sys.exit(21)
try:
    with open(os.devnull, 'w') as sink:
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            exec(code, {'__name__': '__main__'})
except AssertionError:
    sys.exit(20)
except (ImportError, ModuleNotFoundError):
    sys.exit(22)
except BaseException:
    sys.exit(23)
sys.exit(0)
"""


def extract_code(answer):
    fenced = re.search(r"```(?:python)?\s*\n(.*?)```", answer, re.I | re.S)
    return (fenced.group(1) if fenced else answer).strip() + "\n"


def extract_tests(prompt):
    marker = "Test cases:"
    if marker not in prompt:
        raise ValueError("prompt has no frozen Test cases section")
    tests = prompt.split(marker, 1)[1].strip()
    if "assert " not in tests:
        raise ValueError("test section has no assertions")
    return tests + "\n"


def classify(returncode):
    return {
        0: "pass",
        20: "assertion_failure",
        21: "syntax_failure",
        22: "import_failure",
        23: "runtime_failure",
        124: "timeout_failure",
        137: "resource_failure",
    }.get(returncode, "sandbox_failure")


def verify(prompt, answer, timeout_s=10):
    program = extract_code(answer) + "\n" + extract_tests(prompt)
    with tempfile.TemporaryDirectory(prefix="msio-bd-e300-") as directory:
        root = Path(directory)
        candidate = root / "candidate.py"
        candidate.write_text(program, encoding="utf-8")
        os.chmod(str(root), 0o755)
        os.chmod(str(candidate), 0o444)
        container_name = "msio-bd-e300-" + uuid.uuid4().hex
        command = [
            "docker", "run", "--rm", "--name", container_name,
            "--network", "none", "--read-only",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--cpus", "1", "--memory", "512m", "--pids-limit", "64",
            "--user", "65534:65534", "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev,size=16777216",
            "--mount", "type=bind,src={},dst=/work,readonly".format(root.resolve()),
            "--entrypoint", "/usr/bin/python3", IMAGE, "-c", WRAPPER,
        ]
        try:
            completed = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=timeout_s + 5, check=False,
            )
            return {
                "classification": classify(completed.returncode),
                "returncode": completed.returncode,
                "stdout_bytes": min(len(completed.stdout), 65536),
                "stderr_bytes": min(len(completed.stderr), 65536),
                "stderr_preview": completed.stderr[:512].decode("utf-8", "replace"),
            }
        except subprocess.TimeoutExpired:
            return {"classification": "timeout_failure", "returncode": 124,
                    "stdout_bytes": 0, "stderr_bytes": 0}
        finally:
            subprocess.run(
                ["docker", "rm", "--force", container_name],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=10, check=False,
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--answer", type=Path, required=True)
    args = parser.parse_args()
    task = json.loads(args.task.read_text(encoding="utf-8"))
    result = verify(task["prompt"], args.answer.read_text(encoding="utf-8"))
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["classification"] in {
        "pass", "assertion_failure", "syntax_failure", "import_failure",
        "runtime_failure", "timeout_failure", "resource_failure"
    } else 2)


if __name__ == "__main__":
    main()
