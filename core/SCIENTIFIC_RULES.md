---
schema: research-os/scientific-rules/v1
status: canonical
owner: human (repository owner)
last_changed: 2026-09-04
change_policy: >
  Any change to this file requires a DECISIONS.md entry (status: accepted,
  decided_by: human). RULES_HASH — the first 12 hex characters of
  sha256(bytes of this file) — changes with every edit; tools/sync.py regenerates
  the adapters (CLAUDE.md, AGENTS.md) and tools/check_drift.py blocks commits that
  leave them stale.
---

# Scientific Rules (canonical)

This file is the constitution of the Research OS. Role specs, adapters, and
project state derive from it or are subordinate to it. Blocks fenced by
`<!-- adapter:include -->` … `<!-- /adapter:include -->` are copied verbatim into
the generated adapters by `tools/sync.py`; everything else is read here.

## 0. Precedence — where truth lives

<!-- adapter:include -->
| layer | file(s) | precedence |
| --- | --- | --- |
| methodological rules | `core/SCIENTIFIC_RULES.md` | 1 (highest) |
| design decisions + rationale | `DECISIONS.md` (cross-project: `core/`; per-project: the project repo) | 2 |
| recorded state | `EXPERIMENT_LEDGER.md`, `RESEARCH_STATE.md`, `HYPOTHESES.md`, `FAILED_IDEAS.md`, `LITERATURE_MAP.md`, `OPEN_QUESTIONS.md`, `STUDY_LOG.md` | 3 |
| role specifications | `core/roles/<role>.md` | 4 (bound by 1–3) |
| generated adapters | `CLAUDE.md`, `AGENTS.md` (never hand-edited) | 5 (derived views) |
| model memory (any vendor) | agent memory stores | recall only — never authority |

When two layers disagree, the higher layer wins and the disagreement is recorded:
as a `DECISIONS.md` entry if the rule itself is wrong, as a memory-curator
proposal (`memory_forget`) if the memory is wrong. Nothing is fixed silently.
<!-- /adapter:include -->

## 1. The seven principles

<!-- adapter:include -->
1. **Git + Obsidian + experiment records are the only scientific source of truth.**
   Model memory is a recall layer, never an authority layer.
2. **Every hypothesis or decision entry carries provenance:** proposer (`human` |
   `fable` | `astra` | `other-model:<name>`), date, status (`proposed` | `accepted` |
   `rejected` | `superseded`), and evidence links.
3. **Model-generated research ideas enter `HYPOTHESES.md` as `status: proposed`
   with model provenance.** They never enter durable memory or rules directly.
4. **Blind review:** a reviewer must never see the provenance or author identity of
   what it reviews. The orchestrator strips these before hand-off
   (`tools/anonymize.py`; label map sealed in `eval/.sealed/`, which reviewers
   never read).
5. **Canary handshake:** agents must prove they actually loaded the rules
   (section 3). Silent instruction loss must become loud failure.
6. **No cherry-picking:** seeds, runs, and metrics are reported per the ledger
   schema (section 4). Failed runs are recorded, never deleted.
7. **Distill, don't dump:** knowledge moves between layers as reviewed diffs,
   never as bulk transcript imports.
<!-- /adapter:include -->

## 2. Provenance schema (every entry in every state file)

Every entry in `DECISIONS.md`, `HYPOTHESES.md`, `FAILED_IDEAS.md`,
`OPEN_QUESTIONS.md`, `LITERATURE_MAP.md`, and every run in
`EXPERIMENT_LEDGER.md` opens with this YAML block:

```yaml
id: <PREFIX>_<NNN>            # DECISION_ / H_ / F_ / Q_ / L_ / RUN_
title: <one line>
date: YYYY-MM-DD              # the day the entry was written
proposer: human | fable | astra | other-model:<name>
status: proposed | accepted | rejected | superseded
decided_by: human | ""        # only a human moves an entry to accepted/rejected
evidence: [<path-or-url>, …]  # git paths, ledger run ids, DOIs; may be empty only while proposed
supersedes: <id> | ""
superseded_by: <id> | ""
```

Rules:
- `status` transitions are append-only: an entry is never rewritten to hide its
  history; a change of mind creates a new entry that `supersedes` the old one.
- `decided_by` is always a human for `accepted` and `rejected`. A model may
  propose, argue, and draft; it may not decide.
- An entry with `proposer` ≠ `human` must state which model produced it, so a
  reviewer can weigh model-originated ideas separately (principle 3).

## 3. Canary handshake protocol

<!-- adapter:include -->
Known failure mode: a spawned agent may not inherit the orchestrator's
instruction files or its own role body. The handshake makes that loss loud.

1. **Embedding.** Any orchestrator spawning a subagent MUST place inside the task
   prompt itself (a) the full canonical role spec text from `core/roles/<role>.md`
   and (b) the literal line `RULES_HASH=<hash>`, where `<hash>` is the current
   RULES_HASH from the adapter header.
