---
ticket: ENG-008
project: aiorders-admin-hub
status: designed
size: M
author: product-manager
created: 2026-08-29
decided: 2026-08-29T09:12:46.283064+00:00
---

# Influencer board admin management — region/campaign-type preference, rating, collaboration count

## Readback

**You said:** "for the influencer board on admin panel we are unable to see
or edit the preference of the influencer in a certain area or update those.
also information on the engagement is missing . influencers should only be
able to see the opportunities available but only be able to apply to ones
they selected for their region. also same thing for the type of campaign
paid or barter. on admin side our staff should be able to rate or add the
number of collaborations the influencer has done with us"

**Understood as:** The influencer board on the admin panel is missing data
staff need to manage influencers: they can't see or set which region(s) an
influencer covers, can't see or set which campaign type(s) (paid or barter)
an influencer takes, can't rate an influencer, and can't track how many
collaborations an influencer has done with AIOrders. Separately, once those
preferences exist, influencers themselves should be able to browse every
open opportunity but only apply to the ones matching their own region and
campaign-type selections. This PRD scopes **this ticket to the admin-side
data (region/campaign-type visibility+editing, rating, collaboration
count) only** — see "Feature shape and sequencing" below for the rest.

**Requirements for this ticket** (admin-side data only — not the
influencer-facing apply gating, not engagement info):

1. `[stated]` Staff can see an influencer's preferred region(s) on the
   admin board.
2. `[stated]` Staff can edit and update an influencer's preferred
   region(s).
3. `[inferred]` Staff can see and edit an influencer's preferred campaign
   type(s) (paid, barter, or both) — the raw request's "also same thing
   for the type of campaign" reads as the same visibility+edit capability
   applied to campaign type, parallel to region.
4. `[stated]` Staff can rate an influencer.
5. `[stated]` Staff can view and update a count of collaborations the
   influencer has done with AIOrders.

**Assumed, and worth correcting if wrong:**
- **"Preference... in a certain area" means regional preference**, read
  together with the second paragraph's "their region." Both independent
  readings converged on this; flagged anyway since the sentence is
  grammatically loose enough to admit another reading.
- **Campaign-type preference allows more than one value** (an influencer
  could accept both paid and barter work) rather than forcing a single
  choice — proposed as the more permissive, easily-narrowed-later default,
  not stated either way.
- **Collaboration count is a manually staff-edited number**, not derived
  from a real collaboration-history ledger — no such ledger exists today
  (see Risks) and "add the number" reads like direct data entry, not a
  computed value.
- **Rating is staff-only** — visible and editable by staff, not exposed to
  the influencer or publicly. Not stated either way; this is the
  lower-risk default and easy to loosen later, harder to walk back once an
  influencer has seen a number.
- **An influencer record and an admin board over it already exist** —
  confirmed by evidence, not assumed (see "Second reading" below).

**Second reading agreed / diverged on:** Two independent readings were
run — this PM's, and, blind to it, the architect's (a subagent given only
the raw request and the business profile, model `opus` per the skill).
Both converged on the core shape: two related but distinct capability
sets (staff-side data management; influencer-side gated browsing), a
shared preference data model (region + campaign type) underneath both, a
rating field, and a collaboration count. Both independently flagged
"engagement" as unresolvable from the text alone — a shared gap, not a
disagreement, and it's being asked as a standing question (see below)
rather than guessed at here.

**One material divergence**, per the skill's own classification a
"different scope" fork: this PM's reading assumed an influencer-facing
apply flow already exists today and is simply over-permissive; the
architect's reading refused that assumption and named "does any
influencer-facing authenticated surface exist at all" as the request's
biggest potential one-way door (a new user/identity class, PII, privacy
law, if the answer is no). Rather than asking the approver a question
answerable from evidence already on disk, checked `aiorders-api`'s
`origin/main` directly and found it already has
`supabase/functions/restaurant-influencer-campaigns/` (with an
`influencer-invitations.ts` handler and its own `utils/auth.ts`),
`supabase/functions/outgoing-communications/actors/influencers.ts`, and
`supabase/functions/migrate-influencer-images/` — real, live backend
surface for the influencer concept. That resolves the fork in favor of
"extend an existing thing," closing the one-way-door risk the architect's
reading correctly refused to wave through, without spending an approver
question on a fact the repo could answer directly. One open thread from
this same evidence, not resolved here: the existing surface reads as
**invitation-based** (a restaurant/staff member invites a specific
influencer to a specific campaign), which is a different access pattern
from "influencer browses all opportunities and applies" — worth a
design-time look when item 4 (below) is actually designed, not a scope
fork for this ticket, which touches none of that code.

## Feature shape and sequencing

The raw request is one message but genuinely more than one piece of work.
Here's the whole shape; **only item 1 is this ticket**:

1. **This ticket (ENG-008)** — admin-side influencer data: region and
   campaign-type preference (view+edit), rating, collaboration count.
   Staff-facing only, no influencer-facing change.
