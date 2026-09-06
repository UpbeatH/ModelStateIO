import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).with_name("validate_material.py")
SPEC = importlib.util.spec_from_file_location("validate_material", MODULE)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def event(index: int) -> dict:
    selected = None if index % 5 == 0 else "repair_a"
    return {
        "event_id": f"e{index}", "task_id": f"t{index}", "node_id": "test",
        "notice_ns": index * 100 + 1,
        "candidate_state_ids": ["repair_a", "repair_b"],
        "dependency_ids": [f"solver-{index}"], "selected_state_id": selected,
        "arrival_ns": None if selected is None else index * 100 + 2,
        "completion_ns": None if selected is None else index * 100 + 3,
        "branch_outcome": "pass" if selected is None else "repair",
        "correctness": True, "decision_view": {"queue_depth": 0},
        "transition_bytes": 0 if selected is None else 10,
        "eviction_required": index == 1,
    }


class MaterialValidatorTests(unittest.TestCase):
    def run_case(self, events, capacity):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            trace = root_path / "trace.jsonl"
            trace.write_text("".join(json.dumps(row) + "\n" for row in events))
            cap = root_path / "capacity.json"
            cap.write_text(json.dumps(capacity))
            return VALIDATOR.validate(trace, cap)

    def test_valid_contract(self):
        result = self.run_case(
            [event(i) for i in range(100)],
            {"usable_hbm_bytes": 100, "per_model_peak_hbm_bytes": {
                "primary": 40, "repair_a": 40, "repair_b": 40}},
        )
        self.assertEqual(result["decision"], "PASS_MATERIAL_CONTRACT_ONLY")

    def test_future_leak_is_rejected(self):
        events = [event(i) for i in range(100)]
        events[0]["decision_view"]["selected_state_id"] = "repair_a"
        with self.assertRaises(VALIDATOR.Invalid):
            self.run_case(events, {"usable_hbm_bytes": 100,
                "per_model_peak_hbm_bytes": {"primary": 40, "repair_a": 40, "repair_b": 40}})

    def test_software_only_capacity_is_rejected(self):
        with self.assertRaises(VALIDATOR.Invalid):
            self.run_case([event(i) for i in range(100)], {
                "usable_hbm_bytes": 200,
                "per_model_peak_hbm_bytes": {"primary": 40, "repair_a": 40, "repair_b": 40}})


if __name__ == "__main__":
    unittest.main()
