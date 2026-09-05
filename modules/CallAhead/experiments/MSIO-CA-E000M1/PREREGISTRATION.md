# MSIO-CA-E000M1 third-model material gate

Status: frozen before acquisition. Date: 2026-09-05.

## Question

Can CallAhead obtain a third provenance-complete, full-model weight artifact
without changing software, running inference or weakening E000's identity and
licensing requirements?

## Frozen artifact

- Repository: `Qwen/Qwen2.5-1.5B-Instruct-GGUF`
- Revision: `a615a81362316d7b9f5a7a9c4313adfdf9b54588`
- File: `qwen2.5-1.5b-instruct-q4_k_m.gguf`
- Official URL: <https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/a615a81362316d7b9f5a7a9c4313adfdf9b54588/qwen2.5-1.5b-instruct-q4_k_m.gguf>
- License: Apache-2.0, as declared by the official repository.
- Expected size: `1,117,320,736` bytes.
- Expected SHA-256 / official linked object identifier:
  `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.

The expected size, repository revision and linked object identifier were
captured from the official pinned resolver before download.

## Acquisition and transfer contract

1. Download only the frozen file into
   `D:\Temp\ModelStateIO-CallAhead\MSIO-CA-E000M1\` using a `.part` suffix.
2. Use the existing session-scoped local proxy only; do not alter global proxy
   or application settings.
3. Require exact size and SHA-256 before renaming the local file.
4. Transfer with the configured `g130-chenhao` SSH identity to
   `/mnt/nvme1/chenhao/modelstateio-runtime/incoming/.callahead-qwen2.5-1.5b-q4_k_m.gguf.part`.
5. On g130 require owner `chenhao`, exact size and SHA-256, then rename inside
   the same directory to `qwen2.5-1.5b-instruct-q4_k_m.gguf` and verify again.
6. Preserve a compact receipt locally. The model stays outside Git.

Do not install packages, start a model/server, change CUDA/driver/service/cache,
touch g129/PFS/Lustre, access other users, or delete any existing artifact.
Stop if the final path already exists with a different identity.

## Decision

- `PASS`: local and remote final files both match the frozen identity and the
  official license/revision receipt is recorded.
- `MATERIAL_BLOCKED`: bounded download or transfer cannot complete.
- `NO_GO`: the official identity/license is inconsistent, or an existing final
  path has conflicting content.

This gate is acquisition evidence only. It does not establish loadability,
performance, generality or CallAhead benefit.

