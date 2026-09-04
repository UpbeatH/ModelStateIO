# MSIO-CP-E022 completed-preparation versus concurrent-fill gate

## Question

E021 showed a timing-qualified 75% prefetch benefit at 0.7 s and an unplanned lead-0 observation. E022 separates the two mechanisms under a new confirmatory ID: no prefetch, 75% prefetch known complete before request, and 75% prefetch still active at request arrival.

## Frozen design

- Six counterbalanced three-arm blocks, 18 valid trials.
- Every arm starts at verified file residency <=20%. The active arms read exactly 75% of model bytes.
- `completed`: begin prefetch, require worker completion and >=70% residency before a 0.8 s arrival; otherwise stop.
- `concurrent`: begin the same prefetch and launch immediately at arrival; require the worker to be active at arrival, otherwise stop.
- Record request-visible latency from arrival (including residency readback), trigger-to-OK, bytes, preparation duration, residency, worker state, correctness and cleanup.

## Decision

Completed-preparation replication requires at least five of six completed-minus-none contrasts negative, paired median request-latency reduction >=10%, and a fixed-seed 95% block-bootstrap interval excluding zero. Concurrent-fill is reported separately and cannot be merged with completed-preparation evidence. Any identity, state, correctness or residue failure is No-Go for the gate.

This is one-model/one-host mechanism separation, not a controller or generalization result.
