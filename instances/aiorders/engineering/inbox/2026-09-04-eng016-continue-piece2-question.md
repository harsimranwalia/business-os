---
type: eng-decision
agent: product-manager
gate: intake-question
project: config-site-builder
ticket: ENG-016
recommendation: Piece 1 shipped and verified — all 13 criteria pass, no scope creep, $0/month as estimated. Proceed to Piece 2 (catering package & price book) only once you've named who maintains each restaurant's price book; hold otherwise. Does not block anything currently in flight — answer when convenient.
raised: 2026-09-04
notified: 2026-09-04T10:58:06
nudged: 2026-09-05T09:31:45
---

# Continue to Piece 2 (catering pricing/price-book) — and who maintains it?

**Context.** `ENG-016` (structured catering order capture + stage
automation, Piece 1 of the catering quote generator) just passed its own
acceptance-check — all 13 criteria verified against the live merged code
across all three repos, no scope creep, cost matched the `$0/month`
estimate. Full detail:
`agents/product-manager/notebook/2026-09-04-eng016-acceptance.md`.

**Why this is a question rather than an automatic next step.**
`skills/acceptance-check/SKILL.md` step 6b auto-files the next item in a
named sequence only when this ticket's *own* G1 explicitly re-affirmed
continuing the whole sequence — the bar `ENG-006`'s G1 set ("the proposed
five-ticket sequence stands as shape to file incrementally"). `ENG-016`'s
G1 answer was "Lets start with piece 1" — read plainly, at the time it was
answered, as confirming build order rather than pre-authorizing what comes
after. That reading doesn't clear 6b's bar, so this is asked rather than
assumed.

**This isn't a plain yes/no.** The PRD's own Recommendation section holds
Piece 2 on a second, separate condition: *"Piece 2 specifically should hold
until the approver answers who maintains each restaurant's price book."*
Piece 2 would add a per-restaurant package/price-book that someone has to
author and keep in sync with the menu — operator time, ongoing, with no
owner named anywhere in the original rewrite. So even a "yes, continue"
needs this answered before Piece 2's own PRD can be written.

**What's already settled, so this isn't re-litigating anything.** Piece 1's
own scope, the two riders it carried (3-vs-2 stage count; fulfillment-value
mapping), and the reason pricing wasn't built first are all already decided
and shipped — see the PRD's "Approver's `changed` response" section if you
want the full history. This question is only about what comes next.

**If yes** — name who maintains each restaurant's price book (you, the
restaurant owner, staff, someone else), and Piece 2 gets filed the same way
Piece 1 was (fresh PRD, readback, its own G1). **If no** — Piece 1 stands on
its own; an owner holding an exact itemized order can already quote it by
phone, which beats today's prose blob. Either answer, `ENG-016` itself is
already `verified` regardless.

## Decision

Filled in by the approver.
