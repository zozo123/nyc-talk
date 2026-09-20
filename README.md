# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
**Principal Engineer and Head of DevRel at Incredibuild.com**

NYC · AI Agent Security Summit · October 21, 2026

**15-minute lightning talk.** Nine main slides, three appendix. Manuscript targets 14 minutes.

[Deck PDF](slides/talk.pdf) · [LaTeX](slides/talk.tex) · [Spoken script](TALK.md) · [Speaker notes](SPEAKER_NOTES.md) · [Runbook](RUNBOOK.md) · [Q&A](QUESTIONS.md)

## What this talk is

**Containment is not attestation.** Isolation answers whether a process can touch the host. Release answers whether we should believe these bytes. Agent factories are collapsing those questions because the harness already lives in the box.

The sting is not a kernel escape and not a writable checker. We lock `checker.py`. The hash is unchanged. The checker still reads worker-written `expected.json`. PASS. The bug ships. The control you would audit is green.

The spine is a **reference software factory** in `factory/`:

The spine is a **reference software factory** in `factory/`:

1. Dev VM produces a candidate.
2. Controller **freezes** chosen paths into immutable storage and hashes a manifest.
3. A fresh accept VM executes **those bytes** as untrusted code.
4. Controller compares against **controller-owned** expected results.
5. A gate binds artifact, run, verifier bundle, expected results, policy and nonce, then publishes **the frozen object**.

The finding we spend time on: **the checker file was protected; `expected.json` was not.** The worker matched the bug. PASS. Independent criteria still failed.

A worker `PASS` file the controller believes is a **deliberate weakened variant** (the experiment can detect failure). It is not an unexpected discovery.

Three other grants — inherited identity, writable mounts, allowed exfil — are independent synthetic checks in `lab/`. They are the surrounding map, not one exploit chain.

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

Not a named-product zero-day. Not a customer incident. Not a model attack-success rate. Not kernel-escape resistance. Five parser cases prove those five cases. The old lab’s 29 checks remain educational isolation demonstrations; they are not 29 vulnerabilities.

## Accepted abstract

> Every namespace and cgroup can work exactly as designed and an agent can still cause a real breach. This talk demonstrates four non-escape escapes: inherited credentials, dangerous mounts, exfiltration through an allowed endpoint, and verifier tampering. Then we close each one at the layer that can actually enforce it: real process isolation, capability-scoped filesystems, short-lived credential projection, and tamper-evident execution history. You leave with four boundaries you can check against your own agent deployment.

The session is 15 minutes. History **detects** rewrites. The gate **enforces** acceptance. Those are different jobs.
