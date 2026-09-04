# MSIO-CP-E004 result

Status: technical NO-GO for the frozen non-interactive one-token smoke; 2026-09-04. This is not a loading-path performance result.

## Established observations

- The Qwen model was acquired from the author-published Apache-2.0 GGUF revision in the preregistration, SHA-256-verified on Windows, user-uploaded to the fixed g130 inbox, then reverified before and after staging at `/mnt/nvme1/chenhao/modelstateio-runtime/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf`.
- Input identity passed: model SHA-256 `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`; `llama-cli` SHA-256 `39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24`.
- The private CUDA 11.6 library environment admitted the binary. The smoke log records that the Q4_K_M model loaded and reached prompt processing (`2032.4 t/s`); a sampled GPU allocation was 868 MiB during the run and 0 MiB/1% after termination.

## Failure and evidence boundary

- `llama-cli` entered its interactive prompt after processing the supplied prompt instead of exiting after the frozen one-token request. The external `timeout 180` terminated it with exit `124`.
- The interactive loop created a 464 MB raw `smoke.log`; it remains outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E004/` together with the input hashes, `smoke.exit`, and before/after GPU samples. No raw log, model, trace, or checkpoint was committed.
- This establishes only that the isolated binary can load the staged model under the selected runtime. It does not establish a successful scripted generation, a comparison between loading modes, an I/O-performance effect, or an optimization contribution.

## Decision and next gate

Do not rerun E004. A separate E005 protocol must first verify a non-interactive llama.cpp invocation (for example, a documented non-conversation/simple I/O mode) with a bounded stdout cap, then run one token under the same identity and resource controls. It must explicitly distinguish load completion from generated-token completion and reject interactive prompt loops before any performance comparison.
