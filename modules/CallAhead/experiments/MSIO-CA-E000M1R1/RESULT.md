# MSIO-CA-E000M1R1 result

## Observation

The direct official-CDN transfer completed quickly, but the temporary file was
1,119,204,896 bytes with SHA-256
`f3b2a0f81ef0c7d7be2ad316aa9f923983e32129aed462ef79d6f6135d767347`,
not the frozen 1,117,320,736 bytes and expected digest. No final rename
occurred.

A post-failure process audit found that the earlier proxy-mediated E000M1
`curl` remained alive after its SSH client was interrupted and was still
writing the same temporary path. The exact task-owned PID was terminated and
its disappearance was verified. An unrelated long-lived `sftp-server` was not
touched.

## Decision

**NO_GO for E000M1R1's reused temporary file.** The failure is a concurrent
writer/protocol defect, not an artifact-identity failure or CallAhead
scientific result. The corrupted temporary path is ineligible for reuse. A new
ID may perform one clean download to a new path only after a no-writer
preflight.

