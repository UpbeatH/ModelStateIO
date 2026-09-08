#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
P0 = HERE.parent / "MSIO-CE-D002-TR1-P0-fast-screen"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def validate() -> dict:
    manifest = json.loads((HERE / "run-manifest.json").read_text(encoding="utf-8"))
    current = load(HERE / "prompts.jsonl")
    source = load(P0 / "prompts.jsonl")
    assert len(current) == len(source) == 24
    for new, old in zip(current, source, strict=True):
        assert new["messages"] == old["messages"]
        assert new["condition"] == old["condition"]
        assert new["scenario_id"] == old["scenario_id"]
        assert new["run_id"] == old["run_id"].replace("D002-TR1-P0-", "D002-TR1-P1-", 1)
    assert manifest["max_tokens"] == 4096
    assert manifest["prompts_sha256"] == hashlib.sha256((HERE / "prompts.jsonl").read_bytes()).hexdigest()
    return {"decision": "P1_PACKET_VALID", "calls": 24, "messages_and_order_preserved": True}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
