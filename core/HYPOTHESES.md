---
schema: research-os/hypotheses/v1
scope: cross-project schema + one worked example. Real hypotheses live in the project repo's HYPOTHESES.md.
purpose: >
  Where every unvalidated idea goes — from any proposer. Model-generated ideas
  enter here as status: proposed with model provenance and nowhere else
  (SCIENTIFIC_RULES principle 3).
entry_template: |
  id: H_<NNN>
  title: <one line>
  date: YYYY-MM-DD
  proposer: human | fable | astra | other-model:<name>
  status: proposed | accepted | rejected | superseded   # accepted = worth testing; the RESULT lives in the ledger
  decided_by: human | ""
  evidence: [<prior runs, papers, notes that motivate it>]
  statement: <falsifiable claim, one sentence>
  prediction: <what we expect to observe if true>
  falsifier: <what observation would refute it>
  decision_rule: <pre-registered: what result moves it to confirmed / refuted>
  test_plan: <smallest decisive experiment; cost estimate>
  linked_runs: [RUN_<NNN>, …]
  outcome: "" | confirmed | refuted | inconclusive   # filled from the ledger, never before the run
  supersedes: ""
  superseded_by: ""
---

# Hypotheses

An idea is not evidence. A hypothesis moves to `accepted` when a human decides it
is worth testing; its *outcome* is written only from ledger rows. Refuted
hypotheses stay here and are cross-linked from `FAILED_IDEAS.md`.

## Entries

```yaml
id: H_000
title: Worked example — a linear-time backbone matches attention at short context under a width-matched ablation
date: 2026-09-04
proposer: other-model:example-assistant     # model-originated ⇒ enters as proposed, with provenance
status: proposed
decided_by: ""
evidence: [L_000]
statement: At the corpus's typical sequence length, a width-matched linear-time backbone reaches the attention baseline's primary metric within a pre-registered margin.
prediction: mean difference within ±<margin> on the primary metric across all seeds and folds.
falsifier: the equivalence test fails (one-sided bound outside the margin) on the full protocol.
decision_rule: TOST with margin <margin> on the fold-clustered bootstrap; parity is claimed only if both one-sided tests pass.
test_plan: reuse existing baseline runs; train the candidate arm on all seeds/folds (≈ <cost>); no new baseline training.
linked_runs: []
outcome: ""
supersedes: ""
superseded_by: ""
```
