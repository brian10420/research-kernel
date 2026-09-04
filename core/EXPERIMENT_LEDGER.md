---
schema: research-os/experiment-ledger/v1
scope: cross-project schema + one worked example. Real runs live in the project repo's EXPERIMENT_LEDGER.md.
purpose: >
  The append-only record of every run that was ever launched. A row exists
  before the metrics do. Nothing is deleted; a wrong row is superseded.
row_template: |
  id: RUN_<NNN>
  title: <one line: what question this run answers>
  date: YYYY-MM-DD                      # launch date
  proposer: human | fable | astra | other-model:<name>
  operator: <role that launched it, e.g. experiment-runner>
  ack: "ACK RULES_HASH=<hash>"          # first line of the run log; REQUIRED — missing ⇒ regression-guardian rejects the row
  status: planned | running | complete | failed | aborted | rejected
  reason: ""                            # required when failed / aborted / rejected (e.g. missing_ack, OOM, diverged, drift-gate)
  hypothesis: H_<NNN>                   # the HYPOTHESES.md entry this run tests, or "characterization"
  pre_registered: true | false          # decisive runs must be true
  protocol: <name + pointer to its verbatim definition>
  config: <path to the exact config / command line>
  code_rev: <git sha>
  seeds: [<all seeds planned>]          # ALL of them, planned up front
  folds: [<all folds>]
  metrics:                              # one block per metric; per-seed × per-fold values, then mean ± sample sd
    <metric_name>:
      per_run: {<seed>/<fold>: <value>, …}
      mean: <value>
      sd: <value>
      n: <count>
  artifacts: [<checkpoint / log / output paths>]
  anomalies: [<diverged fold, early stop that fired suspiciously early, …>]
  evidence: [<log paths>]
  supersedes: ""
  superseded_by: ""
---

# Experiment Ledger

Rules that bind every row (SCIENTIFIC_RULES §4): all seeds, all folds; mean ±
sample standard deviation; failed runs stay; checkpoint selection on validation
only; one committed script per published number.

## Rows

```yaml
id: RUN_000
title: Worked example — backbone ablation, matched width, protocol P (illustrative values)
date: 2026-09-04
proposer: human
operator: experiment-runner
ack: "ACK RULES_HASH=<hash-at-launch>"
status: complete
reason: ""
hypothesis: H_000
pre_registered: true
protocol: P (5-fold leave-one-group-out, rotating inner validation; verbatim in the project's protocol doc)
config: configs/example.yaml --model <arm> --seed <s>
code_rev: <sha>
seeds: [1, 2, 3]
folds: [0, 1, 2, 3, 4]
metrics:
  primary_metric:
    per_run: {1/0: 0.61, 1/1: 0.64, 1/2: 0.60, 1/3: 0.63, 1/4: 0.62,
              2/0: 0.60, 2/1: 0.65, 2/2: 0.61, 2/3: 0.62, 2/4: 0.63,
              3/0: 0.62, 3/1: 0.63, 3/2: 0.59, 3/3: 0.64, 3/4: 0.62}
    mean: 0.621
    sd: 0.017
    n: 15
artifacts: [outputs/example/<arm>/seed_<s>/fold_<k>/best_model.pt]
anomalies: [seed 3 / fold 2 early-stopped at epoch 4 — kept, flagged]
evidence: [outputs/example/<arm>/training.log]
supersedes: ""
superseded_by: ""
```

*(Illustrative numbers only — they belong to no real project.)*
