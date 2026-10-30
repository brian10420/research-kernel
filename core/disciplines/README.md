# Disciplines — field cards for research that crosses into another field

A discipline card holds what a researcher from outside a field needs before a
draft or a review touches it: how that field weighs evidence, which words mean
what there, what its reviewers ask, and what its ethics require. Cards are
cross-project and generic; a project names the cards it uses in its overlay
(`## Disciplines`), and the `conductor` passes their paths into the briefs of
the stages that touch the field.

**No cards yet.** This file fixes the format only.

## Card format

One file per field, `core/disciplines/<field>.md` (kebab-case field name).

```markdown
---
schema: research-os/discipline-card/v1
field: <field name>
proposer: human | fable | astra | other-model:<name> | joint:<list>
date: YYYY-MM-DD
decided_by: human | ""
status: proposed | accepted | rejected | superseded
evidence: [<sources the card rests on>]
supersedes: ""
superseded_by: ""
---

# <Field name>

## Evidence conventions
- What counts as evidence here, which designs and statistics reviewers expect,
  effect-size and reporting conventions. Each item: one line + its source.

## Terminology
- term — meaning in this field — the near-miss term it must not be confused
  with (source).

## What reviewers in the field ask
- The questions a referee from this field raises first (source or venue).

## Ethics and consent norms
- Approval, consent, data-handling and reporting duties specific to the field
  (source).

## Methodology switch
- quantitative / qualitative / mixed: what changes in the evidence conventions,
  the reporting and the review questions under each (source).
```

## Rules for cards

- **Every item carries a source**, verified the way `LITERATURE_MAP.md` entries
  are (`verified: {how, on, by}`); an item without one is marked unverified.
- **A model-written card enters as `status: proposed`** with model provenance
  (SCIENTIFIC_RULES principles 2–3); only the human operator moves it to
  `accepted` or `rejected`.
- **No project facts** (DECISION_001): a card describes the field, never a
  project's data, numbers or claims.
- A card advises a draft or a review; it never overrides `SCIENTIFIC_RULES.md`,
  a `DECISIONS.md` entry or a role's hard rules.
