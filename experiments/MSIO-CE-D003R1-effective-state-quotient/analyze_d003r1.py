#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def signature(row: dict, root: Path) -> str:
    plan = row["effective_plan"]
    log = (root / "raw" / row["trial"] / "server.log").read_text(errors="replace")
    flash_values = re.findall(r"^.*llama_context: flash_attn\s+=\s+(\w+)\s*$", log,
                              flags=re.MULTILINE)
    flash_status = flash_values[-1] if flash_values else None
    value = {
        "model": row["model"],
        "load_mode": plan["load_mode"],
        "offloaded_layers": plan["offloaded_layers"],
        "total_layers": plan["total_layers"],
        "n_ctx": plan["n_ctx"],
        "n_batch": plan["n_batch"],
        "n_ubatch": plan["n_ubatch"],
        "flash_status": flash_status,
        "kv_buffers_mib": plan["kv_buffers_mib"],
        "model_buffers_mib": plan["model_buffers_mib"],
        "mapped_model": row["mapped_model_lines"] > 0,
    }
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def main() -> int:
    root = Path(sys.argv[1])
    rows = json.loads((root / "receipts.json").read_text())
    valid = [row for row in rows if row["valid"] and row["cleanup_ok"]]
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in valid:
        groups[signature(row, root)].append(row)
    repeated = [members for members in groups.values() if len(members) > 1]
    cross_label = [members for members in repeated
                   if len({m["expected_equivalence"] for m in members}) > 1]
    duplicate_executions = sum(len(members) - 1 for members in repeated)
    duplicate_fraction = duplicate_executions / len(valid) if valid else 0.0
    decision = ("GO_TO_EQUAL_BUDGET_TUNING" if len(valid) == 30 and cross_label
                and duplicate_fraction >= 0.20 else "NO_GO_EFFECTIVE_QUOTIENT_GAP")
    result = {
        "scheduled": len(rows), "valid": len(valid),
        "effective_classes": len(groups),
        "duplicate_executions": duplicate_executions,
        "duplicate_execution_fraction": duplicate_fraction,
        "repeated_classes": [[{
            "trial": m["trial"], "requested_name": m["requested_name"],
            "expected_equivalence": m["expected_equivalence"],
            "ready_s": m["ready_s"], "request_s": m["request_s"],
        } for m in members] for members in repeated],
        "unexpected_cross_label_classes": [[m["trial"] for m in members] for members in cross_label],
        "decision": decision,
        "claim_boundary": "exploratory one llama.cpp runtime on one V100S",
    }
    (root / "analysis.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
