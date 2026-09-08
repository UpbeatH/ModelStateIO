#!/usr/bin/env python3
"""Reference semantics for D003; this module does not execute actions."""

from __future__ import annotations

from typing import Any


HISTORY_ADMITTED = {"EFFECTIVE_VERIFIED", "CANONICALIZED_VERIFIED"}


def _lookup(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for component in path.split("."):
        if not isinstance(current, dict) or component not in current:
            raise KeyError(path)
        current = current[component]
    return current


def _predicate_holds(observations: dict[str, Any], predicate: dict[str, Any]) -> bool:
    actual = _lookup(observations, predicate["path"])
    expected = predicate["value"]
    op = predicate["op"]
    tolerance = predicate.get("tolerance", 0)
    if op == "eq":
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return abs(actual - expected) <= tolerance
        return actual == expected
    if op == "ge":
        return actual >= expected - tolerance
    if op == "le":
        return actual <= expected + tolerance
    if op == "contains":
        return expected in actual
    raise ValueError(f"unsupported predicate operator: {op}")


def evaluate(contract: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    """Classify one frozen action/receipt pair and decide history admission."""
    if not receipt["precheck"]["passed"]:
        classification = "PRECHECK_REJECTED"
    elif receipt["ack"]["accepted"] is not True:
        classification = "ACK_REJECTED"
    else:
        required = contract["receipt_requirements"]["channels"]
        observations = receipt["observations"]
        missing = [channel for channel in required if not observations.get(channel)]
        if missing or not receipt["freshness_verified"] or not receipt["identity_verified"]:
            classification = "EFFECTIVE_UNVERIFIED"
        else:
            try:
                matches = all(
                    _predicate_holds(observations, predicate)
                    for predicate in contract["semantic_intent"]["predicates"]
                )
            except (KeyError, TypeError, ValueError):
                matches = False
            if not matches:
                classification = "SEMANTIC_MISMATCH"
            elif receipt["outcome"]["status"] != "COMPLETED" or receipt["outcome"]["correct"] is not True:
                classification = "OUTCOME_INVALID"
            elif contract["rollback"]["required"] and receipt["rollback"]["verified"] is not True:
                classification = "ROLLBACK_FAILED"
            elif not receipt["cleanup"]["verified"]:
                classification = "CLEANUP_FAILED"
            elif receipt["canonicalization"]["changed"]:
                classification = "CANONICALIZED_VERIFIED"
            else:
                classification = "EFFECTIVE_VERIFIED"
    return {
        "classification": classification,
        "history_admitted": classification in HISTORY_ADMITTED,
    }
