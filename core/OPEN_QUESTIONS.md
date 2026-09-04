---
schema: research-os/open-questions/v1
scope: cross-project schema + one worked example. Real entries live in the project repo's OPEN_QUESTIONS.md.
purpose: >
  Questions that matter and are not yet answered, with what would answer them.
  Distinct from HYPOTHESES.md (which holds falsifiable claims) — a question here
  usually spawns one or more hypotheses.
entry_template: |
  id: Q_<NNN>
  title: <the question, as a question>
  date: YYYY-MM-DD
  proposer: human | fable | astra | other-model:<name>
  status: proposed | accepted | rejected | superseded   # accepted = worth pursuing; closed questions get superseded_by the answer
  decided_by: human | ""
  evidence: [<what raised it>]
  why_it_matters: <one sentence — which decision hinges on it>
  what_would_answer_it: <the observation or experiment>
  blocked_by: [<data, compute, another question>]
  spawned: [H_<NNN>, …]
  answer: ""                              # filled only from ledger / literature entries, with their ids
  supersedes: ""
  superseded_by: ""
---

# Open Questions

## Entries

```yaml
id: Q_000
title: Worked example — does the short-context parity between backbones survive at the long-sequence regime?
date: 2026-09-04
proposer: human
status: accepted
decided_by: human
evidence: [L_000, H_000]
why_it_matters: The efficiency argument for the linear-time backbone only holds if accuracy does not degrade where the cost advantage appears.
what_would_answer_it: The same width-matched ablation at the long-sequence encoder setting, all seeds and folds, with the pre-registered equivalence test.
blocked_by: [long-sequence encoder runs (compute)]
spawned: [H_000]
answer: ""
supersedes: ""
superseded_by: ""
```
