# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz**  
Principal Engineer and Head of DevRel at Incredibuild.com

AI Agent Security Summit · NYC · October 21, 2026 · 15 minutes

Speak in full sentences. Read the snippets on the slide. Do not set up a contrast and then flip it.

## 1. Title — 00:00–00:30

I am Yossi Eliaz.

The title is the claim. The agent stays inside the sandbox. Namespaces and cgroups do what they were built to do. A real breach still happens.

Four cases. Each one uses an interface we gave the worker so it could finish the job.

## 2. What we gave it — 00:30–01:15

A working coding agent needs four things from us: a credential, some files, one network path that can publish, and a signal that the work is done.

Those four things are the four cases in the abstract: inherited credentials, dangerous mounts, exfiltration through an allowed endpoint, and verifier tampering.

The process never leaves the box. Those four interfaces still move data, files, and merge decisions.

## 3. Inherited credentials — 01:15–03:20

We started the worker with the runner token already in the environment, because CI already had that token.

```
Authorization: Bearer fixture-runner
GET /projects/other/private
200  {"fixture":"SYNTHETIC-PRIVATE-FIXTURE"}
```

The sandbox did not steal this. The worker sent a GET with the token we injected.

We replaced that token with one scoped to the current task.

```
Authorization: Bearer fixture-task
GET /projects/other/private          403
GET /input/parser-fix               200
```

Expired tokens and the wrong audience also return 403. The job can still read its own input.

The lock is short-lived credential projection: mint for this task, this audience, this hour. Do not copy the runner secret into the worker.

## 4. Dangerous mounts — 03:20–05:00

We mounted another job’s directory into the worker and left it writable.

```
Path("/shared/next-job.json").write_text('{"queue":"attacker"}')
# writable bind: WRITE_SUCCEEDED, host file changed
# read-only bind: WRITE_DENIED,   host file unchanged
Path("/output/patch.txt").write_text("legitimate patch output")
# still succeeds
```

The write is a normal open. The host file changes because we configured the bind that way.

The lock is a capability-scoped filesystem: `/input` read-only, `/output` writable, the next job’s path absent. The worker can still produce its patch.

If you snapshot this disk and fork it for the next agent, that next agent inherits the same files.

## 5. Allowed endpoint — 05:00–07:00

We allowed the worker to reach the report service so it could publish.

```
POST /accounts/other/uploads
{"data":"SYNTHETIC-PRIVATE-FIXTURE"}
201
```

The hostname is the one we allowlisted. The path is another account. The body is the private fixture. The service stored it.

The worker does not get to choose the URL, the recipient, or the body. It may request one operation. A broker on the controller sends a fixed report.

```
request = {"operation":"publish_report","task":"parser-fix"}
# extra keys -> DENIED, no delivery
# broker POST /accounts/team/reports  {"task":"parser-fix","status":"completed"}
```

The worker’s network namespace cannot reach the service. The legitimate report still lands on the team path.

The lock is real process isolation plus a broker that owns the envelope.

## 6. Verifier tampering — 07:00–09:45

The ticket is: unauthenticated `/admin` returns 401. A green check means the patch may merge.

We keep `checker.py` read-only. Its hash does not change. The checker loads cases from the workspace.

```
# checker.py  (hash unchanged)
expected = json.loads(Path("expected.json").read_text())
for case in expected:
    out = run(["python3", "handler.py", case["input"]])
    assert json.loads(out) == case["output"]
print("PASS")
```

The worker writes `expected.json`:

```
{"input": "admin:none", "output": 200}
```

The checker prints PASS. The independent controller still requires 401 for `admin:none`.

```
python3 handler.py admin:none
200          # shipped handler
401          # required
```

The worker did not edit the checker. It edited the cases the checker trusts. CI is green. `/admin` with no cookie returns 200.

A second machine that still reads that `expected.json` will print PASS as well.

The controller also ignores a worker `PASS` file. That file is how we prove the experiment can see a bad accept. It is not the main case.

## 7. Close each one — 09:45–11:45

Inherited credentials: short-lived credential projection. Task-scoped token. 403 on the other project. 200 on task input.

Dangerous mounts: capability-scoped filesystems. Read-only input, writable output. Host file unchanged.

Allowed endpoint: real process isolation. Worker cannot open the service. Broker sends only the team report.

Verifier tampering: freeze `handler.py` into controller storage, run those bytes, compare on the controller against controller-owned cases. Publish that digest. A rewritten log produces a different hash-chain head if the controller kept the original head. The log does not decide the merge. The compare does.

```
freeze({"handler.py": bytes})
outputs = run_frozen(bytes, cases)
approve(digest, run, verifier, expected, policy, nonce)
publish(frozen)   # live path after a swap -> DENIED
```

Open `/admin` is not published. Locked `/admin` is published. Replay of a used nonce is denied.

## 8. Four boundaries — 11:45–13:15

On your own agent host, write four answers.

Which credential does the worker receive, and what else can that credential read?

Which paths are mounted, and which of them are writable, including snapshots you will fork?

Which URLs can it POST to, and who chooses the path and the body?

Which object is compared before merge, and can the worker change the cases or the PASS file?

The component that returns 403, EROFS, DENIED, or reject has to sit outside the worker. After you add that component, run the legitimate ticket again and confirm it still completes.

## 9. Close — 13:15–14:00

We gave the worker a token, a filesystem, a publish URL, and a checker that read its workspace. The sandbox stayed up. Those four interfaces were enough for a breach.

The four locks are in the abstract. The repo has the recorded commands.

Who gave this process the authority?

> Stop.
