#!/usr/bin/env python3
"""Audit the frozen development material without opening model outcomes."""

import argparse
import json
from collections import Counter
from pathlib import Path

from verify_candidate import extract_tests


def audit(path):
    counts = Counter()
    tasks = 0
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            tests = [item for item in extract_tests(row["prompt"]).splitlines()
                     if item.strip()]
            counts[len(tests)] += 1
            tasks += 1
    if tasks != 300:
        raise ValueError("expected 300 frozen development tasks")
    if counts != Counter({3: 300}):
        raise ValueError("nonuniform assertion contract: {}".format(dict(counts)))
    return {"tasks": tasks, "assertions_per_task": dict(counts),
            "decision": "PASS_TASK_STRUCTURE_ONLY"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("development", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.development), sort_keys=True))


if __name__ == "__main__":
    main()
