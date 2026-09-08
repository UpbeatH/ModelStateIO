#!/usr/bin/env python3

from __future__ import annotations

import json
import hashlib
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def wilson_lower(successes: int, total: int, z: float = 1.959963984540054) -> float:
    p = successes / total
    denominator = 1 + z * z / total
    centre = p + z * z / (2 * total)
    spread = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total))
    return (centre - spread) / denominator


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads((HERE / "run-manifest.json").read_text(encoding="utf-8"))
    action_schema = json.loads((HERE / "action-contract.schema.json").read_text(encoding="utf-8"))
    receipt_schema = json.loads((HERE / "receipt-record.schema.json").read_text(encoding="utf-8"))
    required = {
        "DESIGN.md", "PREREGISTRATION.md", "EXPERIMENT_PLAN.md",
        "action-contract.schema.json", "receipt-record.schema.json",
        "gate_reference.py", "test_gate_reference.py", "run-manifest.json",
        "RESULT.md",
    }
    assert required <= {path.name for path in HERE.iterdir()}
    assert manifest["status"] == "LOCAL_DESIGN_FROZEN_NO_MODEL_OR_SYSTEM_RUN"
    assert manifest["cluster_execution_authorized"] is False
    assert manifest["proposal_generation_authorized"] is False
    dependency_paths = {
        "MSIO-CE-D000/decision-episode.schema.json": HERE.parent / "MSIO-CE-D000-receipt-normalization" / "decision-episode.schema.json",
        "MSIO-CE-D001/RESULT.md": HERE.parent / "MSIO-CE-D001-counterevidence-evaluator" / "RESULT.md",
        "MSIO-CE-D002-TR1-P1/RESULT.md": HERE.parent / "MSIO-CE-D002-TR1-P1-token-budget-repair" / "RESULT.md",
        "MSIO-CE-D002-TR1-P1/ANALYSIS.json": HERE.parent / "MSIO-CE-D002-TR1-P1-token-budget-repair" / "ANALYSIS.json",
    }
    assert set(manifest["development_dependencies"]) == set(dependency_paths)
    for name, path in dependency_paths.items():
        assert manifest["development_dependencies"][name] == sha256(path)
    planned = manifest["planned_d003a"]
    assert planned["proposal_cells"] * planned["proposals_per_cell"] == 30
    assert planned["post_ack_mismatch_go_count"] == 7
    assert wilson_lower(6, 30) < 0.10 < wilson_lower(7, 30)
    assert action_schema["additionalProperties"] is False
    assert receipt_schema["additionalProperties"] is False
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in ("7/30", "two-sided 95% Wilson", "two action families", "D003_A_NO_GO_AFFECTED_SET"):
        assert token in prereg
    result = {
        "decision": "D003_LOCAL_DESIGN_STATIC_VALID",
        "proposal_or_system_calls": 0,
        "planned_proposals": 30,
        "go_count": 7,
        "wilson_lower_at_7_of_30": round(wilson_lower(7, 30), 6),
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
