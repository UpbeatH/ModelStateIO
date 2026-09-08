# D002 local model-execution task packet

Status: authorized for executor preflight and, only after qualification, model
execution. Date: 2026-09-08.

## 1. Identity and authority

- Task ID: `MSIO-CE-D002-EXEC-LOCAL-001`.
- Research module and experiment ID: `ModelStateIO`, `MSIO-CE-D002`.
- Local repository: `D:\Workspace\Working\Working\Research\ModelStateIO`.
- Observed branch and commit before dispatch: `main`,
  `84e8a973755bd48f68ebf2fe7e326a4b50313d2e`.
- Execution environment: saved local Research project; no remote host.
- Execution model/operator: `gpt-5.6-luna`, reasoning effort `high`.
- Authorized operations: read the frozen D002 packet; perform read-only executor
  qualification; create the task-owned external attempt root; issue the 72
  frozen model invocations only if every qualification condition passes; write
  raw responses and receipts below the external attempt root; write compact
  `predictions.jsonl`, `SCORE.json`, and `EXECUTION-RECEIPT.json` in this D002
  directory; update `RESULT.md` only with verified execution observations and
  the frozen scorer decision.
- Forbidden operations: substitute a model or reasoning effort; reuse a model
  context; expose an oracle or another response to an invocation; repair or
  selectively retry a response; change frozen packet/scorer bytes; connect to
  a remote host; use a GPU; install software; change system/storage settings;
  edit outside the task-owned result paths; delete or overwrite any existing
  data; stage, commit, push, pull, checkout, reset, or rewrite Git history.

The repository is already dirty. Preserve every pre-existing tracked and
untracked change.

## 2. Research boundary

- Research question: does counterevidence-aware retrieval improve safe tuning
  decisions and decision stability over positive-only retrieval on the frozen
  D001 development harness?
- Prior evidence: D001 deterministic sanity baselines only; they are not LLM
  accuracy evidence.
- Hypothesis: under the same pinned model and prompt contract, counterevidence
  improves exact scenario decisions by at least three, while retaining apply
  recall and eliminating premature apply decisions.
- Evidence this task can establish: Luna/high prompt-following and decision
  stability on this curated, development-exposed harness.
- Claims this task cannot establish: real-system performance, hidden-set
  generalization, tuning benefit, novelty, causal storage effects, or CCF-B
  readiness.
- Comparison: `positive_only` versus `counterevidence_aware` under equal model,
  reasoning, scenario, and repetition budgets.
- Primary metric and thresholds: exactly those frozen in `PROTOCOL.md`; the
  executor must not reinterpret them.

## 3. Frozen inputs and budget

- Protocol: `PROTOCOL.md`.
- Manifest: `run-manifest.json`.
- Prompt schedule: `prompts.jsonl`, expected SHA-256
  `f2800c0863858e00a1c7c1bcc98b39701e36fe20f605e1834a31c30e5d145bc9`.
- Prediction template: `prediction-template.jsonl`, expected SHA-256
  `e90ff85681c50fe98a8b519c7b305c445f336e75743442a46d96160d02ea20a2`.
- Model and requested effective setting: `gpt-5.6-luna`, reasoning effort
  `high`; returned model identity and effective reasoning receipt must be
  recorded when exposed.
- Schedule: the exact 72 `run_id` rows already ordered in `prompts.jsonl`;
  one independent fresh context per row; no reordering or retry.
- Repetitions: three per condition/scenario.
- Maximum model-call budget: exactly 72 attempted calls, with no replacement
  call for an invalid response.
- External data root:
  `D:\Workspace\Working\Working\Research\ModelStateIO-data\MSIO-CE-D002\attempt-001`.
- Ownership marker: the new external root must contain
  `TASK-OWNER.json` naming `MSIO-CE-D002-EXEC-LOCAL-001` before the first call.
- Existing external attempt root: immediate stop; do not overwrite, merge, or
  choose a new attempt number without new authority.

## 4. Mandatory preflight

From the D002 directory, record commands, outputs, exit codes, and timestamps:

