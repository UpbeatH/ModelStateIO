# MSIO-SP-E201 real lifecycle and prior-art audit

Date: 2026-09-06. Status: **research No-Go for the present StatePatch
candidate**. This source-level gate follows the closed CallAhead E201 audit;
it starts no GPU process and does not reinterpret E200 as a performance result.

## Frozen admission requirements

A StatePatch successor must have a lawful, provenance-complete real adapter
lifecycle trace with immutable adapter/base versions, request-to-adapter
binding, task-quality oracle, arrival/completion and a measured finite capacity
conflict. It must also retain a mechanism not already delivered by online
adapter serving systems.

## Audited evidence

- [Kiln](https://github.com/ericflo/kiln) documents bounded online-LoRA SFT,
  atomic publication, live hot-swap, managed agent trajectories, adapter
  transitions, and evaluation endpoints. Its published scope is a local,
  correctness-first service rather than a high-concurrency performance claim.
- [S-LoRA](https://github.com/S-LoRA/S-LoRA) already provides unified paging
  across dynamic adapter weights and KV cache tensors for many concurrent LoRA
  adapters. This rules out claiming adapter capacity management in the
  abstract as StatePatch's novelty.
- [Multi-LoRA Serving Benchmark](https://github.com/priyaltaneja/multi-lora-serving-benchmark)
  exposes a real serving capacity knob (`max_loras`) and measured traffic/memory
  effects, but explicitly uses random synthetic adapters and one fixed prompt;
  it lacks a task-quality oracle and real lifecycle trace.
- The local E200 result establishes only idle-only global apply/disable for two
  adapters. Its observed adapter outputs are identical to each other for the
  fixed prompt, so it supplies no adapter-selection or quality distinction.

## Decision

No located source jointly supplies the required real lifecycle corpus and
quality/capacity evidence. More importantly, the online lifecycle capability
demonstrated in E200 is directly adjacent to public Kiln functionality, while
adapter-capacity management is already the subject of S-LoRA and later serving
systems. The current StatePatch mechanism has neither a novel separation nor
the evidence needed to test one. It is **Research No-Go**.

## Re-entry condition

Re-entry needs a previously unavailable, prospectively recorded real workload
where adapter version correctness, finite capacity, and tenant-visible harm
interact, plus a mechanism that differs concretely from online hot-swap and
existing adapter paging/routing. A new design must clear prior art before a
new execution ID is created.
