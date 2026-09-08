#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
TR1 = HERE.parent / "MSIO-CE-D002-TR1-tokenrhythm"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def validate() -> dict:
    manifest = json.loads((HERE / "run-manifest.json").read_text(encoding="utf-8"))
    prompts = load(HERE / "prompts.jsonl")
    templates = load(HERE / "prediction-template.jsonl")
    source = {
        (row["condition"], row["scenario_id"]): row
        for row in load(TR1 / "prompts.jsonl")
        if row["repetition"] == 1
    }
    assert len(prompts) == len(templates) == 24
    assert len({row["run_id"] for row in prompts}) == 24
    assert Counter(row["condition"] for row in prompts) == {
        "positive_only": 12,
        "counterevidence_aware": 12,
    }
    for prompt, template in zip(prompts, templates, strict=True):
        old = source[(prompt["condition"], prompt["scenario_id"])]
        assert prompt["messages"] == old["messages"]
        assert prompt["repetition"] == 1
        assert template["run_id"] == prompt["run_id"]
    assert manifest["prompts_sha256"] == hashlib.sha256((HERE / "prompts.jsonl").read_bytes()).hexdigest()
    return {"decision": "P0_PACKET_VALID", "planned_invocations": 24, "messages_preserved": True}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
