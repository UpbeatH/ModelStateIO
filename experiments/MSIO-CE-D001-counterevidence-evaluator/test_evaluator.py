#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUILDER = HERE / "build_evaluator.py"
sys.path.insert(0, str(HERE))
from build_evaluator import build_cards, build_scenarios, decide, retrieve


class EvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(BUILDER)], check=True, capture_output=True, text=True)
        cls.cards = build_cards()
        cls.scenarios = {row["scenario_id"]: row for row in build_scenarios()}

    def test_counterevidence_changes_pacing_decision(self) -> None:
        item = self.scenarios["S02-CA-PACING-NECESSITY"]
        self.assertEqual(decide(item, retrieve(self.cards, item, True)), "PROBE")
        self.assertEqual(decide(item, retrieve(self.cards, item, False)), "ABSTAIN")

    def test_scope_veto_blocks_fixhead_apply(self) -> None:
        item = self.scenarios["S09-E006-FIXHEAD"]
        self.assertEqual(decide(item, retrieve(self.cards, item, True)), "APPLY")
        self.assertEqual(decide(item, retrieve(self.cards, item, False)), "PROBE")

    def test_exact_context_does_not_mix_grouped_and_alternating(self) -> None:
        item = self.scenarios["S04-LB-ALTERNATING"]
        ids = {row["card_id"] for row in retrieve(self.cards, item, False)}
        self.assertIn("LB-ALT-POS", ids)
        self.assertNotIn("LB-GROUPED-NULL", ids)

    def test_removing_harm_veto_changes_layerlease_decision(self) -> None:
        item = self.scenarios["S06-LAYERLEASE-CAPACITY"]
        full = retrieve(self.cards, item, False)
        self.assertEqual(decide(item, full), "ABSTAIN")
        without_harm = [row for row in full if row["card_id"] != "LL-E939-HARM"]
        self.assertEqual(decide(item, without_harm), "PROBE")

    def test_model_inputs_do_not_contain_hidden_labels(self) -> None:
        forbidden = ("oracle_decision", "oracle_basis", "implications", '"veto"', '"polarity"')
        for name in ("model-inputs-positive-only.jsonl", "model-inputs-counterevidence-aware.jsonl"):
            text = (HERE / name).read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text)

    def test_dual_build_is_byte_identical(self) -> None:
        names = (
            "evidence-cards.jsonl",
            "scenarios-with-oracles.jsonl",
            "model-inputs-positive-only.jsonl",
            "model-inputs-counterevidence-aware.jsonl",
            "retrieval-audit.jsonl",
            "baseline-results.json",
        )
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            subprocess.run([sys.executable, str(BUILDER), "--output-dir", first], check=True, capture_output=True, text=True)
            subprocess.run([sys.executable, str(BUILDER), "--output-dir", second], check=True, capture_output=True, text=True)
            for name in names:
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
