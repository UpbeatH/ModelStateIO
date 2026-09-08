#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
P0 = HERE.parent / "MSIO-CE-D002-TR1-P0-fast-screen"


def module(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / name)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class RepairTests(unittest.TestCase):
    def test_validation(self):
        self.assertEqual(module("validate_repair.py").validate()["decision"], "P1_PACKET_VALID")

    def test_only_messages_and_order_match(self):
        current = [json.loads(line) for line in (HERE / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        source = [json.loads(line) for line in (P0 / "prompts.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([row["messages"] for row in current], [row["messages"] for row in source])
        self.assertEqual([(row["condition"], row["scenario_id"]) for row in current], [(row["condition"], row["scenario_id"]) for row in source])

    def test_request_change_is_token_budget_only(self):
        repair = module("run_repair.py")
        body = json.loads(repair.request_body([{"role": "user", "content": "json"}]))
        self.assertEqual(body["max_tokens"], 4096)
        self.assertEqual(body["model"], "deepseek-v4-pro-0813")
        self.assertEqual(body["reasoning_effort"], "high")
        self.assertNotIn("tools", body)

    def test_dual_build(self):
        builder = module("build_repair.py")
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            builder.build(Path(one)); builder.build(Path(two))
            for name in ("prompts.jsonl", "prediction-template.jsonl", "run-manifest.json"):
                self.assertEqual((Path(one) / name).read_bytes(), (Path(two) / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
