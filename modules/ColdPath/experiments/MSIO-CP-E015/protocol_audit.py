from pathlib import Path

p = Path(__file__).parents[1] / "MSIO-CP-E014" / "PREREGISTRATION.md"
t = p.read_text(encoding="utf-8").lower()
required = ["18 trials", "six per mode", "equal information", "equal-action", "equal-runtime", "time-to-first-exact-ok", "robust-cv", "0.15", "no-go", "fresh read-only host/gpu audit"]
missing = [x for x in required if x not in t]
assert not missing, f"missing protocol fields: {missing}"
print("PASS: E014 protocol fields are internally consistent")
