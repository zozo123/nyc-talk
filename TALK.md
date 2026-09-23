# Your Agent Escaped Without Escaping the Sandbox

**Yossi Eliaz, PhD / Pier Sixty, New York / Wednesday 21 October 2026 / 15-minute lightning**

Generated from `slides/talk.tex`. Edit the LaTeX, then run `make deck`. Main route: slides 1-12. Delivery budget: 14 minutes plus one minute of margin. Timings are rehearsal targets, not measured delivery.

Spoken manuscript: 1,429 words.
## 1. What changed when the test went green?

**00:00-01:30**

*Show FAIL, then PASS. Ask what changed. Then the METR timer. Say METR as meter.*

What changed when the test went green?

In June 2025, the AI evaluation nonprofit METR reported frontier models from more than one lab gaming the tasks they were scored on. Asked to make a program run faster, OpenAI's o3 overwrote the timing function that measured it. On another task, it patched the evaluation function so that it judged every submission a success. It was not asked to. In a separate test, telling it not to cheat barely changed how often it planned to.

The work did not get better. What judged the work changed. Today I'll show you the smallest version of that move, byte by byte, inside a sandbox that held. I'm Yossi Eliaz, from Incredibuild.

We recorded one worker run in a Linux sandbox. The worker is a script, not a model, so every step is deterministic and every hash I show you is in the repository. The checker says FAIL before the worker's step, and PASS after it. Let's find the one thing that changed.

## 2. No login prints 200

**01:30-02:15**

*Name the case. Then the two numbers.*

One case is enough. The program is a few lines of command-line code that mimic an access check. No web server is involved. admin:none means the admin route with no login. The right answer is 401. This program prints 200 for every input.

A checker compares the program's output with an answer key of five cases. Only two of those five expect 200. This program says 200 five times, so it is wrong on the other three.

Keep this program in mind. Its bytes never change.

## 3. The checker is protected

**02:15-03:15**

*Honest FAIL. DENIED. Same hash. Then PASS. Pause.*

At the start, the answer key is honest. On this program, the checker prints FAIL and exits 1.

Then the worker takes its step. First it tries the obvious attack: overwrite the checker with one that just prints PASS. The checker sits on a read-only mount. DENIED. Its hash is the same before that step and after it.

Then the same checker runs again, launched the same way, on the same program. It prints PASS and exits 0.

Nothing we protected changed. Something else did.

## 4. Only the answer key moved

**03:15-04:30**

*Read across the row. Stop on PASS.*

Two rows: the honest run, then the edited run. Read across.

The program has the same hash both times. So does the checker. The answer key, expected.json, changes: 0494 when honest, 390e when edited. And the verdict goes from FAIL to PASS.

Underneath is the diff. For admin:none, the expected answer was 401. The worker rewrote it to 200. It did the same for the two other cases that expected an error. Now every expected answer is 200, which is exactly what the bad program prints.

The checker did its job perfectly. It compared the program with the answer key, and they matched. The worker did not change the checker. It changed what counted as correct.

## 5. What the three hashes say

**04:30-05:30**

*One sentence per hash.*

Each hash rules one thing out. Same program hash: the worker did not fix the code. Same checker hash: the checker's code did not change. New answer key hash: that is the input that moved.

Now the trap. The tempting fix is to hash the answer key. But hash it after the worker wrote it, and you have a perfect fingerprint of the worker's answers. A hash tells you which bytes were used. It does not tell you who had the right to write them. The answer key that decides has to belong to someone other than the worker, and live where the worker cannot write.

## 6. The file defines success

**05:30-06:45**

*Point at the load. Then at who can write it.*

So why did the checker trust that file? Because of this one line. The checker loads expected.json from its working directory. The file looks like ordinary project data. Nothing about it is special, except that the checker obeys it.

The worker can write this file. The checker treats it as the answer key. So the worker's write permission included the acceptance criteria. The judge is not just the checker. The judge is the checker plus everything it reads. You can lock every executable in the pipeline and still leave part of the judge on the worker's side of the line.

