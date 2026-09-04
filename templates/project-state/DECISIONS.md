---
schema: research-os/decisions/v1
scope: this project
seeded_from: research-os templates/project-state (schema v1)
entry_template: |
  id: DECISION_<NNN>
  title: <one line>
  date: YYYY-MM-DD
  proposer: human | fable | astra | other-model:<name> | joint:<list>
  decided_by: human
  status: proposed | accepted | rejected | superseded
  evidence: [<paths/urls>]
  supersedes: ""
  superseded_by: ""
  context: <what prompted the decision>
  decision: <what was decided, in one paragraph>
  consequences: <what changes because of it; what it forbids>
  alternatives_rejected: [<one line each>]
---

# Decisions — <project name>

Append-only. A reversed decision is a new entry that `supersedes` the old one.
Only a human moves an entry to `accepted` or `rejected`.

## Entries

```yaml
id: DECISION_000
title: Adopt research-os project-state files for this project
date: <YYYY-MM-DD>
proposer: human
decided_by: human
status: accepted
evidence: [<research-os commit or tag>]
supersedes: ""
superseded_by: ""
```

**Context.** <why this project adopts the two-layer structure>

**Decision.** Cross-project rules and roles are read from research-os; this
project's state lives in these files.

**Consequences.** Every run gets a ledger row; every idea gets provenance; role
specs carry no project facts.

**Alternatives rejected.** <one line each, or "none considered">
