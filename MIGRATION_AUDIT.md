# MIGRATION_AUDIT.md — Phase 0 audit for the `research-os` migration

- **Date:** 2026-09-04
- **Target repository:** this repo (`brian10420/claude_research_team`, local
  `<home>/claude-research-team`), to be renamed **`research-os`** (owner `brian10420`).
- **Provenance:** architecture converged through a dual-model cross review
  (Claude Fable 5 + GPT-5.6, 2026-09-04); final decision by the repo owner. Recorded as
  DECISION_000 in `core/DECISIONS.md` (Phase 1).
- **Status:** P0 APPROVED by the owner on 2026-09-04 with the rulings below.

> **Public-repository note.** This repository is public. The consumer research
> project's name and all private filesystem paths are replaced by placeholders:
> `<consumer-project>` (the private research repo whose `.claude/` was the
> canonical source), `<consumer-vault>` (its notes vault), `<home>` (the owner's
> home directory). The literal values are in the private session record.

## Owner rulings (2026-09-04, binding)

1. **Target repo:** `<home>/claude-research-team`. <consumer-project> (`<consumer-project>`) is
   strictly read-only this session: doctrine cross-check only.
2. **DECISION_001 ratified:** the former "memory wins" doctrine is superseded. Git,
   Obsidian, and experiment ledgers are authoritative; model memory is recall-only; memory
   drift is handled through memory-curator *proposals*, never silent edits.
3. **Two-track inversion accepted** as a consequence recorded inside DECISION_000. Hard
   conditions: the private leak-gate must print CLEAN before the final report, and the
   migration session never pushes.
4. The Phase 0/1 wording appears once (execution outline below).

## Conflict 1 — which repository is "this repository" (ruled)

The migration session was launched in `<consumer-project>` (the <consumer-project> research
codebase), but the mission describes a *skill collection* that gets renamed, holds
cross-project rules, and ships templates "to copy into <consumer-project>". That is this repo:
the public mirror of the consumer project's private `.claude/` team (MIT; `main` @ `9775931`;
`sync-status` up to date with the private originals on 2026-09-04).

Why it cannot be <consumer-project>: (a) "GitHub repo rename to research-os" is meaningless for
the research repo; (b) Phase 2 generates `CLAUDE.md` at repo root, which in <consumer-project>
would overwrite the project-instructions file protected by the standing rule "no agent
edits it"; (c) the manual action "copy templates/project-state into <consumer-project>".

## Audit table

Legend — classification is one of {core-methodology, claude-adapter, deprecate};
"→ legacy/" means the original is moved with `git mv` (history kept) in Phase 4 and a
one-line reason is appended to this file.

### A. Target repo `<home>/claude-research-team` (becomes `research-os`)

