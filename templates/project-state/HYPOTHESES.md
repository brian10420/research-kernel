---
schema: research-os/hypotheses/v1
scope: this project
seeded_from: research-os templates/project-state (schema v1)
purpose: >
  Where every unvalidated idea goes — from any proposer. Model-generated ideas
  enter here as status: proposed with model provenance and nowhere else.
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

# Hypotheses — <project name>

An idea is not evidence. A hypothesis moves to `accepted` when a human decides
it is worth testing; its *outcome* is written only from ledger rows. Refuted
hypotheses stay here and are cross-linked from `FAILED_IDEAS.md`.

## Entries

<!-- append entries below -->
