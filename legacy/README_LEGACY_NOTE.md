# legacy/ — superseded Claude-specific originals

Moved here in Phase 4 of the `research-os` migration (2026-09-04), unchanged
except for the one-line header in `README.md`. Kept for history and for the
sync manifest of the private originals; **nothing here is loaded by any
runtime**. The canonical content now lives in `core/roles/` (specs) and the
generated wrappers under `.claude/`.

| moved item | reason |
| --- | --- |
| `skills/*/SKILL.md` (7) | Claude-skill bodies superseded by `core/roles/<role>.md` + generated `.claude/skills/<role>/SKILL.md` wrappers |
| `agents/*.md` (4) | Claude-subagent bodies superseded by `core/roles/<role>.md` + generated `.claude/agents/<role>.md` wrappers |
| `RESEARCH_TEAM.md` | roster contract superseded by `core/roles/README.md` (doctrine) and the generated adapters (mechanism table) |
| `README.md` | Claude Code install guide superseded by the new root README (two layers, compile layer, wrappers) |
| `docs/customization.md` | `<placeholder>` fill-in guide for copied `.claude/` files superseded by `templates/project-state/README.md` and the overlay slots in each role spec |
