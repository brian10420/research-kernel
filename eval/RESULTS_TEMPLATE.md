---
schema: research-os/eval-results/v1
comparison: A | B                      # one file per comparison; never both
rubric_version: 1
protocol_version: 1
date_range: <YYYY-MM-DD>..<YYYY-MM-DD>
conditions:                            # filled by the human AFTER un-blinding
  A: <model or stack, exact ids>
  B: <model or stack, exact ids>
unblinded_by: human
unblinded_on: <YYYY-MM-DD>
sealed_bundle_ids: [<id>, …]
deviations_from_protocol: [<one line each, or "none">]
---

# Results — comparison <A|B>

## Runs (every run, including failed / timed-out / halted)

| run id | condition (letter) | task | rep | tool calls | wall clock | halt/timeout | bundle path |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Scores (blind; one row per grader per run)

| run id | task | grader | score (1–5) | anchor met | notes |
| --- | --- | --- | --- | --- | --- |

## Agreement

| task | κ (quadratic-weighted) | adjudicated runs |
| --- | --- | --- |

## Summary (per condition letter; un-blinded names added only after the freeze of all scores)

| condition | T1 | T2 | T3 | T4 | T5 | weighted total (mean ± sd over reps) | 95 % CI |
| --- | --- | --- | --- | --- | --- | --- | --- |

**Difference (A − B) in weighted total:** <estimate> [<CI>] → <"better" only if
the CI excludes 0; otherwise "inconclusive">.

## Secondary outcomes

- halts / timeouts per condition: …
- ACK line present on every dispatch (comparison B only): …
- tool calls and wall clock, per task: …

## Limitations

- n per cell = …; CI width …
- tool-budget asymmetry (B): …
