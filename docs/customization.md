# Customization guide

## Fill-in pass (do this once after installing)

Every project-specific slot is marked one of two ways:

1. `<angle-bracket-placeholders>` — single values (paths, margins, targets).
2. `<!-- PROJECT-SPECIFIC: … -->` — fenced blocks you replace wholesale.

Find them all:

```bash
grep -rn "PROJECT-SPECIFIC\|<[a-z-]*-\(path\|target\|language\|dir\)>" skills/ agents/ RESEARCH_TEAM.md
```

Per file, the load-bearing fills:

| File | What you must fill |
|---|---|
| `RESEARCH_TEAM.md` | nothing required — adjust roles/model pins to taste |
| `skills/research-mentor` | ground-truth snapshot (dated), stance resources |
| `skills/math-reviewer` | your pinned invariants, domain signal math |
| `skills/dl-engineer` | AMP policy location, architecture contracts, active surfaces |
| `skills/results-analyst` | analysis-script inventory, TOST margin, collection rule |
| `skills/paper-writer` | paper tree, locked story, guardrails, headline numbers, tracks |
| `skills/study-coach` | learner profile, `<study-log-path>` (seed from `templates/STUDY_LOG_TEMPLATE.md`) |
| `skills/science-presenter` | language policy, source table (numbers/figures/story pointers), guard list, `<deck-source-dir>`, `<presentation-log-path>` (seed from `templates/PRESENTATION_LOG_TEMPLATE.md`) |
| `agents/blind-reviewer` | venue list, domain, field-specific scrutiny list |
| `agents/experiment-runner` | run commands, protocol block (verbatim), collection source |
| `agents/regression-guardian` | test runner, guard-suite list, invariant table |
| `agents/repo-maintainer` | remote, the never-push list and its gitignore layering |

Also set each agent's `model:` and `tools:` frontmatter to match your plan and
comfort level.

## The two-track publishing pattern (how this repo itself is maintained)

If your filled-in versions contain unpublished research or private details,
run two tracks:

- **Private track (canonical):** the filled-in files live in your project's
  `.claude/`, version-controlled in your PRIVATE repo.
- **Public track (derived):** a scrubbed copy in a public repo. Values →
  placeholders; project facts → invented generic examples (never thin renames
  of real names); no PII, no internal dates, no embargo notes.

Rules that keep this safe:

1. **Never build an automatic scrubber.** Porting private → public is manual
   diff-review, hunk by hunk: doctrine ports, project-state doesn't.
2. **Keep a leak-check script in the PRIVATE repo** (the deny-list itself
   names your secrets — it can never be public; `templates/leakcheck.template.sh`
   shows the shape). Run it on the public tree before every push, and eyeball
   every allowlisted line.
3. **Keep a provenance manifest** (private source → public path + content hash
   at last sync) so staleness is detectable, and put a visible "Last synced"
   date in the public README so rot is observable from outside.
4. Sync on doctrine changes or quarterly, whichever comes first.
