---
schema: research-os/research-state/v1
scope: cross-project (this repository). A project keeps its own RESEARCH_STATE.md (see templates/project-state/).
purpose: >
  The single dated snapshot a session reads FIRST. It answers: what is active,
  what is frozen, what is blocked, what happens next. It replaces volatile facts
  that used to be baked into role files. Roles never carry these facts; they
  read them here.
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

# Research State

One snapshot per update, newest first. A snapshot never edits history; it
supersedes the previous one. Numbers quoted here cite their ledger row or
committed source.

## Snapshots

```yaml
state_as_of: 2026-09-04
updated_by: fable
status: accepted            # accepted by the owner with the Phase 0 approval
sources: [MIGRATION_AUDIT.md, core/DECISIONS.md#DECISION_000]
active_tracks:
  - research-os migration: Phases 1–6 in progress on branch migration/research-os
frozen:
  - core/SCIENTIFIC_RULES.md section 1 (the seven principles): change requires a DECISIONS entry
blocked:
  - public push: waits on the private leak-gate printing CLEAN and the owner's own push
deadlines: none
next_actions:
  - Phase 2 compile layer (tools/sync.py, tools/check_drift.py) — owner role: dl-engineer
  - Phase 4 wrappers + tools/anonymize.py — owner role: dl-engineer
  - copy templates/project-state into the first consumer project — owner: human
guards:
  - "adapters are generated — edit core/, not CLAUDE.md or AGENTS.md"
```
