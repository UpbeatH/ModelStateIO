# MSIO-CP-E024 execution task

Run only after the repository commit containing this directory is available.
Use g130 private runtime and `LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64`.
Before launch, verify no `llama-cli` exists, GPU use is zero, E024 output does
not exist, and the three pinned SHA-256 values in `run_e024.py` match. Run the
script once. Stop without repair on any nonzero exit. Return the output path,
raw receipt hash, exit code, final process/GPU audit, and do not interpret
results or start another experiment.
