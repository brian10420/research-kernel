---
schema: research-os/open-questions/v1
scope: this project
seeded_from: research-os templates/project-state (schema v1)
purpose: >
  Questions that matter and are not yet answered, with what would answer them.
  A question here usually spawns one or more hypotheses.
entry_template: |
  id: Q_<NNN>
  title: <the question, as a question>
  date: YYYY-MM-DD
  proposer: human | fable | astra | other-model:<name>
  status: proposed | accepted | rejected | superseded   # closed questions get superseded_by the answer
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

# Open Questions — <project name>

## Entries

<!-- append entries below -->
