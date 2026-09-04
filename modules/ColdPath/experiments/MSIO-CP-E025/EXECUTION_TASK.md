# MSIO-CP-E025 execution task

On g130 private runtime, verify hashes, no `llama-cli`, zero GPU use and absent
E025 output. Run `run_e025.py` once with private CUDA 11.6 libraries and a
600-second timeout. Return raw path, receipt SHA-256, exit code and cleanup.
