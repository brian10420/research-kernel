---
schema: research-os/experiment-ledger/v1
scope: this project
seeded_from: research-os templates/project-state (schema v1)
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
  reason: ""                            # required when failed / aborted / rejected
  hypothesis: H_<NNN>                   # or "characterization"
  pre_registered: true | false          # decisive runs must be true
  protocol: <name + pointer to its verbatim definition>
  config: <path to the exact config / command line>
  code_rev: <git sha>
  seeds: [<all seeds planned>]
  folds: [<all folds>]
  metrics:
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

# Experiment Ledger — <project name>

Binding rules (SCIENTIFIC_RULES §4): all seeds, all folds; mean ± sample
standard deviation; failed runs stay; checkpoint selection on validation only;
one committed script per published number; a row before every launch.

## Rows

<!-- append rows below, newest last -->
