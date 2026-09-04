# Handoff prompt — <lane name> session
*(paste the block below into a fresh session in `<project-dir>`)*

---

/<skill-name>

RULES_HASH=<paste the hash from CLAUDE.md / AGENTS.md — `python3 tools/sync.py --hash`>
Role spec: paste the FULL text of `core/roles/<role>.md` here — never rely on
the runtime having loaded it (SCIENTIFIC_RULES §3). Expected first reply line:
`ACK RULES_HASH=<the same hash>`; a reply that starts otherwise means the rules
did not load — stop and re-dispatch.

Lane: <lane name and one-line purpose>. Continue from <the persistent state
this lane keeps — a study log, a campaign memory block, a TODO file> — read it
first, then <the lane's default opening move>.

Boundaries: <what this lane does NOT do — one line per adjacent lane, naming
where those requests go instead>. <Any standing project-wide notes every lane
must carry — e.g., deadline status, launch authorization state.>

---

<!-- Why this exists: multi-session projects rot when each session re-derives
context. A one-screen handoff with a scope fence keeps lanes from bleeding
into each other and keeps standing decisions (deadlines, authorizations)
propagating. Keep one of these per lane, dated, in your docs/. -->
