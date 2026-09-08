# MSIO-CE-D002-TR1 TokenRhythm gateway development protocol

Status: frozen before authenticated API access. Date: 2026-09-08.

## Purpose

TR1 tests the same development-exposed question as D002 through the
TokenRhythm aggregation gateway: whether counterevidence-aware retrieval
improves safe decisions over positive-only retrieval under one fixed model
request contract. It is a new experiment, not a substitute result for the
Luna-pinned D002.

The result may establish only gateway-mediated model behavior on the curated
D001 harness. It cannot establish official DeepSeek backend identity,
real-system tuning benefit, hidden-set generalization, novelty, or CCF-B
readiness.

## Frozen identity and receipt contract

- gateway: `https://tokenrhythm.studio/v1`;
- endpoint: `POST /chat/completions`;
- requested model: `deepseek-v4-pro-0813`;
- requested thinking mode: `enabled`;
- requested reasoning effort: `high`;
- stream: `false`;
- JSON response mode: `json_object`;
- tools: omitted;
- prompt contexts: exactly one fresh stateless HTTP request per run ID;
- schedule: 2 conditions x 12 scenarios x 3 repetitions = 72 calls;
- retry budget: zero.

The gateway response must return a matching `model`, nonempty request `id`,
nonempty `system_fingerprint`, usage fields, and nonempty
`choices[0].message.reasoning_content`. These verify returned model identity,
backend fingerprint, accounting, and observed thinking behavior. The gateway
does not document an echoed effective reasoning-effort field, so `high` remains
a requested setting, not a verified effective setting. This limitation is
prespecified and must remain visible in any paper claim.

The provider must be reported as TokenRhythm gateway. Do not call it an
official DeepSeek API run unless independent provider provenance later proves
that claim.

## Frozen inputs and comparison

The D002 source packet SHA-256 must be
`f2800c0863858e00a1c7c1bcc98b39701e36fe20f605e1834a31c30e5d145bc9`.
TR1 reuses every source `messages` object without modification while replacing
only experiment/run identity and request metadata. The scenario, condition,
repetition, response schema, invalid-output rules, scorer logic, and seven
development Go requirements remain those in D002 `PROTOCOL.md`.

## Credential and outbound-data boundary

The runner reads `TOKENRHYTHM_API_KEY` from the process environment only. It
must not accept a key on the command line, print it, write it, hash it, or place
it in Git. A missing key stops before any authenticated request or data-root
creation.

The user authorized sending the frozen development prompts to this gateway.
No secrets, credentials, raw production traces, model weights, private user
data, or oracle fields may enter a request. TokenRhythm states that calls and
conversations may appear in its account records; this is an external-data
handling limitation.

## Two-stage execution

1. `--smoke` performs `GET /models`, requires the exact requested model, then
   sends one synthetic JSON-only prompt using the exact thinking/reasoning
   request parameters. It writes raw request/response bytes outside Git and a
   compact `PREFLIGHT.json` without secrets.
2. `--run` is allowed only after a qualified preflight. It creates a fresh
   one-shot attempt root, executes the 72 rows in frozen order, preserves every
   raw request and response before parsing, and never retries.

External roots are:

```text
D:\Workspace\Working\Working\Research\ModelStateIO-data\MSIO-CE-D002-TR1\
  smoke-001\
  attempt-001\
```

An existing target root is an immediate stop. Never delete, merge, or
overwrite it.

## Failure and decision rules

- Missing/compromised credential: `TR1_TECHNICAL_STOP_CREDENTIAL`.
- Requested model absent: `TR1_TECHNICAL_STOP_MODEL_UNAVAILABLE`.
- Missing model/fingerprint/request/thinking receipt or rejected exact request
  parameters: `TR1_TECHNICAL_STOP_GATEWAY_QUALIFICATION`.
- Leakage, prompt mismatch, context history, tool exposure, or source mutation:
  `TR1_TECHNICAL_STOP_CONTAMINATION`.
- More than three invalid scheduled calls in either condition:
  `D002_TECHNICAL_STOP_INVALID_OUTPUT_RATE`.

Do not repair, retry, substitute a model, relax a receipt, or create a second
attempt under TR1. A completed ledger is scored exactly once with the reused
D002 scorer logic. The frozen D002 development Go conditions are applied
unchanged. Any failure is scoped to this gateway/model/request/harness
combination and is not a scientific No-Go for counterevidence-aware tuning.
