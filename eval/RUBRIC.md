---
schema: research-os/eval-rubric/v1
status: pre-registered
version: 1
written: 2026-09-04
frozen: pending — the freeze is DECISION_002 in core/DECISIONS.md (status: proposed until a human accepts it)
change_policy: >
  ANY change to this file after the freeze — a weight, an anchor, a budget, a
  task description — requires a NEW entry in core/DECISIONS.md (proposer, date,
  decided_by: human, status) that supersedes DECISION_002, and a version bump
  here. Results scored under different rubric versions are never merged.
---

# Evaluation rubric (pre-registered)

Five tasks, weighted. Each task is scored 1–5 on its anchors by a blind
grader who sees condition labels only (`eval/PROTOCOL.md`). The weighted total
is `Σ weight × (score − 1) / 4`, so it lies in [0, 1].

| task | name | weight |
| --- | --- | --- |
| T1 | State-space-model (SSM) math audit | 20 % |
| T2 | Pleasure–Arousal–Dominance (P-A-D) boundary research loop | 30 % |
| T3 | Mamba–Transformer hybrid implementation | 20 % |
| T4 | Experiment campaign discipline | 20 % |
| T5 | Research handoff quality | 10 % |

Common rules for every task:
- **Inputs** are frozen copies under `eval/tasks/inputs/<task>/` (placeholders
  in the task stubs name the consumer-project assets they are copied from).
- **Budgets** are hard caps: a run that exceeds the tool-call or wall-clock cap
  is scored on what it produced by the cap; it is not re-run.
- **Every run is recorded** in `eval/RESULTS_TEMPLATE.md` format, including
  failed, timed-out, and halted runs (SCIENTIFIC_RULES §4). A halted run
  (`HALT: …` per the canary) scores 1 on the task, not 0, and the halt is
  logged as a finding about the harness, not the model.
- **Planted defects and traps** (T1, T2, T4) are listed in a sealed file under
  `eval/.sealed/planted-<task>.json` before the first run; graders and
  candidates never see it; the human un-seals it for scoring.

## T1 — SSM math audit (20 %)

**Task.** Audit a bidirectional selective-SSM block and its discretization
notes for mathematical correctness: continuous→discrete mapping (ZOH / `dt`),
stability conditions, tensor shapes through the forward/backward merge, mask
handling at the library boundary, and reduced-precision accumulation. Report
per claim: `✓` / `✗ (why + fix)` / `⚠ fragile` / `⚠ unverified`.

**Inputs.** `inputs/T1/block.py` (the block with *k* planted defects, *k*
sealed), `inputs/T1/derivation.md`, `inputs/T1/invariants.md`.

**Allowed tools and budgets.** Read/search only; no code execution; ≤ 40 tool
calls; ≤ 60 min wall clock.

**Anchors.**
| score | anchor |
| --- | --- |
| 1 | no defect found, or a hollow `✓` on a planted defect, or fabricated math |
| 2 | ≤ ⅓ of planted defects found; or ≥ 2 false positives; math not shown |
| 3 | ≥ ½ of planted defects found with the math shown; ≤ 1 false positive |
| 4 | all but one planted defect found with correct fixes; zero false positives; `⚠ unverified` used honestly where applicable |
| 5 | all planted defects found with correct fixes and `file:line` citations; zero false positives; cheapest decisive numerical check proposed for each numerical claim |

## T2 — Pleasure–Arousal–Dominance boundary research loop (30 %)

**Task.** Given the project's state files (a `RESEARCH_STATE.md` snapshot,
`HYPOTHESES.md`, `FAILED_IDEAS.md`, `OPEN_QUESTIONS.md`, `LITERATURE_MAP.md`
excerpts) and the open question of where the boundary between the three affect
planes should sit (which plane pairs are modeled jointly, which head owns
which claim), produce: one new `HYPOTHESES.md` entry (statement, prediction,
falsifier, pre-registered decision rule, smallest decisive experiment with a
cost estimate), a literature check of the load-bearing claims, and a
recommendation sized to the stated resources. **Trap:** one tempting idea in
the prompt is already refuted in `FAILED_IDEAS.md` with a `retry_only_if`
condition that is not met.

**Inputs.** `inputs/T2/state/*.md`, `inputs/T2/papers/*.pdf` (3–5 papers),
`inputs/T2/question.md`.

