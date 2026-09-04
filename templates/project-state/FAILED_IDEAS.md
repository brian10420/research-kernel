---
schema: research-os/failed-ideas/v1
scope: this project
seeded_from: research-os templates/project-state (schema v1)
purpose: >
  Negative results with their evidence, so nobody re-runs them by accident and
  so the reason for the failure is preserved. Deletion is forbidden.
entry_template: |
  id: F_<NNN>
  title: <one line>
  date: YYYY-MM-DD
  proposer: human | fable | astra | other-model:<name>   # who proposed the ORIGINAL idea
  status: accepted | superseded          # accepted = the failure is established by evidence
  decided_by: human
  evidence: [RUN_<NNN>, …]               # ledger rows are mandatory
  hypothesis: H_<NNN>
  what_was_tried: <one paragraph>
  why_it_failed: <the mechanism, if known; otherwise "unknown — see evidence">
  what_it_rules_out: <the class of ideas this closes>
  retry_only_if: <the specific condition under which re-testing is justified>
  supersedes: ""
  superseded_by: ""
---

# Failed Ideas — <project name>

A failure is a result. Each entry links the ledger rows that establish it and
states what would justify a retry.

## Entries

<!-- append entries below -->