1. `git -C ..\.. status --short` and `git -C ..\.. rev-parse HEAD`; accept a
   dirty tree but record it. Stop if the repository root or observed commit is
   different from this packet.
2. `python validate_packet.py`; require exit code 0 and decision
   `D002_PACKET_STATIC_VALID`.
3. `python -m unittest -v test_packet.py`; require exit code 0 and all seven
   tests passing.
4. Recompute SHA-256 for `prompts.jsonl`, `prediction-template.jsonl`,
   `run-manifest.json`, and `score_predictions.py`; require the two frozen
   hashes above to match and record all four.
5. Audit the proposed invocation interface without making a model request.
   Require explicit support for `gpt-5.6-luna`, `high`, independent stateless
   calls, raw response capture, per-call status/timing, and returned model
   identity or an equivalent trustworthy request/effective receipt.
6. Confirm the external attempt root does not exist. Only after steps 1-5 pass,
   create it and its ownership marker without deleting anything.

Failure of any item is `D002_TECHNICAL_STOP_EXECUTOR_QUALIFICATION`; write only
the audit receipt and make zero model calls.

## 5. Ordered execution

1. Copy `prediction-template.jsonl` to a new task-owned working ledger under
   the external attempt root; do not modify the template.
2. For each scheduled prompt row in its frozen order, create a new stateless
   model request containing only that row's `messages`, request Luna/high, and
   capture the exact raw response before parsing.
3. Record start/end timestamps, latency, client build, requested model,
   returned model, reasoning receipt when available, status, raw response
   SHA-256, and parsed response for that `run_id`.
4. On an invalid response, preserve it and continue only when isolation and
   packet identity remain intact. Never repair or retry it.
5. If leakage, context reuse, model mismatch, packet mutation, or receipt
   ambiguity is detected, stop further calls immediately and classify the
   technical stop.
6. After the scheduled calls or an early stop, write the complete external
   ledger first. Copy a compact prediction ledger into this D002 directory
   only if it contains exactly the frozen 72 run IDs, including explicit
   unexecuted statuses after an early stop.
7. Run `python score_predictions.py predictions.jsonl --output SCORE.json`
   exactly once only when all 72 ledger rows exist. Preserve the scorer exit
   code and output. A scorer rejection is evidence, not permission to repair.

No individual model call may be allowed to execute shell commands, use tools,
or change local or remote state.

## 6. Stop and contamination rules

- Apply every stop rule in `PROTOCOL.md`.
- More than three invalid calls in either condition is the frozen technical
  stop; do not relabel it as a scientific No-Go.
- Any oracle or cross-call response leakage is an immediate technical stop.
- Any model/reasoning substitution, context reuse, missing trustworthy receipt,
  or prompt-byte deviation is an immediate executor-qualification stop.
- New user authority is required for another attempt root, a rerun, a new
  executor, a model switch, changed prompts, selective retry, repository
  integration outside the listed result files, or any remote/system action.

The task must not open D001 `scenarios-with-oracles.jsonl`, D001 baseline
results, or any earlier conversation containing outcomes before all model
calls finish. The scorer may read its frozen oracle input only after output
collection is irrevocably complete.

## 7. Cleanup and postflight

- No process, service, mount, or setting may be changed, so none should require
  rollback.
- Verify no residual model-client process created by this task remains.
- Do not delete raw responses, ledgers, receipts, or failures.
- Record final Git status; it may include pre-existing dirt and only the
  authorized new D002 compact artifacts from this task.

## 8. Required return package

Return executor-qualification decision; exact client/app build and effective
model/reasoning receipts; start/end timestamps; command ledger with exit codes;
call counts by completed/invalid/unexecuted status; external raw/log paths and
file counts; SHA-256 values; `predictions.jsonl` and `SCORE.json` identity when
created; failures and unexecuted rows; final Git status; and a strict separation
of observations from interpretation.

If qualification fails, return the exact failed requirement and prove that
zero model calls were made. Do not propose a scientific Go/No-Go.

## 9. Primary-agent review boundary

The execution task reports observations and the frozen scorer output. The
primary task independently checks evidence completeness before accepting a
development Go/No-Go or opening D003 design.
