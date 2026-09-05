# MSIO-KVG-E003 state-restore necessity gate with order isolation

## Reason for a new experiment

E002R2 established exact continuations but not a valid timing comparison: the
fresh long-context arm exhibited an unseparated first-block warm-up effect.
E003 does not reuse its timing data or alter its necessity threshold.

## Frozen question

When a previously produced, owned KV snapshot exists, does save + restore +
continuation have a directionally different incremental cost from fresh
recomputation for short versus long prefixes under an isolated loopback
runtime?

## Protocol

Use only the existing SHA-256-verified Qwen2.5-0.5B Q4_K_M GGUF. Run six
independent blocks: short/long each three times, with arm order `RP, PR, RP`
within each context, where `R` is fresh full-prefix recomputation and `P` is
base-prefix evaluation, save, restore to a different slot, then suffix-only
continuation. A new loopback `llama-server` process is created and cleanly
stopped for every block. Before either measured arm, issue two fixed,
unrelated 32-token warm-up requests. Start the server with `--cache-ram 0`
and `--no-cache-prompt`; no request may set `cache_prompt=true`.

The warm-up and common base-prefix computation are not charged to either
resumed-request arm. Persistence costs exactly `save_wall + restore_wall +
suffix-continuation wall`; recomputation costs full-prefix continuation wall.
The saved state is created once per block and never reused across blocks.

## Controls and recorded fields

Slots 0/1/2, model hash, server command, warm-up completion, per-arm HTTP
wall time, server prompt timing and token counts, save/load bytes, exact
response equality, block order, server PID, process cleanup, and GPU idle
state are recorded. Any server start failure, incorrect continuation, missing
state file, nonzero residual server, or failed slot erase invalidates that
block and stops the experiment.

## Decision rule

All six blocks must be correct and clean. Separately by context class, compute
the median of `P - R`. KVGuard has a necessity signal only if the sign changes
between short and long classes and each sign magnitude is at least 10% of the
respective recomputation median. Otherwise the fixed-policy explanation is
sufficient and KVGuard is a paper-level No-Go under the available artifacts.

This is still a state-lifecycle necessity test, not a capacity, policy,
tail-latency, or paper-performance result.
