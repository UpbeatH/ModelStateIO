#!/usr/bin/env python3

from __future__ import annotations

import copy
import unittest

from gate_reference import evaluate


def base_contract() -> dict:
    return {
        "receipt_requirements": {
            "channels": ["control_plane", "physical"],
            "freshness_required": True,
            "identity_match_required": True,
        },
        "semantic_intent": {
            "predicates": [
                {"path": "physical.offloaded_layers", "op": "eq", "value": 42},
                {"path": "control_plane.total_layers", "op": "eq", "value": 42},
            ]
        },
        "rollback": {"required": False, "predicate": None},
    }


def base_receipt() -> dict:
    return {
        "precheck": {"passed": True, "reason": None},
        "ack": {"accepted": True, "receipt": {"exit_code": 0}},
        "observations": {
            "control_plane": {"total_layers": 42},
            "physical": {"offloaded_layers": 42},
            "semantic": None,
            "lineage": None,
        },
        "freshness_verified": True,
        "identity_verified": True,
        "canonicalization": {"changed": False, "requested": 42, "effective": 42},
        "outcome": {"status": "COMPLETED", "correct": True, "metrics": {}},
        "rollback": {"required": False, "verified": None},
        "cleanup": {"verified": True},
    }


class GateReferenceTests(unittest.TestCase):
    def test_exact_effective_state_is_admitted(self) -> None:
        self.assertEqual(evaluate(base_contract(), base_receipt()), {
            "classification": "EFFECTIVE_VERIFIED", "history_admitted": True})

    def test_benign_canonicalization_is_admitted(self) -> None:
        receipt = base_receipt()
        receipt["canonicalization"] = {"changed": True, "requested": 999, "effective": 42}
        self.assertEqual(evaluate(base_contract(), receipt)["classification"], "CANONICALIZED_VERIFIED")

    def test_acknowledged_semantic_mismatch_is_rejected(self) -> None:
        receipt = base_receipt()
        receipt["observations"]["physical"]["offloaded_layers"] = 0
        result = evaluate(base_contract(), receipt)
        self.assertEqual(result["classification"], "SEMANTIC_MISMATCH")
        self.assertFalse(result["history_admitted"])

    def test_missing_required_readback_is_unverified(self) -> None:
        receipt = base_receipt()
        receipt["observations"]["physical"] = None
        self.assertEqual(evaluate(base_contract(), receipt)["classification"], "EFFECTIVE_UNVERIFIED")

    def test_stale_or_wrong_identity_is_unverified(self) -> None:
        for field in ("freshness_verified", "identity_verified"):
            with self.subTest(field=field):
                receipt = base_receipt()
                receipt[field] = False
                self.assertEqual(evaluate(base_contract(), receipt)["classification"], "EFFECTIVE_UNVERIFIED")

    def test_precheck_and_ack_fail_closed(self) -> None:
        receipt = base_receipt()
        receipt["precheck"]["passed"] = False
        self.assertEqual(evaluate(base_contract(), receipt)["classification"], "PRECHECK_REJECTED")
        receipt = base_receipt()
        receipt["ack"]["accepted"] = False
        self.assertEqual(evaluate(base_contract(), receipt)["classification"], "ACK_REJECTED")

    def test_failed_outcome_does_not_enter_history(self) -> None:
        receipt = base_receipt()
        receipt["outcome"]["correct"] = False
        self.assertEqual(evaluate(base_contract(), receipt)["classification"], "OUTCOME_INVALID")

    def test_rollback_and_cleanup_are_terminal_gates(self) -> None:
        contract = copy.deepcopy(base_contract())
        contract["rollback"]["required"] = True
        receipt = base_receipt()
        receipt["rollback"] = {"required": True, "verified": False}
        self.assertEqual(evaluate(contract, receipt)["classification"], "ROLLBACK_FAILED")
        receipt = base_receipt()
        receipt["cleanup"]["verified"] = False
        self.assertEqual(evaluate(base_contract(), receipt)["classification"], "CLEANUP_FAILED")


if __name__ == "__main__":
    unittest.main()