| # | item | current type | classification | destination | risk notes |
|---|------|--------------|----------------|-------------|------------|
| A1 | `skills/math-reviewer/SKILL.md` | Claude skill (in-session, 67 lines) | core-methodology + claude-adapter | spec → `core/roles/math-reviewer.md`; thin wrapper → `.claude/skills/math-reviewer/SKILL.md`; original → `legacy/skills/` | verify-only rule; the "⚠ unverified — re-check in a stronger session" grammar must survive; runtime = inherit / high |
| A2 | `skills/dl-engineer/SKILL.md` | Claude skill (70 lines) | core-methodology + claude-adapter | `core/roles/dl-engineer.md` + wrapper; original → legacy | never self-certifies (guardian gate); placeholder blocks (AMP policy, contracts) become per-project state pointers |
| A3 | `skills/research-mentor/SKILL.md` | Claude skill (59 lines) | core-methodology + claude-adapter | `core/roles/research-mentor.md` + wrapper; original → legacy | carries the "memory wins" doctrine (Conflict 3); the ARS deep-research boundary is Claude-specific → adapter only |
| A4 | `skills/results-analyst/SKILL.md` | Claude skill (59 lines) | core-methodology + claude-adapter | `core/roles/results-analyst.md` + wrapper; original → legacy | honesty doctrine → SCIENTIFIC_RULES; output contract must reference the EXPERIMENT_LEDGER schema |
| A5 | `skills/paper-writer/SKILL.md` | Claude skill (76 lines) | core-methodology + claude-adapter | `core/roles/paper-writer.md` + wrapper; original → legacy | "memory wins" line; ARS academic-paper boundary → adapter only; honest-framing guardrails are methodology |
| A6 | `skills/study-coach/SKILL.md` | Claude skill (62 lines) | core-methodology + claude-adapter | `core/roles/study-coach.md` + wrapper; original → legacy | Study Log persistence → `core/STUDY_LOG.md` schema; vault path = per-project placeholder |
| A7 | `skills/science-presenter/SKILL.md` | Claude skill (103 lines) | core-methodology + claude-adapter | `core/roles/science-presenter.md` + wrapper; original → legacy | heaviest Claude coupling (Artifact tool ×9, `design` canvas, Explore subagent); spec keeps a medium-agnostic contract (HTML deck file; poster = design canvas *if the runtime provides one*, else SVG/PDF); tool names → adapter |
| A8 | `agents/blind-reviewer.md` | Claude subagent (74 lines; `model: inherit`; tools Read/Grep/Glob/WebSearch/WebFetch) | core-methodology + claude-adapter | `core/roles/blind-reviewer.md`; thin `.claude/agents/blind-reviewer.md` (canary halt); original → legacy | input contract = anonymized bundle via `tools/anonymize.py`; the ACK line carries the hash only (no provenance), compatible with principle 4; web tools = "if the runtime provides them, else list unverified claims"; runtime inherit / high |
| A9 | `agents/experiment-runner.md` | Claude subagent (62 lines; `model: sonnet`) | core-methodology + claude-adapter | `core/roles/experiment-runner.md`; thin agent wrapper; original → legacy | every run log must start with an ACK line (guardian rejects otherwise); ledger schema = output contract; runtime = smaller model / medium |
| A10 | `agents/regression-guardian.md` | Claude subagent (70 lines; `model: inherit`) | core-methodology + claude-adapter | `core/roles/regression-guardian.md`; thin agent wrapper; original → legacy | gains the Phase-3 duty: reject logs lacking a valid ACK and record the rejection in EXPERIMENT_LEDGER; "partial suite never certifies" kept; runtime inherit / high |
| A11 | `agents/repo-maintainer.md` | Claude subagent (53 lines; `model: sonnet`) | core-methodology + claude-adapter | `core/roles/repo-maintainer.md`; thin agent wrapper; original → legacy | **not in the mission's role lists (Conflict 2)** — kept as an isolated subagent (mechanical, dispatched), smaller model / medium; the never-push-list doctrine is methodology |
| A12 | `RESEARCH_TEAM.md` | roster contract (skills-vs-subagents, model pins, Agent tool) | core-methodology (boundaries, flows, hard rules) + claude-adapter (mechanism/model table) | doctrine → `core/roles/README.md` (provider-neutral roster); mechanism table → generated `CLAUDE.md`; original → `legacy/` | contains "memory wins" (Conflict 3) and Claude model pins (Conflict 5) |
| A13 | `README.md` | Claude Code install guide + team narrative | claude-adapter (install) + core-methodology (why roles, honesty note) | rewritten `README.md` (two-layer statement, pointer map, hooksPath, adapters); original → `legacy/README.md` | the install snippet `cp skills → .claude/skills` becomes wrong after Phase 4; "Last synced" line and MIT line are leak-allowlisted (keep) |
| A14 | `docs/design-notes.md` | rationale (context posture, independence, memory-wins) | core-methodology | keep in `docs/`; cited from DECISION_000; the memory-wins paragraph is superseded by DECISION_001 (annotated, not deleted) | provider-neutral except mechanism nouns |
| A15 | `docs/customization.md` | fill-in guide for `<placeholder>` slots in `.claude/` copies | claude-adapter | → `legacy/docs/customization.md`; replaced by `templates/project-state/README.md` + the new README install section | the paths it documents cease to exist after Phase 4 |
| A16 | `docs/creating-skills-with-tdd.md` | process doc (RED→GREEN for role files) | core-methodology | keep in `docs/` unchanged | mentions superpowers `writing-skills` by attribution only |
| A17 | `templates/STUDY_LOG_TEMPLATE.md` | per-project vault template | core-methodology | keep; `core/STUDY_LOG.md` gets the schema header + example | the mission puts STUDY_LOG in `core/`, not in `templates/project-state` — respected |
| A18 | `templates/PRESENTATION_LOG_TEMPLATE.md` | per-project log template | core-methodology | keep (science-presenter output contract points here) | — |
| A19 | `templates/session-handoff-prompt.md` | lane handoff template | core-methodology | keep; Phase 3 amends it to carry `RULES_HASH` + the role spec | already harness-neutral |
| A20 | `templates/leakcheck.template.sh` | two-track hygiene pattern | core-methodology | keep | the real deny-list stays private in <consumer-project> (B8) |
| A21 | `assets/team-map.svg`, `assets/team-flows.svg` | diagrams of the Claude skill/subagent mechanism | claude-adapter | keep in `assets/`; README labels them "the Claude Code runtime view" | redraw for the two-layer model = optional manual action |
| A22 | `LICENSE` | MIT © Ting-Yi Lin | (unclassified — legal file, keep) | unchanged | the owner's own choice; allowlisted name |
| A23 | hooks / commands / settings under a `.claude/` dir | **none exist** in this repo | — | Phase 2 creates `.githooks/pre-commit`; Phase 4 creates `.claude/{agents,skills}/` wrappers | the repo currently installs by copying into a consumer's `.claude/` |

