# MSIO-CP-E023 result

## Established observation

The held-out 7B confirmation completed all 12 preregistered trials on g130.
Every invocation exited zero and returned exactly one `OK`; the final audit
found no `llama-cli` process and no CUDA compute allocation. The raw receipt
set has SHA-256 `5c84268eb7a77d3cd88196e2fa2460edc96ec9672f2fc6bec3af2e80d603cfc6`
at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E023/`.

Every trial began at zero observed residency. All six prepared trials read the
frozen 75% prefix, reached 75.003% residency, and completed preparation within
the 3.5 s lead budget (2.226--3.122 s).

## Paired result

All six `lead3500 - none` block contrasts were negative. The paired median
time-to-OK difference was -2.127 s, a 35.51% reduction relative to the
no-preparation median of 5.991 s. A fixed-seed 10,000-resample block bootstrap
gave a 95% interval of [-2.554, -1.567] s.

## Decision and scope

**PASS: completed 75%-prefix preparation retains a material request-visible
benefit on this hash-distinct 7B model under the frozen g130 setup.** This is
cross-model replication of a fixed action and fixed timing rule, not evidence
for a learned controller, total-work reduction, cross-device portability, or a
general storage policy.
