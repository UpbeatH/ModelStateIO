# MSIO-SP-E005 result: user-local Python runtime qualification

## Decision

**Technical No-Go for the frozen complete-standard-library runtime criterion.**
The private Python 3.10.14 build and installation succeeded, but its `_sqlite3`
extension is unavailable because the host lacks the corresponding development
headers. No system package, interpreter, CUDA component, model, server, or GPU
state was changed.

## Established observations

- Official source archive: `Python-3.10.14.tgz`, downloaded over HTTPS into
  `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e005/src/`;
  the source URL and SHA-256 are recorded outside Git.
- Private prefix:
  `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e005/prefix`.
- `prefix/bin/python3.10 --version` succeeded. Imports of `ssl` and `zlib`
  succeeded. The original sequential smoke reached `sqlite3` first and did not
  establish `ctypes`.
- The frozen smoke failed at `import sqlite3` with
  `ModuleNotFoundError: No module named '_sqlite3'`.
- E006R1 later independently established that `_ctypes` is also unavailable.
  This correction narrows the prior observation; it does not change E005's
  Technical No-Go decision.
- No llama/converter residue was introduced and GPU memory remained 0 MiB.

## Interpretation and boundary

E005 neither repairs nor changes E004. It shows that a user-local Python 3.10
runtime can be built on this host, but not that it satisfies the deliberately
broader standard-library criterion. `sqlite3` is not imported by the inspected
llama.cpp HF or LoRA converter paths; that narrower fact needs an independent
protocol and cannot retroactively make E005 pass.

## Next gate

E006 may independently install the exact converter dependency set into this
private Python and qualify only the actual converter imports. It must retain
the E005 `_sqlite3` limitation and must not use `apt`, `sudo`, a system Python,
or a global package change.
