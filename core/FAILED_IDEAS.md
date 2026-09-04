---
schema: research-os/failed-ideas/v1
scope: cross-project schema + one worked example. Real entries live in the project repo's FAILED_IDEAS.md.
purpose: >
  Negative results with their evidence, so nobody re-runs them by accident and
  so the *reason* for the failure is preserved. Deletion is forbidden.
entry_template: |
  id: F_<NNN>
  title: <one line>
  date: YYYY-MM-DD
  proposer: human | fable | astra | other-model:<name>   # who proposed the ORIGINAL idea
  status: accepted | superseded          # accepted = the failure is established by evidence
  decided_by: human
  evidence: [RUN_<NNN>, …]               # ledger rows are mandatory — a failed idea without runs is a hypothesis, not a failure
  hypothesis: H_<NNN>
  what_was_tried: <one paragraph>
  why_it_failed: <the mechanism, if known; otherwise "unknown — see evidence">
  what_it_rules_out: <the class of ideas this closes>
  retry_only_if: <the specific condition under which re-testing is justified>
  supersedes: ""
  superseded_by: ""
---

# Failed Ideas

A failure is a result. Each entry links the ledger rows that establish it and
states what would justify a retry — so "let's try X again" has to argue against
a recorded reason.

## Entries

```yaml
id: F_000
title: Worked example — a fixed anisotropic label-smoothing width did not improve the primary metric
date: 2026-09-04
proposer: human
status: accepted
decided_by: human
evidence: [RUN_000]
hypothesis: H_000
what_was_tried: A fixed, input-independent anisotropic soft-target width replaced the isotropic default under the full protocol, all seeds and folds.
why_it_failed: The learned head already absorbs the anisotropy; a fixed prior adds no information and slightly worsens calibration.
what_it_rules_out: Fixed (input-independent) target-shape priors of this family.
retry_only_if: The width is made input-dependent (learned per sample) — that is a different hypothesis, file it as a new H_ entry.
supersedes: ""
superseded_by: ""
```
