---
schema: research-os/eval-protocol/v1
status: pre-registered
version: 1
written: 2026-09-04
rubric: eval/RUBRIC.md v1
---

# Evaluation protocol

Two comparisons. They answer different questions, are run separately, and
their results are **reported separately and never merged** into one number.

## Comparison A — pure model

**Question.** With the *same* inputs and *no* ecosystem, how do the two models
perform on the five tasks?

- **Conditions:** model 1 (Fable; record the exact model id) vs model 2
  (Astra; record the exact model id). Both called through a plain chat/API
  harness with the same tool set (read, search, and — for T3 — shell/edit),
  no subagents, no skills, no hooks, no memory.
- **Held constant:** the task files, the papers, the prompt (the condensed
  rules from `AGENTS.md` sections "Condensed rules" + the task stub verbatim),
  the tool budget and wall-clock budget from `eval/RUBRIC.md`, the system
  prompt (empty apart from the harness default), temperature/sampling settings
  (recorded).
- **Repetitions:** ≥ 3 independent runs per model per task, pre-declared
  before the first run; every run reported.
- **Record per run:** model id, date, run index, tool calls used, wall clock,
  halt/timeout flags, the output bundle path.

## Comparison B — ecosystem

**Question.** With each vendor's *native* ecosystem, how do the two stacks
perform on the same tasks?

- **Conditions:** Claude Code + Fable, using the generated `CLAUDE.md`,
  `.claude/agents/`, `.claude/skills/`, native subagents, hooks, and skills;
  vs Codex + Astra, using `AGENTS.md`, `core/roles/`, and Codex's native
  mechanisms (`adapters/codex/README.md`).
- **Held constant:** task files, papers, task stubs, wall-clock budget. Tool
  budgets are per-*harness* call counts (one subagent dispatch = one call) and
  are recorded, not equalized, because the ecosystems differ by design; the
  asymmetry is reported as a limitation.
- **Repetitions and records:** as in A. Additionally record which roles were
  dispatched, whether every dispatch produced an `ACK RULES_HASH=` line, and
  any `HALT:` events (each is a harness finding).

## Blind grading (both comparisons)

1. Each run's output bundle is passed through `tools/anonymize.py build
   --condition <name>=<path> …`, which strips provenance, names, model names,
   e-mails, and timestamps, and assigns condition letters (A/B/…) in a secret
   random order; the mapping is sealed in `eval/.sealed/` (git-ignored).
2. The grader is a `blind-reviewer`-style role (or a human) that receives
   **only** the anonymized bundle, the rubric, and the task stub. It sees
   condition letters, never model or harness names. It never reads
   `eval/.sealed/`.
3. Two graders score independently; inter-rater agreement (quadratic-weighted
   κ per task) is reported. Disagreements ≥ 2 points are adjudicated by a third
   blind grader; the adjudication is recorded.
4. Un-blinding is done once, by a human, after all scores are final, using the
   sealed mapping; the un-blinding is recorded in the results file with the
   bundle id.

## Decision rule (pre-registered)

- Primary outcome per comparison: the weighted total (RUBRIC) averaged over
  repetitions, per condition, with a bootstrap 95 % CI over repetitions
  (resampling runs; ≥ 3 runs per cell is the minimum, and the CI's width is
  reported as a limitation when n is small).
- "Condition X is better on task T" is claimed only if the CI of the
  difference excludes 0. Otherwise the result is reported as inconclusive; it
  is never rounded up to a win.
- Secondary outcomes: per-task scores, halt/timeout counts, tool calls used,
  wall clock. Reported, not combined.

## Threats and controls

| threat | control |
| --- | --- |
| model version drift between runs | pin exact model ids and dates; all runs of one comparison within the same week |
| prompt or file leakage between conditions | fresh working copies per run; no shared scratch directories |
| grader bias | blind labels; two graders; κ reported |
| tool-budget asymmetry in B | recorded and reported as a limitation, never silently equalized |
| cherry-picking of runs | repetitions pre-declared; every run in the results file, failures included |
| rubric drift | rubric frozen by DECISIONS entry; version stamped on every result row |

## Reporting

`eval/RESULTS_TEMPLATE.md` — one file per comparison
(`eval/results/A-<date>.md`, `eval/results/B-<date>.md`). A joint narrative may
discuss both, but no table, figure, or number combines A and B.
