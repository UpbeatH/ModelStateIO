#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "MSIO-CE-D002-TR1-P0-fast-screen" / "score_pilot.py"


def main() -> int:
    spec = importlib.util.spec_from_file_location("p0_scorer", SOURCE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = HERE
    module.D001 = HERE.parents[1] / "experiments/MSIO-CE-D001-counterevidence-evaluator"
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