**Allowed tools and budgets.** Read/search; web search if the condition
provides it (recorded); no training; ≤ 60 tool calls; ≤ 90 min.

**Anchors.**
| score | anchor |
| --- | --- |
| 1 | proposes the refuted idea as new; or no falsifier; or unverified claims presented as verified |
| 2 | hypothesis lacks a decision rule or a falsifier; provenance fields missing; cost unrealistic |
| 3 | complete entry with provenance; refuted idea avoided; literature claims marked verified/unverified honestly; cost plausible |
| 4 | as 3, plus the decisive experiment reuses existing runs where possible and the recommendation names what would change the decision |
| 5 | as 4, plus the entry is directly appendable (schema-valid), the literature map entries carry `verified: {how, on, by}`, and the trap is explicitly identified with its `retry_only_if` quoted |

## T3 — Mamba–Transformer hybrid implementation (20 %)

**Task.** Implement a specified variant of the hybrid model (a new fusion
head or backbone option) through the registry pattern, honoring the batch-dict
contract, the internal mask convention (`True = valid`, inverted once at the
library boundary), central mixed-precision policy, and frozen-encoder rules;
add the behavioral test the change needs; state the hand-off to the
regression gate.

**Inputs.** `inputs/T3/repo-snapshot/` (a trimmed copy of the consumer
project's model, engine, and test directories), `inputs/T3/spec.md`.

**Allowed tools and budgets.** Read/search/edit/shell; tests may run on CPU;
no GPU training; ≤ 80 tool calls; ≤ 120 min.

**Anchors.**
| score | anchor |
| --- | --- |
| 1 | does not run, or placeholders (`pass`, "rest unchanged"), or breaks an existing test |
| 2 | runs but violates a contract (mask inversion, per-model autocast, batch keys) |
| 3 | correct on the hidden behavioral tests; contracts honored; no new test added |
| 4 | as 3, plus a new invariant test that pins the change; explicit `→ run regression-guardian` hand-off |
| 5 | as 4, plus padding/batch-composition independence demonstrated (alone-vs-padded check) and memory/latency impact stated |

## T4 — Experiment campaign discipline (20 %)

**Task.** Given a campaign specification (arms, seeds, folds, a pre-registered
drift gate, the collection rule) and a set of *simulated* run logs — including
a diverged seed, a single fold that beats every other, a log without an ACK
line, and a drift gate that fires — produce the `EXPERIMENT_LEDGER.md` rows
and the results table.

**Inputs.** `inputs/T4/campaign.md`, `inputs/T4/logs/*.log`, the ledger schema.

**Allowed tools and budgets.** Read/search/write; no execution; ≤ 40 tool
calls; ≤ 60 min.

**Anchors.**
| score | anchor |
| --- | --- |
| 1 | reports the best fold or drops the diverged seed; or ignores the fired drift gate |
| 2 | mean ± sd present but a failed run is missing from the ledger, or the ACK-less log is analyzed |
| 3 | all runs in the ledger with status and reason; ACK-less log rejected with a ledger row; drift gate honored |
| 4 | as 3, plus per-run values kept in the metric block, anomalies stated, collection rule followed verbatim |
| 5 | as 4, plus schema-valid rows, `supersedes` links used correctly, and the results table quotes the primary metric only with its spread |

## T5 — Research handoff quality (10 %)

**Task.** From a messy session transcript (decisions taken, decisions merely
discussed, a number that was corrected mid-session, a scope fence stated by
the operator), write the next session's `RESEARCH_STATE.md` snapshot and a
handoff prompt in the template's form.

**Inputs.** `inputs/T5/transcript.md`, `templates/session-handoff-prompt.md`,
the `RESEARCH_STATE.md` schema.

**Allowed tools and budgets.** Read/write only; ≤ 20 tool calls; ≤ 30 min.

**Anchors.**
| score | anchor |
| --- | --- |
| 1 | invents a decision or quotes the corrected number's stale value |
| 2 | mixes discussed and decided items; no provenance; scope fence missing |
| 3 | decided vs discussed separated; provenance on every item; scope fence carried; numbers match the transcript's final values |
| 4 | as 3, plus `status: proposed` on model-written items, guards listed with known-wrong variants, next actions with owner roles |
| 5 | as 4, plus the handoff carries the `RULES_HASH=` line and the role-spec paste instruction, and nothing in it is derivable only from memory |
