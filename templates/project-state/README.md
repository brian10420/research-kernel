# Project-state templates

**Two layers, two homes.** Cross-project rules and roles live in the
`research-os` repository (`core/SCIENTIFIC_RULES.md`, `core/roles/`). Per-project
state lives in each research project's own repository, in the six files
below, seeded from these templates. A project never edits `core/`; `core/`
never contains a project's facts.

## Install into a project

```bash
# from the root of your research project
mkdir -p project-state
cp <research-os>/templates/project-state/{RESEARCH_STATE,DECISIONS,EXPERIMENT_LEDGER,HYPOTHESES,FAILED_IDEAS,OPEN_QUESTIONS}.md project-state/
```

Then, in the project:
1. Fill `RESEARCH_STATE.md` with the first dated snapshot (active tracks, frozen
   items, deadlines or "none", guards). This is what every session reads first.
2. Record the adoption as `DECISION_000` in the project's `DECISIONS.md`
   (proposer, date, decided_by: human, status: accepted).
3. Point the roles at these files through the project's overlay (see the
   "Project overlay slots" section at the end of each `core/roles/<role>.md`).

## The files

| file | holds | schema source |
| --- | --- | --- |
| `RESEARCH_STATE.md` | the dated snapshot a session reads first | `core/RESEARCH_STATE.md` |
| `DECISIONS.md` | design decisions with provenance and rationale | `core/DECISIONS.md` |
| `EXPERIMENT_LEDGER.md` | every run ever launched; append-only | `core/EXPERIMENT_LEDGER.md` |
| `HYPOTHESES.md` | unvalidated ideas, any proposer, with provenance | `core/HYPOTHESES.md` |
| `FAILED_IDEAS.md` | negative results with evidence and retry conditions | `core/FAILED_IDEAS.md` |
| `OPEN_QUESTIONS.md` | what is unanswered and what would answer it | `core/OPEN_QUESTIONS.md` |

`STUDY_LOG.md` and `LITERATURE_MAP.md` are cross-project schemas in `core/`; a
project's live Study Log usually sits in its notes vault
(`templates/STUDY_LOG_TEMPLATE.md`), and a project may add a `LITERATURE_MAP.md`
alongside the six files when it needs one.

## Rules that travel with the templates

- Provenance on every entry (`SCIENTIFIC_RULES.md` §2); only a human moves an
  entry to `accepted` or `rejected`.
- Append-only; supersede, never rewrite.
- Failed runs and refuted ideas are kept, never deleted.
- Model-originated ideas enter `HYPOTHESES.md` as `proposed`, nowhere else.
