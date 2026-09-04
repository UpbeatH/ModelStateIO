# StateTier automatic progression policy

This line is configured for continuation across task turns until a registered
`GO` or `NO-GO` decision is reached.

- After each completed gate, continue to the next frozen gate automatically.
- A technical failure, missing input, contamination, unsupported interface,
  or safety ambiguity pauses progression at that gate; it is not silently
  retried or reclassified as scientific evidence.
- Every new remote action requires a packet with explicit scope. Existing
  user authorization permits the StateTier line to proceed, but does not
  permit system/PFS parameter writes, installations, mounts, service changes,
  or destructive cleanup unless separately and explicitly added.
- PFSOpt remains the only cluster-active mainline. StateTier may use a
  provisionally suitable node only after an immediate read-only audit.
- Each gate records observations, raw external paths, hashes where applicable,
  decision status, and the exact next gate. Repository changes are committed
  and pushed after review when the remote is available.
- Automatic progression terminates only at the preregistered StateTier
  `GO`/`NO-GO`, or when a missing external authority/input cannot be resolved
  within the current scope. The current unified multi-state route has reached
  `NO-GO` on 2026-09-04; any single-state downgrade requires a new protocol.
