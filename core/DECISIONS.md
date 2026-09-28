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


---

```yaml
id: DECISION_004
title: Amend DECISION_003's effort policy — operations roles on the strong model at medium; the guardian and the sparring partner at xhigh
date: 2026-09-28
proposer: fable          # ported from the source project's routing pass
decided_by: human
status: proposed
evidence: [core/effort_policy.yaml, README.md]
supersedes: ""           # amends point (3) of DECISION_003 only; points (1)–(2) stand
superseded_by: ""
```

**Context.** DECISION_003 (3) pinned the two operations roles to a smaller model
at `low` ("never needs frontier reasoning") and left `regression-guardian`
unlisted. In the source project the operator reversed the first half on
2026-09-28: operations errors are the expensive ones — a launch pattern that
matches the wrong process, a protected path in a push — and they come from
missed context, not from hard reasoning. The same pass pinned the guardian,
because certify-or-reject is a closed, single-answer judgement of exactly the
shape the policy already puts at `xhigh`. Separately, the documentation claim
that "`model: inherit` does not inherit effort" was checked against the live
Claude Code docs and is wrong: a wrapper without an `effort:` key inherits the
session effort.

**Decision (proposed).** `experiment-runner` and `repo-maintainer`: `model:
opus`, `effort: medium`. `regression-guardian` and the new `sparring-partner`
(DECISION_005): `effort: xhigh`, model inherited. The doctrine sentence becomes
"closed verification at `xhigh`, operations at `medium` on the strong model,
everything else inherits". The effort-inheritance sentence is corrected in
`core/effort_policy.yaml` and `README.md`. The provider-neutral `runtime:`
recommendations in the role specs are unchanged (a smaller model stays a valid
recommendation for other runtimes; policy and recommendation may differ on
purpose, DECISION_003).

**Consequences.** Operations dispatches cost more tokens per call than under
0.1.0. No role pins `max`; the operator-held session switch is unchanged. The
team-map diagrams still show the 0.1.0 badges until they are redrawn.

**Alternatives rejected.**
- Keep `sonnet` @ `low` for operations — cheapest, but the costly failures of
  those roles are context misses that a smaller model makes more often.
- Pin `xhigh` on operations — the reasoning is shallow; `medium` suffices once
  the model is strong.

---

```yaml
id: DECISION_005
title: Add sparring-partner — an isolated premise auditor for decisions, dispatched from a research-mentor gate
date: 2026-09-28
proposer: fable          # built and tested in the source project's optimization week
decided_by: human
status: proposed
evidence: [core/roles/sparring-partner.md, core/roles/research-mentor.md, core/roles/README.md]
supersedes: ""
superseded_by: ""
```

**Context.** No role audited the premises of a *decision*. The blind reviewer
judges manuscripts and the guardian judges code changes; proposals for new
experiments or claim changes were discussed only in the shared-context mentor
lane, where the auditor shares the proposer's assumptions. In the source
project most recorded reversals were premise failures that could have been
found in the files before any compute was spent.

**Decision (proposed).** A thirteenth role, `sparring-partner` (isolated;
Read / Grep / Glob / read-only shell / web). It receives the proposal as
written plus its evidence paths — never the proposer's reasoning — and returns
a verdict (`PROCEED` / `PROCEED-WITH-CHANGES` / `RETHINK`), a premise audit with
file:line or command evidence, the strongest alternative including doing
nothing, kill criteria with the cheapest disconfirming test, a regret list and
what is solid. It follows a data-contact rule (it computes nothing a
not-yet-contacted readout will report), a rebuttal scale with "one push, then
retreat", and never vetoes. `research-mentor` gains a sparring gate (hard rule
7): above the project's compute threshold, at the design phase of a large plan,
and after a quick operator–mentor agreement on direction, it dispatches the
role and opens its answer with the audit's verdict.

**Evidence and its limits.** The source project ran a pre-declared RED/GREEN
test (three planted-flaw scenarios, two sound controls, one pressure rebuttal;
three repeats per cell). A fresh, equally isolated generic reviewer on the same
model already caught every planted flaw, so the pre-declared "strictly better
than the baseline" criterion was **not met** (a tie at the ceiling). What the
role measurably added was the decision contract — an explicit verdict label,
kill criteria and a do-nothing comparison in every output (the generic
reviewer: none), and no veto headline for a cheap fix — and, after one
refactor, the data-contact rule: both arms had computed a protected outcome in
some reviews of an un-contacted pre-registration, and the refactored role did so
in none of its re-runs. The mentor gate was tested separately: without the
structural slot the mentor dispatched the audit but absorbed it (verdict shown
in none of three answers); with it, the verdict opened three of three. Small n,
one grader, same model family throughout.

**Consequences.** One audit costs about as much as a plain isolated review
(≈ +13 % in the source test). Claims about the role are limited to "adds the
decision contract and the data-contact rule"; never "catches more flaws".

**Alternatives rejected.**
- A generic "review this" dispatch — same catch rate in the test, but no
  verdict contract, and it broke the single-contact discipline.
- A shared-context devil's advocate inside the mentor — shares the proposer's
  assumptions, which is the failure this role exists to avoid.
