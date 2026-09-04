#!/usr/bin/env python3
import argparse
import json
import time
from pathlib import Path


def evaluate(case, snapshots, gpu_snapshot, settle_window_s=5.0):
    receipt = {
        "case": case,
        "settle_window_s": settle_window_s,
        "sample_count": len(snapshots),
        "samples": [{"monotonic_s": t, "processes": pids} for t, pids in snapshots],
        "gpu": gpu_snapshot,
        "timestamp_ns": time.time_ns(),
    }
    initial = snapshots[0][1] if snapshots else []
    final = snapshots[-1][1] if snapshots else []
    if not initial:
        receipt.update(decision="PASS", reason="no_owned_process")
    elif not final:
        receipt.update(decision="SETTLED", reason="transient_process_cleared")
    else:
        receipt.update(decision="NO_GO", reason="owned_process_persisted_through_settle_window")
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("no-process", "transient-fixture", "persistent-fixture"), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    process = [{"pid": 4242, "cmd": "fixture-process --e008"}]
    if args.case == "no-process":
        snapshots = [(0.0, [])]
    elif args.case == "transient-fixture":
        snapshots = [(0.0, process), (5.0, [])]
    else:
        snapshots = [(0.0, process), (5.0, process)]
    receipt = evaluate(args.case, snapshots, {"memory_used_mib": 0, "utilization_pct": 1})
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    expected = {"no-process": "PASS", "transient-fixture": "SETTLED", "persistent-fixture": "NO_GO"}[args.case]
    return 0 if receipt["decision"] == expected else 2


if __name__ == "__main__":
    raise SystemExit(main())

