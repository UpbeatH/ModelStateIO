# MSIO-SP-E007 private prerequisite rebuild

## Objective

Repair only the two missing private Python extension prerequisites established
by E005/E006R1: `libffi` for `_ctypes` and SQLite for `_sqlite3`. Build both
from official source archives under a new private prefix, then build a fresh
Python 3.10.14 against that prefix.

## Frozen scope

- New root: `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e007`.
- Official archives: libffi 3.4.6 release, SQLite 3.45.3 autoconf release, and
  Python 3.10.14. Record HTTPS URLs, bytes, and SHA-256 before each build.
- Install all three only below `<root>/deps` and `<root>/prefix`, using bounded
  configure/make/install commands. Python receives only explicit private
  include/library/rpath flags.
- No `sudo`, system package manager, system interpreter change, source patch,
  model conversion/load, server, GPU work, cache change, Lustre/PFS, g129, or
  other-user access.

## Pass rule

The new private Python must import `ssl`, `zlib`, `sqlite3`, and `ctypes`
individually, report `_sqlite3` and `_ctypes` extension locations below its
private prefix, and leave no converter/model process or GPU allocation. Any
source, configure, build, import, scope, or cleanup failure is Technical
No-Go; it must not be repaired with a system package.

## Boundary

E007 is an interpreter-qualification repair only. A new ID must reinstall and
qualify converter dependencies against this new interpreter.
