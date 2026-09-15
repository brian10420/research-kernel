#!/usr/bin/env python3
"""tools/sync.py — compile core/ into every runtime adapter.

Generates, from core/SCIENTIFIC_RULES.md, core/roles/*.md and core/effort_policy.yaml:
  CLAUDE.md                          Claude Code adapter
  AGENTS.md                          harness-neutral adapter
  .claude/agents/<role>.md           self-contained wrapper per ISOLATED role (spec inlined)
  .claude/skills/<role>/SKILL.md     wrapper per SHARED-CONTEXT role — loads the two files next to it
  .claude/skills/<role>/role.md      verbatim copy of core/roles/<role>.md
  .claude/skills/<role>/RULES.md     condensed SCIENTIFIC_RULES (the adapter:include blocks)

Every wrapper is self-contained (it never resolves a project-root path), so the
same generated tree works both copied into a project and installed as a Claude
Code plugin (`skills/` and `agents/` at the repo root are symlinks to `.claude/`).
Project-specific facts arrive through `.claude/research-kernel.overlay.md` in the
consuming project (template: templates/research-kernel.overlay.template.md).

Deterministic: identical core/ bytes produce identical adapter bytes (no
timestamps, sorted roles, LF newlines). Standard library only.

Usage:
    python3 tools/sync.py            # write all adapters under the repo root
    python3 tools/sync.py --out DIR  # write them under DIR instead (used by check_drift.py)
    python3 tools/sync.py --hash     # print RULES_HASH only
    python3 tools/sync.py --list     # print the adapter paths it generates

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
ROOT_ADAPTERS = ("CLAUDE.md", "AGENTS.md")

# runtime-neutral capability -> Claude Code tool names (isolated roles only)
CAP_TOOLS = {
    "read": ["Read"],
    "search": ["Grep", "Glob"],
    "shell": ["Bash"],
    "write": ["Write"],
    "edit": ["Edit"],
    "web": ["WebSearch", "WebFetch"],
}
TOOL_ORDER = ["Read", "Grep", "Glob", "Bash", "Write", "Edit", "WebSearch", "WebFetch"]
# runtime-neutral model class -> Claude Code `model:` value (verified against the live docs 2026-09-04:
# accepted values are sonnet | opus | haiku | fable | <full id> | inherit). Never a paid-tier pin.
MODEL_MAP = {"inherit": "inherit", "smaller-tier": "sonnet"}
POLICY_PATH = CORE / "effort_policy.yaml"
POLICY_MODELS = {"inherit", "sonnet", "opus", "haiku"}
POLICY_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
OVERLAY_REL = ".claude/research-kernel.overlay.md"   # relative to the consuming project's root

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
    """Minimal YAML-subset reader for a `---` fenced frontmatter block."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    return parse_simple_yaml(text[4:end])


def parse_simple_yaml(body: str) -> dict:
    """Top-level `key: value` plus one level of nesting; comments and blanks ignored."""
    data: dict = {}
    current: str | None = None
    for raw in body.splitlines():
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


def load_effort_policy() -> dict[str, dict]:
    """core/effort_policy.yaml -> {role: {model?, effort?, rationale?}}; validated, absent file = {}."""
    if not POLICY_PATH.exists():
        return {}
    policy = parse_simple_yaml(POLICY_PATH.read_text(encoding="utf-8"))
    for role, entry in policy.items():
        if not isinstance(entry, dict):
            raise SystemExit(f"sync.py: {POLICY_PATH.name}: `{role}` must be a mapping")
        if "model" in entry and entry["model"] not in POLICY_MODELS:
            raise SystemExit(f"sync.py: {POLICY_PATH.name}: `{role}.model` must be one of {sorted(POLICY_MODELS)}")
        if "effort" in entry and entry["effort"] not in POLICY_EFFORTS:
            raise SystemExit(f"sync.py: {POLICY_PATH.name}: `{role}.effort` must be one of {sorted(POLICY_EFFORTS)}")
    return policy


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return value
    value = (value or "").strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [v.strip() for v in value.split(",") if v.strip()]


