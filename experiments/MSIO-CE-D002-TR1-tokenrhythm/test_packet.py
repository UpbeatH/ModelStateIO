#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
D002 = HERE.parent / "MSIO-CE-D002-pinned-model-run"


def load(name: str):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PacketTests(unittest.TestCase):
    def test_static_validation(self):
        self.assertEqual(load("validate_packet.py").validate()["decision"], "TR1_PACKET_STATIC_VALID")

    def test_exact_schedule_and_identity(self):
        rows = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 72)
        self.assertEqual({row["model"] for row in rows}, {"deepseek-v4-pro-0813"})
        self.assertEqual({row["reasoning_effort"] for row in rows}, {"high"})
        self.assertTrue(all(row["fresh_context_required"] for row in rows))

    def test_messages_are_byte_equivalent_objects(self):
        current = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        source = [json.loads(line) for line in (D002 / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([row["messages"] for row in current], [row["messages"] for row in source])

    def test_request_has_no_tools_or_history(self):
        runner = load("run_gateway.py")
        body = json.loads(runner.request_body([{"role": "user", "content": "json"}]))
        self.assertNotIn("tools", body)
        self.assertEqual(body["thinking"], {"type": "enabled"})
        self.assertEqual(body["reasoning_effort"], "high")
        self.assertFalse(body["stream"])
        self.assertEqual(len(body["messages"]), 1)

    def test_prediction_contract_rejects_unknown_citation(self):
        runner = load("run_gateway.py")
        prompt = json.loads((HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()[0])
        prediction = {
            "scenario_id": prompt["scenario_id"],
            "decision": "ABSTAIN",
            "cited_card_ids": ["not-supplied"],
            "effective_state_assessment": "UNVERIFIED",
            "reason": "json contract test",
        }
        self.assertFalse(runner.valid_prediction(prediction, prompt))

    def test_missing_key_stops_without_network(self):
        env = dict(os.environ)
        env.pop("TOKENRHYTHM_API_KEY", None)
        result = subprocess.run(
            [sys.executable, str(HERE / "run_gateway.py"), "--smoke"],
            cwd=HERE,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("TR1_TECHNICAL_STOP_CREDENTIAL", result.stderr + result.stdout)

    def test_dual_build_is_identical(self):
        builder = load("build_packet.py")
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            builder.build(Path(first))
            builder.build(Path(second))
            for name in ("prompts.jsonl", "prediction-template.jsonl", "run-manifest.json"):
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())

    def test_no_key_literal_in_packet(self):
        for path in HERE.iterdir():
            if path.is_file():
                self.assertNotIn("sk" + "_tr_", path.read_text(encoding="utf-8", errors="ignore"))


if __name__ == "__main__":
    unittest.main()
