# MSIO-CA-E000M1 result

## Observation

The official artifact downloaded locally and passed the frozen size and
SHA-256 checks. The configured `scp`/SFTP path transferred only a few MiB over
multiple minutes, and a proxy-mediated remote resolver download projected
many hours. Both were stopped while still writing the temporary remote name.
No final path was created and no model was launched.

## Decision

**MATERIAL_BLOCKED for the frozen transfer method.** The artifact identity is
valid; the transport path is not operationally bounded. A direct request to
the official pinned resolver's signed CDN target was separately observed to be
reachable from g130. That alternative requires a new frozen subgate and may
reuse the partial bytes only through HTTP range-resume followed by a full hash.

