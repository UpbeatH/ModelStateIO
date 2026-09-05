# StatePatch design

Status: artifact-qualified feasibility candidate, not an active paper claim.

## Question

Can a single user-local runtime attach and detach a provenance-complete LoRA
adapter over one fixed GGUF base model without replacing the base artifact,
silently changing the output contract, or leaving an adapter active after the
requested detach?

## Why this is a new entry condition

The earlier StatePatch stop was an artifact stop: there was no lawful,
traceable base/adapter pair.  The current candidate uses a public Apache-2.0
Qwen2.5-0.5B-Instruct base and a separately published Apache-2.0 GSM8K LoRA
adapter declaring that exact base.  This establishes only an acquisition
condition.  It does not establish a state-management contribution, an online
controller, or a performance benefit.

## Minimal mechanism

Convert only the declared Q/V LoRA tensors into the runtime's GGUF-LoRA
representation; then use the runtime's documented adapter control surface to
show a bounded attach / disable / re-enable lifecycle.  The base GGUF is
immutable.  Every adapter output is checked against the fixed identities and
checksums recorded in the experiment preregistration.

## Falsification conditions

Stop this candidate immediately if any of the following occurs:

1. tensor names, shapes, rank, or base identity do not map unambiguously;
2. an adapter cannot be applied and disabled through a user-local interface;
3. a detach leaves output or runtime state indistinguishable from the attached
   state when compared with the same fixed prompt and decoding configuration;
4. the implementation needs a global package, a system CUDA change, a model
   download without a disclosed license, or an unverified artifact.

## Scope limit

Passing the first gate is technical feasibility only.  A CCF-B candidate would
still need multiple adapter versions, a real lifecycle/reuse trace, capacity
conflict, an equal-budget baseline, total-cost accounting, correctness and
isolation under concurrent tenants.  None is inferred from a one-adapter
smoke.