### B. <consumer-project> `<consumer-project>` (private canonical source + first consumer; read-only this session)

| # | item | current type | classification | destination | risk notes |
|---|------|--------------|----------------|-------------|------------|
| B1 | `.claude/skills/*` ×7, `.claude/agents/*` ×4, `.claude/RESEARCH_TEAM.md` | private canonical role files (project facts baked in; 71–161 diff lines vs public each) | core-methodology (doctrine source) — stays | untouched; doctrine cross-checked from here while writing `core/roles/`; later re-derivation as wrappers + project overlay = manual follow-up | **contains project-specific numbers, names, and personal details that must never enter public `core/`** → leak-gate before any push |
| B2 | `CLAUDE.md` (project instructions, 8.3 KB) | Claude project instructions; protected by the standing rule "no agent edits it" (verified: the ARS PreToolUse guard deliberately does **not** protect `CLAUDE.md` (ARS #459) and only fences ARS's own Bucket-A agents, so the rule is the only guard) | core-methodology (project-level) — stays | untouched; **not** generated by `sync.py` | would have been clobbered had the target been <consumer-project> (Conflict 1, ruled); a dedicated write-guard is listed as a follow-up in `docs/hardening.md` (Phase 3) |
| B3 | `.claude/settings.json` (enables the ARS plugin) | project runtime config | claude-adapter — stays | untouched | — |
| B4 | `.claude/settings.local.json` (permission allowlist, untracked) | local harness state | claude-adapter — stays | untouched; never copied (machine paths) | — |
| B5 | `.claude/scheduled_tasks.lock`, `.claude/worktrees/` | transient harness state (gitignored) | claude-adapter (transient) | untouched | — |
| B6 | `README.md` (research README) | project doc | out of scope | untouched | — |
| B7 | `docs/` (100 files: pre-registrations, handoffs, skeletons, sweeps, presentations, release/) | per-project research records | core-methodology content, **per-project** | stays; future distillation into the consumer project's project-state files as reviewed diffs (principle 7) | never bulk-imported |
| B8 | `tools/release/leakcheck_public_tree.sh` + `leakcheck_allowlist.txt` + `sync-status.sh`; `docs/release/PUBLIC_SYNC_CHECKLIST.md` + `public_sync_manifest.txt` | two-track publication gate (private) | core-methodology (hygiene doctrine) — stays private | untouched; **manifest public paths must be remapped after Phase 4** (`skills/x/SKILL.md` → `core/roles/x.md` + wrapper) = manual action | the leak-gate must run on the research-os tree before any push |
| B9 | project memory dir (55 files, `~/.claude/projects/…/memory/`) | model recall layer | — (governed by the Phase 5 policy) | untouched; memory-curator's audit target | demoted from authority (DECISION_001) |
| B10 | plugins: ARS (project scope), superpowers + obsidian (user scope) | Claude plugins referenced by role boundaries | claude-adapter | references genericized in `core/roles/`; named only in the generated `CLAUDE.md` | ARS descriptions must never be edited (A/B-evaluated upstream) |
| B11 | `~/.claude/skills/` third-party ×10 (mattpocock) | user-level skills | out of scope | README attribution kept | never vendored |
| B12 | Obsidian vault `<consumer-vault>` (Study Log, Results Ledger, Presentation Log) | per-project truth layer (principle 1) | core-methodology, per-project | referenced via placeholders in templates | live symlink `Claude Memory/` → memory dir: never rename memory files |

## Ambiguous items and conflicts

1. **Target repo** — RULED: `claude-research-team`.
2. **`repo-maintainer` is missing from the mission's subagent/skill lists** ("plus any
   others" covers it). Disposition: canonical spec + thin subagent wrapper; runtime =
   smaller model, medium effort; its never-push list stays a hard rule.
3. **"Memory wins" doctrine vs principle 1** — RULED (DECISION_001, status accepted,
   decided by the owner 2026-09-04). `RESEARCH_TEAM.md` and five skills said "when a role
   file and memory disagree, trust memory". Superseded: role specs carry **no volatile
   facts** (those move to `RESEARCH_STATE.md` / `EXPERIMENT_LEDGER.md`), git/Obsidian/
   ledger win, memory drift → memory-curator proposes `memory_forget`, never a silent edit.
4. **Two-track doctrine inversion** — RULED: recorded as a consequence inside
   DECISION_000. Before: private `.claude/` canonical, public derived by manual scrub.
   After: `research-os/core/` is canonical for cross-project rules and roles; the consumer project's
   `.claude/` becomes a project overlay. Hard conditions: the leak-gate prints CLEAN before
   the final report; manifest remap = manual action; no push by the migration session.
5. **Model pins.** Standing rule: the Fable pin was reversed on an earlier internal date — nothing may
   pin a paid tier. The mission's "inherit at high effort" complies. `effort:` as an
   agent-frontmatter key is unverified → Phase 4 checks the live docs; if unverifiable,
   `model: inherit` with the effort stated in the `runtime:` prose block only.
   **VERIFIED 2026-09-04 against the live Claude Code docs (sub-agents page):** accepted
   `model:` values are `sonnet`, `opus`, `haiku`, `fable`, a full model id, or `inherit`
   (= the main conversation's model); there is **no `effort` key for subagents** (skills
   have one: low/medium/high/xhigh/max). Wrappers therefore use `inherit` for
   reasoning-heavy roles and `sonnet` for mechanical ones; effort lives in the
   `runtime:` block and the wrapper body. The `fable` alias exists and is never used
   (standing no-paid-tier rule).
6. **Provider-specific tooling inside role contracts** (science-presenter: Artifact and
   `design`; blind-reviewer: WebSearch/WebFetch; mentor: ARS). Disposition: capability
   phrasing in `core/roles/` ("if the runtime provides X, else Y"); concrete tool names
   only in the Claude wrappers and the generated `CLAUDE.md`.
7. **Diagrams and the README install snippet** become stale after Phase 4. Disposition:
   README rewritten (Phase 4); SVGs kept and labeled as the Claude runtime view; redraw is
   optional.
8. **`LICENSE`** does not fit the three classes — kept unchanged, flagged here.
9. **Public repo hygiene.** Everything written into `core/` must be project-neutral
   (placeholders; no metric values; no personal details beyond the allowlisted MIT line).
   The private leak-gate (`<consumer-project>/tools/release/leakcheck_public_tree.sh`) is
   run against the working tree before the final report and its result printed.

## Execution outline (all in `<home>/claude-research-team`, one commit per phase)

- **Phase 0**: branch `migration/research-os` from `main`; this file →
  `phase-0: migration audit`.
- **Phase 1**: `core/` (SCIENTIFIC_RULES + 8 state files, schema headers + one example
  each; DECISION_000 with the two-track consequence; DECISION_001 memory-wins
  superseded), `core/roles/` (11 specs + `README.md` roster; `runtime:` block filled in
  Phase 4), `templates/project-state/` (6 files + README). Sources: the public role files
  (doctrine), the private <consumer-project> files read-only for cross-check.
  → `phase-1: canonical core scaffold`.
- **Phase 2**: `tools/sync.py` (stdlib; deterministic; banner + RULES_HASH + pointer map
  + condensed rules → `CLAUDE.md`, `AGENTS.md`), `tools/check_drift.py`,
  `.githooks/pre-commit`, README note for `git config core.hooksPath .githooks`.
  → `phase-2: compile layer`.
- **Phase 3**: canary protocol text into SCIENTIFIC_RULES, both adapters, every role
  spec's first rule, the guardian's reject duty; `docs/hardening.md` (PreToolUse ACK
  validation idea, not implemented, plus the follow-up item: a PreToolUse write-guard for
  the consumer project's `CLAUDE.md`). → `phase-3: canary handshake`.
- **Phase 4**: `.claude/agents/{blind-reviewer,experiment-runner,regression-guardian,
  repo-maintainer}.md` thin wrappers; `.claude/skills/<7>/SKILL.md` wrappers loading
  `core/roles/<name>.md` by relative path; `tools/anonymize.py` (+ `eval/.sealed/`);
  `model:` values verified against the live docs; `adapters/codex/README.md`; `git mv`
  originals → `legacy/` with reasons appended below; README rewrite.
  → `phase-4: role restructure`.
- **Phase 5**: routing table appended to SCIENTIFIC_RULES; `docs/memory-setup.md`;
  `core/roles/memory-curator.md` + skill wrapper. → `phase-5: memory policy`.
- **Phase 6**: `eval/RUBRIC.md` (weights 20/30/20/20/10, anchors 1–5, freeze clause),
  `PROTOCOL.md` (A pure-model vs B ecosystem; blind grading), `RESULTS_TEMPLATE.md`,
  `tasks/T1–T5.md` with <consumer-project> path placeholders. → `phase-6: evaluation scaffold`.

## Legacy moves (Phase 4, 2026-09-04) — `git mv`, history preserved

| moved item | to | reason |
| --- | --- | --- |
| `skills/*/SKILL.md` (7 files) | `legacy/skills/` | Claude-skill bodies superseded by `core/roles/<role>.md` + generated `.claude/skills/<role>/SKILL.md` wrappers |
| `agents/*.md` (4 files) | `legacy/agents/` | Claude-subagent bodies superseded by `core/roles/<role>.md` + generated `.claude/agents/<role>.md` wrappers |
| `RESEARCH_TEAM.md` | `legacy/RESEARCH_TEAM.md` | roster contract superseded by `core/roles/README.md` (doctrine) + the generated adapters (mechanism table) |
| `README.md` (pre-migration text restored from `9775931`) | `legacy/README.md` | Claude Code install guide superseded by the new root README |
| `docs/customization.md` | `legacy/docs/customization.md` | `<placeholder>` fill-in guide for copied `.claude/` files superseded by `templates/project-state/README.md` + the overlay slots in each role spec |

Kept in place (still valid): `docs/design-notes.md` (memory-wins paragraph
annotated as superseded by DECISION_001), `docs/creating-skills-with-tdd.md`,
`templates/*`, `assets/*.svg` (labeled the Claude Code runtime view), `LICENSE`.
