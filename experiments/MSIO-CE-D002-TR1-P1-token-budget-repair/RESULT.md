# MSIO-CE-D002-TR1-P1 result

Date: 2026-09-08. Decision: `P1_NO_GO_STOP_API_PROMPT_BRANCH`.

## Frozen result

P1 completed all 24 calls from 14:53:12 through 15:03:36 +08:00. Increasing
the sole request parameter `max_tokens` from 900 to 4,096 removed the systematic
truncation: 23 calls finished with `stop`; one counterevidence-aware call
returned an HTTP 504 and was retained as invalid without retry.

| condition | valid | exact | premature apply |
| --- | ---: | ---: | ---: |
| positive-only | 12/12 | 2/12 | 0 |
| counterevidence-aware | 11/12 | 6/12 | 0 |

Counterevidence improved exact decisions by four scenarios, exceeding the
relative-effect gate, but its absolute 6/12 result missed the frozen 10/12
threshold. P1 therefore does not open prompt/model expansion.

## Descriptive error decomposition

Counterevidence improved ABSTAIN recall from 2/7 to 5/7 and PROBE recall from
0/1 to 1/1. Both conditions had APPLY recall 0/4: the model consistently chose
PROBE for every oracle-APPLY scenario. Paired exact outcomes were five
counterevidence-only wins, one positive-only win, one both-correct case, and
five both-wrong cases. These are development-exposed descriptive observations,
not inferential or real-system evidence.

The actionable result is that counterevidence changes decisions in the desired
direction, but this model/API contract is too conservative to serve as the
final action selector. Stop prompt tuning. Reuse the signal by moving to a
real-system design where the LLM proposes candidates and a deterministic
requested/effective/state receipt gate validates or rejects actions.

Predictions SHA-256 is
`150a308ececd2734475265fb01add8a5939ba3f1d26bd219c849567d218df1e0`;
score SHA-256 is
`f88d3691209e8c76ccb750d2f07c266c59d1a9427fc3bfa014e2f236a611c00c`.
Raw requests and responses remain outside Git under
`ModelStateIO-data/MSIO-CE-D002-TR1-P1/attempt-001`.
