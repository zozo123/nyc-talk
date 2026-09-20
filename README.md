# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
**Principal Engineer and Head of DevRel at Incredibuild.com**

NYC · AI Agent Security Summit · October 21, 2026

**15-minute lightning talk.** Nine main slides, three appendix. Manuscript targets 14 minutes.

[Deck PDF](slides/talk.pdf) · [LaTeX](slides/talk.tex) · [Spoken script](TALK.md) · [Speaker notes](SPEAKER_NOTES.md) · [Runbook](RUNBOOK.md) · [Q&A](QUESTIONS.md)

## What this talk is

The Sessionize talk. Four non-escape escapes, four locks, four questions. Friendly 15 minutes.

The process never leaves. A decision you care about still moves:

1. **Dad’s badge** — inherited credentials → mint a tiny, short-lived task token
2. **Next job’s chair** — dangerous mounts → read this, write that
3. **Allowed door** — exfil through an allowed host → broker the envelope
4. **The test said yes** — verifier / `expected.json` → freeze bytes, grade off the worker. `/admin` with no cookie is 401, not 200.

Then: real process isolation, capability-scoped filesystems, short-lived credential projection, tamper-evident history.

`lab/` is stories 1–3. `factory/` is story 4 (`/admin`). Neither is a vendor 0-day.

## Run it

```sh
make factory        # local freeze / judge / gate; no cloud
make demo           # Linux + bubblewrap isolation lab
make deck           # verify recorded hashes, export notes, compile PDF
```

Optional Boat accept-VM (`BOAT_API_KEY`, `noEnv`, short TTL):

```sh
make factory-boat
```

`make deck` does not provision machines.

Python 3.10+ standard library. Isolation lab needs bubblewrap on disposable Linux. Deck needs TeX Live with Beamer.

## What the evidence is not

Not a named-product zero-day. Not a customer incident. Not a model attack-success rate. Not kernel-escape resistance. Five `/admin` cases prove this policy, not that the app is secure. The old lab’s 29 checks remain educational isolation demonstrations; they are not 29 vulnerabilities.

## Accepted abstract

> Every namespace and cgroup can work exactly as designed and an agent can still cause a real breach. This talk demonstrates four non-escape escapes: inherited credentials, dangerous mounts, exfiltration through an allowed endpoint, and verifier tampering. Then we close each one at the layer that can actually enforce it: real process isolation, capability-scoped filesystems, short-lived credential projection, and tamper-evident execution history. You leave with four boundaries you can check against your own agent deployment.

The session is 15 minutes. History **detects** rewrites. The gate **enforces** acceptance. Those are different jobs.
