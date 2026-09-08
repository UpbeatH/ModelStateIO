#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
FORBIDDEN_MODEL_KEYS = {"oracle_decision", "oracle_basis", "implications", "veto", "polarity"}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def walk_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=HERE)
    args = parser.parse_args()
    cards = load_jsonl(args.input_dir / "evidence-cards.jsonl")
    scenarios = load_jsonl(args.input_dir / "scenarios-with-oracles.jsonl")
    positive = load_jsonl(args.input_dir / "model-inputs-positive-only.jsonl")
    balanced = load_jsonl(args.input_dir / "model-inputs-counterevidence-aware.jsonl")
    audit = load_jsonl(args.input_dir / "retrieval-audit.jsonl")
    results = json.loads((args.input_dir / "baseline-results.json").read_text(encoding="utf-8"))
    assert len(cards) == 15
    assert len(scenarios) == len(positive) == len(balanced) == len(audit) == 12
    assert len({row["card_id"] for row in cards}) == 15
    assert len({row["scenario_id"] for row in scenarios}) == 12
    assert all(row["development_exposed"] is True for row in cards + scenarios)
    assert all(re.fullmatch(r"[0-9a-f]{64}", row["source"]["sha256"]) for row in cards)
    assert all(row["oracle_basis"] for row in scenarios)
    for packet in positive + balanced:
        assert not (set(walk_keys(packet)) & FORBIDDEN_MODEL_KEYS)
        assert len(packet["evidence"]) <= 3
        assert len(json.dumps(packet["evidence"], sort_keys=True)) <= packet["max_evidence_chars"]
    assert all(packet["mode"] == "positive_only" for packet in positive)
    assert all(packet["mode"] == "counterevidence_aware" for packet in balanced)
    assert results["not_llm_evaluation"] is True
    assert results["top_k"] == 3
    assert results["max_evidence_chars"] == 1800
    assert results["baselines"]["counterevidence_aware"]["correct"] == 12
    assert results["baselines"]["counterevidence_aware"]["harmful_apply"] == 0
    assert results["baselines"]["counterevidence_aware"]["missed_abstain"] == 0
    assert results["baselines"]["positive_only"]["premature_apply"] == 1
    assert results["baselines"]["positive_only"]["missed_abstain"] == 7
    cards_by_id = {row["card_id"]: row for row in cards}
    scenarios_by_id = {row["scenario_id"]: row for row in scenarios}
    for row in audit:
        item = scenarios_by_id[row["scenario_id"]]
        if item["oracle_decision"] in {"PROBE", "ABSTAIN"}:
            retrieved = [cards_by_id[card_id] for card_id in row["counterevidence_aware"]]
            assert any(
                card["veto"]
                and card["implications"].get(item["contract_id"]) == item["oracle_decision"]
                and card["card_id"] in item["oracle_basis"]
                for card in retrieved
            )
    print(json.dumps({
        "decision": "D001_LOCAL_HARNESS_VALID",
        "cards": len(cards),
        "scenarios": len(scenarios),
        "scores": {name: row["correct"] for name, row in results["baselines"].items()},
        "model_inputs_hide_oracles": True,
        "not_llm_evaluation": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
