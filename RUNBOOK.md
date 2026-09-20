# Fifteen-minute lightning talk

Deliver nine main slides in 14 minutes. Slides 10–12 are appendix. Script: [TALK.md](TALK.md).

## Delivery

PDF on screen. No live terminal. One idea: containment is not attestation. The sting is a green checker hash and a still-wrong release. Three other grants are one slide, not a chain. Margin is silence.

## Timing

| Clock | Slide | Beat |
|---|---|---|
| 00:00–00:50 | 1 | Cold open: CI green, `/admin` no cookie is 200 |
| 00:50–02:20 | 2 | Cage vs belief: isolation is not attestation |
| 02:20–05:20 | 3 | Checker hash unchanged; policy rewrite via expected.json |
| 05:15–06:45 | 4 | Verified A, shipped B |
| 06:45–08:15 | 5 | Process never left: token, mount, allowed host |
| 08:15–11:00 | 6 | Subject, not witness |
| 11:00–12:15 | 7 | Same job, different witness |
| 12:15–13:20 | 8 | If the writer is also the witness |
| 13:20–14:00 | 9 | Containment is not attestation. Stop. |
| 14:00–15:00 | — | Margin |

## Overrun cuts

Drop the three-grant examples to one sentence. On slide 6 skip nonce fields: “Timeout is no approval. The gate names the bytes we checked.” Never cut slide 3 or the close.

## Reproduction

```sh
make factory        # no cloud
make demo           # Linux isolation lab
make deck           # hashes + PDF
```
