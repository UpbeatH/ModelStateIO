# MSIO-SP-E007R2 private prerequisite build without remote re-download

## Objective

Run the still-unexecuted private prerequisite build without repeating E007R1's
stalled Python download. Reuse only complete, locally verified archives already
within the permitted runtime tree.

## Frozen scope

- New root: `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e007r2`.
- Before copying, hash and record the complete E005 Python 3.10.14 archive,
  E007R1 libffi 3.4.6 archive, and E007R1 SQLite 3.45.3 archive.
- Build libffi and SQLite below `<root>/deps`, then Python 3.10.14 below
  `<root>/prefix` using only explicit private include/library/rpath flags.
- No download, no model/converter invocation, no system package change,
  cache operation, global path change, GPU work, Lustre/PFS, g129, or
  other-user path access.

## Pass rule

Python must separately import `ssl`, `zlib`, `sqlite3`, and `ctypes`; both
`_sqlite3` and `_ctypes` locations must resolve under the new prefix. A build,
import, isolation, process-residue, or GPU-residue failure is Technical No-Go.
