# MSIO-KVG-E004 one-slot capacity and abandonment gate

## Question

Does the E003R1 action-reversal signal remain useful when one owned KV state competes with a foreground request for a single server slot, including a preannounced abandoned return?

## Frozen workload and actions

Use only the verified 0.5B model, loopback llama-server, one exposed slot, and the short/long E003 prefixes. For every block, establish one owned prefix state A. A fixed unrelated foreground B request then needs the only slot. The trace announces before the action whether A will return or be abandoned.

Actions are retain (do not admit B; record an admission miss), save (save A, erase it, admit B, restore A if it returns), recompute (erase A, admit B, then recompute A if it returns), and controller. Controller may use only announced return/abandon status and measured state-size class: it drops known abandoned A, saves long returning A, and recomputes short returning A. Every arm receives the same announcement and can complete B. The controller does not receive actual completion times or an oracle beyond the announcement.

## Matrix and budget

Run short/long x return/abandon x retain/save/recompute/controller, three counterbalanced repetitions. One fresh server process per block, cache RAM zero, fixed warm-up, exact model hash and full cleanup are mandatory. Each return arm compares full-prefix recomputation with restore-plus-full-prompt continuation. No model download, cache clearing, new workload, retry, or sample expansion is allowed.

## Metrics and decision

Record B admission/result wall time, A return completion wall time, saved and restored bytes/time, discarded state bytes, correct output, slot/server cleanup, and announced cancellation. Retain's B non-admission is a foreground harm, not a zero-cost sample. The controller is a capacity-policy candidate only if all blocks are correct/clean, it admits B in every block, it avoids all writes for announced abandonment, and its returning-A median completion is at least 10% lower than the strongest non-oracle fixed action under the same context class without increasing B median by more than 10%.

A failure to induce the single-slot conflict, to record state accounting, or to beat the fixed baseline is a KVGuard paper-level No-Go on this platform. This gate still cannot prove multi-tenant or production generalization.
