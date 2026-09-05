# MSIO-SP-E005 user-local Python runtime qualification

## Objective

Build and qualify a Python 3.10 runtime entirely below the permitted g130
private StatePatch runtime root, because E004 established that the existing
system Python 3.8 cannot import the selected llama.cpp converter.

## Frozen scope

- Source: the official Python 3.10.14 source archive over HTTPS; record its
  final URL, byte count, and SHA-256 outside Git before configure.
- Build root: `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e005`.
- Install prefix: `<build-root>/prefix`; no `sudo`, system package manager,
  system site-packages, CUDA, driver, service, cache, Lustre/PFS, g129, or
  other-user paths.
- Configure only with `--prefix=<prefix> --without-ensurepip`; compile with a
  bounded timeout. Do not convert a model or invoke llama.cpp during E005.

## Pass rule

PASS requires Python 3.10.x from the private prefix, a successful standard
library import smoke (`ssl`, `zlib`, `sqlite3`, `ctypes`), and no process/GPU
residue. A missing build prerequisite, failed archive identity, configure or
compile failure is Technical No-Go for this runtime path; it does not justify
editing the system interpreter or converter.

## Boundary

This only qualifies an interpreter. A fresh E006 must install converter
dependencies into a matching private site directory before import or
conversion may be attempted.
