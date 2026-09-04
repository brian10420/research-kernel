# adapters/codex — placeholder

No Codex configuration is generated yet. When a Codex adapter is built, its
sources are exactly two things and nothing else:

1. `AGENTS.md` at the repository root — the harness-neutral adapter generated
   by `tools/sync.py` (banner, `RULES_HASH`, pointer map, condensed rules,
   roster). Codex reads `AGENTS.md` natively.
2. `core/roles/<role>.md` — the canonical role specs. A Codex dispatch must
   embed the full spec text and the `RULES_HASH=<hash>` line in the task,
   exactly as the canary protocol requires for every runtime
   (SCIENTIFIC_RULES §3).

Any Codex-specific file (a config, a custom-instructions block, an agent
manifest) must be produced by extending `tools/sync.py`, so that
`tools/check_drift.py` guards it the same way it guards `CLAUDE.md` and
`AGENTS.md`. Hand-written Codex config is out of policy.

Evaluation of the Codex ecosystem against the Claude Code ecosystem is defined
in `eval/PROTOCOL.md` (comparison B); it does not require this adapter to exist
beyond `AGENTS.md`.
