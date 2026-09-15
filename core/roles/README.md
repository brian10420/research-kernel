# Roles — the canonical, provider-neutral roster

Every role is one file in this directory: purpose, input contract, output
contract, hard rules, and a `runtime:` block (a recommendation, never a vendor
requirement). Vendor runtimes load these specs through generated wrappers; the
spec text is the authority, the wrapper is a pointer.

## The roster

| role | posture | what it is for | never does |
| --- | --- | --- | --- |
| [`math-reviewer`](math-reviewer.md) | shared-context | verify math, shapes, derivations, signal math, numerics | implement |
| [`dl-engineer`](dl-engineer.md) | shared-context | write and reactively debug model / training / pipeline code | self-certify |
| [`research-mentor`](research-mentor.md) | shared-context | direction, pressure-testing, concepts; literature-verified claims | assert its own ideas as facts |
| [`results-analyst`](results-analyst.md) | shared-context | publication-grade statistics, tables, figures; ledger metric blocks | massage a number |
| [`paper-writer`](paper-writer.md) | shared-context | discuss, revise, compile the manuscript | invent a number; re-inflate a downgraded claim |
| [`study-coach`](study-coach.md) | shared-context | teach the operator their own project; persistent Study Log | verify, build, or present |
| [`science-presenter`](science-presenter.md) | shared-context | audience-facing decks, posters, one-pagers | compute a new statistic; skip the brief |
| [`blind-reviewer`](blind-reviewer.md) | **isolated** | memoryless peer-review panel on an anonymized bundle | accept project context |
| [`experiment-runner`](experiment-runner.md) | **isolated** | launch and babysit runs; protocol verbatim; ledger rows | cherry-pick; deviate from protocol |
| [`regression-guardian`](regression-guardian.md) | **isolated** | the silent-bug gate; whole suite; writes missing tests | fix code; certify from a partial run |
| [`repo-maintainer`](repo-maintainer.md) | **isolated** | git/GitHub with the never-push list | push protected content; forced push unasked |
| [`memory-curator`](memory-curator.md) | shared-context | janitor for the recall layer: route facts, audit memory against git, propose session-end distillation | gatekeep; edit `core/`; commit a scientific claim |

**Posture** is the load-bearing design decision. *Shared-context* roles join
the operator's session and see everything — discussion, design, revision,
teaching. *Isolated* roles get a fresh context, see only their dispatch prompt
and its inputs, and return one report — review-of-record, certification,
mechanical operations. Choose by asking: does this role's value come from
sharing the operator's context, or from NOT sharing it?

## Boundaries that matter (why these are separate)

- **`math-reviewer` vs `blind-reviewer`:** one checks math correctness with full
  context; the other is a blind peer reviewer that sees only the anonymized
  manuscript.
- **`dl-engineer` vs `regression-guardian`:** the author cannot self-certify
  silent correctness — the blind spot that created a bug is the one that would
  certify it.
- **`experiment-runner` vs `results-analyst`:** one runs (ops, GPU, long
  processes); the other analyzes (statistics, publication figures).
- **`research-mentor` vs `paper-writer`:** one discusses the research
  (direction, concepts, "should we claim X", literature); the other discusses
  and edits the manuscript.
- **`study-coach` vs `math-reviewer`:** one teaches established material; the
  other verifies new math at the rigor bar.
- **`science-presenter` vs `results-analyst`:** one makes audience visuals; the
  other makes publication figures and every new number.
- **`science-presenter` vs `study-coach`:** one builds what the operator shows;
  the other preps the operator. Defense prep: presenter makes the deck and
  backup-math slides, coach runs the rehearsal.

## Hard rules baked into the team

- **The author never certifies their own work**, and the reviewer-of-record
  never shares the author's context.
- **`blind-reviewer` receives only an anonymized bundle** (`tools/anonymize.py`)
  and declines anything else.
- **`repo-maintainer` enforces the never-push list** by staging check before
  every push.
- **Role specs carry no volatile project facts** (DECISION_001). Facts live in
  the project's `RESEARCH_STATE.md` and `EXPERIMENT_LEDGER.md`, read at session
  start.
- **Every role's first rule is the canary handshake** (SCIENTIFIC_RULES §3):
  echo `ACK RULES_HASH=<hash>` first, or halt.
- **One dispatch = one complete report** for isolated roles.

## Runtime routing doctrine

A team optimized *by* a frontier model must never *require* one. Reasoning-heavy
roles (`math-reviewer`, `blind-reviewer`, `regression-guardian`) recommend
`inherit` — run them from the strongest session the plan affords — at high
effort. Mechanical roles (`experiment-runner`, `repo-maintainer`,
`memory-curator`) recommend a smaller model at medium effort. Nothing here pins a
paid tier or a vendor; the `runtime:` block in each spec is a recommendation.

What Claude Code actually *enforces* is `core/effort_policy.yaml`: the roles
listed there get `effort:` / `model:` in their generated wrapper (closed
verification at `xhigh`, mechanical roles at `low` on a smaller model); everyone
else inherits the session. Effort is chosen by task shape up front, never by
"it got stuck"; no role pins `max` — the operator raises the session effort for
an unbounded-judgement step and lowers it again (DECISION_003).

## Typical flows

**Code / experiment:** discuss (`research-mentor`) → verify theory
(`math-reviewer`) → implement (`dl-engineer`) → **gate** (`regression-guardian`)
→ run (`experiment-runner`) → analyze (`results-analyst`) → commit
(`repo-maintainer`).

**Paper:** discuss research (`research-mentor`) → pull numbers/figures
(`results-analyst`) → write/revise + compile (`paper-writer`) → verify equations
(`math-reviewer`) → anonymize (`tools/anonymize.py`) → independent critique
(`blind-reviewer`) → revise again (`paper-writer`) → commit (`repo-maintainer`).

**Present:** verified numbers/figures (`results-analyst`) → brief + pre-flight
scan + build (`science-presenter`) → for a defense, rehearse (`study-coach`).

**Learn:** read the Study Log → one topic in three layers → quiz → update the log
(`study-coach`).
