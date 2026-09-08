#!/usr/bin/env python3
"""Deterministic requested/effective/state adjudication baseline for D000."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


def _result(episode: dict[str, Any], decision: str, checks: dict[str, bool | None]) -> dict[str, Any]:
    failed = sorted(name for name, value in checks.items() if value is False)
    unverified = sorted(name for name, value in checks.items() if value is None)
    return {
        "episode_id": episode["episode_id"],
        "action": episode["requested_receipt"]["action"],
        "decision": decision,
        "checks": checks,
        "failed_checks": failed,
        "unverified_checks": unverified,
    }


def adjudicate_episode(episode: dict[str, Any]) -> dict[str, Any]:
    requested = episode["requested_receipt"]
    effective = episode["effective_receipt"]
    state = episode["state_receipt"]
    action = requested["action"]
    checks: dict[str, bool | None] = {
        "accepted": effective["accepted"],
        "control_plane_verified": effective["control_plane_verified"],
        "physical_verified": effective["physical_verified"],
        "semantic_verified": effective["semantic_verified"],
    }

    if action == "file_scoped_background_preparation":
        parameters = requested["parameters"]
        observations = effective["observations"]
        checks["bytes_match"] = observations["preparation_bytes"] == parameters["target_bytes"]
        checks["fraction_within_tolerance"] = (
            abs(observations["prepared_residency_fraction"] - parameters["target_fraction"])
            <= parameters["fraction_abs_tolerance"]
        )
        if parameters["rate_ceiling_bytes_per_s"] is not None:
            checks["rate_ceiling_respected"] = (
                observations["preparation_bytes_per_s"] <= parameters["rate_ceiling_bytes_per_s"] * 1.001
            )
    elif action == "model_loading_mode":
        checks["cache_state_qualified"] = bool(effective["observations"].get("qualified_cache_state"))
    elif action == "placement_and_context_construction_order":
        observations = effective["observations"]
        checks["declared_device_matches"] = observations["declared_dev"] == "CUDA0"
        checks["all_tensors_on_gpu"] = (
            observations["tensor_gpu"] == observations["tensor_total"]
            and observations["tensor_cpu"] == 0
        )
        checks["state_lineage_present"] = bool(state["lineage"])
    elif action == "request_admission_order":
        mode = requested["parameters"]["mode"]
        actual = effective["observations"]["actual_c_minus_b_ms"]
        if mode == "C_FIRST_50":
            checks["order_direction_matches"] = actual < 0
        elif mode == "B_FIRST_50":
            checks["order_direction_matches"] = actual > 0
        elif mode == "SIMULTANEOUS_0":
            checks["order_direction_matches"] = abs(actual) <= 20
        elif mode in {"B_DISPATCH", "SERIAL_BC"}:
            checks["order_direction_matches"] = actual > 0
        else:
            checks["order_direction_matches"] = False
    else:
        return _result(episode, "UNSUPPORTED_ACTION", {"supported_action": False})

    # A direct file-I/O action has no separate acknowledgement/control plane.
    # Once physical and semantic readback exist, a not-applicable lower layer
    # must not downgrade the action to unverified.
    hard_checks = {
        name: value
        for name, value in checks.items()
        if name not in {"accepted", "control_plane_verified"}
    }
    if any(value is False for value in hard_checks.values()):
        decision = "REQUEST_EFFECTIVE_MISMATCH"
    elif any(value is None for value in hard_checks.values()):
        decision = "EFFECTIVE_UNVERIFIED"
    else:
        decision = "EFFECTIVE_APPLIED"
    return _result(episode, decision, checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=HERE / "dev-corpus.jsonl")
    parser.add_argument("--output", type=Path, default=HERE / "adjudication-results.jsonl")
    args = parser.parse_args()
    episodes = [json.loads(line) for line in args.corpus.read_text(encoding="utf-8").splitlines()]
    results = [adjudicate_episode(episode) for episode in episodes]
    with args.output.open("w", encoding="utf-8", newline="\n") as target:
        for result in results:
            target.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    counts: dict[str, int] = {}
    for result in results:
        counts[result["decision"]] = counts.get(result["decision"], 0) + 1
    print(json.dumps({"episodes": len(results), "decision_counts": dict(sorted(counts.items()))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
