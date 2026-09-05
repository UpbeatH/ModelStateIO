# MSIO-KVG-E003 result — technical contract No-Go

The first short `RP` block started and cleaned up correctly, but failed the
registered exact-continuation condition. With `--no-cache-prompt` and a
suffix-only resumed request, the restored slot's continuation content differed
from the fresh full-prompt output. The runner stopped at the first invalid
block; there is no `receipts.json` and no timing inference.

The raw partial receipt and server log remain outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E003/b1-short/`.
This is an API-contract failure for the suffix-only/no-prompt-cache invocation,
not evidence for or against state persistence.

E003R1 may change only that invocation contract: full prompt on the restored
slot with slot-local prompt alignment enabled. It retains process-per-block
isolation, `--cache-ram 0`, exact model, contexts, repetitions, orders and
decision threshold.
