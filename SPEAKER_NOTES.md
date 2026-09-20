# Speaker notes

This is the Sessionize talk: four non-escape escapes, four locks.
Fun, short, friendly. Point at the slide. No terminal.
Story four: /admin with no cookie returns 200 and CI is green.

## Slide 1

00:00 to 00:30. Hi, I'm Yossi. Spoiler: the agent never climbed the wall. Namespaces fine, cgroups fine, still a bad day. Four short stories. We hold the door.

## Slide 2

00:30 to 01:15. Sandbox is cute and necessary, not the end of the movie. Fat badge, writable folder, mailroom stamp, pencil that grades homework: mess without leaving. Four stories, four locks, four questions, reception.

## Slide 3

01:15 to 03:15. Inherited credentials. Job needed a token, CI already had a fat one. Other project returns 200. Sandbox did not steal it. Fix: this task, this audience, short life. Same request 403. Own input still 200. Short life is not small scope.

## Slide 4

03:15 to 05:00. Dangerous mounts. Shared folder, writable because why not. Ordinary write, next job's file changes. Fix: read this, write that. Same write denied. Output folder still works. If the next job shouldn't be in the room, don't put the chair in the room.

## Slide 5

05:00 to 07:00. Exfil through an allowed endpoint. Report service is allowed. It mails the private fixture to another account on the same host. Firewall liked the hostname. Who and what were the question. Broker builds a boring postcard. Extra fields no. Direct route gone. Real report still arrives.

## Slide 6

07:00 to 09:30. Fun one. Ticket: /admin without cookie is 401. Checker locked, hash unchanged. It still reads expected.json. Worker makes 200 the spec. PASS. Curl is 200. Policy rewrite, then a merge you'd approve. Second box that reads the same folder is a new hoodie. PASS file is the smoke detector.

## Slide 7

09:30 to 11:30. Hit the four abstract locks: credential projection, scoped filesystems, process isolation, tamper-evident history. History detects a rewrite. It does not make /admin 401. Locked door still merges. Open door does not. PASS file ignored. Fake rulebook ignored. Swap denied.

## Slide 8

11:30 to 13:15. One agent job, four sticky notes. If who says /admin is locked is the same disk that wrote the handler, you have a confident diary. Name the thing that can refuse outside the worker. Prove the legitimate lock still merges.

## Slide 9

13:15 to 14:00. Sandbox contained the process. We issued the badge, the chair, the stamp, and the rulebook. That's the talk you came for. Ask who gave this process the authority. Repo on the slide. Stop. Smile. No tenth slide.

## Slide 10

Appendix only. Factory is the /admin path. Lab is badge, chair, mailbox. Isolated lab fails closed. No live terminal in the talk.

## Slide 11

Appendix only. If asked: not a customer incident, not model success rates, not kernel escape. History is a controller copy of the log, not a blockchain product.

## Slide 12

Appendix only. Point at the repo if people linger. Do not present these in the 15 minutes.
