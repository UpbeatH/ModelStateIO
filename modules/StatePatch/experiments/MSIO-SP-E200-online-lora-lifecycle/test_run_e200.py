import importlib.util
import json
import unittest
from pathlib import Path


MODULE = Path(__file__).with_name("run_e200.py")
SPEC = importlib.util.spec_from_file_location("run_e200", MODULE)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class RunnerContractTests(unittest.TestCase):
    def test_completion_contract(self):
        self.assertEqual(RUNNER.output_text({"content": "ok"}), "ok")
        with self.assertRaises(RUNNER.Stop):
            RUNNER.output_text({"content": 7})

    def test_idle_contract(self):
        RUNNER.ensure_idle({"slots": [{"is_processing": False}]})
        with self.assertRaises(RUNNER.Stop):
            RUNNER.ensure_idle(json.loads('{"is_generating": true}'))


if __name__ == "__main__":
    unittest.main()
