#!/usr/bin/env bash
# leakcheck.template.sh — deny-list scanner for a scrubbed PUBLIC tree.
# Two-track pattern: your PRIVATE repo keeps the real version of this script
# with the real deny-list — because the deny-list itself names your secrets,
# it must never be committed to the public repo. This public copy ships dummy
# patterns only, as documentation of the pattern.
#
# Usage: leakcheck.sh <path-to-public-tree>   — exit 1 on any hit.
set -u
TREE="${1:?usage: leakcheck.sh <public-tree>}"
ALLOW="$(dirname "$0")/leakcheck_allowlist.txt"   # lines: "path-regex<TAB>pattern-regex"

PATTERNS=(
  # your project codename(s) and infrastructure
  'my[-_ ]?secret[-_ ]?project' 'myuser/private-repo' '/home/myuser'
  # your datasets, campaign names, model keys
  '\bMYCORPUS\b' 'campaign_[a-z0-9]+'
  # value-attached metrics and known result numbers
  'ACC\s*[≈=~]\s*0\.[0-9]' '0\.123|4\.56'
  # personal details
  'my-real-name' 'my-email@'
  # internal dates that stamp private history
  '20XX-[0-9]{2}-[0-9]{2}'
)

fail=0
for p in "${PATTERNS[@]}"; do
  hits="$(grep -rInE --binary-files=without-match "$p" "$TREE" --exclude-dir=.git 2>/dev/null)"
  [ -z "$hits" ] && continue
  if [ -f "$ALLOW" ]; then
    while IFS=$'\t' read -r apath apat; do
      [ -z "$apath" ] && continue
      hits="$(printf '%s\n' "$hits" | grep -vE "^[^:]*${apath}[^:]*:.*${apat}" || true)"
    done < "$ALLOW"
  fi
  if [ -n "$hits" ]; then
    echo "── LEAK candidate — pattern /$p/:"; printf '%s\n' "$hits"; fail=1
  fi
done
[ "$fail" -eq 0 ] && echo "leakcheck: CLEAN (0 hits) — eyeball allowlisted lines anyway"
exit $fail
