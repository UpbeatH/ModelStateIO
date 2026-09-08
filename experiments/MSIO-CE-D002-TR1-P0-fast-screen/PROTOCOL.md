# MSIO-CE-D002-TR1-P0 fast model screen

Status: frozen after TR1 smoke and before pilot output. Date: 2026-09-08.

## Question and scope

P0 is a fast development screen, not a paper experiment. It asks whether
counterevidence-aware retrieval is sufficiently promising to justify immediate
real-system work. It reuses the first repetition of every D002/TR1 condition
and scenario: 2 conditions x 12 scenarios = 24 stateless calls.

The TokenRhythm smoke returned HTTP 200, the exact requested
`deepseek-v4-pro-0813` model, a request ID, token usage, and nonempty thinking
content. It returned `system_fingerprint=null`. P0 records that limitation but
does not make fingerprint a hard gate. Requested reasoning effort high also
remains requested-only.

## Frozen request

- gateway: `https://tokenrhythm.studio/v1`;
- model: `deepseek-v4-pro-0813`;
- thinking: enabled;
- requested reasoning effort: high;
- JSON object output; no tools; stream false;
- one request containing only one frozen system/user pair;
- no model substitution and no content repair;
- no retry; HTTP or schema failure is one invalid row.

The 24 rows are scenario-paired and condition order alternates between pairs
to reduce simple temporal ordering bias. Every `messages` object is unchanged
from the matching TR1 repetition-one row.

## Fast Go/No-Go

`P0_GO_TO_REAL_SYSTEM_DESIGN` requires all of:

1. at least 11/12 valid calls in each condition;
2. counterevidence-aware exact decisions at least 10/12;
3. counterevidence-aware exact decisions at least three higher than
   positive-only;
4. zero counterevidence-aware premature applies.

Anything else is `P0_NO_GO_TO_PROMPT_EXPANSION`: stop API/prompt expansion and
redirect effort to deterministic evidence handling or another mainline. A Go
does not validate performance; it opens immediate prospective real-system
design. The unused second and third repetitions remain optional robustness
work only after a real-system effect exists.

Raw request/response bytes are stored outside Git under
`ModelStateIO-data/MSIO-CE-D002-TR1-P0/attempt-001`. Compact predictions,
score, and receipt may be committed. The environment key is never written.
