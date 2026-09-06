#!/usr/bin/env python3
"""Non-GPU integration smoke for the frozen E300 Docker verifier."""

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("verify_candidate", HERE / "verify_candidate.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PROMPT = "Return one.\nTest cases:\nassert f() == 1"
passed = MODULE.verify(PROMPT, "def f(): return 1")
failed = MODULE.verify(PROMPT, "def f(): return 2")
print("pass_smoke={}".format(passed))
print("assertion_smoke={}".format(failed))
if passed["classification"] != "pass":
    raise SystemExit("expected pass classification")
if failed["classification"] != "assertion_failure":
    raise SystemExit("expected assertion_failure classification")
