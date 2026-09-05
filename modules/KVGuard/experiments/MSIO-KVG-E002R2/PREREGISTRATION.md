# MSIO-KVG-E002R2 launcher correction

E002R2 changes only the E002R1 wrapper predicate: it injects `--cache-ram 0`
only into the `llama-server` command and leaves preflight subprocess calls
unchanged. All E002R1 scientific controls remain frozen. E002 and E002R1 raw
data are not reused.
