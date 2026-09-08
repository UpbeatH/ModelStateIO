# MSIO-CE-D002-TR1 packet-freeze result

Date: 2026-09-08. Decision:
`TR1_TECHNICAL_STOP_GATEWAY_QUALIFICATION`.

## Completed preparation

TR1 freezes a TokenRhythm-gateway request for
`deepseek-v4-pro-0813`, thinking enabled, requested reasoning effort high,
JSON-object output, no tools, no retry, and one stateless request for each of
72 run IDs. All D002 `messages` objects are preserved without modification;
only experiment identity and gateway request metadata changed.

Static validation returned `TR1_PACKET_STATIC_VALID`. Eight unit tests passed,
including exact 72-row identity, D002 message equivalence, no-tools request
construction, missing-credential fail-closed behavior, invalid-citation
rejection, absence of the exposed key literal, and byte-identical dual builds.

| file | SHA-256 |
| --- | --- |
| `prompts.jsonl` | `db9cf94880d038b2d75b7a6c6c0a4ff300378d525ee302323f4c19061203e216` |
| `prediction-template.jsonl` | `94013af993bfae26b74c4d6f9c858939fe0cd78e356a116e0d4878b35acf7849` |
| D002 source `prompts.jsonl` | `f2800c0863858e00a1c7c1bcc98b39701e36fe20f605e1834a31c30e5d145bc9` |

## Gateway smoke observation

After the user configured a rotated user-level environment key, the runner
performed the single authorized synthetic smoke. `GET /models` exposed the
requested model. The chat request returned HTTP 200,
`deepseek-v4-pro-0813`, a nonempty request ID, usage accounting, and observed
thinking content in 1,938 ms. It returned `system_fingerprint=null`, so the
strict TR1 qualification decision is
`TR1_TECHNICAL_STOP_GATEWAY_QUALIFICATION`.

The credential value was loaded from the user environment into one child
process and cleared without being printed or written. The credential pasted in
conversation was not copied into a command or repository file. Raw smoke data
are outside Git under `ModelStateIO-data/MSIO-CE-D002-TR1/smoke-001`.

## Evidence boundary and next gate

Strict TR1 issued one synthetic model call and no 72-call experiment. It is
neither a development-model No-Go nor evidence about counterevidence-aware
decisions. The separately frozen P0 fast screen treats fingerprint as optional
and records the gateway limitation explicitly. TR1 remains a TokenRhythm
gateway experiment and must not be reported as an official DeepSeek API run.
