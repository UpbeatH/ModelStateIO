#!/usr/bin/env python3
"""Run the frozen D002 scorer logic against the TR1 packet."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "MSIO-CE-D002-pinned-model-run" / "score_predictions.py"


def main() -> int:
    spec = importlib.util.spec_from_file_location("d002_frozen_scorer", SOURCE)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load frozen D002 scorer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = HERE
    module.MSIO = HERE.parents[1]
    module.D001 = module.MSIO / "experiments/MSIO-CE-D001-counterevidence-evaluator"
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
