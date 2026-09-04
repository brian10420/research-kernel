---
schema: research-os/research-state/v1
scope: this project
seeded_from: research-os templates/project-state (schema v1)
purpose: >
  The single dated snapshot a session reads FIRST: what is active, frozen,
  blocked, and next. Roles never carry these facts; they read them here.
entry_template: |
  state_as_of: YYYY-MM-DD
  updated_by: human | fable | astra | other-model:<name>
  status: proposed | accepted        # a model-written snapshot is proposed until a human accepts it
  sources: [<ledger run ids, decision ids, docs>]
  active_tracks: [<name>: <one line>]
  frozen: [<what may not change, and the decision that froze it>]
  blocked: [<what is waiting on what>]
  deadlines: <real external deadlines, or "none">
  next_actions: [<ordered, each with its owner role>]
  guards: [<phrasings or numbers that must be quoted exactly, with their known-wrong variants>]
---

# Research State — <project name>

One snapshot per update, newest first. A snapshot never edits history; it
supersedes the previous one. Numbers quoted here cite their ledger row or
committed source.

## Snapshots

```yaml
state_as_of: <YYYY-MM-DD>
updated_by: human
status: accepted
sources: []
active_tracks: []
frozen: []
blocked: []
deadlines: none
next_actions: []
guards: []
```
