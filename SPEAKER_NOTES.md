# Speaker notes

Read the code on each slide. Full sentences. No 'this is not X' contrasts.
Case four: checker hash unchanged, expected.json says 200, handler returns 200, policy requires 401.

## Slide 1

00:00 to 00:30. I am Yossi Eliaz. The title is the claim. The agent stays inside the sandbox. Namespaces and cgroups do what they were built to do. A real breach still happens. Four cases. Each uses an interface we gave the worker so it could finish the job.

## Slide 2

00:30 to 01:15. A working coding agent needs a credential, files, one publish path, and a signal that the work is done. Those are the four abstract cases. The process never leaves the box. These four interfaces still move data, files, and merge decisions.

## Slide 3

01:15 to 03:20. We started the worker with the runner token already in the environment. The GET with that token returned 200 and the private fixture. We replaced it with a task-scoped token. Other project 403. Task input 200. Expired and wrong-audience tokens 403. Do not copy the runner secret into the worker.

## Slide 4

03:20 to 05:00. We mounted another job directory writable. The write is a normal open. The host file changes. Read-only bind denies the same write. Output still works. If you snapshot this disk and fork it, the next agent inherits the same files.

## Slide 5

05:00 to 07:00. We allowed the report host. The worker posted the private fixture to another account on that host. 201. The worker does not choose URL, recipient, or body. Extra keys denied. Direct route gone. Team report still arrives.

## Slide 6

07:00 to 09:45. Ticket: unauthenticated /admin returns 401. checker.py is read-only. It loads expected.json from the workspace. Worker writes admin:none -> 200. Checker prints PASS. Independent case still requires 401. Shipped handler prints 200. A second machine that reads the same expected.json also prints PASS. Ignore a worker PASS file; that is the detector.

## Slide 7

09:45 to 11:45. Read the four abstract locks as you walk the snippet. Task token 403 on the other project. Read-only input. Worker cannot open the service. Freeze handler.py, compare on the controller, publish that digest. Used nonce cannot replay. Open admin is not published. Locked admin is published. The log does not decide the merge.

## Slide 8

11:45 to 13:15. On your host, fill in the four question marks. After you add the refusing component, run the legitimate ticket again and confirm it still completes.

## Slide 9

13:15 to 14:00. We gave the worker a token, a filesystem, a publish URL, and a checker that read its workspace. The sandbox stayed up. Those four interfaces were enough for a breach. The four locks are in the abstract. The repo has the recorded commands. Ask who gave this process the authority. Stop.

## Slide 10

Appendix only. Factory is verifier and /admin. Lab is credentials, mounts, publish. Isolated lab fails closed.

## Slide 11

Appendix only. No vendor zero-day claim. No model success rate. History head is held by the controller.

## Slide 12

Appendix only. Do not present in the 15 minutes.
