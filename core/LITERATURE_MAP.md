---
schema: research-os/literature-map/v1
scope: cross-project schema + one worked example. Real entries live in the project repo's LITERATURE_MAP.md.
purpose: >
  Verified positions of the papers that bear on a claim: what each one actually
  shows, how it was verified, and how it relates to our claims. A citation that
  has not been verified against its source is marked so.
entry_template: |
  id: L_<NNN>
  key: <bibtex key>
  title: <paper title>
  date: YYYY-MM-DD                       # the day the entry was written
  proposer: human | fable | astra | other-model:<name>
  status: proposed | accepted            # accepted = a human read the source (or the verified fields below)
  decided_by: human | ""
  evidence: [<DOI / arXiv id / URL>]
  claim_in_paper: <what the paper shows, in one sentence, as it appears there>
  relation: supports | contradicts | neighbour | baseline | method-source
  our_claim: <which of our claims / hypotheses it touches, by id>
  verified: {how: <read-full-text | abstract-only | metadata-only | unverified>, on: YYYY-MM-DD, by: <proposer>}
  scope_notes: <corpus version, protocol, split — anything that makes a number non-comparable>
  supersedes: ""
  superseded_by: ""
---

# Literature Map

The "what does the literature say" answers of record. A number quoted from a
paper carries the paper's protocol next to it; comparisons across protocols
are labeled as such.

## Entries

```yaml
id: L_000
key: example2026linear
title: Worked example — "Linear-time sequence models for <task>: a controlled comparison"
date: 2026-09-04
proposer: fable
status: proposed                          # not yet read in full by a human
decided_by: ""
evidence: [https://doi.org/10.0000/example]
claim_in_paper: At matched parameter count the linear-time model is within noise of attention at short context and faster at long context.
relation: neighbour
our_claim: H_000
verified: {how: abstract-only, on: 2026-09-04, by: fable}
scope_notes: different corpus and split protocol from ours — numbers are not directly comparable; only the qualitative finding transfers.
supersedes: ""
superseded_by: ""
```
