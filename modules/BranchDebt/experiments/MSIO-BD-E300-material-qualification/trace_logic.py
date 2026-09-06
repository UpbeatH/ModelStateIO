#!/usr/bin/env python3
"""Frozen outcome-blind BranchDebt E300 trace logic."""

import ast
import hashlib

from verify_candidate import extract_code


PRIMARY = "qwen2.5-7b-instruct-q4_k_m"
ASSERTION_REPAIR = "qwen2.5-14b-instruct-q4_k_m"
STRUCTURAL_REPAIR = "qwen2.5-32b-instruct-q5_k_m"
CANDIDATES = [ASSERTION_REPAIR, STRUCTURAL_REPAIR]


def route_verifier_classification(classification):
    if classification == "pass":
        return None
    if classification == "assertion_minor":
        return ASSERTION_REPAIR
    if classification in {
        "assertion_major",
        "syntax_failure", "import_failure", "runtime_failure",
        "timeout_failure", "resource_failure",
    }:
        return STRUCTURAL_REPAIR
    raise ValueError("unqualified verifier classification: {}".format(classification))


def static_features(answer):
    code = extract_code(answer)
    try:
        tree = ast.parse(code)
        syntax_ok = True
        function_count = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                             for node in ast.walk(tree))
        import_count = sum(isinstance(node, (ast.Import, ast.ImportFrom))
                           for node in ast.walk(tree))
    except SyntaxError:
        syntax_ok, function_count, import_count = False, 0, 0
    return {
        "answer_sha256": hashlib.sha256(answer.encode("utf-8")).hexdigest(),
        "answer_bytes": len(answer.encode("utf-8")),
        "syntax_parse_ok": syntax_ok,
        "function_count": function_count,
        "import_count": import_count,
    }


def outcome_blind_view(task, answer, resident_states):
    view = {
        "task_id": task["task_id"],
        "prompt_sha256": task["prompt_sha256"],
        "candidate_state_ids": list(CANDIDATES),
        "resident_state_ids": sorted(resident_states),
        "dependency_id": "verify-primary-{}".format(task["task_id"]),
    }
    view.update(static_features(answer))
    return view


def repair_prompt(task_prompt, initial_answer, failure_class):
    if failure_class not in {
        "assertion_minor", "assertion_major", "syntax_failure", "import_failure",
        "runtime_failure", "timeout_failure", "resource_failure",
    }:
        raise ValueError("repair prompt requires a frozen failure class")
    return (
        "Solve the programming task below. The previous answer failed with "
        "the coarse verifier class `{}`. Return only a corrected Python "
        "implementation; do not repeat the tests.\n\nTASK:\n{}\n\nPREVIOUS "
        "ANSWER:\n{}\n".format(failure_class, task_prompt, initial_answer)
    )
