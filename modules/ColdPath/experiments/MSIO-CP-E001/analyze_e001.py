import json
import statistics
import sys
from pathlib import Path


source = Path(sys.argv[1])
if source.is_dir():
    rows = []
    for path in sorted(source.glob("rep-*-*.json")):
        _, rep, state = path.stem.split("-")
        row = json.loads(path.read_text(encoding="utf-8"))
        row.update(rep=int(rep), state=state)
        rows.append(row)
else:
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line]
if len(rows) != 10:
    raise SystemExit(f"TECHNICAL_FAIL: expected 10 rows, found {len(rows)}")

by_state = {state: [r for r in rows if r["state"] == state] for state in ("cold", "warm")}
if any(len(group) != 5 for group in by_state.values()):
    raise SystemExit("TECHNICAL_FAIL: expected five cold and five warm rows")

def ms(value):
    return value / 1_000_000

cold_load = [ms(r["load_duration"]) for r in by_state["cold"]]
warm_load = [ms(r["load_duration"]) for r in by_state["warm"]]
cold_total = [ms(r["total_duration"]) for r in by_state["cold"]]
warm_total = [ms(r["total_duration"]) for r in by_state["warm"]]
median_cold = statistics.median(cold_load)
median_warm = statistics.median(warm_load)
ratio = median_cold / median_warm if median_warm else float("inf")
decision = "PASS" if median_cold >= 1000 and ratio >= 5 else "NO_GO"

result = {
    "evidence_level": "model_residency_materiality_only",
    "valid_pairs": 5,
    "cold_load_ms": cold_load,
    "warm_load_ms": warm_load,
    "cold_total_ms": cold_total,
    "warm_total_ms": warm_total,
    "median_cold_load_ms": median_cold,
    "median_warm_load_ms": median_warm,
    "cold_warm_load_ratio": ratio,
    "decision": decision,
}
print(json.dumps(result, indent=2))
