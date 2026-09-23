# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning. Delivery ceiling: 14:00.** Expect about 12:30-13:00 at a natural pace; the last minute is for the host. The final stage clock is still to be confirmed. Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-14. Slides 15-22 are for questions. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published.

The spoken script contains 1,425 words, about 102 words per minute over 14:00. The windows are ceilings: reaching a checkpoint early means you are on pace. Do not slow down or add material to fill the clock. This is an estimate, not a measured rehearsal; replace it with the time of one timed run-through.

## The talk in one line

**Sandboxes limit reach. Breaches happen at acceptance.** Every non-escape escape in the abstract happened on the far side of a wall that held: something outside said yes to something the agent handed it. Stop thickening the wall; secure the acceptors, and give each one an owner outside the wall.

## The story and its three deep dives

A ticket anyone could have assigned (lock down /admin) goes green, ships, and the door is still open. A whodunit clears the code and the checker and finds the answer key. Then three deep dives, each one non-obvious and each backed by the recording:

1. **A perfect receipt for a bad decision** (slide 6). Every byte was hashed; a signed attestation would verify. Provenance names bytes, not who had the right to write them.
2. **Two routes into the judge** (slides 7-8). METR's o3 changed the stopwatch from inside its scorer; our agent rewrote what its checker reads. The judge is the checker plus everything it reads and runs.
3. **Which control said no?** (slide 12). A denial proves nothing until you know which control denied; our own first test could not tell.

In between, the message: one shape four times (slide 9), secure the acceptors (slide 10), an outside owner for each and the ticket closed (slide 11). One question for Monday (slide 13). The close returns to the ticket and ends on the title (slide 14).

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-00:45 | 1 | A Friday afternoon. The ticket. The four locks. It ships. |
| 00:45-01:45 | 2 | Green. Pause. 200: anyone can walk in. The part the sandbox cannot see. Introduce yourself. |
| 01:45-02:45 | 3 | We built it ourselves: tiny model, scripted agent (hold that objection), Linux sandbox, stopped at green. |
| 02:45-03:45 | 4 | Three suspects. The code and the checker: unchanged. The third card: still unexplained. |
| 03:45-04:45 | 5 | The answer key. The diff. Click. It made the test pass the code. |
| 04:45-05:45 | 6 | Deep dive 1, for the supply-chain people: a perfect receipt for a bad decision. Which bytes, not who had the right. |
| 05:45-06:45 | 7 | The objection. METR. Click at the timing function. It changed the stopwatch. |
| 06:45-07:45 | 8 | Deep dive 2: why the door stayed open. Walk the picture. Two routes into the judge: what it reads, what it runs. |
| 07:45-08:45 | 9 | One shape, four times. One breath per row. Something outside said yes. |
| 08:45-10:00 | 10 | THE MESSAGE. Sandboxes limit reach; breaches happen at acceptance. Show of hands, yours first. The permission is the work. |
| 10:00-11:00 | 11 | Give every acceptor an outside owner. Row by row. The rule. Back to the ticket: REJECT, the door never opens, ACCEPT. |
| 11:00-12:15 | 12 | Deep dive 3: which control said no? Four rows. Our own first test got it wrong. Only the control under test may say no. |
| 12:15-13:15 | 13 | Before your next ticket ships: the question. Pause. Three moves. |
| 13:15-14:00 | 14 | Repository. The ticket. The sandbox held, the checker held, the door stayed open. Something outside said yes. The title. |
| 14:00-15:00 | - | Margin for the host. |

## Rehearsal

Rehearse with an audible timer. The ticket at the start, 200 by minute one, the answer key by minute four, the receipt by minute five, the stopwatch by minute six, one shape by minute eight, the message by minute nine, the proof by minute eleven, and the close by minute fourteen at the latest.

No slide is budgeted above about 117 spoken words per minute, and the build refuses any slide above 150. The beats are two or three seconds each: after "It ships." (1), after "200." (2), after "It made the test pass the code." (5), after "a perfect receipt for a bad decision" (6), after "It changed the stopwatch." (7), after "Breaches happen at acceptance" and after "Look around." (10), after "The door never opens." (11), and between the three short lines of the close (14).

Two clicks. On slide 5, click just before "It did not make the code pass the test." On slide 7, click on "It overwrote the timing function". The PDF therefore has 24 pages; its page labels follow the slide numbers.

Say "admin" plainly; the only case read aloud is no login. Do not read hashes aloud: the slides carry them. Say METR as "meter". Name METR, the date and o3 exactly as written on slide 7, and add no rates on stage; the numbers and METR's own caveats are in QUESTIONS.md. The printed script gives no minute count, because the stage clock is still unconfirmed. Do not add one on stage.

Slides 1 and 2 are a scenario, and slide 3 says so: "We built that pipeline ourselves" and "We stopped at the green check. Your pipeline would not have." Keep those lines; they are what make the scene honest.

If behind, cut words, never the disclosures or the message. Keep slides 1, 2, 3, 5, 9, 10, 11 and 14. Slide 3 may drop only its list of the five cases. Slide 6 may shrink to its takeaway. Slide 7 keeps METR, the date, o3, the timing function and the stopwatch, and may drop the evaluator and the separate test. Slide 12 may shrink to its first sentence and the four rows. Slides 4, 8 and 13 can each lose a paragraph.

## Evidence on stage

The slide outputs summarize recorded executions. Do not present them as a live session. The centerpiece uses a CLI status-code model. The supporting credential and upload cases use loopback HTTP. The archived API audit belongs in Q&A and requires controller-object access.

The talk claims a controlled reproduction of a known mechanism. Do not improvise a customer incident, vendor flaw or model attack-success rate. Five policy cases establish their tested behavior only.

## Local preparation

```sh
make test
make evidence
make snapshot
```

After changing experiment source, first run `make record-all` on disposable Linux with bubblewrap. Ubuntu 24.04 restricts unprivileged user namespaces, and bubblewrap then fails while bringing up a network namespace. On that release:

```sh
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

The current records come from a privileged Ubuntu 22.04 container on kernel 6.8.0-64, where that sysctl is not needed; on a stock Ubuntu 24.04 host it is. Inspect the compiled PDF and keep it offline. `make replay` is an optional explicitly labeled recording. No cloud login or live terminal is part of the delivery.

## Organizer and AV

Use the accepted title. The 15-minute duration comes from the session brief. Exact stage time and AV arrangements still require organizer confirmation. This package does not imply that logistical confirmation has happened.
