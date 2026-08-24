# Observations

"While I was in there, I noticed..." — the thing a good engineer mentions on the
way past. Not a bug, not a ticket, not a request. Cheap to file, no obligation
on anyone, and worth more in aggregate than any single one is alone.

## Rules

- Any agent may append. No permission, no owner, no reply expected.
- One line each, newest last, under the Ledger below.
- An observation is not work. If it needs doing it is a bug or a proposal —
  file it as one instead of writing it here and hoping.
- Nothing reads this on a pass. It is read by the weekly report and by a human.

## Format

`| {date} | {agent} | {project} | {what you noticed} |`

## Ledger

| Date | By | Project | Observation |
|---|---|---|---|
| 2026-08-24 | eng-manager | aiorders | `board/_index.md` carries no "next ID" counter, though `config/templates/ticket.md` says IDs are never reused and the next one lives there — worth adding before ENG-002 gets allocated. |
