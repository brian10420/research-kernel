# Memory setup (optional) — agent memory as a recall layer

Nothing here is installed by the migration. Agent memory is **optional** and,
when present, is a **recall layer only** (SCIENTIFIC_RULES §0–§1, §5;
DECISION_001). Git, the notes vault, and the experiment ledgers are the
authority.

## Optional install (Claude Code, MCP)

```bash
claude mcp add --transport stdio memory -- npx -y agentsmd-memory
```

This registers the `agentsmd-memory` server for the current project scope.
Other harnesses have their own memory mechanisms; the policy below applies to
all of them, including a harness's built-in auto-memory.

## What memory MAY store

- environment quirks and workarounds (driver/library mismatches, sandbox
  behaviour, "run this detached")
- commands, flags, and run patterns (`uv run …`, env-check scripts, build
  commands)
- paths and locations (analysis directory, log line to collect from)
- tool and harness gotchas (a hook that misfires, a permission rule syntax)
- hardware limits (VRAM headroom, safe batch sizes)
- flaky-test notes and formatting preferences

## What memory MAY NOT store

- methodological rules → `core/SCIENTIFIC_RULES.md`
- design decisions and their rationale → `DECISIONS.md`
- experiment results and metric values → `EXPERIMENT_LEDGER.md`
- hypotheses or ideas from any proposer → `HYPOTHESES.md` with provenance;
  model-speculated ideas never go into durable memory at all
- anything a paper could cite; anything with scientific authority
- personal data beyond what a command needs; secrets, tokens, credentials

## The audit rule

`memory-curator` (`core/roles/memory-curator.md`) audits memory against git at
session end or on request. When memory contradicts git or a state file,
**memory loses**: the curator proposes `memory_forget` for the entry and never
edits `core/` or a state file to match memory. Session-end distillation is a
reviewed diff with provenance and `status: proposed`; a human accepts it.

## Removing

```bash
claude mcp remove memory
```
