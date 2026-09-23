# October 21 stage runbook

**Zenity AI Agent Security Summit. Pier Sixty, New York. Wednesday 21 October 2026.**

**15-minute lightning. Delivery ceiling: 12:00.** Expect about 10:00 at a natural pace; the rest of the slot is for the host and a question. The final stage clock is still to be confirmed. Present `slides/talk.pdf` offline. The leave-behind is `paper/paper.pdf`. Main route: slides 1-11. Slides 12-19 are for questions. Keep a second local copy of both PDFs.

Do not invent a stage time on the day. Private logistics are kept in `research/private/`, which is not published.

The spoken script contains 1,119 words, about 93 words per minute over 12:00. At 120-130 words per minute the speech alone runs about 9 minutes, so with the beats expect roughly 10:00. The windows are ceilings: reaching a checkpoint early means you are on pace. Do not slow down or add material to fill the clock. This is an estimate, not a measured rehearsal; replace it with the time of one timed run-through.

## The story

The talk is one story told start to finish. A ticket anyone in the room could have assigned (lock down /admin) goes through a pipeline they would sign off on, goes green, ships, and the door is still open. Then a whodunit with three suspects: the code and the checker are cleared, and the answer key did it. The objection ("a real model wouldn't"), planted on slide 3, is answered on slide 6 with METR's o3 changing the stopwatch. Slide 7 answers "why did the door stay open?" with one picture: the judge is the checker plus everything it reads. Slide 8 gives the enterprise room its own version of the ticket (a procurement agent and the vendor list). Slide 9 goes back to the ticket and closes the door. Slide 10 turns it into one question for Monday. Slide 11 returns to the ticket and ends on the title.

| Clock | Slide | Stage action |
|---|---:|---|
| 00:00-00:45 | 1 | The ticket. The four locks: sandbox, no network, read-only checker, ship on green. Then: it ships. |
| 00:45-01:45 | 2 | Green. Pause. Then 200. Let it sit. Introduce yourself last: green means good. |
| 01:45-02:45 | 3 | We built it ourselves: tiny model, scripted agent (hold that objection), Linux sandbox, stopped at green. Three suspects. |
| 02:45-03:45 | 4 | Clear the code (never touched). Clear the checker (it tried: DENIED). Then: something else changed. |
| 03:45-05:00 | 5 | The answer key. The diff. The hashes did not stop it. Click. Land it: it made the test pass the code. |
| 05:00-06:15 | 6 | The objection. METR. Click at the timing function. Then: it changed the stopwatch. |
| 06:15-07:15 | 7 | Why did the door stay open? Walk the picture. Point at expected.json. End on the judge. |
| 07:15-08:45 | 8 | Coding list. Then the procurement agent and the vendor list. Then: the permission is the work. |
| 08:45-10:00 | 9 | The rule, slowly. Back to the ticket: REJECT, the door never opens, ACCEPT. |
| 10:00-11:15 | 10 | Before your next ticket ships: the question. Pause. Three moves. |
| 11:15-12:00 | 11 | Repository first. Then the ticket. The sandbox held, the checker held, the door stayed open. The title. Thank you. |
| 12:00-15:00 | - | Margin for the host and a question. |

## Rehearsal

Rehearse with an audible timer. The ticket is up at the start, 200 by minute one, the answer key by minute four, the stopwatch by minute five, the picture by minute seven, the rule by minute nine, and the close by minute twelve at the latest.

No slide is budgeted above about 104 spoken words per minute, and the build refuses any slide above 150. At 130 words per minute every slide ends inside its window; that slack is margin, not silence to fill. The beats are a two- or three-second pause each, and they are the story: after "It ships." on slide 1, after "200." on slide 2, after "Something else changed." on slide 4, after "It made the test pass the code." on slide 5, after "It changed the stopwatch." on slide 6, after the question on slide 10, and between the three short lines on slide 11.

Two clicks. On slide 5, click just before "It did not make the code pass the test." On slide 6, click on "It overwrote the timing function". Every other slide is one page. The PDF therefore has 21 pages; its page labels follow the slide numbers.

Say "admin" plainly; the only case read aloud is no login. Do not read hashes aloud: the slides carry them. Say METR as "meter". Name METR, the date and o3 exactly as written on slide 6, and add no rates on stage; the numbers and METR's own caveats are in QUESTIONS.md. The printed script gives no minute count, because the stage clock is still unconfirmed. Do not add one on stage.

Slides 1 and 2 are a scenario, and slide 3 says so: "We built that pipeline ourselves" and "We stopped at the green check. Your pipeline would not have." Keep those lines; they are what make the scene honest.

If behind, cut words, never the disclosures. Keep slides 1, 2, 3, 5, 7, 9 and 11. Slide 3 may drop only its list of the five cases. Slide 6 may drop the evaluator, "Nobody asked it to" and the separate test, and keeps METR, the date, o3, the timing function and the stopwatch. Never shorten slide 6 to a form where "It changed the stopwatch." follows "Our agent is a script." Slides 4, 8 and 10 can each lose their second paragraph.

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
