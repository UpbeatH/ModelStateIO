import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
for name in ("verify_candidate", "trace_logic"):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
LOGIC = sys.modules["trace_logic"]


class TraceLogicTest(unittest.TestCase):
    def test_routing_is_frozen(self):
        self.assertIsNone(LOGIC.route_verifier_classification("pass"))
        self.assertEqual(LOGIC.route_verifier_classification("assertion_failure"),
                         LOGIC.ASSERTION_REPAIR)
        self.assertEqual(LOGIC.route_verifier_classification("syntax_failure"),
                         LOGIC.STRUCTURAL_REPAIR)
        with self.assertRaises(ValueError):
            LOGIC.route_verifier_classification("sandbox_failure")

    def test_decision_view_is_outcome_blind(self):
        task = {"task_id": "mbpp-a", "prompt_sha256": "abc"}
        view = LOGIC.outcome_blind_view(task, "def f():\n    return 1", {LOGIC.PRIMARY})
        self.assertTrue(view["syntax_parse_ok"])
        self.assertEqual(view["function_count"], 1)
        forbidden = {"branch_outcome", "correctness", "arrival_ns",
                     "completion_ns", "selected_state_id", "branch_resolution_ns"}
        self.assertFalse(forbidden & set(view))

    def test_syntax_error_is_available_without_tests(self):
        features = LOGIC.static_features("def broken(:\n pass")
        self.assertFalse(features["syntax_parse_ok"])


if __name__ == "__main__":
    unittest.main()
