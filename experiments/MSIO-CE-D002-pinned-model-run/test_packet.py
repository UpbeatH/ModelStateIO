#!/usr/bin/env python3

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUILDER = HERE / "build_packet.py"
SCORER = HERE / "score_predictions.py"
D001_SCENARIOS = HERE.parent / "MSIO-CE-D001-counterevidence-evaluator" / "scenarios-with-oracles.jsonl"
D001_BASELINES = HERE.parent / "MSIO-CE-D001-counterevidence-evaluator" / "baseline-results.json"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(BUILDER)], check=True, capture_output=True, text=True)
        cls.prompts = load_jsonl(HERE / "prompts.jsonl")

    def test_exact_schedule(self) -> None:
        self.assertEqual(len(self.prompts), 72)
        self.assertEqual(len({row["run_id"] for row in self.prompts}), 72)

    def test_every_call_is_fresh_luna_high(self) -> None:
        self.assertTrue(all(row["fresh_context_required"] for row in self.prompts))
        self.assertTrue(all(row["model"] == "gpt-5.6-luna" for row in self.prompts))
        self.assertTrue(all(row["reasoning_effort"] == "high" for row in self.prompts))

    def test_three_repetitions_per_condition_scenario(self) -> None:
        groups = {}
        for row in self.prompts:
            groups.setdefault((row["condition"], row["scenario_id"]), []).append(row["repetition"])
        self.assertEqual(len(groups), 24)
        self.assertTrue(all(sorted(repetitions) == [1, 2, 3] for repetitions in groups.values()))

    def test_prompt_has_no_oracle_fields(self) -> None:
        text = (HERE / "prompts.jsonl").read_text(encoding="utf-8")
        for token in ("oracle_decision", "oracle_basis", '"veto"', '"polarity"', "implications"):
            self.assertNotIn(token, text)

    def test_two_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            subprocess.run([sys.executable, str(BUILDER), "--output-dir", first], check=True, capture_output=True, text=True)
            subprocess.run([sys.executable, str(BUILDER), "--output-dir", second], check=True, capture_output=True, text=True)
            for name in ("prompts.jsonl", "prediction-template.jsonl", "run-manifest.json"):
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())

    def _completed_oracle_rows(self) -> list[dict]:
        oracles = {row["scenario_id"]: row["oracle_decision"] for row in load_jsonl(D001_SCENARIOS)}
        positive_predictions = json.loads(D001_BASELINES.read_text(encoding="utf-8"))["baselines"]["positive_only"]["predictions"]
        rows = []
        for prompt in self.prompts:
            supplied = json.loads(prompt["messages"][1]["content"])["input"]["evidence"]
            rows.append({
                "run_id": prompt["run_id"],
                "condition": prompt["condition"],
                "scenario_id": prompt["scenario_id"],
                "repetition": prompt["repetition"],
                "requested_model": "gpt-5.6-luna",
                "returned_model": "gpt-5.6-luna",
                "reasoning_effort": "high",
                "client_build": "test-fixture",
                "started_at": "fixture",
                "completed_at": "fixture",
                "latency_ms": 1,
                "status": "COMPLETED",
                "raw_response_sha256": hashlib.sha256(prompt["run_id"].encode()).hexdigest(),
                "response": {
                    "scenario_id": prompt["scenario_id"],
                    "decision": (
                        positive_predictions[prompt["scenario_id"]]
                        if prompt["condition"] == "positive_only"
                        else oracles[prompt["scenario_id"]]
                    ),
                    "cited_card_ids": [supplied[0]["card_id"]] if supplied else [],
                    "effective_state_assessment": "NOT_APPLICABLE",
                    "reason": "Synthetic scorer fixture, not a model response.",
                },
            })
        return rows

    def test_scorer_accepts_complete_schema_valid_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            predictions = root / "predictions.jsonl"
            output = root / "score.json"
            predictions.write_text(
                "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in self._completed_oracle_rows()),
                encoding="utf-8",
                newline="\n",
            )
            subprocess.run([sys.executable, str(SCORER), str(predictions), "--output", str(output)], check=True, capture_output=True, text=True)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["decision"], "D002_DEVELOPMENT_MODEL_GO_TO_D003_DESIGN")
            self.assertTrue(result["development_only"])

    def test_scorer_stops_after_more_than_three_invalid_calls(self) -> None:
        rows = self._completed_oracle_rows()
        changed = 0
        for row in rows:
            if row["condition"] == "positive_only" and changed < 4:
                row["status"] = "ERROR"
                changed += 1
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            predictions = root / "predictions.jsonl"
            output = root / "score.json"
            predictions.write_text(
                "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
                encoding="utf-8",
                newline="\n",
            )
            subprocess.run([sys.executable, str(SCORER), str(predictions), "--output", str(output)], check=True, capture_output=True, text=True)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["decision"], "D002_TECHNICAL_STOP_INVALID_OUTPUT_RATE")


if __name__ == "__main__":
    unittest.main()
