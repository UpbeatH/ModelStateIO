#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
TR1 = HERE.parent / "MSIO-CE-D002-TR1-tokenrhythm"
D001 = HERE.parents[1] / "experiments/MSIO-CE-D001-counterevidence-evaluator"


def module(name: str):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class PilotTests(unittest.TestCase):
    def test_packet(self):
        self.assertEqual(module("validate_pilot.py").validate()["decision"], "P0_PACKET_VALID")

    def test_exact_24_and_source_messages(self):
        prompts = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        source = {(row["condition"], row["scenario_id"]): row for row in [json.loads(line) for line in (TR1 / "prompts.jsonl").read_text(encoding="utf-8").splitlines()] if row["repetition"] == 1}
        self.assertEqual(len(prompts), 24)
        for row in prompts:
            self.assertEqual(row["messages"], source[(row["condition"], row["scenario_id"])]["messages"])

    def test_condition_order_is_bounded(self):
        conditions = [json.loads(line)["condition"] for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertFalse(any(len(set(conditions[index:index + 3])) == 1 for index in range(len(conditions) - 2)))

    def test_fingerprint_is_optional_but_model_and_thinking_are_required(self):
        runner = module("run_pilot.py")
        receipt = {"http_status": 200, "response_id": "id", "returned_model": "deepseek-v4-pro-0813", "usage": {}, "thinking_observed": True, "system_fingerprint": None}
        self.assertTrue(runner.receipt_ok(receipt, {}))
        receipt["thinking_observed"] = False
        self.assertFalse(runner.receipt_ok(receipt, {}))

    def test_scorer_go_fixture(self):
        prompts = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        oracles = {row["scenario_id"]: row["oracle_decision"] for row in [json.loads(line) for line in (D001 / "scenarios-with-oracles.jsonl").read_text(encoding="utf-8").splitlines()]}
        rows = []
        for prompt in prompts:
            decision = oracles[prompt["scenario_id"]] if prompt["condition"] == "counterevidence_aware" else "PROBE"
            rows.append({
                "run_id": prompt["run_id"], "status": "COMPLETED",
                "requested_model": "deepseek-v4-pro-0813", "returned_model": "deepseek-v4-pro-0813",
                "raw_response_sha256": "0" * 64,
                "response": {"scenario_id": prompt["scenario_id"], "decision": decision},
            })
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "predictions.jsonl"
            output = Path(temp) / "score.json"
            ledger.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(HERE / "score_pilot.py"), str(ledger), "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["decision"], "P0_GO_TO_REAL_SYSTEM_DESIGN")


if __name__ == "__main__":
    unittest.main()
