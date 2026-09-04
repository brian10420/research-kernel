#!/usr/bin/env python3
"""tools/check_drift.py — fail if the committed adapters are stale relative to core/.

Regenerates CLAUDE.md and AGENTS.md into a temporary directory with tools/sync.py
and compares them byte-for-byte against either the working tree (default) or the
git index (--against index, used by .githooks/pre-commit so a commit can never
carry adapters that disagree with the core/ it commits).

Exit status: 0 = no drift; 1 = drift or a missing adapter; 2 = tool error.
Standard library only.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync  # noqa: E402

ROOT = sync.ROOT


def committed_bytes(name: str, against: str) -> bytes | None:
    if against == "worktree":
        p = ROOT / name
        return p.read_bytes() if p.exists() else None
    # index: the staged version (falls back to HEAD content when unstaged)
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "show", f":{name}"], capture_output=True
    )
    return proc.stdout if proc.returncode == 0 else None


def first_diff_line(a: bytes, b: bytes) -> str:
    al, bl = a.splitlines(), b.splitlines()
    for i, (x, y) in enumerate(zip(al, bl), 1):
        if x != y:
            return f"line {i}: expected {x[:80]!r} got {y[:80]!r}"
    return f"length differs ({len(al)} vs {len(bl)} lines)"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--against", choices=("worktree", "index"), default="worktree")
    args = ap.parse_args(argv)

    with tempfile.TemporaryDirectory(prefix="research-os-sync-") as tmp:
        sync.write(Path(tmp))
        fresh = {name: (Path(tmp) / name).read_bytes() for name in sync.ADAPTERS}

    drift = False
    for name in sync.ADAPTERS:
        have = committed_bytes(name, args.against)
        if have is None:
            print(f"check_drift: {name} is missing from the {args.against} — run: python3 tools/sync.py")
            drift = True
            continue
        if have != fresh[name]:
            print(f"check_drift: {name} is STALE relative to core/ ({args.against}); {first_diff_line(fresh[name], have)}")
            drift = True
    if drift:
        print("check_drift: FAIL — regenerate with `python3 tools/sync.py` and stage CLAUDE.md + AGENTS.md")
        return 1
    print(f"check_drift: OK — adapters match core/ (RULES_HASH={sync.rules_hash(sync.RULES_PATH.read_bytes())})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
