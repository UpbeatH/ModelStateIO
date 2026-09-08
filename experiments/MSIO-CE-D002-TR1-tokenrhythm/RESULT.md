# MSIO-CE-D002-TR1 packet-freeze result

Date: 2026-09-08. Decision: `PACKET_FROZEN_CREDENTIAL_STOP`.

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

## Credential gate observation

`TOKENRHYTHM_API_KEY` was absent from the current process. The authorized
preflight invocation therefore stopped locally with
`TR1_TECHNICAL_STOP_CREDENTIAL` before network-request construction. The
gateway smoke root, formal attempt root, `PREFLIGHT.json`, predictions, raw
responses, execution receipt, and score are all absent. Authenticated/model
calls: **0**.

The credential pasted in conversation was treated as compromised and was not
copied into a command, file, environment variable, or log. A rotated key must
be configured outside the conversation as `TOKENRHYTHM_API_KEY`.

## Evidence boundary and next gate

No model result exists. This is neither a development-model No-Go nor evidence
about counterevidence-aware decisions. TR1 is a TokenRhythm gateway experiment
and must not be reported as an official DeepSeek API result. Requested
reasoning effort high is not an effective-setting receipt because the gateway
does not document an echoed effective effort field.

With a rotated environment key present, the exact next command is:

```text
python run_gateway.py --smoke
```

Only a `TR1_GATEWAY_QUALIFIED` receipt opens the already authorized one-shot
`python run_gateway.py --run`. No model substitution, receipt relaxation,
retry, second attempt root, or secret persistence is permitted.
