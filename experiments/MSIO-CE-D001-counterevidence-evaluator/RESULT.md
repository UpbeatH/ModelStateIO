# MSIO-CE-D001 result

Date: 2026-09-08. Decision: `D001_LOCAL_HARNESS_VALID`.

## Scope and evidence level

D001 is a deterministic local development sanity test over outcomes already
known before the evaluator was designed. It did not invoke an LLM, optimizer,
remote host, GPU experiment, or live action. The scenario contracts, evidence
interpretations, and oracles are curated and development-exposed.

Therefore the scores below demonstrate only that the frozen harness implements
its intended evidence and veto semantics. They are not model accuracy,
generalization, causal benefit, novelty, or paper-level evidence.

## Frozen material

The builder produced 15 hash-addressed evidence cards and 12 scenario-specific
decision contracts. The oracle population contains four `APPLY`, one `PROBE`,
and seven `ABSTAIN` scenarios. Each scenario preserves its own metric,
direction, materiality threshold, uncertainty requirement, safety constraints,
and represented scope; metrics from different experiments are not combined
into a post-hoc scalar utility.

Both retrieval baselines use top-k three and a maximum rendered evidence budget
of 1,800 characters. Generated model inputs exclude `oracle_decision`,
`oracle_basis`, evidence polarity, veto flags, and rule implications.

## Deterministic development results

| baseline | exact decisions | apply recall | probe recall | abstain recall | premature apply | missed abstain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| receipt only | 2/12 | 1/4 | 1/1 | 0/7 | 0 | 7 |
| positive only | 4/12 | 4/4 | 0/1 | 0/7 | 1 | 7 |
| counterevidence aware | 12/12 | 4/4 | 1/1 | 7/7 | 0 | 0 |

The important harness behaviors are qualitative:

- the E001 null harm receipt changes pacing necessity from `PROBE` to
  `ABSTAIN` without preventing a separately contracted readiness action;
- the E939 harmful result prevents E938R2 technical feasibility from being
  promoted into a capacity-conflict performance action;
- the E006A common-arrival limitation changes a FIX_HEAD no-stall observation
  from premature `APPLY` to `PROBE`;
- structured context compatibility prevents the grouped E801 null result from
  being applied to the alternating-trace contract;
- requested/effective technical qualification remains separately expressible
  through E800.

The 12/12 result is expected because the rules and curated sanity scenarios
share the same frozen evidence interpretation. It must not be presented as an
advantage of an LLM or retrieval method.

## Validation

Python compilation, the independent local validator, six unit tests, hidden-
field inspection, counterevidence-removal mutation tests, and byte-identical
dual builds passed.

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `evidence-cards.jsonl` | 10,638 | `9dbba640f37b7f8b54aa06180f17f534cbacd1102312af709e3ba9bfd7b4deca` |
| `scenarios-with-oracles.jsonl` | 7,198 | `e74a8dbae366612909862c48070672e305bd87e1726052481c2db3f054cd3545` |
| `model-inputs-positive-only.jsonl` | 14,021 | `598313608a21dbd5ea7719711d75256c1787f560060f352565a72aa0433f6f8c` |
| `model-inputs-counterevidence-aware.jsonl` | 19,447 | `b8be05a516c4c402592838661a776306d03a330c6707ddf96b67c567be51e89f` |
| `retrieval-audit.jsonl` | 1,444 | `c7d7fb71e9fdeda1ee97546397ee39f94c7c9f2ad9c30a08752c8c922f595be5` |
| `baseline-results.json` | 3,230 | `f0da14d81adb4cd9350a938ee7334bb4d0aa56430b44cef75ebf43a3b4ec7b9d` |

## Exact next gate

The next local gate is D002 model-run packet freeze, not a scientific result.
It must pin one model/version, prompt, temperature, seed or repeat policy,
maximum input/output budget, parser, failure policy, and prediction schema
before any model output is observed. Positive-only and counterevidence-aware
packets must use the D001 bytes unchanged. Model outputs must be stored outside
the prompt packets and evaluated once by a deterministic scorer.

The standing research-model default is GPT-5.6 Luna. D002 must use that default
unless the user separately confirms a model switch after the reason and target
model are stated; no silent switch is permitted.

D002 may assess whether a pinned LLM follows the already-curated development
contracts. It still cannot test generalization because all source outcomes and
scenario design are exposed. A scientific D003 gate requires new,
prospectively frozen and outcome-hidden real-system episodes, with complete
requested/effective/state/rollback receipts. No cluster slot is activated.
