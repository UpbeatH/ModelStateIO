# D002 local executor audit

Date: 2026-09-08. Scope: read-only capability check before model output.

## Requested execution identity

- model: `gpt-5.6-luna`;
- reasoning effort: `high`;
- required isolation: 72 independent fresh contexts;
- expected conditions: positive-only and counterevidence-aware, 12 scenarios
  and three repetitions each.

## Observations

1. The current Codex desktop environment exposes `gpt-5.6-luna` as an
   available task model with `high` reasoning support.
2. The installed command resolves to
   `C:\Program Files\WindowsApps\OpenAI.Codex_26.818.3698.0_x64__2p2nqsd0c76g0\app\resources\codex.exe`.
3. One read-only invocation attempt, `codex --version` followed by
   `codex exec --help`, failed before command execution with Windows
   `Access is denied`. It produced no model request or response.
4. `OPENAI_API_KEY` is absent from the current process environment. No
   API-key helper or independent batch-model tool is callable in this task.
5. Official OpenAI documentation search/open attempts for Codex CLI model
   selection returned no retrievable page content in the available web tool,
   so they do not independently establish a supported batch command here.

## Decision

The D002 packet is frozen, but formal model execution is `NOT_RUN`. The
current conversation must not answer its own prompts because it has seen the
oracles and would not provide independent fresh contexts. No substitute model,
prompt relaxation, context reuse, selective repetition, or fabricated output
is permitted.

Execution may begin only through a separately auditable mechanism that can
preserve the exact packet bytes, requested Luna identity, 72 fresh contexts,
per-call receipts, and raw response hashes. If those requirements cannot be
met, D002 remains an unexecuted development packet rather than a No-Go result.

## Current qualification audit

Audit timestamp: 2026-09-08T11:20:39+08:00 through 2026-09-08T11:22:00+08:00.

The required read-only preflight observations were:

- `git -C ..\\.. status --short`: exit 0; the repository was already dirty.
- `git -C ..\\.. rev-parse HEAD`: exit 0; `84e8a973755bd48f68ebf2fe7e326a4b50313d2e`, matching the task packet.
- `python validate_packet.py`: exit 0; `D002_PACKET_STATIC_VALID`.
- `python -m unittest -v test_packet.py`: exit 0; all 7 tests passed.
- The proposed external root did not exist: `ModelStateIO-data\\MSIO-CE-D002\\attempt-001`.
- Frozen input hashes matched: `prompts.jsonl` SHA-256
  `f2800c0863858e00a1c7c1bcc98b39701e36fe20f605e1834a31c30e5d145bc9` and
  `prediction-template.jsonl` SHA-256
  `e90ff85681c50fe98a8b519c7b305c445f336e75743442a46d96160d02ea20a2`.
  The other required hashes were `run-manifest.json` SHA-256
  `0954a6d7721f087d5f98bc55ac7d38a168d9e026e288881a826242a21e129244` and
  `score_predictions.py` SHA-256
  `175a3b1fb1bd90e1ad8f1858191dd6852b5ede91dc7ee021e76a7618987d04a9`.

The no-request interface audit failed. The callable catalog exposes
`multi_agent_v1__spawn_agent` and Codex thread creation as orchestration
interfaces, but neither provides all of the following as a trustworthy
per-call receipt: effective returned model identity, effective reasoning
effort, exact raw model response before agent/tool processing, and a hard
no-tools/no-state-access boundary. `multi_agent_v1__send_input` and thread
continuation additionally reuse an existing context. No direct batch-model or
single-request interface with the required receipt and isolation contract was
callable in this task.

## Decision for this audit

`D002_TECHNICAL_STOP_EXECUTOR_QUALIFICATION`.

Model invocations: **0**. No attempt root, ownership marker, ledger, raw
response, prediction ledger, or scorer output was created. No D001 scenario,
baseline result, prior outcome, or oracle was opened. This is an executor
qualification stop only, not a scientific Go/No-Go decision. The existing
task-packet files and pre-existing dirty repository contents were preserved.

Final read-only verification at 2026-09-08T11:23:44+08:00: repository status
command exit 0; external attempt root still absent; `predictions.jsonl`,
`SCORE.json`, and `EXECUTION-RECEIPT.json` were all absent. No model-client
process was created by this zero-call audit.
