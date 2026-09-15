# research-kernel

> Built on the provider-neutral **research-os** architecture; internal schemas keep the `research-os/` namespace.

**A provider-neutral Research OS: the research methodology and its decision
history are the canonical asset; every AI vendor is a replaceable runtime
reached through generated adapters.** MIT-licensed. Formerly
`claude_research_team` (a Claude Code skill collection); the GitHub rename to
`research-kernel` is pending — see [`MIGRATION_AUDIT.md`](MIGRATION_AUDIT.md).

## Install in 30 seconds (Claude Code plugin)

```
/plugin marketplace add brian10420/claude_research_team   # becomes brian10420/research-kernel after the rename
/plugin install research-kernel@research-kernel
/reload-plugins
```

The twelve roles then appear namespaced as `/research-kernel:<role>` (skills)
and as dispatchable subagents. Add your project's facts in **one file the
plugin never touches**:

```bash
cp <plugin-cache>/templates/research-kernel.overlay.template.md .claude/research-kernel.overlay.md
# or fetch the template from this repository; then fill the slots
```

Every skill injects `.claude/research-kernel.overlay.md` when it loads; isolated
roles receive it through the dispatch prompt. Nothing inside the plugin is ever
hand-edited — a plugin update replaces the whole tree, and your overlay survives.
Copy [`templates/project-state/`](templates/project-state/) into the project as
well (its README has the commands). The copy-install path is still supported —
see "Using it without the plugin" below.

## Two layers, two homes

| layer | lives in | contents |
| --- | --- | --- |
| **cross-project** | *this repository* | `core/SCIENTIFIC_RULES.md` (the constitution), `core/roles/` (canonical role specs), cross-project `core/DECISIONS.md`, schemas for every state file, the compile layer, the evaluation scaffold |
| **per-project** | *each research project's own repository* | `RESEARCH_STATE.md`, `DECISIONS.md`, `EXPERIMENT_LEDGER.md`, `HYPOTHESES.md`, `FAILED_IDEAS.md`, `OPEN_QUESTIONS.md`, seeded from [`templates/project-state/`](templates/project-state/) |

Model memory (any vendor) is a recall layer, never an authority layer. Git,
the notes vault, and the experiment ledgers are the only scientific source of
truth (`core/SCIENTIFIC_RULES.md` §0–§1).

## Layout

```
core/                     canonical, provider-neutral — edit HERE
  SCIENTIFIC_RULES.md     rules; RULES_HASH = sha256(this file)[:12]
  DECISIONS.md            DECISION_000 (architecture), DECISION_001 (memory is recall-only)
  RESEARCH_STATE.md  EXPERIMENT_LEDGER.md  HYPOTHESES.md  FAILED_IDEAS.md
  LITERATURE_MAP.md  OPEN_QUESTIONS.md  STUDY_LOG.md      (schemas + one worked example each)
  roles/                  one spec per role + README roster
  effort_policy.yaml      which roles carry an enforced Claude Code effort/model (task-shape doctrine)
CLAUDE.md  AGENTS.md      GENERATED adapters (tools/sync.py) — never hand-edit
.claude/agents/ .claude/skills/   GENERATED self-contained wrappers for Claude Code (spec + rules next to each SKILL.md)
skills/  agents/          symlinks to .claude/ so the repository is itself the plugin
.claude-plugin/           plugin.json + marketplace.json (this repository is its own marketplace)
adapters/codex/           placeholder: AGENTS.md + core/roles are the Codex sources
tools/                    sync.py · check_drift.py · anonymize.py
.githooks/pre-commit      refuses commits whose adapters disagree with core/
templates/project-state/  per-project state files to copy into a research repo
templates/                Study Log, Presentation Log, session handoff, leak-check pattern, project overlay
eval/                     pre-registered rubric, blind protocol, task stubs, sealed label maps
docs/                     design notes, hardening options, memory setup, skill-building process
legacy/                   the pre-migration Claude-specific originals (not loaded by anything)
```

## The roles

Twelve canonical roles in [`core/roles/`](core/roles/README.md): eight
*shared-context* roles that work inside your session (`math-reviewer`,
`dl-engineer`, `research-mentor`, `results-analyst`, `paper-writer`,
`study-coach`, `science-presenter`, `memory-curator`) and four *isolated* roles dispatched with a
fresh context (`blind-reviewer`, `experiment-runner`, `regression-guardian`,
`repo-maintainer`). Every spec has a purpose, an input contract, an output
contract, hard rules (rule 0 is always the canary handshake), and a `runtime:`
recommendation that never pins a vendor or a paid tier.

The diagrams in [`assets/`](assets/) show the **Claude Code runtime view** of
the same team (skills inside the session, subagents behind a context boundary,
the guardian as the only gate); they predate the migration and remain accurate
for that runtime.

