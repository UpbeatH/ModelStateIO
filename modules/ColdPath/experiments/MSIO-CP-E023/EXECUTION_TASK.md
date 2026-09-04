# MSIO-CP-E023 execution task

After a fresh g130 audit verifies no GPU work, the pinned runtime/model and
measurement hashes, and a fresh E023 log root, run `run_e023.py` exactly once.
It may write only under its declared external log root. Return the receipts
hash, all rows, and final GPU/process cleanup. Stop without retry on failure.