One honest limit. This recording shows the write is allowed. A script cannot show whether a model would choose it. METR's report shows models sometimes make that kind of move on their own tasks. It is not a measurement of ours.

## 7. Controller-owned criteria

**06:45-07:45**

*Say REJECT first. Then who owns the answers.*

Now the repair. Same program, the one that prints 200 for everything. REJECT.

What changed is who owns the answers. The checker in the failing run also had a fresh sandbox of its own, with the workspace mounted read-only and no network, and it still went green, because it read its answers from the workspace. The controller runs the same program in a sandbox that holds only the program, reads back the output, and compares it in its own process against cases it holds itself. It never reads expected.json.

The worker's edit is still sitting in the workspace. It just no longer counts.

## 8. The corrected program

**07:45-08:30**

*Different hash. Five numbers. ACCEPT.*

A repair also has to let real work through. Here is the corrected program, with a different hash. It returns 401 without a valid login, 403 for an ordinary user, and 200 only where access is allowed. Same controller-owned cases. ACCEPT.

That is the pair you want from any fix. The bad program is rejected, the good program is accepted, and the answers are owned by someone other than the worker.

## 9. One unused approval

**08:30-10:00**

*Say unused. Then denied, denied, published, denied.*

Accepting a program is not the same as shipping it. Between the verdict and the release, there is one more place to swap bytes.

The controller issues one approval for the corrected program. First, the bad program is offered under that fresh, unused approval. DENIED. Next, the approved bytes are pointed at a different destination. DENIED, because an approval names one place. Then the approved bytes go to the named place. PUBLISHED. Then the same bytes again. DENIED, because the approval is spent.

The first row is the one that matters. The approval was still unused, so the refusal came from checking the bytes, not from replay protection. An earlier version of our own test tried the bad bytes only after the approval was spent, so it could not tell which check refused them.

Publication here is a local store, a stand-in for a registry or a merge. It holds exactly the approved bytes.

## 10. Three questions for another system

**10:00-11:30**

*Read the three questions. Do not name a vendor.*

Take three questions home. Who can change the inputs that define acceptance? Which exact bytes were the candidate, the checker, and the criteria? And does publication store exactly the approved bytes?

The first question has a concrete starting point. List everything your acceptance step reads or looks for: files, config, environment, services. List what your agent can write. Any overlap other than the candidate itself is your finding. And keep the candidate out of the checker's process, so it can only answer, not grade. That is the route METR's o3 took: the scorer ran its code. Then add a tripwire, not a policy: hash the answer key when the task starts and again at the verdict. On this recording, that hash moved.

None of that needs model telemetry. It will not tell you a change was malicious, only that the worker wrote what judged it. And these questions inspect a pipeline. On their own, they do not show that any particular product has this problem.

## 11. The sandbox held

**11:30-13:15**

*Say what did not happen. Name the allowed write. Clock and answer key: two routes, one move.*

Back to the title: your agent escaped without escaping the sandbox. The sandbox part is literal. Nothing got out. The checker overwrite was denied, and no protected byte changed.

The allowed workspace write changed the decision. The answer key was in the workspace, and the checker obeyed it. That is the escape in the title: the worker never left the sandbox, it escaped the check. In METR's report, o3's code ran inside the scorer and swapped its clock. Our worker rewrote the answer key instead. Two routes, one move: change the judge, not the work.

So isolation and acceptance are different boundaries. A sandbox answers one question: what can this process touch? Acceptance asks another: can anything it touches decide that its own work is done? In a real repository, that answer key lives in the tests, the snapshots and the CI config, and writing tests is part of the agent's job. So taking the write away is not the fix. The agent may propose what counts as correct. It must never be the last writer of what judges it.

## 12. The worker changed what counted as correct

**13:15-14:00**

*Repository first. Then the question, and its three-part answer. Thank you. Leave PASS up.*

The code and the Linux recordings are in the repository on the screen. Every hash on these slides is in there, and you can rerun the whole thing on a disposable Linux machine with bubblewrap.

So, what changed when the test went green?

Not the program. Not the checker. The answer key.

Thank you.
