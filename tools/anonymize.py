#!/usr/bin/env python3
"""tools/anonymize.py — build a blind-review bundle (SCIENTIFIC_RULES §4, §7).

Strips provenance fields, author names, model names, e-mail addresses, session
trailers, and timestamps from text files, replacing each with a stable label
([NAME-1], [MODEL-2], [DATE-3], …). Optionally assigns blind condition labels
(A/B/…) to several inputs in a secret random order. The label→original mapping
is written ONLY to eval/.sealed/<bundle>.json (mode 0600, git-ignored);
reviewer roles never read that directory.

Usage
  python3 tools/anonymize.py build  --out eval/bundles/<id> [--name "Jane Doe"]... \
        [--names-file names.txt] [--condition NAME=PATH]... [PATH ...]
  python3 tools/anonymize.py verify eval/bundles/<id> [--name ...] [--names-file ...]
        # exit 1 if any residual provenance pattern is found

Text files (.md .txt .tex .bib .json .yaml .yml .csv .py .html .rst) are
rewritten. Other files (e.g. .pdf) are copied unchanged with a WARNING: their
embedded metadata must be stripped with an external tool before the bundle is
handed to a reviewer. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEALED_DIR = ROOT / "eval" / ".sealed"
TEXT_SUFFIXES = {".md", ".txt", ".tex", ".bib", ".json", ".yaml", ".yml", ".csv", ".py", ".html", ".rst"}

# --- patterns ---------------------------------------------------------------
PROVENANCE_KEYS = (
    "proposer", "decided_by", "updated_by", "operator", "author", "authors",
    "created_by", "reviewed_by", "originSessionId", "session", "sessionId",
    "ack", "derived_from", "owner",
)
PROVENANCE_LINE = re.compile(
    r"^(\s*(?:-\s*)?)(" + "|".join(PROVENANCE_KEYS) + r")\s*:\s*.*$", re.M
)
TRAILER_LINE = re.compile(
    r"^\s*(Co-Authored-By|Claude-Session|Signed-off-by|Reviewed-by|Generated-by)\s*:.*$", re.M | re.I
)
MODEL_NAME = re.compile(
    r"\b(?:"
    r"claude(?:[- ](?:fable|opus|sonnet|haiku|mythos|code))?(?:[- ]v?\d[\d.]*)?"
    r"|(?:fable|opus|sonnet|haiku|mythos)(?:[- ]v?\d[\d.]*)?"
    r"|astra|codex|anthropic|openai|deepmind"
    r"|gpt-?\d[\w.-]*"
    r"|gemini(?:[- ][\w.]+)?"
    r"|llama(?:[- ]\d[\d.]*)?|mistral|deepseek(?:[- ][\w.]+)?"
    r"|other-model:[A-Za-z0-9._-]+"
    r")\b",
    re.I,
)
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
ISO_DT = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?)?\b")
LONG_DATE = re.compile(
    r"\b(?:\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4})\b",
    re.I,
)
CLOCK = re.compile(r"\b(?:[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\b")
SESSION_URL = re.compile(r"https?://\S*session[_A-Za-z0-9/-]*", re.I)


class Labeler:
    """Stable label per distinct original string, per category."""

    def __init__(self) -> None:
        self.map: dict[str, dict[str, str]] = {}   # category -> {label: original}
        self.rev: dict[str, dict[str, str]] = {}   # category -> {original(lower): label}

    def label(self, category: str, original: str) -> str:
        key = original.strip().lower()
        rev = self.rev.setdefault(category, {})
        if key in rev:
            return rev[key]
        lab = f"[{category}-{len(rev) + 1}]"
        rev[key] = lab
        self.map.setdefault(category, {})[lab] = original.strip()
        return lab


def scrub_text(text: str, names: list[str], lab: Labeler) -> str:
    # 1. provenance lines and trailers → removed, but marked so the reviewer sees a field existed
    text = PROVENANCE_LINE.sub(lambda m: f"{m.group(1)}{m.group(2)}: [PROVENANCE-REMOVED]", text)
    text = TRAILER_LINE.sub("[TRAILER-REMOVED]", text)
    text = SESSION_URL.sub("[SESSION-URL-REMOVED]", text)
    # 2. e-mails first (a name inside an address must not break the address pattern)
    text = EMAIL.sub(lambda m: lab.label("EMAIL", m.group(0)), text)
    # 3. author names (longest first so "Jane Doe" wins over "Doe")
    for name in sorted({n for n in names if n.strip()}, key=len, reverse=True):
        text = re.sub(r"(?<!\w)" + re.escape(name) + r"(?!\w)", lambda m, n=name: lab.label("NAME", n), text, flags=re.I)
    # 4. model names, dates, clock times
    text = MODEL_NAME.sub(lambda m: lab.label("MODEL", m.group(0)), text)
    text = ISO_DT.sub(lambda m: lab.label("DATE", m.group(0)), text)
    text = LONG_DATE.sub(lambda m: lab.label("DATE", m.group(0)), text)
    text = CLOCK.sub(lambda m: lab.label("TIME", m.group(0)), text)
    return text


def residuals(text: str, names: list[str]) -> list[str]:
    hits: list[str] = []
    for name in names:
        if name.strip() and re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text, re.I):
            hits.append(f"name:{name}")
    for pat, tag in ((EMAIL, "email"), (MODEL_NAME, "model"), (ISO_DT, "date"), (LONG_DATE, "date"),
                     (CLOCK, "time"), (TRAILER_LINE, "trailer"), (SESSION_URL, "session-url")):
        m = pat.search(text)
        if m:
            hits.append(f"{tag}:{m.group(0)[:40]}")
    for m in PROVENANCE_LINE.finditer(text):
        if "[PROVENANCE-REMOVED]" not in m.group(0):
            hits.append(f"provenance:{m.group(2)}")
            break
    return hits


def load_names(args) -> list[str]:
    names = list(args.name or [])
    if args.names_file:
        names += [ln.strip() for ln in Path(args.names_file).read_text(encoding="utf-8").splitlines() if ln.strip()]
    return names


def iter_files(path: Path):
    if path.is_file():
        yield path
    else:
        for p in sorted(path.rglob("*")):
            if p.is_file() and ".sealed" not in p.parts and ".git" not in p.parts:
                yield p


def cmd_build(args) -> int:
    names = load_names(args)
    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        print(f"anonymize: refusing to write into non-empty {out}", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    lab = Labeler()
    warnings: list[str] = []
    inputs: list[tuple[str, Path]] = [(f"input-{i+1}", Path(p)) for i, p in enumerate(args.paths or [])]

    # blind condition labels: secret random assignment of A, B, C, … to the named conditions
    conditions: dict[str, str] = {}
    if args.condition:
        pairs = [c.split("=", 1) for c in args.condition]
        letters = [chr(ord("A") + i) for i in range(len(pairs))]
        order = list(range(len(pairs)))
        for i in range(len(order) - 1, 0, -1):          # Fisher–Yates with a CSPRNG
            j = secrets.randbelow(i + 1)
            order[i], order[j] = order[j], order[i]
        for letter, idx in zip(letters, order):
            cond_name, cond_path = pairs[idx]
            conditions[letter] = cond_name
            inputs.append((letter, Path(cond_path)))

    for label, src in inputs:
        if not src.exists():
            print(f"anonymize: missing input {src}", file=sys.stderr)
            return 2
        dest_root = out / label
        for f in iter_files(src):
            rel = f.relative_to(src) if src.is_dir() else Path(f.name)
            dest = dest_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if f.suffix.lower() in TEXT_SUFFIXES:
                dest.write_text(scrub_text(f.read_text(encoding="utf-8", errors="replace"), names, lab), encoding="utf-8")
            else:
                shutil.copy2(f, dest)
                warnings.append(f"{dest}: binary copied unchanged — strip embedded metadata externally")

    bundle_id = out.name
    SEALED_DIR.mkdir(parents=True, exist_ok=True)
    sealed = SEALED_DIR / f"{bundle_id}.json"
    payload = {"bundle": str(out), "conditions": conditions, "labels": lab.map,
               "inputs": {label: str(src) for label, src in inputs}}
    sealed.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.chmod(sealed, 0o600)
    for w in warnings:
        print("WARNING:", w)
    print(f"anonymize: bundle written to {out}; mapping sealed at {sealed} (reviewers never read it)")
    return 0


def cmd_verify(args) -> int:
    names = load_names(args)
    bad = 0
    for f in iter_files(Path(args.bundle)):
        if f.suffix.lower() not in TEXT_SUFFIXES:
            continue
        hits = residuals(f.read_text(encoding="utf-8", errors="replace"), names)
        if hits:
            bad += 1
            print(f"RESIDUAL {f}: {', '.join(hits)}")
    if bad:
        print(f"anonymize verify: FAIL — {bad} file(s) with residual provenance")
        return 1
    print("anonymize verify: OK — zero residual provenance patterns")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build an anonymized bundle")
    b.add_argument("paths", nargs="*", help="files or directories to anonymize (unlabeled inputs)")
    b.add_argument("--out", required=True, help="output bundle directory (must be empty or absent)")
    b.add_argument("--name", action="append", help="author/person name to strip (repeatable)")
    b.add_argument("--names-file", help="file with one name per line")
    b.add_argument("--condition", action="append", metavar="NAME=PATH",
                   help="named condition to blind-label (A/B/… assigned in secret random order)")
    b.set_defaults(func=cmd_build)
    v = sub.add_parser("verify", help="fail if a bundle still contains provenance patterns")
    v.add_argument("bundle")
    v.add_argument("--name", action="append")
    v.add_argument("--names-file")
    v.set_defaults(func=cmd_verify)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
