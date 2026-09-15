---
schema: research-os/decisions/v1
scope: cross-project (this repository). Per-project decisions live in the project repo's own DECISIONS.md.
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

# Decisions

Append-only. A reversed decision is a new entry that `supersedes` the old one.
Only a human moves an entry to `accepted` or `rejected`.

## Entries

```yaml
id: DECISION_000
title: Adopt the provider-neutral Research OS architecture
date: 2026-09-04
proposer: joint:[fable-5, gpt-5.6]   # dual-model cross review, 2026-09-04
decided_by: human
status: accepted
evidence: [MIGRATION_AUDIT.md, core/SCIENTIFIC_RULES.md]
supersedes: ""
superseded_by: ""
```

**Context.** The research team existed as a Claude-specific skill collection: role
files that only one vendor's runtime could load, with volatile project facts baked
into the role bodies and a "memory wins" clause to paper over staleness.

**Decision.** The research methodology and its decision history are the canonical
asset. They live in `core/` (rules, state schemas, role specs) under git. Every AI
vendor — Claude Code, Codex, future agents — is a replaceable runtime reached
through *generated* adapter files (`CLAUDE.md`, `AGENTS.md`, thin wrappers) produced
by `tools/sync.py` from `core/`. Adapters are never hand-edited; drift is blocked by
`tools/check_drift.py`.

**Consequences.**
- Cross-project rules and roles live in this repository; per-project state
  (`RESEARCH_STATE`, `DECISIONS`, `EXPERIMENT_LEDGER`, `HYPOTHESES`,
  `FAILED_IDEAS`, `OPEN_QUESTIONS`) lives in each project repository, seeded from
  `templates/project-state/`.
- **Two-track inversion (owner ruling 2026-09-04).** Before: a project's private
  `.claude/` was canonical and this public repo was derived by manual scrub. After:
  `core/` here is canonical for cross-project rules and roles; a project's
  `.claude/` becomes a project-specific overlay. The publication hygiene does not
  relax: the private leak-gate must print CLEAN before any public push, and
  project-specific facts never enter `core/`.
- Role specs carry no volatile project facts; those move to the project's state
  files (see DECISION_001).
- Subagents must receive the full role spec and `RULES_HASH` inside the task prompt
  (canary handshake, SCIENTIFIC_RULES §3).

**Alternatives rejected.**
- Keep one vendor's format as canonical and translate outward — leaves the
  methodology hostage to that vendor's file conventions.
- Store rules in model memory — violates principle 1 (memory is recall, not
  authority).

---

```yaml
id: DECISION_001
title: Supersede the "memory wins" doctrine — git state is authoritative, memory is recall
date: 2026-09-04
proposer: fable          # raised in the Phase 0 audit as Conflict 3
decided_by: human        # ratified at P0 approval, 2026-09-04
status: accepted
evidence: [MIGRATION_AUDIT.md, docs/design-notes.md]
supersedes: ""           # supersedes the doctrine paragraph in docs/design-notes.md and the former RESEARCH_TEAM.md
superseded_by: ""
```

**Context.** The former roster and five role files said: "when a role file and
project memory disagree, trust memory and flag the drift." That rule existed
because role files baked in facts that rotted between sync passes.

**Decision.** Git, Obsidian, and the experiment ledgers are authoritative; model
memory is recall-only. Role specs carry no volatile facts at all — those live in
the project's `RESEARCH_STATE.md` and `EXPERIMENT_LEDGER.md`, which are read at
session start. When memory contradicts git state, memory loses: the
memory-curator proposes a `memory_forget`, never a silent edit, and never an edit
to `core/`.

**Consequences.** Every "memory wins" clause is removed from role specs; the
design-notes paragraph is annotated as superseded (kept for history). Staleness
is now a *state-file* problem with a git diff, not a memory problem with no
audit trail.

