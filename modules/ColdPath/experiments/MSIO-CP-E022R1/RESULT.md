# MSIO-CP-E022R1 result

## Established observation

E022R1 ran all 18 frozen trials on g130 with the E022 identities and
counterbalanced three-arm schedule. Every foreground invocation exited zero,
emitted exactly one `OK`, and the final audit found no `llama-cli` process and
no CUDA compute allocation. The raw receipt set has SHA-256
`f77b6bd5aa17296a30e8e0ef21f1d145ff36f70fc7892d69aa64169b522d2cfa` and
remains outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E022R1/`.

The corrected immutable arrival snapshot found the concurrent reader active in
all six concurrent trials. Each had read 368,550,024 bytes at arrival; this is
evidence of overlap, not evidence that the intended 75% preparation had
completed.

## Paired outcomes

Against the matched no-prefetch trial in each block, the completed-75% arm was
negative in 6/6 blocks: median arrival-to-OK difference -0.345 s, or 12.92%
relative to the no-prefetch median. The fixed-seed 10,000-resample block
bootstrap 95% interval is [-0.457, -0.161] s.

The concurrent-75% arm was likewise negative in 6/6 blocks: median
arrival-to-OK difference -0.384 s, or 14.36% relative to the no-prefetch
median. Its fixed-seed 10,000-resample block-bootstrap 95% interval is
[-0.531, -0.150] s.

## Decision and limitation

**PASS: the E022R1 snapshot correction establishes a request-time concurrent
fill state and a material request-visible improvement on this exact 0.5B,
g130, file-scoped-cold setup.** It also independently replicates completed
preparation.

This does not establish a controller, end-to-end total-work saving, causality
beyond the frozen host/model/storage setting, or cross-model generalization.
E022 remains closed and is not rerun. The next independent confirmation must
use a new experiment ID and the hash-distinct 7B model.
