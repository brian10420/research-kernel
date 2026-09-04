#!/usr/bin/env python3
"""tools/sync.py — compile core/ into the runtime adapters CLAUDE.md and AGENTS.md.

Deterministic: identical core/ bytes produce identical adapter bytes (no
timestamps, sorted roles, LF newlines). Standard library only.

Usage:
    python3 tools/sync.py            # write CLAUDE.md and AGENTS.md at the repo root
    python3 tools/sync.py --out DIR  # write them into DIR instead (used by check_drift.py)
    python3 tools/sync.py --hash     # print RULES_HASH only

Edit core/, never the generated files.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "core"
RULES_PATH = CORE / "SCIENTIFIC_RULES.md"
ROLES_DIR = CORE / "roles"
ADAPTERS = ("CLAUDE.md", "AGENTS.md")

INCLUDE_START = "<!-- adapter:include -->"
INCLUDE_END = "<!-- /adapter:include -->"


# ----------------------------------------------------------------------------
# core/ readers
# ----------------------------------------------------------------------------
def rules_hash(data: bytes) -> str:
    """First 12 hex characters of sha256 over the raw bytes of SCIENTIFIC_RULES.md."""
    return hashlib.sha256(data).hexdigest()[:12]


def extract_includes(text: str) -> list[tuple[str, str]]:
    """Return [(section_heading, block_text)] for every adapter:include block, in order."""
    blocks: list[tuple[str, str]] = []
    heading = ""
    collecting = False
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
        if line.strip() == INCLUDE_START:
            collecting = True
            buf = []
            continue
        if line.strip() == INCLUDE_END:
            collecting = False
            blocks.append((heading, "\n".join(buf).strip("\n")))
            continue
        if collecting:
            buf.append(line)
    if collecting:
        raise SystemExit(f"sync.py: unterminated {INCLUDE_START} block in {RULES_PATH}")
    return blocks


def _clean(value: str) -> str:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-subset reader: top-level `key: value` plus one level of nesting."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    data: dict = {}
    current: str | None = None
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  ") and current is not None:
            key, _, value = raw.strip().partition(":")
            data[current][key.strip()] = _clean(value)
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = _clean(value)
        if value == "":
            data[key] = {}
            current = key
        else:
            data[key] = value
            current = None
    return data


def load_roles() -> list[dict]:
    roles = []
    for path in sorted(ROLES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm.get("role"):
            continue
        runtime = fm.get("runtime", {}) if isinstance(fm.get("runtime"), dict) else {}
        roles.append(
            {
                "role": fm["role"],
                "posture": fm.get("posture", "?"),
                "isolation": fm.get("isolation_required", "?"),
                "summary": fm.get("summary", ""),
                "model": runtime.get("model", "?"),
                "effort": runtime.get("effort", "?"),
                "path": f"core/roles/{path.name}",
            }
        )
    return roles


# ----------------------------------------------------------------------------
# renderers
# ----------------------------------------------------------------------------
POINTER_MAP = [
    ("methodological rules (highest precedence)", "`core/SCIENTIFIC_RULES.md`"),
    ("cross-project design decisions + rationale", "`core/DECISIONS.md`"),
    ("canonical role specifications", "`core/roles/<role>.md` (roster: `core/roles/README.md`)"),
    ("per-project state: RESEARCH_STATE, DECISIONS, EXPERIMENT_LEDGER, HYPOTHESES, FAILED_IDEAS, OPEN_QUESTIONS",
     "the research project's own repository, seeded from `templates/project-state/`"),
    ("literature positions", "`LITERATURE_MAP.md` (schema in `core/`; per project alongside its state files)"),
    ("study log", "the project's notes vault (schema `core/STUDY_LOG.md`, template `templates/STUDY_LOG_TEMPLATE.md`)"),
    ("environment quirks, commands, gotchas", "agent memory / code docs — recall only, never authority"),
    ("blind-review label mapping", "`eval/.sealed/` — reviewers never read it"),
    ("evaluation rubric, protocol, tasks", "`eval/`"),
    ("migration record", "`MIGRATION_AUDIT.md`"),
    ("these adapters", "generated by `tools/sync.py`; drift blocked by `tools/check_drift.py`"),
]


def render_pointer_map() -> str:
    lines = ["| kind of truth | lives in |", "| --- | --- |"]
    for kind, where in POINTER_MAP:
        lines.append(f"| {kind} | {where} |")
    return "\n".join(lines)


def render_roster(roles: list[dict]) -> str:
    lines = [
        "| role | posture | runtime (recommendation) | spec |",
        "| --- | --- | --- | --- |",
    ]
    for r in roles:
        lines.append(
            f"| `{r['role']}` | {r['posture']} | model `{r['model']}`, effort {r['effort']} | `{r['path']}` |"
        )
    return "\n".join(lines)


def render_condensed(blocks: list[tuple[str, str]]) -> str:
    out = []
    for heading, block in blocks:
        out.append(f"### {heading}\n\n{block}")
    return "\n\n".join(out)


def banner(target: str) -> str:
    return (
        f"<!-- AUTO-GENERATED by tools/sync.py from core/ — edit core/, not this file. -->\n"
        f"<!-- Regenerate: python3 tools/sync.py   Verify: python3 tools/check_drift.py -->\n"
        f"<!-- target: {target} -->\n"
    )


def render_common_head(title: str, h: str) -> str:
    return (
        f"# {title}\n\n"
        f"RULES_HASH = {h}\n\n"
        f"Canary line to embed verbatim in every agent prompt: `RULES_HASH={h}`\n"
        f"Expected first output line of every role: `ACK RULES_HASH={h}`\n\n"
        f"## Where truth lives (pointer map)\n\n{render_pointer_map()}\n\n"
        f"**Two layers, two homes:** cross-project rules and roles live in this repository; "
        f"per-project state lives in each research project's repository.\n"
    )


def render_claude(h: str, blocks, roles) -> str:
    parts = [
        banner("Claude Code"),
        render_common_head("CLAUDE.md — Claude Code adapter for research-os", h),
        "## Condensed rules (verbatim from `core/SCIENTIFIC_RULES.md`)\n\n" + render_condensed(blocks) + "\n",
        "## Roles (canonical specs in `core/roles/`)\n\n" + render_roster(roles) + "\n",
        "## Claude Code mechanics\n\n"
        "- **Shared-context roles** are loaded as skills: `.claude/skills/<role>/SKILL.md` is a thin wrapper "
        "that reads `core/roles/<role>.md` by relative path and passes the RULES_HASH above. "
        "The spec text is the authority; the wrapper is a pointer.\n"
        "- **Isolated roles** are dispatched as subagents: `.claude/agents/<role>.md` is a thin wrapper "
        "whose body only states that the full spec and RULES_HASH must arrive in the task prompt. "
        "When you spawn one with the Agent tool, paste the ENTIRE `core/roles/<role>.md` text and the line "
        f"`RULES_HASH={h}` into the prompt yourself — subagents may not inherit this file or their agent body.\n"
        "- **Missing ACK is a loud failure.** A role whose first line is not `ACK RULES_HASH=…` did not load the "
        "rules; stop and re-dispatch. `regression-guardian` rejects run logs without it.\n"
        "- **Blind review:** never hand `blind-reviewer` anything but the bundle produced by "
        "`tools/anonymize.py`; `eval/.sealed/` is off-limits to reviewers.\n"
        "- **Model routing:** `inherit` for reasoning-heavy roles, a smaller model for mechanical roles; "
        "no role pins a paid tier. Concrete tool and plugin names (artifact publishing, design canvas, "
        "web search, research-report pipelines) are project-overlay matters, not part of the canonical specs.\n"
        "- **Never edit this file or `AGENTS.md` by hand.** Edit `core/`, run `python3 tools/sync.py`, commit both. "
        "The pre-commit hook (`git config core.hooksPath .githooks`) refuses commits with stale adapters.\n",
    ]
    return "\n".join(parts)


def render_agents(h: str, blocks, roles) -> str:
    parts = [
        banner("any harness (AGENTS.md convention)"),
        render_common_head("AGENTS.md — harness-neutral adapter for research-os", h),
        "## Condensed rules (verbatim from `core/SCIENTIFIC_RULES.md`)\n\n" + render_condensed(blocks) + "\n",
        "## Roles (canonical specs in `core/roles/`)\n\n" + render_roster(roles) + "\n",
        "## Loading a role (any agent runtime)\n\n"
        "1. Read `core/roles/<role>.md` in full.\n"
        f"2. Put its entire text plus the line `RULES_HASH={h}` into the agent's instructions or task prompt. "
        "Do not rely on the runtime inheriting this file.\n"
        f"3. Expect `ACK RULES_HASH={h}` as the agent's first output line; anything else means the rules were "
        "not loaded — stop and re-dispatch.\n"
        "4. Isolated roles (`blind-reviewer`, `experiment-runner`, `regression-guardian`, `repo-maintainer`) run "
        "in a fresh context with only their inputs; shared-context roles run inside the operator's session.\n"
        "5. `blind-reviewer` receives only the output of `tools/anonymize.py`; no runtime may read `eval/.sealed/` "
        "on a reviewer's behalf.\n"
        "6. Model choice is a recommendation (`inherit` for reasoning-heavy roles, a smaller model for mechanical "
        "roles); never a vendor or paid-tier requirement.\n"
        "7. Never edit this file by hand: edit `core/`, run `python3 tools/sync.py`, commit both.\n",
    ]
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# entry points
# ----------------------------------------------------------------------------
def generate() -> dict[str, bytes]:
    data = RULES_PATH.read_bytes()
    h = rules_hash(data)
    blocks = extract_includes(data.decode("utf-8"))
    roles = load_roles()
    return {
        "CLAUDE.md": render_claude(h, blocks, roles).encode("utf-8"),
        "AGENTS.md": render_agents(h, blocks, roles).encode("utf-8"),
    }


def write(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, content in generate().items():
        (out_dir / name).write_bytes(content)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT, help="output directory (default: repo root)")
    ap.add_argument("--hash", action="store_true", help="print RULES_HASH and exit")
    args = ap.parse_args(argv)
    if args.hash:
        print(rules_hash(RULES_PATH.read_bytes()))
        return 0
    write(args.out)
    print(f"sync.py: wrote {', '.join(ADAPTERS)} to {args.out} (RULES_HASH={rules_hash(RULES_PATH.read_bytes())})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
