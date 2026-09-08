#!/usr/bin/env python3

from __future__ import annotations

import json
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUILDER = HERE / "build_dev_corpus.py"
sys.path.insert(0, str(HERE))
from receipt_adjudicator import adjudicate_episode


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class ReceiptNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(BUILDER)], check=True, capture_output=True, text=True)
        cls.rows = load_jsonl(HERE / "dev-corpus.jsonl")
        cls.by_id = {row["episode_id"]: row for row in cls.rows}

    def test_requested_and_effective_are_not_collapsed(self) -> None:
        row = self.by_id["MSIO-CA-E001-b01-p2-eager75"]
        self.assertEqual(row["requested_receipt"]["parameters"]["target_fraction"], 0.75)
        self.assertAlmostEqual(
            row["effective_receipt"]["observations"]["prepared_residency_fraction"],
            0.7433867088978826,
        )
        self.assertNotEqual(
            row["requested_receipt"]["parameters"]["target_fraction"],
            row["effective_receipt"]["observations"]["prepared_residency_fraction"],
        )

    def test_identical_visible_placement_preserves_different_lineage(self) -> None:
        early = self.by_id["MSIO-PD-E003-b01-qwen05-early_atomic"]
        late = self.by_id["MSIO-PD-E003-b01-qwen05-late_atomic"]
        self.assertEqual(early["effective_receipt"]["observations"], late["effective_receipt"]["observations"])
        self.assertNotEqual(early["state_receipt"]["lineage"], late["state_receipt"]["lineage"])
        self.assertNotEqual(
            early["outcome_receipt"]["metrics"]["median_request_ms"],
            late["outcome_receipt"]["metrics"]["median_request_ms"],
        )

    def test_nominal_and_actual_order_timing_are_separate(self) -> None:
        row = self.by_id["MSIO-NI-E006A-row-01"]
        self.assertEqual(row["requested_receipt"]["parameters"]["nominal_c_minus_b_ms"], 50.0)
        self.assertEqual(row["effective_receipt"]["observations"]["actual_c_minus_b_ms"], 60.0)
        self.assertEqual(row["outcome_receipt"]["status"], "C_stall_nudge_release")

    def test_policy_view_has_no_outcome_or_rollback(self) -> None:
        for row in load_jsonl(HERE / "policy-view.jsonl"):
            self.assertNotIn("outcome_receipt", row)
            self.assertNotIn("rollback_receipt", row)

    def test_mutated_preparation_fraction_is_rejected(self) -> None:
        row = copy.deepcopy(self.by_id["MSIO-CA-E001-b01-p2-eager75"])
        row["effective_receipt"]["observations"]["prepared_residency_fraction"] = 0.50
        result = adjudicate_episode(row)
        self.assertEqual(result["decision"], "REQUEST_EFFECTIVE_MISMATCH")
        self.assertIn("fraction_within_tolerance", result["failed_checks"])

    def test_mutated_order_direction_is_rejected(self) -> None:
        row = copy.deepcopy(self.by_id["MSIO-NI-E006A-row-01"])
        row["effective_receipt"]["observations"]["actual_c_minus_b_ms"] = -60.0
        result = adjudicate_episode(row)
        self.assertEqual(result["decision"], "REQUEST_EFFECTIVE_MISMATCH")
        self.assertIn("order_direction_matches", result["failed_checks"])

    def test_mutated_tensor_state_is_rejected(self) -> None:
        row = copy.deepcopy(self.by_id["MSIO-PD-E003-b01-qwen05-early_atomic"])
        row["effective_receipt"]["observations"]["tensor_gpu"] -= 1
        result = adjudicate_episode(row)
        self.assertEqual(result["decision"], "REQUEST_EFFECTIVE_MISMATCH")
        self.assertIn("all_tensors_on_gpu", result["failed_checks"])

    def test_missing_physical_readback_is_unverified(self) -> None:
        row = copy.deepcopy(self.by_id["MSIO-CA-E001-b01-p2-eager75"])
        row["effective_receipt"]["physical_verified"] = None
        result = adjudicate_episode(row)
        self.assertEqual(result["decision"], "EFFECTIVE_UNVERIFIED")
        self.assertIn("physical_verified", result["unverified_checks"])

    def test_two_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            subprocess.run([sys.executable, str(BUILDER), "--output-dir", first], check=True, capture_output=True, text=True)
            subprocess.run([sys.executable, str(BUILDER), "--output-dir", second], check=True, capture_output=True, text=True)
            for name in ("dev-corpus.jsonl", "policy-view.jsonl", "EVIDENCE-INVENTORY.tsv"):
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
