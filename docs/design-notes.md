# Design notes — why the team is shaped this way

## Skills vs subagents = context posture

The single most load-bearing design decision. A **skill** joins your current
conversation: it sees everything, collaborates, iterates with you. A
**subagent** gets a fresh context: it sees only its dispatch prompt and
reports back once. Choose by asking: *does this role's value come from sharing
my context, or from NOT sharing it?*

- Discussion, design, revision, teaching → skills (context helps).
- Review-of-record, certification, mechanical ops → subagents (independence
  or isolation helps).

## Independence as a design principle

Two roles are subagents *specifically* so they cannot inherit the main
session's assumptions:

- **`blind-reviewer`** simulates peer review. A reviewer who knows the
  authors' intent reviews the intent, not the artifact. Its prompt instructs
  it to *decline* project context if offered.
- **`regression-guardian`** certifies correctness. The author who wrote a bug
  carries the blind spot that produced it; letting the authoring context
  certify its own change re-applies the blind spot. The guardian runs the
  behavioral suite independently and is mandated to *write a missing test*
  when it finds an unguarded invariant.

The general rule: **the author never certifies their own work, and the
reviewer-of-record never shares the author's context.**

## Cheap-reality model routing

A team optimized *by* a frontier model must never *require* one. Skills
inherit the session's model. Reviewers-of-record use `inherit` so you can
dispatch them from the strongest session your plan affords. Mechanical ops
(git, campaign babysitting) pin a small model — they never need more. Each
role file carries "know your limits" language for weaker sessions (e.g., the
math reviewer marks `⚠ unverified — re-check in a stronger session` rather
than emitting a hollow ✓).

## Memory wins

> **Superseded on 2026-09-04 by `core/DECISIONS.md` DECISION_001.** Git,
> Obsidian, and the experiment ledgers are authoritative; model memory is
> recall-only; role specs carry no volatile facts (they live in the project's
> `RESEARCH_STATE.md` / `EXPERIMENT_LEDGER.md`). The paragraph below is kept
> as the historical rationale for the rule it replaced.

Role files bake in project facts so every session starts sharp — but facts
rot. Every file that carries facts opens its facts block with a date stamp and
the clause: *when this file and project memory disagree, trust memory and flag
the drift.* Subagents (which never see memory) get their baked facts refreshed
in periodic sync passes instead. This turns staleness from a correctness bug
into a visible, repairable condition.

## One dispatch = one complete report

Subagents are expensive to re-dispatch and lose their context when they
return. So their prompts demand a complete, self-sufficient report: depth over
length, every sentence a finding. The main session answers follow-ups by
*reading the report*, not by re-dispatching.

## Scope fences between roles

Every role names its neighbors and what belongs to them ("verifying new math
is math-reviewer, writing code is dl-engineer…"). This isn't bureaucracy: it's
what stops a teaching session from mutating code, a writing session from
inventing numbers, and a review from being contaminated by intent. The fences
are in the descriptions (so the right skill triggers) AND in the bodies (so a
loaded skill redirects instead of absorbing).
