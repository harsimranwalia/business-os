---
type: eng-decision
agent: eng-manager
gate: scope
project: aiorders-admin-hub
ticket: ENG-013
recommendation: Reading A — ship the current PRs (per-card manual stage override, already built and passed every gate) and file custom pipeline-stage definitions as a new, separate ticket. It's a materially different, larger capability, and the shipped piece is already independently useful.
raised: 2026-09-02
notified: 2026-09-02T22:34:04
decision: approved
decided: 2026-09-03T15:23:36.496711+00:00
---

# ENG-013 — ship what's built, or hold for custom stage definitions? (one question)

**Context.** `ENG-013` shipped a way for staff to manually override which of
the existing six stages a Foodswipe listing sits in. Your reply to the
merge request said this "was meant to allow custom pipeline stages for the
whole foodswipe funnel" — i.e., defining/editing the stage set itself, not
just assigning a card to one of the fixed six.

**Why this is a question rather than a guess.** The PRD did flag this
exact possibility as a named, proposed assumption ("the existing six-stage
set stays... whether the stage names themselves are wrong is the standing
question") and its own G1 was approved without comment — read at the time
as accepting that assumption. Your reply now says otherwise. What's
genuinely unclear is not *whether* you want custom stages (you do) but
*how this should ship*:

**Reading A:** Merge the two open PRs now — the per-card override works,
is tested, and is useful on its own (staff can already fix a
wrongly-classified card today). File stage-taxonomy configuration as
`ENG-0XX`, a new ticket, built on top of this.

**Reading B:** Hold both PRs. Fold stage-taxonomy configuration into
`ENG-013` itself — no partial ship — and redesign/rebuild before anything
merges.

**Which?** (Either way, the actual design for "how staff define custom
stages" — a new admin screen, ordering, whether stages can be deleted once
in use, etc. — is separate follow-up work either as this ticket's own
next design round or as the new ticket's; not decided by this question.)

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-09-03T15:23:36.496711+00:00

Reading a approved

---

**Processed 2026-09-03**, `decision` event pass (context this file) —
Reading A: `ENG-013`'s two PRs confirmed still open, not merged
(`git`/`gh`, fresh) — stays `blocked`, no reply needed, same shape
`ENG-009`/`ENG-010`'s plain merge requests. Follow-up ticket filed per this
decision's own direction: `ENG-028` (staff-configurable Foodswipe pipeline
stage set), G1 raised (`inbox/2026-09-03-eng028-g1-scope.md`). Full
reasoning on `ENG-013`'s own board file. Journaled in
`agents/eng-manager/config/decision-journal.md`.
