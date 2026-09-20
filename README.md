# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
**Principal Engineer and Head of DevRel at Incredibuild.com**

NYC · AI Agent Security Summit · October 21, 2026

**15-minute lightning talk.** Nine main slides, three appendix. Manuscript targets 14 minutes.

[Deck PDF](slides/talk.pdf) · [LaTeX](slides/talk.tex) · [Spoken script](TALK.md) · [Speaker notes](SPEAKER_NOTES.md) · [Runbook](RUNBOOK.md) · [Q&A](QUESTIONS.md)

## What this talk is

Fifteen minutes. Four recorded cases from the abstract. Full sentences and the commands on the slides.

1. Inherited credentials: runner token reads another project (`200`). Task token returns `403`. Task input still `200`.
2. Dangerous mounts: writable bind changes `next-job.json`. Read-only bind denies the write. `/output` still works.
3. Allowed endpoint: `POST /accounts/other/uploads` stores the fixture. Broker sends only `/accounts/team/reports`.
4. Verifier tampering: `checker.py` hash unchanged. Worker writes `expected.json` so `admin:none` is `200`. Independent case still requires `401`.

Locks: short-lived credential projection, capability-scoped filesystems, process isolation, freeze-and-compare plus a hash chain the worker cannot rewrite.

`lab/` is cases 1–3. `factory/` is case 4. Neither is a vendor 0-day.

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
