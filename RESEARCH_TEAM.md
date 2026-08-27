# Research Team — a role roster for ML research with Claude Code

A PhD-level division of labor, expressed as Claude Code configuration. Two
mechanisms with different context postures:

- **Skills** load into the *current* conversation — they collaborate and share
  full context. Invoke by mentioning the function or typing `/<name>`.
- **Subagents** run in their *own* context — dispatch-and-report, isolated.
  Dispatch via the Agent tool by name.

| # | Name | Kind | Model | Invoke when you want to… | Mechanism rationale |
|---|------|------|-------|--------------------------|---------------------|
| 1 | `math-reviewer` | Skill | session | verify math / tensor shapes / theory / derivations | collaborate, full context |
| 2 | `dl-engineer` | Skill | session | write or reactively debug model/training code | you're the author, share context |
| 3 | `research-mentor` | Skill | session | discuss direction, concepts; literature-verified | dialogue needs context |
| 4 | `blind-reviewer` | **Subagent** | inherit | an independent, venue-calibrated peer review | **must be memoryless** |
| 5 | `repo-maintainer` | **Subagent** | small/cheap | commit / push / git hygiene | dispatched mechanical task |
| 6 | `experiment-runner` | **Subagent** | small/cheap | launch training, run a campaign, collect results | long-running / background |
| 7 | `results-analyst` | Skill | session | stats, figures, tables from results | iterate on figures with you |
| 8 | `regression-guardian` | **Subagent** | inherit | certify a change didn't silently break correctness | **independence = the point** |
| 9 | `paper-writer` | Skill | session | discuss + revise manuscript prose + compile the PDF | content-revision lane = main session |
| 10 | `study-coach` | Skill | session | be TAUGHT: guided study of your own notes, reading recommendations, quizzes | teaching lane; persistent Study Log |

**Model routing (cheap-reality doctrine):** skills run in-session → they use
whatever model the session runs. A team like this may be *optimized by* a
frontier model, but it must never *require* one — pin nothing to a paid tier.
Reviewers-of-record (`blind-reviewer`, `regression-guardian`) use `inherit`:
dispatch them from the strongest session your plan affords. Mechanical ops
agents pin a small/cheap model — they never need more. Subagent discipline:
**one dispatch = one complete report** — don't re-dispatch for clarifications
the main session can answer by reading the report.

## Boundaries that matter (why these are separate roles)

- **`math-reviewer` vs `blind-reviewer`**: one checks *math correctness* with
  full context (collaborative); the other is a *blind peer reviewer* that sees
  only the manuscript. Different jobs, different context posture.
- **`dl-engineer` vs `regression-guardian`**: the author cannot self-certify
  silent correctness — the blind spot that wrote the bug also reviews it. The
  guardian is the independent gate. Historical silent bugs in the source
  project all passed the author's own smoke test; the behavioral regression
  suite is the real gate.
- **`experiment-runner` vs `results-analyst`**: one *runs* (ops, GPU,
  background); the other *analyzes* (statistics, publication figures).
  Different mindset, different mechanism.
- **`research-mentor` vs `paper-writer`**: one discusses the *research*
  (direction, concepts, "should we claim X"); the other discusses and executes
  the *manuscript* (phrasing, structure, LaTeX, compile). Same "let's talk"
  feel, different altitude.
- **`study-coach` vs `math-reviewer`**: the coach *teaches* established
  material (you learn); the reviewer *verifies* new material (the work is
  checked). The coach never certifies correctness and never builds.

## Two hard rules baked into the team

- **`repo-maintainer` enforces a project-defined never-push list** — paths that
  must not reach the remote (e.g., an in-review manuscript) — by a staging
  check before every push, not a blanket block. Finding protected content
  already on the remote is an incident: stop and report, never silently fix.
- **`blind-reviewer` is never given project memory or author intent** — its
  blindness is its value.

## Coexistence with installed plugins

When a plugin ships a role that overlaps one of yours (e.g., a research
pipeline or a paper-writing pipeline), resolve the trigger collision from YOUR
side: scope your skill to the in-context / this-repo lane and route the formal
pipeline use-case to the plugin explicitly in both descriptions. Don't edit the
plugin's descriptions — yours are the ones you control.

**Memory wins:** volatile project state lives in project memory (and whatever
ledger your project keeps) — when a role file and memory disagree, trust memory
and flag the drift. Subagents don't receive project memory by design; refresh
their baked facts in periodic sync passes.

## Typical flows

**Code/experiment:** discuss (`research-mentor`) → verify theory
(`math-reviewer`) → implement (`dl-engineer`) → **gate** (`regression-guardian`)
→ run (`experiment-runner`) → analyze (`results-analyst`) → commit
(`repo-maintainer`).

**Paper:** discuss research (`research-mentor`) → pull numbers/figures
(`results-analyst`) → write/revise + compile (`paper-writer`) → verify equations
(`math-reviewer`) → independent critique (`blind-reviewer`, PDF-only) → revise
again (`paper-writer`) → commit (`repo-maintainer`, never-push list enforced).

**Learning:** open a study session (`study-coach`) → it reads your Study Log →
teaches one topic from your own notes → quizzes you → updates the log.
