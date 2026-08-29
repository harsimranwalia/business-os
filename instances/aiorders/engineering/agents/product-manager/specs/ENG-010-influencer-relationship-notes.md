---
ticket: ENG-010
project: aiorders-admin-hub
status: awaiting-scope
size: S
author: product-manager
created: 2026-08-29
decided:
---

# Influencer relationship notes — staff log for personality, preferences, and off-platform conversations

## Readback

**You said:** "potentially add notes by the staff to collaborate on the
influencer and see how their personality is or what they want/like or what
conversations have happened with them off the platform. we want our
community mangers(staff) to be able to more easily use these influencers
for our restaurant campaings." (a rider on `ENG-009`'s own G1 answer,
`inbox/2026-08-29-eng009-g1-scope.md`)

**Understood as:** Staff need a shared, running log on each influencer's
admin record — not a single overwritable field — where any staff member can
add a note about that influencer's personality, preferences, or a
conversation that happened off-platform (DM, call, in person), and every
other staff member can read the accumulated history. The goal is
continuity: relationship knowledge currently trapped in one community
manager's head or inbox becomes visible to whoever picks up that
influencer for the next campaign.

**Assumed, and worth correcting if wrong:**
- Entries accumulate (a log), each carrying its author and timestamp —
  "collaborate" and "conversations have happened" (plural, ongoing) both
  point at multiple contributions over time, not one field one person
  overwrites.
- **Staff-only, and specifically never visible to the influencer being
  described.** Influencers are themselves authenticated AIOrders users
  (an existing `user_id` on the influencer record, per `ENG-008`'s own
  design evidence) — this isn't a hypothetical risk, there's a real
  account that could reach this data if the write/read path isn't scoped
  to staff the same way the rest of the admin board already is.
- Attached to the influencer's own record, not to a specific campaign —
  the value is knowing the person across every campaign they're
  considered for, not per-campaign.
- Freeform text, not a structured field — distinct from `ENG-008`'s
  region/campaign-type/rating and `ENG-009`'s activity/engagement
  signals, which are separate, already-scoped structured data.
- Manual entry only. Nothing here reads from Meta, email, or any external
  system — same boundary `ENG-009` already drew for its own social figure.

**Second reading agreed / diverged on:** Two independent readings were
run — this PM's, and, blind to it, the architect's (a subagent given only
the raw request, `knowledge/business-profile.md`, and `config/projects.md`,
model `opus` per the skill). **No material divergence** — both converged
on the core shape: a multi-entry, authored/timestamped notes log on the
influencer record, staff-only, never influencer-visible, freeform,
attached to the influencer rather than a campaign. The architect's reading
added technical texture rather than disagreement: it named the concrete
mechanism the influencer-visibility risk runs through (the `user_id` on
the influencer record), flagged that admin-hub also serves brand/agency/
reseller roles who arguably shouldn't see internal staff notes either
(not stated in the request either way — carried into Non-goals/Risks
below rather than guessed at), and flagged that notes should surface
where staff actually pick an influencer for a campaign, not sit on a
buried tab. Per the skill's own classification table this is "same
picture, different words" / additive texture — fine, proceed, not a fork
to ask about.

## Problem

Community managers build up real knowledge about an influencer —
personality, preferences, what's been discussed off-platform — but today
that knowledge lives only in the individual manager's memory or private
messages. When a different staff member (or the same one, later) needs to
activate that influencer for a restaurant campaign, that context doesn't
transfer, so influencers get re-learned or mishandled every time staff
turnover or workload shifts who's running a given campaign.

## Why now

Raised by the approver in the same conversation as `ENG-009`'s scope
answer, immediately after describing the admin-side data `ENG-008` adds —
read as a direct continuation of the same influencer-management request,
not a separate ask arriving cold. `[proposed]` sequencing: build after
`ENG-008` (and likely after `ENG-009`), since all three touch the same
admin-UI file and the same influencer record — avoids a needless merge
conflict; the EM's call at `ready`, not decided here.

## Users

AIOrders staff (community managers) operating the admin panel. Not
influencer-facing — this ticket adds nothing an influencer can see about
themselves. Whether brand/agency/reseller admin-hub users should see
these notes is an open assumption — see Risks.

## Proposed change

After this ships, any staff member viewing an influencer's admin record
can read every note previously left about that influencer (who wrote it
and when) and add a new one. Nothing else on the influencer record
changes.

## Acceptance criteria

1. `[stated]` Given an influencer's admin record, when a staff member adds
   a note, then it's saved with that staff member's identity and a
   timestamp.
2. `[inferred]` Given an influencer with existing notes, when any staff
   member opens that influencer's admin record, then they see every prior
   note, newest first, each showing its author and when it was added.
3. `[inferred]` Given multiple staff members over time, when each adds a
   note, then all notes accumulate — no note overwrites or removes a
   previous one.
4. `[inferred]` Given an authenticated influencer session (not staff),
   when that request reaches the notes read or write path, then it's
   rejected — same authorization boundary as the rest of the admin
   portal, and the negative case is explicitly tested given influencers
   are themselves platform accounts.

## Non-goals

- Editing or deleting another staff member's note — not asked for; if
  wanted, that's a follow-up once this ships and the gap is felt.
- Any structured/typed categorization of notes (call vs. DM vs. meeting)
  — freeform text only, per the raw request.
- Any automated ingestion from DMs, email, or a social platform — manual
  entry only, same boundary `ENG-009` drew for its own social figure.
- Notifications, mentions, or assignment on a note.
- Whether brand/agency/reseller admin-hub roles (distinct from AIOrders
  staff) can read these notes — genuinely unresolved, see Risks; this
  ticket defaults to staff-only until answered.
- Search/filter over note contents — read as a flat chronological log
  for now; searchability is a reasonable future ask, not this ticket.

## Risks and unknowns

- **Influencer-visibility is the one thing this ticket cannot get wrong.**
  Influencers hold real AIOrders accounts (`user_id` on the influencer
  record, confirmed independently by both readings) — candid staff
  commentary about a person, readable by that same person, is the
  concrete failure mode the architect must design against, not a
  theoretical edge case.
- **Whether brand/agency/reseller admin-hub roles should see these notes
  is unresolved.** Neither reading could settle it from the text — the
  raw request says "staff" and "community managers" throughout, which
  reads as internal AIOrders employees, not the restaurant-side or
  reseller-side accounts the admin hub also serves. Defaulting to
  AIOrders-staff-only is the lower-risk choice (easy to widen later,
  harder to walk back after a reseller has seen internal commentary about
  an influencer) — flagged rather than silently assumed, correct here if
  wrong.
- **Notes about a real, identifiable person, in Canada** — deletion and
  data-subject-access questions exist the moment this ships, even for an
  internal tool. Not blocking this small a ticket, but worth the
  architect naming a deletion path rather than assuming one is never
  needed.
- No stated deadline.

## Cost

- Build: `S` — one new table (author, timestamp, influencer reference,
  freeform text), a small read/write surface reusing the existing
  admin-auth gate, and a notes section added to the same influencer
  detail view `ENG-008`/`ENG-009` are already extending.
- Run: `$0/month` — no new vendor.

## Decision

Filled in by the approver.
