# eval/.sealed/ — sealed label mappings (reviewers never read this directory)

`tools/anonymize.py build` writes one JSON file per bundle here: the mapping
from every `[NAME-n]`, `[MODEL-n]`, `[DATE-n]` label back to its original, and
the secret assignment of blind condition letters (A/B/…) to named conditions.

Rules (SCIENTIFIC_RULES §7):
- No reviewer role (`blind-reviewer`, the evaluation grader) may open, list, or
  be told the contents of this directory. An orchestrator that pastes a mapping
  into a reviewer prompt has broken the blind.
- Files are written with mode 0600 and are git-ignored (`eval/.sealed/*`);
  only this README and `.gitkeep` are tracked.
- Un-blinding happens once, after grading, by a human, and the un-blinded
  result is recorded in `eval/RESULTS_TEMPLATE.md`'s format with the bundle id.
