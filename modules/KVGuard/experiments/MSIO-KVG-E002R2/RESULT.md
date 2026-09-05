# MSIO-KVG-E002R2 result — invalid comparison

**Technical observation:** `--cache-ram 0` was accepted and all six
save/restore continuations were content-equal to fresh completions. The raw
receipt is outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E002R2/receipts.json`
(SHA-256 `32fa80e955a48c29a25083a6f33daef1c1fd92ad74c2467d7645b394b3540923`).

**Why this cannot decide E002:** the first long fresh recomputation took
0.5612 s, whereas the next two long fresh recomputations took 0.0279 s and
0.0237 s, despite each reporting `cache_n=0` and `prompt_n=186`. This strong
within-arm order effect is not separated by the original alternating order.
It may be runtime/device warm-up or another retained state; this result does
not identify which. `--cache-ram 0` alone is therefore not evidence that the
comparison is free of order/state contamination.

**Decision:** E002R2 is a technical correction only and is not used for the
action-reversal decision. It neither supports a KVGuard performance claim nor
changes the original threshold. E003 must use new server processes per
counterbalanced block, fixed independent warm-up, and explicit no-prompt-cache
settings.