2. **Influencer-facing opportunity visibility + apply gating** — influencers
   see every open opportunity but can only apply to ones matching their own
   region and campaign-type selections. Depends on this ticket (needs the
   preference fields to gate against). `[proposed]`, not yet filed, not yet
   sized — to be filed once this ticket verifies, per the same
   incremental-sequence mechanism `ENG-006`/`ENG-007` established
   (`skills/acceptance-check/SKILL.md` step 6b). This is the other half of
   the same request the approver already made, not new agent-invented
   scope — filing it once ENG-008 ships is finishing what was asked, not
   starting something new.
3. **Engagement info** — scope and cost are genuinely unknown from the raw
   text (could be a simple field or a new paid third-party social-platform
   integration — see Risks). A standing, non-blocking question is already
   with the approver:
   `inbox/2026-08-29-eng008-engagement-source-question.md`. This does not
   block ENG-008. Once answered, it becomes its own small ticket, likely
   sequenced after this one since it touches the same board.

**Recommendation: build ENG-008 now.** It's independently useful to staff
today (rating and collaboration tracking need nothing else to ship), it's
the dependency everything in item 2 needs, and it carries no
influencer-facing risk — nothing an influencer sees or can do changes
until item 2 lands on top of it. If this shape or split is wrong, say so
at this G1 rather than after item 2 gets filed.

## Problem

Staff running the admin panel's influencer board can't see or set an
influencer's region or campaign-type preference, can't rate an influencer,
and can't track collaboration history — so matching an influencer to a
campaign and judging whether they're worth working with again happens
off-system (memory, spreadsheets, DMs), which doesn't scale past a
handful of relationships and leaves no record for whoever picks it up
next.

## Why now

Approver-initiated; no stated deadline. It's also the direct prerequisite
for item 2 (the influencer-facing gating the approver explicitly asked
for in the same message) — building it now is the only way item 2 can
exist at all.

## Users

AIOrders staff operating the admin panel. Not influencer-facing — no
influencer sees or interacts with anything this ticket adds.

## Proposed change

After this ships, staff can open an influencer's record on the admin
board and see/edit their preferred region(s) and campaign type(s), give
them a rating, and see/update how many collaborations they've done with
AIOrders. Nothing an influencer or a restaurant sees changes.

## Acceptance criteria

1. `[stated]` Given an influencer with no region set, when staff set one
   or more preferred regions, then the admin board displays them and they
   persist.
2. `[stated]` Given an influencer with a region already set, when staff
   edit it, then the board reflects the update and the prior value is no
   longer shown as current.
3. `[inferred]` Given an influencer with no campaign-type preference set,
   when staff set paid, barter, or both, then the admin board displays the
   selection and it persists.
4. `[inferred]` Given a campaign-type preference already set, when staff
   edit it, then the board reflects the update.
5. `[stated]` Given an influencer with no rating, when staff set one, then
   the admin board displays it and it persists.
6. `[stated]` Given an influencer with an existing rating, when staff
   change it, then the board reflects the new value.
7. `[stated]` Given an influencer with no collaboration count, when staff
   set or increment it, then the admin board displays the current count
   and it persists.
8. `[proposed]` Given a non-admin/non-staff request to any of the above
   write paths, then it's rejected — this is a staff-only surface, same
   authorization gate as the rest of the admin portal.

## Non-goals

- Influencer-facing opportunity visibility or apply-eligibility gating by
  region/campaign-type — item 2 above, filed once this ticket verifies.
- "Engagement" information of any kind — pending the standing question;
  not this ticket regardless of the answer.
- A structured, timestamped collaboration history/ledger — this ticket is
  a count only; per-collaboration records are a bigger feature nobody has
  asked for yet.
- Any change to the existing invitation-based campaign flow
  (`restaurant-influencer-campaigns`) — found during evidence-gathering,
  untouched by this ticket.
- Influencer self-service editing of their own rating or collaboration
  count — staff-only fields.
- A platform-wide enforced region taxonomy — the architect decides at
  design time whether this needs one or can use free text; either is
  compatible with this ticket's acceptance criteria.

## Risks and unknowns

- **"Engagement" could mean two very different things**: the influencer's
  activity on our own platform (free — already-available or easily
  derived data) versus their social-media stats (follower count,
  engagement rate — a new third-party API integration, likely OAuth, and
  an ongoing cost). Genuinely unresolvable from the raw text; both
  independent readings flagged it, neither guessed. Standing question
  open with the approver, not blocking this ticket.
- **Region granularity is undefined** — city, province, a fixed service
  list, or a radius. Left for the architect; doesn't change this ticket's
  acceptance criteria, only its schema.
- **The existing influencer-campaign backend reads as invitation-based**,
  not an open browsable list — relevant to item 2's design, not this
  ticket's, but worth the architect confirming before item 2 is designed
  so it isn't discovered mid-build the way `ENG-007` found Walletly.
- No stated deadline and no specific influencer or campaign named as
  blocked on this today.

## Cost

- Build: `M` — spans two repos (`aiorders-api` for schema/endpoint,
  `aiorders-admin-hub` for the admin UI), though each individually is a
  small, well-understood CRUD change with no new auth model and no new
  datastore. Rough band: half a day to a couple of days.
- Run: `$0/month` — no new vendor, runs inside the existing `aiorders-api`
  Supabase project.

## Decision

Filled in by the approver.
