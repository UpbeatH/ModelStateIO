#!/usr/bin/env python3
"""Build the frozen E300 MBPP development set without importing old outputs."""

import argparse
import hashlib
import json
from pathlib import Path


def prompt_hash(prompt):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def iter_unique_tasks(paths):
    seen = set()
    for path in sorted(paths):
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                row = json.loads(line)
                prompt = row.get("prompt")
                if not isinstance(prompt, str) or "Test cases:" not in prompt:
                    continue
                digest = prompt_hash(prompt)
                if digest in seen:
                    continue
                seen.add(digest)
                yield {
                    "task_id": "mbpp-" + digest[:16],
                    "prompt_sha256": digest,
                    "prompt": prompt,
                    "source_file": path.name,
                    "source_line": line_number,
                }


def prepare(paths, development_path, heldout_path):
    tasks = list(iter_unique_tasks(paths))
    if len(tasks) < 400:
        raise ValueError("need at least 400 unique executable MBPP prompts")
    development = tasks[:300]
    heldout = tasks[300:400]

    with development_path.open("w", encoding="utf-8", newline="\n") as stream:
        for task in development:
            stream.write(json.dumps(task, sort_keys=True) + "\n")

    # Do not place held-out prompt text in the E300 material packet.
    receipt = {
        "count": len(heldout),
        "ordered_prompt_sha256": [task["prompt_sha256"] for task in heldout],
        "content_disclosed": False,
    }
    heldout_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return len(development), len(heldout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--development", type=Path, required=True)
    parser.add_argument("--heldout-receipt", type=Path, required=True)
    args = parser.parse_args()
    paths = [Path(value) for value in args.input]
    counts = prepare(paths, args.development, args.heldout_receipt)
    print("development={} heldout={}".format(*counts))


if __name__ == "__main__":
    main()
