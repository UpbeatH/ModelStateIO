#!/usr/bin/env python3
"""Validate TR1 identity, schedule, and message preservation."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
D002 = HERE.parent / "MSIO-CE-D002-pinned-model-run"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def forbidden(value) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in {"oracle_decision", "implication", "veto", "polarity"}:
                return True
            if forbidden(item):
                return True
    if isinstance(value, list):
        return any(forbidden(item) for item in value)
    return False


def validate() -> dict:
    manifest = json.loads((HERE / "run-manifest.json").read_text(encoding="utf-8"))
    current = rows(HERE / "prompts.jsonl")
    source = rows(D002 / "prompts.jsonl")
    templates = rows(HERE / "prediction-template.jsonl")
    assert len(current) == len(source) == len(templates) == 72
    assert manifest["prompts_sha256"] == sha(HERE / "prompts.jsonl")
    assert manifest["prediction_template_sha256"] == sha(HERE / "prediction-template.jsonl")
    groups = defaultdict(list)
    for now, old, template in zip(current, source, templates, strict=True):
        assert now["messages"] == old["messages"]
        assert now["model"] == manifest["model"] == "deepseek-v4-pro-0813"
        assert now["reasoning_effort"] == "high" and now["thinking"] == "enabled"
        assert now["fresh_context_required"] is True
        assert now["run_id"] == old["run_id"].replace("D002-", "D002-TR1-", 1)
        assert template["run_id"] == now["run_id"]
        assert template["requested_model"] == now["model"]
        assert not forbidden(now["messages"])
        groups[(now["condition"], now["scenario_id"])].append(now["repetition"])
    assert len(groups) == 24
    assert all(sorted(repetitions) == [1, 2, 3] for repetitions in groups.values())
    return {
        "decision": "TR1_PACKET_STATIC_VALID",
        "groups": len(groups),
        "messages_preserved": True,
        "model": manifest["model"],
        "planned_invocations": len(current),
    }


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
