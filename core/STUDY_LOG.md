---
schema: research-os/study-log/v1
scope: cross-project schema + one worked example. A project's live Study Log usually lives in its notes vault (seed it from templates/STUDY_LOG_TEMPLATE.md).
purpose: >
  The learner's persistent record: curriculum arcs, sessions, quiz results, and
  the weak-spot queue — so learning survives across sessions and the study-coach
  never re-derives where the learner is.
session_template: |
  date: YYYY-MM-DD
  topic: <one topic>
  layers_reached: intuition | formalism | defense       # the highest layer completed
  sources: [<notes / files the session was grounded in>]
  quiz: {asked: <n>, correct: <n>, weak_spot_item: <id or "none">}
  new_weak_spots: [<short labels>]
  retired_weak_spots: [<short labels>]
  paper_recommended: <key or "none">
  next_up: <topic>
  updated_by: study-coach | human
---

# Study Log

Joint note: the study-coach appends after each session; the learner may edit
anything. Grading is honest — a wrong answer is recorded as wrong.

## Goal (current arc)

> <One sentence: what the learner should be able to DO when this arc is done.>

## Curriculum

- [ ] **1. <Topic>.** <scope>. Sources: <notes/files>.
- [ ] **2. <Topic>.** …

## Weak-spot queue

| label | first seen | last reviewed | status |
| --- | --- | --- | --- |

## Sessions (newest first)

```yaml
date: 2026-09-04
topic: Worked example — why validation-only checkpoint selection is a protocol requirement
layers_reached: defense
sources: [core/SCIENTIFIC_RULES.md#4]
quiz: {asked: 4, correct: 3, weak_spot_item: none}
new_weak_spots: ["difference between early stopping on validation vs. on test"]
retired_weak_spots: []
paper_recommended: none
next_up: cluster-level bootstrap — why per-sample CIs are wrong for grouped data
updated_by: study-coach
```
