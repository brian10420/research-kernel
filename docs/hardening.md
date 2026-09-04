# Hardening — optional hook-based enforcement (not implemented)

The canary handshake (`core/SCIENTIFIC_RULES.md` §3) is enforced today **at the
instruction layer**: every role's rule 0 demands `ACK RULES_HASH=<hash>` as its
first output line, every orchestrator must embed the full role spec and the
`RULES_HASH=` line in the task prompt, and `regression-guardian` rejects run logs
without a valid ACK. Instruction-layer enforcement fails loudly when an agent
*loads* the rules and honestly reports a missing hash; it cannot catch an
orchestrator that forgets to embed them and an agent that never notices.

This document lists the mechanical enforcement that would close that gap. None
of it is installed. Each item is a decision for the repository owner (recorded
in `DECISIONS.md` when taken).

## H1 — PreToolUse validation of subagent dispatches

**Mechanism.** Claude Code's `PreToolUse` hook receives the tool input as JSON on
stdin. A hook matched to the `Agent` tool can inspect `tool_input.prompt` and
block the dispatch (exit code 2, reason on stderr) unless the prompt contains:

- the literal line `RULES_HASH=<hash>` where `<hash>` equals the current
  `python3 tools/sync.py --hash`; and
- a recognizable copy of a canonical role spec (e.g. the spec's frontmatter
  `role:` line and its `## Hard rules` heading).

**Sketch** (`.claude/settings.json`, not installed):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Agent",
        "hooks": [{ "type": "command", "command": "python3 tools/hooks/validate_dispatch.py" }]
      }
    ]
  }
}
```

`validate_dispatch.py` would read stdin, compute the hash from
`core/SCIENTIFIC_RULES.md`, and exit 2 with a one-line reason when either
condition fails. Harness-neutral equivalents: any runtime with a pre-dispatch
hook or middleware can run the same script.

**Cost.** One process spawn per dispatch; a false block if a legitimate dispatch
uses a role outside `core/roles/` (add an allow-list of non-role dispatches such
as read-only exploration agents).

## H2 — PostToolUse ACK check on subagent output

A `PostToolUse` hook on the `Agent` tool could scan the returned text for the
`ACK RULES_HASH=` line and surface a warning (hooks cannot un-run a subagent, so
this is detection, not prevention). Combined with H1 it turns "silent
instruction loss" into a logged event at both ends of the dispatch.

## H3 — Ledger-row-before-launch check

A `PreToolUse` hook on `Bash` could refuse commands that match the project's
training-launch pattern unless an `EXPERIMENT_LEDGER.md` row with
`status: planned` and the run id given in the command exists. This enforces
SCIENTIFIC_RULES §4 ("a row exists before the metrics do") mechanically. It is
project-specific (the launch pattern and the ledger path belong to the project
overlay), so it would live in the project repository, not here.

## H4 — Write-guard for a project's `CLAUDE.md` (follow-up item, owner request 2026-09-04)

A consumer project keeps a hand-maintained `CLAUDE.md` that no agent
may edit. The ARS plugin's write-scope guard **deliberately does not cover
`CLAUDE.md`** (ARS issue #459), so today the only protection is a standing rule.
A dedicated `PreToolUse` hook matched to `Edit|Write|MultiEdit|NotebookEdit`
that exits 2 when `tool_input.file_path` resolves to that project's `CLAUDE.md`
would make the rule mechanical. Equivalent permission-rule form (already
verified live in the migration session as a session fence):

```json
{ "permissions": { "deny": ["Edit(//home/<user>/<project>/CLAUDE.md)"] } }
```

Note the known gap: `Edit(...)` deny rules do not cover shell-mediated writes
(`sed -i`, heredocs, `python -c`). Only a `Bash`-matched hook that parses the
command for the protected path closes that vector.

## H5 — Generated-adapter integrity at session start

A `SessionStart` hook could run `python3 tools/check_drift.py` and print a
warning when the adapters are stale, so a session never starts on a `CLAUDE.md`
that disagrees with `core/`. The pre-commit hook already prevents *committing*
stale adapters; this would catch an uncommitted edit to `core/`.

## Decision record

Taking any of H1–H5 is a `DECISIONS.md` entry (proposer, date, decided_by:
human, status). Until then, the instruction-layer protocol is the enforcement of
record, and the `regression-guardian` rejection row in the ledger is the audit
trail.
