# MSIO-CP-E002 loading-path feasibility gate

Frozen: 2026-09-04. This gate is read-only on the target host.

## Question

Can the already-installed runtime or source expose at least two genuinely distinct model-loading paths, with effective settings that can be read back, without installing software, patching source, dropping global caches, remounting filesystems, or touching raw devices?

## Allowed inspection

Inspect binaries, help/version output, service configuration, model metadata, and existing source trees. No model request, cache eviction, process start/stop, file copy, or download is allowed in E002.

## Pass/stop rules

- **PASS:** at least two implemented paths are identified, their controls are documented, and each has a non-destructive readback or observable effective setting.
- **NO-GO:** only one opaque path is available, or a second path requires installation, source modification, kernel/mount changes, global cache eviction, or raw-device access.
- A PASS permits drafting E003; it does not authorize an experiment.