## Canary handshake (why agents cannot silently lose the rules)

Subagents may not inherit instruction files. So: any orchestrator that spawns a
role **pastes the full `core/roles/<role>.md` text and the line
`RULES_HASH=<hash>` into the task prompt**; the role's first output line must be
`ACK RULES_HASH=<hash>`, otherwise it halts and reports; `regression-guardian`
rejects any run log without a valid ACK and records the rejection in the
ledger. Details: `core/SCIENTIFIC_RULES.md` §3; optional mechanical enforcement:
[`docs/hardening.md`](docs/hardening.md).

## Compile layer

`CLAUDE.md`, `AGENTS.md`, and the `.claude/` wrappers are generated from `core/`
and carry the current `RULES_HASH`. Never edit them by hand.

```bash
python3 tools/sync.py                 # regenerate every adapter
python3 tools/check_drift.py          # exit 1 if any adapter disagrees with core/
git config core.hooksPath .githooks   # once per clone: pre-commit refuses stale adapters
```

## Using it without the plugin

1. Copy [`templates/project-state/`](templates/project-state/) into the
   project (its README has the exact commands) and write the first
   `RESEARCH_STATE.md` snapshot.
2. For Claude Code: copy `CLAUDE.md` and `.claude/` from here (or generate them
   in place with `tools/sync.py`). The wrappers are self-contained — each skill
   directory carries `role.md` and `RULES.md` — so `core/` does **not** need to
   be reachable from the project root.
3. Seed the overlay: copy `templates/research-kernel.overlay.template.md` to
   `.claude/research-kernel.overlay.md` and fill the slots listed at the end
   of every role spec (paths, protocol block, invariants, guards). Project
   facts go there and in the state files, never into `core/`.
4. For any other harness: `AGENTS.md` + `core/roles/` are the sources
   (`adapters/codex/README.md`).
5. Optional agent memory for environment quirks only: [`docs/memory-setup.md`](docs/memory-setup.md).

## Effort policy (Claude Code)

`core/effort_policy.yaml` decides which wrappers carry an enforced `effort:` /
`model:` (Claude Code honours these for skills and subagents; effort cannot be
passed at dispatch time, and `model: inherit` does not inherit effort). The
doctrine is *task shape decides, up front*:

| task shape | setting | why |
| --- | --- | --- |
| closed, single-answer verification (`math-reviewer`, `blind-reviewer`) | `xhigh` | the curve saturates here; `max` buys about one point for ~40 % more tokens |
| mechanical operations (`experiment-runner`, `repo-maintainer`) | smaller model, `low` | never needs frontier reasoning |
| everything else | inherits the session | authoring, analysis and dialogue happen at the operator's default |
| long-horizon work with a signed plan | session default | verification comes from the plan, the pre-registration and the regression gate — not from effort |

No role pins `max`. For an unbounded-judgement step (interpreting a blind
readout, resolving a record-vs-code contradiction, designing a new statistical
instrument) the role asks the operator to run `/effort max` and to lower it
again afterwards. "Stuck" is a reason to change method — restate the claim as a
checkable test, dispatch a fresh-context role — not to raise effort.

## Blind review and evaluation

`tools/anonymize.py build` strips provenance, names, model names, e-mails, and
timestamps from a review bundle and seals the label map in `eval/.sealed/`
(git-ignored; reviewers never read it). `eval/RUBRIC.md` is pre-registered;
`eval/PROTOCOL.md` defines the two comparisons (pure-model vs ecosystem) that
are reported separately and graded blind.

## How the roles were built

Process documentation lies unless tested. The role files were written
RED→GREEN against observed baseline failures —
[`docs/creating-skills-with-tdd.md`](docs/creating-skills-with-tdd.md). Design
rationale (context posture, independence, why memory is recall-only):
[`docs/design-notes.md`](docs/design-notes.md).

## Companion third-party skills (not vendored — install from upstream)

- [mattpocock/skills](https://github.com/mattpocock/skills) — `tdd`, `diagnose`,
  `grill-me`, `grill-with-docs`, `caveman`, `prototype`, `zoom-out`, `to-prd`,
  `to-issues`
- [vercel-labs/skills](https://github.com/vercel-labs/skills) — the skills CLI
  and `find-skills`
- [Anthropic superpowers plugin](https://github.com/anthropics/claude-code) —
  `writing-skills` powered the TDD process above

None of their code is copied here; all attribution and licensing remain theirs.

## What was removed (honesty note)

The role content was distilled from a working configuration of an active,
unpublished ML research project. Every metric value, dataset specific, campaign
name, file inventory, and personal detail is a placeholder or an invented
generic example; the structure and doctrine are real and battle-tested.

## License

MIT © [Ting-Yi Lin](https://github.com/brian10420)