**Alternatives rejected.**
- Keep "memory wins" but sync more often — still no audit trail for what memory
  asserted.

---

```yaml
id: DECISION_002
title: Freeze eval/RUBRIC.md v1 and eval/PROTOCOL.md v1 as the pre-registered evaluation
date: 2026-09-04
proposer: fable          # drafted in Phase 6 of the migration
decided_by: human        # ratified 2026-09-05
status: accepted
evidence: [eval/RUBRIC.md, eval/PROTOCOL.md]
supersedes: ""
superseded_by: ""
```

**Context.** The evaluation scaffold (five tasks, weights 20/30/20/20/10,
anchors 1–5, two comparisons graded blind) exists; results are meaningful only
against a frozen rubric.

**Decision (proposed).** Accepting this entry freezes rubric v1 and protocol
v1. Any later change requires a new entry that supersedes this one and a
version bump; results across versions are never merged.

**Consequences.** Planted-defect lists for T1/T2/T4 must be sealed before the
first run; repetitions per cell are declared before the first run.

**Alternatives rejected.** Grading against an evolving rubric — makes every
comparison across runs invalid.

---

```yaml
id: DECISION_003
title: Ship research-kernel as a self-contained Claude Code plugin; project facts live in an overlay; effort is chosen by task shape
date: 2026-09-15
proposer: fable          # drafted from the operator's request to make installation as easy as a marketplace plugin
decided_by: human
status: accepted
evidence: [.claude-plugin/plugin.json, .claude-plugin/marketplace.json, core/effort_policy.yaml, templates/research-kernel.overlay.template.md, tools/sync.py]
supersedes: ""
superseded_by: ""
```

**Context.** Installing the kernel took five manual steps (clone, vendor `core/`,
copy `CLAUDE.md` + `.claude/`, run `sync.py`, write the overlay into the
project's instruction file), because the generated skill wrappers resolved
`core/roles/<role>.md` relative to the project root. A Claude Code plugin lives
in an immutable, wholesale-replaced cache directory, so that path — and any
hand-edit inside the plugin — breaks on install or update.

**Decision.** (1) Every generated wrapper is self-contained: a skill directory
carries `SKILL.md` + `role.md` (verbatim spec) + `RULES.md` (condensed rules)
and loads only from its own directory; an isolated role's agent file inlines
its spec. `skills/` and `agents/` at the repository root are symlinks to
`.claude/`, and `.claude-plugin/{plugin,marketplace.json}` make the repository
its own marketplace and plugin (`/plugin marketplace add <owner>/<repo>` →
`/plugin install research-kernel@research-kernel`). (2) Project-specific facts
live in the consuming project's `.claude/research-kernel.overlay.md` (template
in `templates/`), injected by every skill at load time and passed to isolated
roles in the dispatch prompt; nothing inside the plugin is ever edited.
(3) `core/effort_policy.yaml` is the single, data-driven source of the
enforced Claude Code `effort:` / `model:` keys: closed verification roles at
`xhigh`, mechanical roles at `low` on a smaller model, everything else inherits;
no role pins `max`; the operator raises the *session* effort for an
unbounded-judgement step; "stuck" is handled by changing method, not effort.

**Consequences.** The copy-install path keeps working and no longer needs
`core/` in the project. `tools/check_drift.py` covers the new generated files.
The `runtime:` block in each spec stays a provider-neutral recommendation; the
policy file is the Claude Code enforcement, and the two may differ on purpose.
Public pushes still require the private leak-gate to print CLEAN.

**Alternatives rejected.**
- Keep project-root-relative wrappers and document "vendor `core/`" — breaks
  inside the plugin cache and on every update.
- Hand-edit `effort:` into wrappers inside the plugin cache (what a third-party
  plugin forces its users to do) — silently reverted by the next update.
- Pin `max` on the reviewer roles — the closed-task curve saturates at `xhigh`;
  `max` is a session-level decision for long-horizon judgement steps only.