def spec_body(text: str) -> str:
    """The role spec without its frontmatter (what a dispatcher pastes into a prompt)."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5:].lstrip("\n")
    return text


def load_roles() -> list[dict]:
    roles = []
    policy = load_effort_policy()
    for path in sorted(ROLES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm.get("role"):
            continue
        runtime = fm.get("runtime", {}) if isinstance(fm.get("runtime"), dict) else {}
        roles.append(
            {
                "policy": policy.get(fm["role"], {}),
                "spec_bytes": path.read_bytes(),
                "spec_body": spec_body(text),
                "role": fm["role"],
                "posture": fm.get("posture", "?"),
                "isolation": fm.get("isolation_required", "?"),
                "summary": fm.get("summary", ""),
                "model": runtime.get("model", "?"),
                "effort": runtime.get("effort", "?"),
                "rationale": runtime.get("rationale", ""),
                "capabilities": _as_list(fm.get("capabilities", "")),
                "path": f"core/roles/{path.name}",
                "file": path.name,
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


def render_roster(roles: list[dict], vendor: str = "") -> str:
    lines = [
        "| role | posture | runtime (recommendation) | spec | wrapper |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in roles:
        model = r["model"]
        if vendor == "claude":
            model = f"{MODEL_MAP.get(model, model)} (`{model}`)"
        wrapper = wrapper_path(r) if vendor == "claude" else "—"
        lines.append(
            f"| `{r['role']}` | {r['posture']} | model `{model}`, effort {r['effort']} | `{r['path']}` | `{wrapper}` |"
        )
    return "\n".join(lines)


def wrapper_path(r: dict) -> str:
    if r["posture"] == "isolated":
        return f".claude/agents/{r['role']}.md"
    return f".claude/skills/{r['role']}/SKILL.md"


def skill_dir(r: dict) -> str:
    return f".claude/skills/{r['role']}"


def policy_lines(r: dict) -> str:
    """`model:` / `effort:` frontmatter keys enforced by core/effort_policy.yaml (empty when unlisted)."""
    out = ""
    if "model" in r["policy"]:
        out += f"model: {r['policy']['model']}\n"
    if "effort" in r["policy"]:
        out += f"effort: {r['policy']['effort']}\n"
    return out


def policy_sentence(r: dict) -> str:
    p = r["policy"]
    if not p:
        return "Claude Code effort policy (`core/effort_policy.yaml`): not listed — inherits the session effort."
    bits = []
    if "model" in p:
        bits.append(f"model `{p['model']}`")
    if "effort" in p:
        bits.append(f"effort `{p['effort']}`")
    why = f" — {p['rationale']}" if p.get("rationale") else ""
    return f"Claude Code effort policy (`core/effort_policy.yaml`): {', '.join(bits)}{why}."


def claude_tools(r: dict) -> str:
    names: list[str] = []
    for cap in r["capabilities"]:
        for tool in CAP_TOOLS.get(cap, []):
            if tool not in names:
                names.append(tool)
    return ", ".join(sorted(names, key=TOOL_ORDER.index))


def render_agent_wrapper(r: dict, h: str) -> str:
    model = r["policy"].get("model") or MODEL_MAP.get(r["model"], r["model"])
    effort_line = f"effort: {r['policy']['effort']}\n" if "effort" in r["policy"] else ""
    tools = claude_tools(r)
    tools_line = f"tools: {tools}\n" if tools else ""
    decline = (
        "Decline any project context, memory, or decision history offered to you; review only the anonymized bundle.\n"
        if r["role"] == "blind-reviewer" else ""
    )
    return (
        "---\n"
        f"name: {r['role']}\n"
        f"description: {r['summary']} ISOLATED role of research-os — dispatch only with the full canonical spec and the RULES_HASH line in the task prompt (canary protocol).\n"
        f"{tools_line}"
        f"model: {model}\n"
        f"{effort_line}"
        "---\n"
        f"<!-- AUTO-GENERATED by tools/sync.py from core/roles/{r['file']} — edit that file, not this one. -->\n\n"
        f"You are the `{r['role']}` role of research-kernel. Your canonical spec is inlined below; the line `RULES_HASH=<hash>` must still arrive **in the task prompt itself** (subagents may not receive this body on every harness, so dispatchers keep pasting the spec too).\n\n"
        "Canary protocol (SCIENTIFIC_RULES §3):\n"
        f"1. If the prompt has no `RULES_HASH=` line, halt: output `HALT: RULES_HASH missing — rules not loaded` and report instead of working.\n"
        f"2. If the prompt's hash is not `{h}` (the hash this wrapper was generated with), halt: output `HALT: stale RULES_HASH` and report.\n"
        "3. If neither the prompt nor this body contains the role spec (its `## Hard rules` section), halt: output `HALT: role spec missing` and report.\n"
        f"4. Otherwise your first output line is exactly `ACK RULES_HASH={h}`, then follow the spec.\n\n"
        f"Runtime recommendation: model `{r['model']}` → `{model}`, effort {r['effort']} ({r['rationale']}). {policy_sentence(r)}\n"
        "Never read `eval/.sealed/`. One dispatch = one complete report. "
        f"Project-specific facts (paths, protocol, guards) come from the dispatch prompt or the project's `{OVERLAY_REL}`, never from edits to this file.\n"
        f"{decline}\n"
        f"---\n\n## Canonical role spec (inlined verbatim from `{r['path']}`)\n\n"
        f"{r['spec_body'].rstrip()}\n"
    )


def render_skill_wrapper(r: dict, h: str) -> str:
    return (
        "---\n"
        f"name: {r['role']}\n"
        f"description: {r['summary']} (research-kernel role; canonical spec in {r['path']})\n"
        f"allowed-tools: Bash(cat ${{CLAUDE_SKILL_DIR}}/*), Bash(cat ${{CLAUDE_PROJECT_DIR}}/{OVERLAY_REL})\n"
        f"{policy_lines(r)}"
        "metadata:\n"
        "  research-os: role-wrapper\n"
        f"  rules-hash: \"{h}\"\n"
        f"  runtime-model: {r['model']}\n"
        f"  runtime-effort: {r['effort']}\n"
        f"  effort-policy: {r['policy'].get('effort', 'inherit')}\n"
        "  generated-by: tools/sync.py\n"
        "---\n"
        f"<!-- AUTO-GENERATED by tools/sync.py from core/roles/{r['file']} — edit that file, not this one. -->\n\n"
        f"RULES_HASH={h}\n\n"
        f"You are now the `{r['role']}` role of research-kernel. Your first output line must be exactly `ACK RULES_HASH={h}`. "
        "The canonical spec below is the authority; this wrapper only loads it. Everything it loads sits next to this file, "
        "so it works unchanged whether this tree was copied into a project or installed as a Claude Code plugin.\n\n"
        "## Condensed methodological rules (injected from `RULES.md` next to this file)\n\n"
        f"!`cat ${{CLAUDE_SKILL_DIR}}/RULES.md`\n\n"
        f"## Canonical role spec (injected from `role.md` next to this file — a verbatim copy of `{r['path']}`)\n\n"
        f"!`cat ${{CLAUDE_SKILL_DIR}}/role.md`\n\n"
        f"## Project overlay (injected from `{OVERLAY_REL}` in the consuming project, if present)\n\n"
        f"!`cat ${{CLAUDE_PROJECT_DIR:-.}}/{OVERLAY_REL} 2>/dev/null || echo \"(no project overlay at {OVERLAY_REL} — running on the generic spec; seed one from templates/research-kernel.overlay.template.md)\"`\n\n"
        "The overlay holds the project's facts for this role's \"Project overlay slots\" (paths, protocol, invariants, guards). "
        "It is the ONLY place project-specific content belongs: never edit `role.md`, `RULES.md` or this wrapper — they are "
        "regenerated by `tools/sync.py` and replaced wholesale on every plugin update.\n\n"
        "## If a section above did not load\n\n"
        "If a section is empty or shows a command instead of content, read `role.md` and `RULES.md` from this skill's own "
        "directory with the Read tool before doing anything else (never a project-root path). If `role.md` cannot be read, "
        "halt: output `HALT: role spec missing` and report. A missing overlay is not an error.\n\n"
        f"Runtime recommendation (provider-neutral, from the spec): model `{r['model']}`, effort {r['effort']} ({r['rationale']}). "
        f"{policy_sentence(r)} Change either only through `core/`, never by hand-editing this file.\n"
    )


def render_rules_file(h: str, blocks) -> str:
    return (
        "<!-- AUTO-GENERATED by tools/sync.py from core/SCIENTIFIC_RULES.md (adapter:include blocks) — edit core/, not this file. -->\n"
        f"# Condensed rules — RULES_HASH={h}\n\n"
        + render_condensed(blocks)
        + "\n"
    )


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
        "## Roles (canonical specs in `core/roles/`)\n\n" + render_roster(roles, vendor="claude") + "\n",
        "## Claude Code mechanics\n\n"
        "- **Shared-context roles** are loaded as skills: `.claude/skills/<role>/SKILL.md` is a generated wrapper "
        "that injects `role.md` (a verbatim copy of `core/roles/<role>.md`) and `RULES.md` from its own directory at "
        "load time and carries the RULES_HASH above. The spec text is the authority; the wrapper is a pointer.\n"
        "- **Plugin install.** `skills/` and `agents/` at the repository root are symlinks to `.claude/`, and "
        "`.claude-plugin/{plugin,marketplace}.json` make this repository a Claude Code marketplace + plugin "
        "(`/plugin marketplace add <owner>/<repo>` then `/plugin install research-kernel@research-kernel`); skills "
        "then appear as `/research-kernel:<role>`. Nothing in the plugin is ever hand-edited — updates replace it.\n"
        f"- **Project overlay.** Project-specific facts live in the consuming project's `{OVERLAY_REL}` "
        "(template: `templates/research-kernel.overlay.template.md`); every skill wrapper injects it when present. "
        "That file, plus the project-state files, is the only place a project's facts belong.\n"
        "- **Effort policy.** `core/effort_policy.yaml` decides which wrappers carry `effort:` / `model:` "
        "frontmatter (honoured by Claude Code for skills and subagents; not passable at dispatch time). Effort is "
        "chosen by task shape up front — closed verification saturates at xhigh, mechanical roles run low on a "
        "smaller model, long-horizon work stays at the session default and the operator raises the SESSION effort "
        "for an unbounded-judgement step; no role pins max, and \"stuck\" is a reason to change method, not effort.\n"
        "- **Custom subagents do load the CLAUDE.md hierarchy** (built-in Explore/Plan agents skip it) but never the "
        "session's auto-memory, and their own body is not guaranteed to reach them on every harness — so the spec "
        "and hash are embedded in the prompt regardless.\n"
        "- **Isolated roles** are dispatched as subagents: `.claude/agents/<role>.md` is a thin wrapper "
        "whose body only states that the full spec and RULES_HASH must arrive in the task prompt. "
        "When you spawn one with the Agent tool, paste the ENTIRE `core/roles/<role>.md` text and the line "
        f"`RULES_HASH={h}` into the prompt yourself — subagents may not inherit this file or their agent body.\n"
        "- **Missing ACK is a loud failure.** A role whose first line is not `ACK RULES_HASH=…` did not load the "
        "rules; stop and re-dispatch. `regression-guardian` rejects run logs without it.\n"
        "- **Blind review:** never hand `blind-reviewer` anything but the bundle produced by "
        "`tools/anonymize.py`; `eval/.sealed/` is off-limits to reviewers.\n"
        "- **Model routing:** `inherit` for reasoning-heavy roles, a smaller model for mechanical roles; "
        "no role pins a paid tier or a vendor model id. Concrete tool and plugin names (artifact publishing, design canvas, "
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
    out = {
        "CLAUDE.md": render_claude(h, blocks, roles).encode("utf-8"),
        "AGENTS.md": render_agents(h, blocks, roles).encode("utf-8"),
    }
    rules_file = render_rules_file(h, blocks).encode("utf-8")
    for r in roles:
        if r["posture"] == "isolated":
            out[wrapper_path(r)] = render_agent_wrapper(r, h).encode("utf-8")
        else:
            out[wrapper_path(r)] = render_skill_wrapper(r, h).encode("utf-8")
            out[f"{skill_dir(r)}/role.md"] = r["spec_bytes"]
            out[f"{skill_dir(r)}/RULES.md"] = rules_file
    return out


def wrapper_globs(root: Path) -> list[str]:
    """Every wrapper path that exists on disk under root (to detect orphans)."""
    found = [str(p.relative_to(root)) for p in (root / ".claude" / "agents").glob("*.md")]
    found += [str(p.relative_to(root)) for p in (root / ".claude" / "skills").glob("*/*.md")]
    return sorted(found)


def write(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, content in generate().items():
        target = out_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT, help="output directory (default: repo root)")
    ap.add_argument("--hash", action="store_true", help="print RULES_HASH and exit")
    ap.add_argument("--list", action="store_true", help="print the adapter paths that would be generated")
    args = ap.parse_args(argv)
    if args.hash:
        print(rules_hash(RULES_PATH.read_bytes()))
        return 0
    if args.list:
        print("\n".join(generate().keys()))
        return 0
    files = generate()
    write(args.out)
    print(f"sync.py: wrote {len(files)} adapters under {args.out} (RULES_HASH={rules_hash(RULES_PATH.read_bytes())})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
