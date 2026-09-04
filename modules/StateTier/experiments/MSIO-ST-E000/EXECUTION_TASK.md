# MSIO-ST-E000 execution task

Task ID: MSIO-ST-E000-20260904. Required commit: `96608f0` (ModelStateIO `main`). Target: `g127-chenhao`. This packet authorizes read-only preflight and artifact discovery only; it does not authorize model execution, system writes, installations, mounts, or deletion.

## Research boundary

Question: do available real model-state traces or controlled workload artifacts show at least two state classes preferring different residency actions under equal capacity pressure? This task can establish only platform/artifact readiness. It cannot establish a performance gain or the StateTier hypothesis.

## Ordered commands

Run on g127, in order, recording stdout/stderr and exit codes:

1. `hostname; date -Is; git -C ~/ModelStateIO rev-parse HEAD 2>/dev/null || true`
2. `nvidia-smi --query-gpu=name,memory.total,driver_version,temperature.gpu,utilization.gpu,memory.used --format=csv,noheader`
3. `free -h; swapon --show; uptime`
4. `findmnt -t ext4,xfs,lustre; df -hT /mnt/nvme3n1`
5. `pgrep -a -u chenhao || true; nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader`
6. `find /mnt/nvme3n1 /home/chenhao -maxdepth 4 -type f \( -iname '*.gguf' -o -iname '*trace*' -o -iname '*kv*' -o -iname '*state*' \) -printf '%p %s %TY-%Tm-%TdT%TH:%TM:%TS\n' 2>/dev/null | head -n 200`
7. `command -v ollama || true; command -v llama-server || true; ollama list 2>/dev/null || true`

## Stop rules

Stop after preflight if any GPU compute process, heavy user/service load, ambiguous storage identity, missing model/trace artifacts, or missing runtime is observed. Do not generate synthetic traces or claim the hypothesis tested. Return observations and exact paths only.

## Return package

Return command ledger, exit codes, timestamps, host mapping, raw output path, artifact list with sizes and SHA-256 for any candidate input, cleanup proof, and a `NOT_RUN` decision for any workload step.

