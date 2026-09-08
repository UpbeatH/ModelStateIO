#!/usr/bin/env python3
"""Dependency-free structural and evidence-boundary validation for D000."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ROLES = {
    "DEVELOPMENT_ACTION_RECEIPT",
    "DEVELOPMENT_NULL_COUNTEREVIDENCE",
    "DEVELOPMENT_STATE_LINEAGE",
    "DEVELOPMENT_DIAGNOSTIC_COUNTEREXAMPLE",
}
APPLICATION_CLASSES = {
    "ACCEPTED_ONLY",
    "CONTROL_PLANE_EFFECTIVE",
    "PHYSICALLY_EFFECTIVE",
    "SEMANTICALLY_EFFECTIVE",
    "PARTIAL",
    "REJECTED",
    "NO_OP",
    "INCONSISTENT",
    "UNVERIFIED",
}
REQUIRED = {
    "schema_version",
    "episode_id",
    "experiment_id",
    "development_exposed",
    "decision_stage",
    "evidence_role",
    "analysis_unit",
    "source",
    "context_before",
    "requested_receipt",
    "effective_receipt",
    "state_receipt",
    "outcome_receipt",
    "rollback_receipt",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise AssertionError(f"{path.name}:{number}: {error}") from error
    return rows


def validate_episode(row: dict[str, Any]) -> None:
    assert set(row) == REQUIRED, (row.get("episode_id"), sorted(set(row) ^ REQUIRED))
    assert row["schema_version"] == "modelstateio-decision-episode-v0"
    assert row["development_exposed"] is True
    assert row["decision_stage"] == "post_action_validation"
    assert row["evidence_role"] in ROLES
    assert "CONFIRMATORY" not in row["evidence_role"]
    assert row["source"]["outcome_exposure"] == "historical_outcome_opened_before_normalization"
    assert row["source"]["artifacts"]
    for item in row["source"]["artifacts"]:
        assert item["locator"]
        assert SHA256.fullmatch(item["sha256"])
    requested = row["requested_receipt"]
    assert requested["action"] and isinstance(requested["parameters"], dict)
    effective = row["effective_receipt"]
    assert effective["application_class"] in APPLICATION_CLASSES
    for key in ("accepted", "control_plane_verified", "physical_verified", "semantic_verified"):
        assert effective[key] is None or isinstance(effective[key], bool)
    state = row["state_receipt"]
    assert set(("before", "after_action", "after_workload", "after_cleanup", "lineage")) <= set(state)
    assert isinstance(state["lineage"], list)
    rollback = row["rollback_receipt"]
    assert isinstance(rollback["required"], bool)
    assert rollback["verified"] is None or isinstance(rollback["verified"], bool)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=HERE)
    args = parser.parse_args()
    schema = json.loads((args.input_dir / "decision-episode.schema.json").read_text(encoding="utf-8"))
    assert set(schema["required"]) == REQUIRED
    assert set(schema["properties"]) == REQUIRED
    corpus = load_jsonl(args.input_dir / "dev-corpus.jsonl")
    policy = load_jsonl(args.input_dir / "policy-view.jsonl")
    for row in corpus:
        validate_episode(row)
    ids = [row["episode_id"] for row in corpus]
    assert len(ids) == len(set(ids)), "duplicate episode ids"
    assert len(corpus) == 108, len(corpus)
    assert len(policy) == len(corpus)
    for full, visible in zip(corpus, policy):
        assert visible["episode_id"] == full["episode_id"]
        assert "outcome_receipt" not in visible
        assert "rollback_receipt" not in visible
        assert set(visible) == REQUIRED - {"outcome_receipt", "rollback_receipt"}
    with (args.input_dir / "EVIDENCE-INVENTORY.tsv").open("r", encoding="utf-8", newline="") as source:
        inventory = list(csv.DictReader(source, delimiter="\t"))
    assert len(inventory) == 8
    assert sum(row["admission"].startswith("ADAPTED") for row in inventory) == 4
    assert sum(row["admission"].startswith("BLOCKED") for row in inventory) == 4
    adjudications = load_jsonl(args.input_dir / "adjudication-results.jsonl")
    assert len(adjudications) == len(corpus)
    assert {row["episode_id"] for row in adjudications} == set(ids)
    assert Counter(row["decision"] for row in adjudications) == {"EFFECTIVE_APPLIED": 108}
    counts = Counter(row["experiment_id"] for row in corpus)
    assert counts == {
        "MSIO-CA-E001": 18,
        "MSIO-CSR-E100": 6,
        "MSIO-PD-E003": 54,
        "MSIO-NI-E006A": 30,
    }
    print(json.dumps({
        "decision": "LOCAL_DEVELOPMENT_CORPUS_VALID",
        "episodes": len(corpus),
        "experiment_counts": dict(sorted(counts.items())),
        "policy_views_outcome_blind": True,
        "schema_contract_aligned": True,
        "deterministic_adjudications": {"EFFECTIVE_APPLIED": 108},
        "confirmatory_labels": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
