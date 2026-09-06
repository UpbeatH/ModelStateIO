#!/usr/bin/env python3
"""Non-GPU integration smoke for the frozen E300 Docker verifier."""

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("verify_candidate", HERE / "verify_candidate.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PROMPT = "Return one.\nTest cases:\nassert f() == 1\nassert f() > 0"
passed = MODULE.verify(PROMPT, "def f(): return 1")
minor = MODULE.verify(PROMPT, "def f(): return 2")
major = MODULE.verify(PROMPT, "def f(): return 0")
print("pass_smoke={}".format(passed))
print("minor_smoke={}".format(minor))
print("major_smoke={}".format(major))
if passed["classification"] != "pass":
    raise SystemExit("expected pass classification")
if minor["classification"] != "assertion_minor":
    raise SystemExit("expected assertion_minor classification")
if major["classification"] != "assertion_major":
    raise SystemExit("expected assertion_major classification")
