# Creating skills with TDD

The `study-coach` skill in this repo was not written from imagination — it was
written against an observed baseline failure, then verified. The process is
test-driven development applied to process documentation (we followed the
`writing-skills` skill from Anthropic's superpowers plugin; mattpocock's `tdd`
skill teaches the same cycle for code).

## RED — watch the agent fail first

Before writing a word of the skill, we gave a plain agent (no skill) the exact
request the skill would face: *"be my study coach: teach me something today
and quiz me."*

The baseline produced an impressive-looking failure: it opened with the
hardest statistical material in the project, delivered a ~1,500-word wall of
expert-density prose, ended with a 7-question closed-book quiz including trap
questions — on day 1 — and never looked for any record of what the learner had
already studied. Accurate content, wrong shape: it taught *at* an examiner's
level, not *to* a learner.

Naming the failure precisely is the whole value of RED. "Be a good tutor" is
not a spec; "do not open with graduate-level statistics walls and 7-question
trap quizzes on day 1" is.

## Match the form to the failure

This was a *shaping* failure (wrong output shape), not a *discipline* failure
(rule defiance). Prohibition lists backfire on shaping problems — an agent
under a competing incentive negotiates with "don't". So the skill was written
as a **positive session contract**: read the log → ONE topic → three layers
with stops → 3–5-question quiz → update the log. A contract leaves nothing to
negotiate: the output matches the stated shape or it doesn't.

The named baseline failure stays *inside the skill* as a warning landmark:
"the baseline failure mode this skill exists to prevent: …".

## GREEN — verify with the skill present

Same request, skill loaded. The agent: read the study log first, proposed the
foundations topic from the log's "Next up", taught only the intuition layer
(~350 words) then stopped for the learner to explain it back, cited the exact
note to reread (after checking it exists), deferred the quiz to session end,
and described the log update it would make. The behavioral flip is the
evidence the skill earns its place.

## REFACTOR — when needed

If the GREEN run had shown a new failure (e.g., quiz creep back into turn 1),
the fix goes into the contract and the scenario re-runs. Fact-refresh edits to
an already-verified skill don't need pressure re-tests — but any *behavioral*
wording change does.

## Cost note

The full ceremony (multiple pressure scenarios, 5+ reps per wording variant)
is right for discipline-enforcing skills. For a role/recipe skill on a solo
budget, one honest baseline + one verification run caught everything that
mattered. Scale the ceremony to the stakes; never skip RED entirely — if you
didn't watch an agent fail without the skill, you don't know the skill teaches
the right thing.
