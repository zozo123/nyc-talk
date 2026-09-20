# Fifteen-minute lightning talk

Deliver nine main slides in 14 minutes. Slides 10–12 are appendix. Script: [TALK.md](TALK.md).

## Delivery

PDF on screen. No live terminal. One finding gets the middle of the talk: protected checker, worker-controlled expected results. Three other grants are one slide, not a chain.

## Timing

| Clock | Slide | Beat |
|---|---|---|
| 00:00–00:40 | 1 | Question: what made it eligible for release? |
| 00:40–02:00 | 2 | Factory: freeze, execute, judge, gate |
| 02:00–05:00 | 3 | Finding: checker hash unchanged, expected.json worker-written |
| 05:00–06:30 | 4 | Freeze is an operation; swap and replay die |
| 06:30–08:30 | 5 | Identity, files, release — independent, short |
| 08:30–11:00 | 6 | Judgment lives on the controller |
| 11:00–12:20 | 7 | Restricted path: good ships, bug does not |
| 12:20–13:20 | 8 | Four questions |
| 13:20–14:00 | 9 | Close, then stop |
| 14:00–15:00 | — | Margin |

## Overrun cuts

Shorten slide 5 to the three-line listing. On slide 6 skip the nonce list: “Incomplete evidence is no approval. The gate names the bytes we checked.” Never cut slide 3 or the close.

## Reproduction

```sh
make factory        # no cloud
make demo           # Linux isolation lab
make deck           # hashes + PDF
```
