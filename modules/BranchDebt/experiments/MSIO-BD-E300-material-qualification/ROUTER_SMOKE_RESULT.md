# E300 native-router smoke result

Date: 2026-09-06. Frozen code revision:
`eead901652ec3f12d00fe94ea81537a57f5d5315`.

## Established observation

Using the three provenance-complete small artifacts, the pinned router started
with autoload disabled and `models_max=2`. Explicit loads completed as follows:

- Qwen 0.5B: 1263.23 ms; status readback `loaded`.
- Qwen 1.5B: 1262.45 ms; both first models read back `loaded`.
- SmolLM2 1.7B: 1118.82 ms; final readback showed Qwen 0.5B `unloaded`
  and the latter two models `loaded`.

The raw router log explicitly reports `models_max limit reached, removing LRU
name=qwen-0.5b`. Postflight found no GPU compute process or llama process.

Git-external receipts:

- `RESULT.json`: 1,217 bytes; SHA-256
  `c4a2b4b2d2c5b6cc06c20f90dd78305ac0258154f58d108f09bdce7827b081ca`.
- `router.log`: 8,953 bytes; SHA-256
  `b0bd2fb0498382bdaa79b58d7ae7aa51f9b6c5d3f0a13e6d8cf5a17938bba855`.

## Decision

**PASS for technical native-router action/readback qualification.** Explicit
load, status observation, and native LRU eviction can support a later
equal-action policy comparison without modifying llama.cpp.

This is not E300 PASS and not performance evidence. The small artifacts do not
create the frozen physical HBM conflict; the large pinned artifacts, measured
capacity transition, and prospective 100-event workload remain required.
