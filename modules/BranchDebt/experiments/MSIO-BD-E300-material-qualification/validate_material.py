#!/usr/bin/env python3
"""Validate the frozen BranchDebt E300 trace and physical-capacity contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {
    "event_id", "task_id", "node_id", "notice_ns", "candidate_state_ids",
    "dependency_ids", "selected_state_id", "arrival_ns", "completion_ns",
    "branch_resolution_ns", "branch_outcome", "correctness", "decision_view",
    "transition_bytes", "eviction_required",
}
FORBIDDEN_DECISION_FIELDS = {
    "actual_arrival_ns", "arrival_ns", "completion_ns", "selected_state_id",
    "branch_resolution_ns", "branch_outcome", "correctness", "post_residency",
    "transition_bytes",
}


class Invalid(RuntimeError):
    pass


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(trace_path: Path, capacity_path: Path) -> dict[str, object]:
    capacity = load_json(capacity_path)
    if not isinstance(capacity, dict):
        raise Invalid("capacity receipt must be an object")
    usable = capacity.get("usable_hbm_bytes")
    peaks = capacity.get("per_model_peak_hbm_bytes")
    if not isinstance(usable, int) or usable <= 0:
        raise Invalid("invalid usable_hbm_bytes")
    if not isinstance(peaks, dict) or len(peaks) < 3:
        raise Invalid("at least three measured model peaks are required")
    if any(not isinstance(v, int) or v <= 0 for v in peaks.values()):
        raise Invalid("invalid per-model peak")
    if sum(peaks.values()) <= usable:
        raise Invalid("measured state working set does not exceed usable HBM")

    events = []
    seen = set()
    with trace_path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            event = json.loads(line)
            if not isinstance(event, dict) or not REQUIRED.issubset(event):
                raise Invalid(f"line {line_no}: missing required field")
            event_id = event["event_id"]
            if not isinstance(event_id, str) or not event_id or event_id in seen:
                raise Invalid(f"line {line_no}: invalid or duplicate event_id")
            seen.add(event_id)
            candidates = event["candidate_state_ids"]
            if not isinstance(candidates, list) or len(set(candidates)) < 2:
                raise Invalid(f"line {line_no}: fewer than two candidate states")
            if any(state not in peaks for state in candidates):
                raise Invalid(f"line {line_no}: unknown candidate state")
            deps = event["dependency_ids"]
            if not isinstance(deps, list) or not deps:
                raise Invalid(f"line {line_no}: missing dependency")
            view = event["decision_view"]
            if not isinstance(view, dict) or FORBIDDEN_DECISION_FIELDS & view.keys():
                raise Invalid(f"line {line_no}: forbidden future field in decision view")
            notice = event["notice_ns"]
            resolution = event["branch_resolution_ns"]
            selected = event["selected_state_id"]
            arrival = event["arrival_ns"]
            completion = event["completion_ns"]
            if selected is None:
                if arrival is not None or completion is not None:
                    raise Invalid(f"line {line_no}: no-call branch has call timestamps")
                if not all(isinstance(v, int) for v in (notice, resolution)):
                    raise Invalid(f"line {line_no}: invalid branch timestamps")
                if not notice < resolution:
                    raise Invalid(f"line {line_no}: branch was not resolved after notice")
            else:
                if selected not in candidates:
                    raise Invalid(f"line {line_no}: selected state not in candidates")
                if not all(isinstance(v, int) for v in (notice, resolution, arrival, completion)):
                    raise Invalid(f"line {line_no}: invalid timestamps")
                if not notice < resolution <= arrival <= completion:
                    raise Invalid(f"line {line_no}: notice is not prospectively earlier")
            if not isinstance(event["correctness"], bool):
                raise Invalid(f"line {line_no}: correctness must be boolean")
            if not isinstance(event["transition_bytes"], int) or event["transition_bytes"] < 0:
                raise Invalid(f"line {line_no}: invalid transition bytes")
            events.append(event)

    if len(events) < 100:
        raise Invalid("fewer than 100 events")
    opportunities = sum(event["selected_state_id"] is None for event in events)
    if opportunities / len(events) < 0.10:
        raise Invalid("fewer than 10% observed no-call/wrong-path opportunities")
    evictions = sum(event["eviction_required"] is True for event in events)
    if evictions == 0:
        raise Invalid("no measured eviction-required event")
    return {
        "decision": "PASS_MATERIAL_CONTRACT_ONLY",
        "events": len(events),
        "branch_opportunities": opportunities,
        "eviction_required_events": evictions,
        "usable_hbm_bytes": usable,
        "state_peak_sum_bytes": sum(peaks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("capacity", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.trace, args.capacity), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Invalid, json.JSONDecodeError) as exc:
        print(json.dumps({"decision": "NO_GO", "reason": str(exc)}, sort_keys=True))
        raise SystemExit(2)
