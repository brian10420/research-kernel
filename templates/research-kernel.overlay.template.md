# research-kernel project overlay

<!--
Copy this file to `.claude/research-kernel.overlay.md` at the root of YOUR research
project and fill the slots. Every research-kernel skill injects this file when it
loads (the wrapper runs `cat ${CLAUDE_PROJECT_DIR}/.claude/research-kernel.overlay.md`);
isolated roles receive it through the dispatch prompt. This is the ONLY place
project-specific facts belong — never edit the plugin or the generated wrappers,
they are replaced wholesale on every update.

Conventions: keep metric NAMES, put VALUES in the project's state files
(EXPERIMENT_LEDGER.md, RESEARCH_STATE.md) and point at them; no secrets, no
credentials, nothing you would not commit to the project repository itself.
-->

## Project

- **Name:** <project-name>
- **One-line goal:** <what the research is trying to establish>
- **State files:** `<path>/RESEARCH_STATE.md`, `<path>/DECISIONS.md`, `<path>/EXPERIMENT_LEDGER.md`, `<path>/HYPOTHESES.md`, `<path>/FAILED_IDEAS.md`, `<path>/OPEN_QUESTIONS.md` (seeded from `templates/project-state/`)
- **Notes vault / Study Log:** <path or "none">
- **Deadline:** <date or "none">

## Slots by role

Fill only the roles you use; delete the rest. Each role spec ends with a
"Project overlay slots" section listing exactly what it expects.

### math-reviewer
- Pinned invariants: <mask convention, shape contracts, numerics guards>
- Domain signal math / transforms in use: <e.g. STFT settings, filters, normalisations>

### dl-engineer
- Code map: <where models, data, training loop, tests live>
- Behavioral test suite to run after changes: `<command>`
- Mixed-precision / hardware constraints: <e.g. bf16, single-GPU VRAM ceiling>

### research-mentor
- Locked story and claims that must not be re-inflated: <list>
- Protocol of record: <evaluation protocol name + primary metric>

### results-analyst
- Committed analysis generators: <paths>; figures are regenerated, never hand-edited
- Where numbers of record are collected from: <log line / file>
- Statistical conventions: <bootstrap unit, equivalence bounds, seeds>

### paper-writer
- Manuscript paths: <main.tex, sections, bib>; build command: `<latexmk …>`
- Headline numbers and their sources: <metric name → state-file row>
- Honest-framing guardrails: <claims deliberately downgraded; phrasings to keep>

### study-coach
- Study Log path: <vault path>
- Language policy: <e.g. English with a one-point escape hatch>

### science-presenter
- Presentation log path: <path>; output folder: <path>
- Number guards to carry verbatim: <list or pointer>

### memory-curator
- Memory location and what may live there: <recall-only facts>

### blind-reviewer (isolated — passed in the dispatch prompt, not read from disk)
- Anonymized bundle path: <output of tools/anonymize.py>; target venue: <venue>

### experiment-runner (isolated)
- Launch commands and protocol block (verbatim): `<command>`
- Process rule: <e.g. setsid nohup; never harness-background for long runs>
- Where results are collected from: <log pattern>

### regression-guardian (isolated)
- Full suite command: `<command>`; invariants to probe adversarially: <list>

### repo-maintainer (isolated)
- Remote: `<owner>/<repo>`; **never-push list:** <paths that must never reach the remote>
- Large-artifact / ignore rules: <summary>

## Effort protocol (session-level)

Roles never pin `max`. When a step needs unbounded judgement (interpreting a
blind readout, resolving a record-vs-code contradiction, designing a new
statistical instrument), the role stops and asks the operator to run
`/effort max`, and asks for `/effort high` (or the session default) when the
step is done. "Stuck" is handled by changing method first (restate the claim
as a checkable test; dispatch a fresh-context role), not by raising effort.
