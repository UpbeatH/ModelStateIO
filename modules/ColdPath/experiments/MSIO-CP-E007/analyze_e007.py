#!/usr/bin/env python3
import argparse
import json
import statistics
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt_dir")
    parser.add_argument("output")
    args = parser.parse_args()
    receipts = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(Path(args.receipt_dir).glob("*.receipt.json"))]
    result = {"experiment": "MSIO-CP-E007", "valid_trials": 0, "expected_trials": 18, "modes": {}}
    all_valid = len(receipts) == 18
    for receipt in receipts:
        valid = (
            receipt["failure"] is None and receipt["exit_code"] == 0
            and receipt["time_to_ok_s"] is not None and receipt["exact_ok_count"] == 1
            and receipt["exit_marker"] and receipt["stdout_bytes"] <= 1_048_576
            and receipt["stderr_bytes"] <= 1_048_576
        )
        result["valid_trials"] += int(valid)
        all_valid = all_valid and valid
    for mode in ("mmap", "none", "dio"):
        values = [float(r["time_to_ok_s"]) for r in receipts if r["mode"] == mode and r["time_to_ok_s"] is not None]
        if len(values) != 6:
            result["modes"][mode] = {"n": len(values)}
            all_valid = False
            continue
        median = statistics.median(values)
        mad = statistics.median(abs(value - median) for value in values)
        robust_cv = 1.4826 * mad / median if median > 0 else None
        result["modes"][mode] = {
            "n": 6,
            "median_time_to_ok_s": median,
            "mad_time_to_ok_s": mad,
            "robust_cv": robust_cv,
            "min_time_to_ok_s": min(values),
            "max_time_to_ok_s": max(values),
        }
        all_valid = all_valid and robust_cv is not None and robust_cv <= 0.15
    result["decision"] = "PASS" if all_valid and result["valid_trials"] == 18 else "NO_GO"
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["decision"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())