2. **Acknowledgement.** Every role's first rule (rule 0 in every
   `core/roles/<role>.md`): the first output line must be
   `ACK RULES_HASH=<hash>`, echoing the hash it was given. If no `RULES_HASH=`
   line is present in the prompt or loader, the role halts, outputs
   `HALT: RULES_HASH missing — rules not loaded`, and reports instead of
   working. A role cannot derive the correct hash itself; validity — equality
   with the RULES_HASH of the rules in force at launch, as recorded in the
   adapter header at that revision — is checked by the orchestrator on receipt
   and by `regression-guardian` on every run log. A generated wrapper that
   carries the current hash additionally halts on a mismatching prompt hash
   (`HALT: stale RULES_HASH`).
3. **Enforcement at the record.** `regression-guardian` rejects any experiment or
   run log that lacks a valid ACK line — missing, malformed, or stale — and
   records the rejection in `EXPERIMENT_LEDGER.md` (`status: rejected`,
   `reason: missing_ack` or `stale_ack`). No metric from a rejected log is
   analyzed or reported; the rejection row is never deleted.
4. **Shared-context roles too.** When a role is loaded into a live session (a
   skill wrapper), the wrapper passes the hash and the role echoes the ACK line at
   the start of its first response.
<!-- /adapter:include -->

## 4. Reporting rules (no cherry-picking)

<!-- adapter:include -->
- Every run that starts gets a ledger row before its metrics exist
  (`status: planned` → `running` → `complete` | `failed` | `aborted` | `rejected`).
- All seeds and all folds of a protocol are reported; the result is the mean ±
  sample standard deviation across them, with the per-seed / per-fold values kept
  in the row. A single best seed or fold is never "the result".
- Failed, diverged, and aborted runs stay in the ledger with their reason. Rows
  are never deleted; a wrong row is superseded by a new one.
- Equivalence or "parity" claims require a formal test with a pre-registered
  margin; "by construction" is not evidence.
- Decisive runs are pre-registered: the hypothesis, the decision rule, and the
  stopping rule are written into `HYPOTHESES.md` (and the project's pre-registration
  docs) before the run launches.
- Checkpoint selection and early stopping use validation data only; the held-out
  test split is read once, at the end.
- Every published number has exactly one committed script as its source of
  record; convenience summaries are never the source.
- Unflattering metrics (calibration, negative results) are reported as found.
<!-- /adapter:include -->

## 5. Knowledge routing table

<!-- adapter:include -->
| information | destination |
| --- | --- |
| environment quirks, commands, gotchas | agent memory (agentsmd-memory) / code docs |
| methodological rules (e.g. never cherry-pick seeds) | SCIENTIFIC_RULES.md |
| design decisions and rationale | DECISIONS.md |
| experiment results | EXPERIMENT_LEDGER.md |
| unvalidated ideas (any proposer) | HYPOTHESES.md, with provenance |
| model-speculated ideas | never directly into durable memory |

Agent memory (any backend, including a harness's own auto-memory) **may store:**
environment quirks and workarounds, commands and their flags, paths, tool and
harness gotchas, hardware limits, flaky-test notes, formatting preferences.
It **may not store:** methodological rules, design decisions or their
rationale, experiment results or metric values, hypotheses or ideas from any
proposer, anything a paper could cite, personal data beyond what a command
needs, secrets. When memory contradicts git, memory loses: the memory-curator
proposes `memory_forget`; nobody edits `core/` to match memory.
<!-- /adapter:include -->

## 6. Distillation rule

- Knowledge moves between layers (session → state file → rule; project → core)
  only as a **reviewed diff**: a proposed patch with provenance that a human
  accepts or rejects.
- Bulk transcript imports, pasted chat logs, and "summaries of everything" are
  not admissible as entries.
- Session-end distillation is the memory-curator's job (section 5 routing); it
  proposes, a human commits.

## 7. Blind review

- The reviewer-of-record (`blind-reviewer`) receives only an anonymized bundle:
  provenance fields, author names, model names, and timestamps stripped by
  `tools/anonymize.py`. The label mapping is written to `eval/.sealed/`; no
  reviewer role reads that directory.
- A reviewer that is offered project context, decision history, or "what we
  meant" declines it.
- Evaluation grading (see `eval/PROTOCOL.md`) is blind in the same way: the grader
  sees condition labels only.

## 8. Role discipline

- **The author never certifies their own work**, and the reviewer-of-record never
  shares the author's context.
- **One dispatch = one complete report.** Isolated roles return a self-sufficient
  report; the orchestrator answers follow-ups by reading it, not by re-dispatching.
- **Scope fences.** Every role names its neighbours and redirects out-of-scope
  requests in one line instead of absorbing them.
- **Know your limits.** A role that cannot verify something at the required rigor
  marks it `⚠ unverified` rather than emitting a hollow pass.
- **No paid-tier pins.** Role specs recommend a runtime posture (`inherit` for
  reasoning-heavy roles, a smaller model for mechanical roles); they never require
  a specific vendor or a paid tier.
