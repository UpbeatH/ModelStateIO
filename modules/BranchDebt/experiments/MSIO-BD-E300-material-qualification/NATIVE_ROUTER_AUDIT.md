# Native llama.cpp router audit

Audit date: 2026-09-06. Evidence level: pinned-source and built-binary
qualification; no performance claim.

## Identity

- llama.cpp source/build revision:
  `d230ddd763ffe27781c7ffd237ea78b639b36b6d`; the official source archive and
  isolated build are already bound by the E003 receipt (archive SHA-256
  `2625b2172f06ab97e0b4331ac6d2ff93d76278922699212b1be61758d27e816f`).
- `tools/server/server-models.cpp` SHA-256:
  `c594bd934ee4539001e34e4f91842dc506ad2447fa1ebf71df9aeffd23b7e8c5`.
- `tools/server/README.md` SHA-256:
  `43ffb21ba93368e58ed6639598f26d6a309a0a0a24fad962fc6b6730965a6655`.
- The built `llama-server --help` exposes `--models-dir`, `--models-preset`,
  `--models-max` and `--[no-]models-autoload`.

## Established native behavior

The pinned router can discover local multi-shard GGUF subdirectories, route
requests by the JSON `model` field, report model status through `GET /models`,
and explicitly load/unload a named model through `POST /models/load` and
`POST /models/unload`.

The source implementation calls `unload_lru()` before a new load when
`models_max` is reached. It selects a victim through the router scheduler,
logs that it is removing the least-recently-used model, waits for unload, and
then starts the requested instance. A second locked capacity check prevents
concurrent loads from exceeding the configured instance count.

## Consequence for BranchDebt

- Native LRU is a mandatory strong baseline, not a strawman.
- BranchDebt does not need to modify the inference engine for its first gate.
  An external, frozen controller can observe only the prospective program
  receipt, use the explicit load/unload endpoints, and verify action readback
  through `GET /models` and SSE events.
- `models_max` remains a software instance limit and cannot establish the
  paper's physical-capacity premise. E300 still requires measured HBM and a
  real eviction/reload transition.
- The defensible novelty question is narrower: whether prospective dependency,
  wrong-branch probability and eviction debt select a materially better state
  transition than the pinned native LRU and equal-information heuristics under
  real capacity pressure. Merely adding preloading or exposing the endpoints
  is not novel.

## Frozen interface for later gates

E301 will run the pinned router locally with autoload disabled. Every policy,
including baselines, receives the same frontier receipt and may issue only the
same named `load`, `unload`, or `abstain` actions. Completion is established
from router status/events rather than request return alone. Network download
and model deletion endpoints are out of scope.
