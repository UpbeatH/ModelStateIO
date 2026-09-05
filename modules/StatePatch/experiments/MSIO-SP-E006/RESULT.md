# MSIO-SP-E006 result: bootstrap URL failure

## Decision

**Technical No-Go; no converter qualification was reached.** The frozen PyPA
bootstrap URL `https://bootstrap.pypa.io/pip/3.10/get-pip.py` returned HTTPS
404 before pip installation or any converter command. E006 is closed and must
not be rerun.

## Evidence boundary

No model, adapter, converter, server, GPU, source-tree file, system package,
or global path changed. The private E005 interpreter and E006 target directory
remain available, but their existence is not E006 success evidence.

## Successor rule

A new E006R1 may first read-only verify an official PyPA bootstrap endpoint,
freeze its exact URL and SHA-256, then repeat the same converter-subset scope.
It must not reuse E006 as a dependency or converter result.
