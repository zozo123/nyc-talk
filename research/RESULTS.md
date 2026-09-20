# Results

Pinned factory: `factory/` on this branch. Educational lab remains `lab/` at `fc34e2f`.

## Local (`make factory`)

| Check | Result | Classification |
|---|---|---|
| Intended: good parser frozen, accepted, published | PASS | successful defense, our factory |
| Intended: buggy parser rejected, not published | PASS | successful defense, our factory |
| Intended: approval does not authorize swapped digest | PASS | successful defense, our factory |
| Intended: consumed nonce cannot replay | PASS | successful defense, our factory |
| Weakened: worker PASS file accepted the bug | PASS | **deliberate** boundary violation (detector) |
| Weakened: protected checker + worker `expected.json` → PASS | PASS | **deliberate** boundary violation (detector) |

Independent judge on the bug: `1,,3` and empty input fail; three other cases pass.

## Boat accept-VM (`make factory-boat`)

`noEnv: true`. Fresh VM executed frozen bytes. Controller compared. Idle was not used as quiescence.

| Candidate | Verdict |
|---|---|
| Good parser | accept, five matches |
| Buggy parser | reject (`1,,3` and empty fail) |

Sandbox stopped after the run. Infrastructure: completed, not a crash-as-defense.

## What we will not claim

Not a Boat product vulnerability. Not novelty for in-sandbox graders (known). Not model ASR. Not 29 lab assertions as 29 bugs.
