---
ticket: ENG-028
project: aiorders-admin-hub
status: awaiting-scope
size: M
author: product-manager
created: 2026-09-03
decided:
---

# Foodswipe funnel — staff-configurable pipeline stage set

## Readback

**This ticket has a real quote but no fresh two-reading run, and both facts
are deliberate.** The words below are the approver's own, and the scope was
already narrowed to a single named reading by a question the approver
answered explicitly. `skills/request-readback/SKILL.md` exists to catch two
careful readers disagreeing about ambiguous raw input; the ambiguity here
was already found, asked, and closed. So this is a readback-equivalent —
same job, different evidence — following the precedent set on `ENG-027`.

**You said,** verbatim, replying to `ENG-013`'s merge request
(2026-09-01T17:13:54):

> "You added manual update of stage to the card what about the funnel
> stages itself on the page, if I want custom pipeline flow stages not
> just per card. This ticket was meant to allow custom pipeline stages for
> the whole foodswipe funnel, the stage updates per card can be manual or
> automatic."

**And you then chose how it ships.** That reply was genuinely ambiguous
between shipping the built piece and filing the larger ask separately,
versus holding everything for one combined ship — so it was asked rather
than guessed (`inbox/2026-09-02-eng013-stage-config-question.md`) and
answered **approved / "Reading a approved"** on 2026-09-03T15:23:36: merge
`ENG-013`'s two PRs now, and file stage-taxonomy configuration as a new,
separate ticket built on top. That question's own closing line deferred
the design — "a new admin screen, ordering, whether stages can be deleted
once in use, etc." — to this ticket's design round. This PRD respects
that: it describes capability, not screens or schema.

**Understood as:** `ENG-013` made a card movable within a board whose
columns are fixed in code. You want the columns themselves to be yours.
The Foodswipe funnel should present the pipeline your sales and onboarding
team actually runs — stages you can add, name, order and remove — rather
than the six onboarding milestones the codebase happens to compute.
Per-card stage assignment stays exactly as `ENG-013` built it and is not
reopened here; what changes is that the set of stages a card can sit in
becomes something staff define instead of something an engineer deploys.

**Assumed, and worth correcting if wrong** (only the ones that change the
build):

- **The six stages that exist today survive this change** — same names,
  same order, same listings in them, and each still assigned
  automatically by the same signal it uses now. This is a migration of a
  hardcoded list into configuration, not a blank slate the team has to
  repopulate. If you'd rather start empty and define the pipeline from
  scratch, say so — it's a materially different first day for the page.
- **Stages you add beyond those six are manual-only.** This is the one
  that matters most, and it deserves saying plainly. Checked in code, not
  assumed: `classifyStage()` is a fixed if/else chain over specific
  database columns — has a name and phone, has a restaurant row, has
  menus, has Google Business Profile shared, has website interest. There
  is **no generic rule concept** anywhere in the system. A stage you
  invent has no signal attached to it, so nothing could ever put a card
  there automatically. Your own words say "the stage updates per card can
  be manual or automatic," which reads most plausibly as: the originals
  keep their automatic behaviour, new ones are set by hand. **If you meant
  that you should also be able to define the *conditions* under which a
  custom stage is auto-assigned, this is a much larger ticket** — that's a
  rules engine, not a config screen, and it should be split rather than
  absorbed.
- **One pipeline, shared by everyone.** Not per-user, per-role, or
  multiple boards. Nothing in your words suggests otherwise; cheap to say
  now, expensive to discover mid-build.
- **This is the Foodswipe funnel only.** The Brands page's own
  client-stage concept is a different page tracking a different thing,
  and this ticket does not touch or unify with it.

**Second reading: none run, deliberately.** There is no fresh raw input to
read two ways. Your reply above is unambiguous about *what* you want; the
only genuine ambiguity it carried was about sequencing, and that was asked
and answered rather than averaged. The code grounding under "Risks" below
did the job a second reading normally does — it turned "can custom stages
be automatic?" from a guess into a checked answer.

## Approver's `changed` response (2026-09-06T09:09:08Z) — hardcode a named stage set, drop the config screen

**The answer** (`inbox/2026-09-03-eng028-g1-scope.md`, `decision: changed`,
decided 2026-09-06T09:09:08.947929+00:00), in full:

> "Lets hard code stages Make new stages waitlisted, contacted, meeting
> scheduled, Follow Up,Onboarding,Not Interested,On Hold, activated,Upsell.
> Can we have autopilot email/sms setup on admin panel like brand portal for
> each stage update"

Two clauses, doing two different things. The first rejects this ticket's
whole premise and answers it with something smaller. The second is a new
ask this ticket's own Non-goals already named and pointed elsewhere.

**Clause one: no config screen. Hardcode this exact list, replacing the six
that exist today.** "Let's hardcode stages" answers the one question this
G1's readback asked most plainly — config screen or a literal list — and
lands on the cheaper side this PRD's own Risks section named as "the
strongest argument against this ticket." The named set, in the order
given: **Waitlisted, Contacted, Meeting Scheduled, Follow Up, Onboarding,
Not Interested, On Hold, Activated, Upsell.**

**Checked against the live code, not assumed.** The six stages this ticket
was built to make editable are `account_created`, `profile_updated`,
`listing_claimed`, `menu_uploaded`, `gbp_shared`, `website_interest`
(`aiorders-api` `admin-portal/handlers/foodswipe.ts`'s `Stage` union and
`VALID_STAGES`, mirrored in the `foodswipe_stage_override` `CHECK`
constraint and in `aiorders-admin-hub`'s `STAGES` display array). **None of
the nine new names correspond to any of the six old ones.** The old set
names data-completeness milestones a listing passes through automatically
(has a name and phone, has a restaurant row, has menus, shared their
Google Business Profile, showed website interest); the new set names
sales-conversation progress a human has with a lead (contacted, a meeting
scheduled, followed up, onboarded, gone cold, parked, converted, sold
further). Nothing in `profiles`, `restaurants`, or the listing data this
handler already reads could ever detect "a meeting was scheduled." This is
not a renaming of the same six ideas; it is a different pipeline replacing
them.

**What that means for `classifyStage()`, said plainly rather than left
implicit: automatic classification is retired for this funnel.** Proposed:
every one of the nine new stages is staff-set only;
`foodswipe_stage_override` (or its successor column — naming is the
architect's call at `designed`) stops being an *override* of a computed
default and becomes the only stage a listing has; `classifyStage()`'s
if/else chain is deleted rather than kept as dark code behind a column
nobody computes from anymore. This is the most literal reading of "let's
hardcode stages" — it is also a bigger functional change than it sounds,
because the funnel page has never operated without automatic
classification since `ENG-013` shipped it, and it is the single thing on
this rescope most worth the approver correcting if it's wrong. **If
instead the six originals should keep auto-classifying alongside the nine
new manual ones, that's a dual-taxonomy system, not a hardcode** — a
materially bigger, different ticket, not this one.

**What happens to a listing sitting in one of the six old stages today has
no principled answer, so one is proposed rather than guessed.** There is no
honest mapping from "has shared their Google Business Profile" to "Meeting
Scheduled" — the two vocabularies don't correspond, so any mapping this
PRD invented would be a guess wearing the shape of a migration. **Proposed:
every existing Foodswipe listing starts at `Waitlisted`** (the new
pipeline's own first stage) when this ships, and staff move each one
forward by hand as they work it. This is a real, visible change on ship
day — every listing's displayed stage moves, where this PRD's own original
acceptance criteria promised the opposite ("a migration, not a reset") —
named here as the second thing most worth correcting rather than folded
quietly into the acceptance criteria below.

**A trade worth stating outright, since the approver is the one accepting
it.** The original ticket's entire premise was that a future pipeline
change would cost nothing — no engineer, no deploy. Hardcoding again
means a future stage-set change goes back to costing exactly that, same as
today, for whichever list ships here. That is what "let's hardcode" buys
and what it gives up; not hidden in the acceptance criteria below.

**Ordering and display**, lower-stakes, decided rather than asked: the nine
stages are proposed in the order given, as the kanban's column order, with
`Not Interested` and `On Hold` most likely wanting visual treatment as
off-ramps rather than sequential steps (design's call, not G1's). Casing in
the approver's own message is inconsistent (`waitlisted` vs. `Not
Interested`); proposed as Title Case display labels throughout
(`Waitlisted`, `Meeting Scheduled`, ...) over snake_case internal keys,
matching the existing six's own convention — not worth a question.

**Sizing verdict: `M`, down from `L`, one ticket.** What made the original
ticket `L` — a net-new admin management screen, add/rename/reorder/remove
endpoints, and a deletion-semantics question large enough to expect its own
G2 — is exactly the scope this answer removes. What's left is close in
shape to `ENG-013` itself: change a `CHECK` constraint's literal list,
delete a classification function instead of extending it, relabel a
display array, and backfill every existing row to `Waitlisted`. **What
would push this back to `L`:** the dual-taxonomy reading above (old six
auto-classify, new nine sit alongside them), since that keeps
`classifyStage()` alive and adds a real merge/precedence question between
the two systems.

**Clause two: autopilot email/SMS on stage change is this ticket's own
already-named non-goal, and stays split out.** This PRD's Non-goals section
already excluded "automations, notifications, or nurture sequences
triggered by a stage," pointing at `ENG-017`. `ENG-017` doesn't cover this,
though — it nurtures the presignup `leads` table (a different pipeline
with different stages), not Foodswipe `profiles` listings — so the
approver's ask doesn't fold into it. Filed as a new ticket instead, same
split this board already used once for exactly this shape (`ENG-013`'s
broadened ask splitting into `ENG-013` plus `ENG-028`): **`ENG-042`**.
`ENG-042` needs this ticket's final nine-stage list as its own trigger
vocabulary and so carries `depends_on: [ENG-028]` for *building*, but its
own scope is reviewed on its own G1 in parallel — nothing about reviewing
"which stage changes should fire a message" requires this ticket to have
shipped first.

## Problem

Sales and onboarding staff have a Foodswipe funnel page whose columns are
decided in code. Six stage names are bound in four separate places across
two repositories — a TypeScript union type and a validation array in the
API handler, a database `CHECK` constraint, the classifier's own if/else
chain, and a display array in the admin frontend — so changing the
pipeline the team works, in any way at all, is an engineering ticket and
two deploys.

The evidence this is wrong for the team is the approver's own, given
twice. `ENG-013`'s original request already said staff were "not able to
update or have **proper peipleine stages**"; that PRD named the fixed
six-stage set as a proposed assumption and flagged "the six-value set
itself is wrong for how staff work" as a live risk. The G1 approved it
without comment, and the merge reply then said outright that fixed stages
were not what was meant. What nobody has said — and this is worth naming
rather than hiding — is *which* stages are missing. No specific stage
name, no restaurant stuck in the wrong column, no count.

## Why now

Two reasons, one of them structural. `ENG-013`'s two PRs are sitting
unmerged on a Reading A decision whose whole premise is that this
follow-up ticket is real — approving "ship the small thing and file the
big thing separately" is only a good call if the big thing gets filed.
Second, this is the sharpest correction the approver has issued on this
board: a `changed` verdict that contradicts a named assumption the same
approver's own G1 had approved. Acting on it promptly is how the
department demonstrates the correction landed.

Said plainly: no deadline exists, no restaurant is named as stuck, and
nothing breaks tomorrow if this waits. It is not the most urgent thing on
the board — `ENG-022` is.

## Users

AIOrders sales and onboarding staff working Foodswipe-sourced restaurant
signups on the admin panel — the same people `ENG-013` served, and the
approver, who is the one who has actually asked for this. The job that
gets easier: changing how the team tracks onboarding stops being a
request to engineering and becomes something the team does on a Tuesday.
Not the restaurant side, not the consumer "foodswipe customer" identity
(an unrelated concept that shares the brand name), and not the
agency/reseller admin scoping raised separately.

## Proposed change (rescoped — hardcode nine named stages)

**Superseded by the approver's `changed` answer, kept as history rather
than deleted:** the original proposal described a staff-configurable stage
editor — a staff member could open the Foodswipe funnel's stage
configuration, add a stage, rename an existing one, change the order
stages appear in, and remove one, with the funnel page immediately
reflecting that set for every staff member, no engineering change and no
deploy. The six stages the board showed at the time of writing would have
stayed intact, in order, each still classified automatically by the same
underlying signal as before. The approver's `changed` answer rejected this
shape outright — see "Approver's `changed` response" above.

**What ships instead.** The Foodswipe funnel shows nine stages —
**Waitlisted, Contacted, Meeting Scheduled, Follow Up, Onboarding, Not
Interested, On Hold, Activated, Upsell** — hardcoded the same way the
current six are: one literal list, changed by an engineer on a deploy, not
a staff-facing config screen. `classifyStage()`'s automatic derivation is
removed; every listing's stage is set by a staff member using the control
`ENG-013` already built, and every existing listing starts at `Waitlisted`
on the day this ships. No new admin screen, no add/rename/reorder/remove
capability, no deletion-semantics question — the thing that made this
ticket `L` is exactly the thing this answer said not to build.

## Acceptance criteria (rescoped)

**Superseded by the approver's `changed` answer** (kept as history — these
assumed a staff-configurable editor, which was rejected):

1. ~~Given the Foodswipe funnel, when an authorised staff member defines a
   new stage, then it appears as a stage on the funnel page for all staff,
   with no code change and no deploy.~~
2. ~~Given an existing stage, when an authorised staff member renames it,
   then the funnel page shows the new name everywhere, and no listing's
   stage assignment changes as a result.~~
3. ~~Given the configured stages, when an authorised staff member changes
   their order, then the funnel page presents the stages in that order for
   all staff.~~
8. ~~Given a stage that has listings assigned to it, when an authorised
   staff member attempts to remove it, then either the removal is refused,
   or every affected listing is moved to a defined stage as part of the
   same action.~~ (Moot — there is no remove capability in the rescoped
   ticket; the stage list is fixed in code again.)
9. ~~Given a staff-defined stage, when the funnel page renders, then it is
   visually distinguishable as its own column without an engineer having
   authored anything specific for it.~~ (Moot — every stage is
   engineer-authored again.)

**What ships instead:**

1. `[stated]` Given the Foodswipe funnel, when this ships, then the nine
   named stages (Waitlisted, Contacted, Meeting Scheduled, Follow Up,
   Onboarding, Not Interested, On Hold, Activated, Upsell) are present, in
   that order, and the six stages that existed before are gone.
2. `[proposed]` Given any Foodswipe listing that existed before this
   ships, when it first renders under the new stage set, then it shows
   `Waitlisted` — not a computed guess at an equivalent old stage.
3. `[proposed]` Given any Foodswipe listing, when its stage is displayed
   or changed, then no automatic classification runs — `classifyStage()`
   no longer determines any listing's stage, staff do.
4. `[stated]` Given an authorised staff member, when they set a listing to
   any of the nine stages, then the change sticks and is visible to every
   staff member, using the write path `ENG-013` already built — unchanged
   from that ticket.
5. `[inferred]` Given a request to set a listing's stage from a caller
   without admin access to this page, then it is rejected by the same
   authorisation gate the funnel page's existing endpoints already use —
   unchanged from `ENG-013`.
6. `[inferred]` Given the nine-stage list hardcoded in this change, when
   the API's type and validation array, the database constraint, and the
   frontend's display array are compared, then all agree on the same nine
   names — and so does `ENG-042`'s own trigger vocabulary, once that
   ticket builds against this one's shipped list.
7. `[inferred]` Given a listing whose stage was set manually under
   `ENG-013` before this ships, when the new stage set replaces the old
   one, then it resolves to `Waitlisted` (criterion 2) — no listing
   anywhere references or displays a stage that is not one of the nine.

## Non-goals

**Superseded by the approver's `changed` answer:** a staff-facing config
screen to add, rename, reorder or remove stages was this ticket's original
subject, not its non-goal — the answer rejected that capability outright;
wanted later, it is a new ticket, not a re-opening of this one. Keeping the
six old stages or any automatic classification alive alongside the new
nine is also now out of scope, per the dual-taxonomy note above, unless
the approver says otherwise on the fresh G1.

**Unchanged:**

- **Making the automatic classifier itself configurable.** Moot — the
  classifier is deleted, not made configurable.
- **Changing how a listing's stage is set per card.** `ENG-013` built that
  and it is not reopened.
- **Editing a listing's underlying details** (name, phone, email,
  restaurant info) — inherited unchanged from `ENG-013`.
- **Per-user, per-role, or multiple parallel pipelines.** One shared stage
  set.
- **Any other board's stage concept**, including the Brands page's
  client-stage work. Different page, different object, no unification
  here.
- **A history or audit trail of stage-set changes** — who set what, when.
  Not asked for; a real feature if wanted later.
- **Backfilling or reclassifying existing listings onto a plausible
  equivalent old-to-new mapping.** No such mapping exists (see "Approver's
  `changed` response" above); every existing listing resets to
  `Waitlisted` instead.
- **A pre-signup / cold-lead pipeline.** Still `ENG-017`'s territory —
  unaffected by this rescope, a different table entirely (`leads`, not
  `profiles`).
- **Automations, notifications, or nurture sequences triggered by a
  stage.** Filed as **`ENG-042`**, not `ENG-017` — `ENG-017` is scoped to
  the presignup `leads` pipeline, a different set of stages on a different
  table; the Foodswipe funnel's own stage-triggered automation is its own
  ticket.

## Risks and unknowns (rescoped)

**Resolved by the `changed` answer, kept for the record:** the
config-screen risks below no longer apply — there is no config screen, no
add/rename/reorder/remove capability, and therefore no deletion-semantics
question and no expected G2. `ENG-013`'s two PRs have since merged and
`ENG-013` reached `verified`, so the unmerged-sibling risk is also closed.
`ENG-022` (`P0`) has since shipped and verified, so it no longer competes
for the approver's attention against this ticket.

**Current:**

- **Automatic classification is retired, and that's a bigger change than
  it reads.** The funnel page has never operated without `classifyStage()`
  since `ENG-013` shipped it. Deleting it, and resetting every listing to
  `Waitlisted`, is the proposal — not yet the confirmed answer. This is
  the single thing on this rescope most worth the approver correcting if
  wrong (see "Approver's `changed` response" above).
- **The reset-to-`Waitlisted` migration is a visible change on ship day,**
  not an invisible one — every listing's displayed stage moves. Framed
  plainly rather than folded quietly into the acceptance criteria.
- **`ENG-042` (the autopilot ask, split out) depends on this ticket's
  final stage list.** A stage rename after `ENG-028` ships would require a
  matching change in `ENG-042`'s own trigger vocabulary — the same shape
  of coupling the original PRD flagged against `ENG-017`, now narrower and
  one-directional instead of open-ended, since the list is fixed again
  once this ships rather than perpetually editable.
- **A future ticket that changes this nine-stage list again inherits the
  same hardcode-in-four-places cost this rescope accepted** — the
  `changed` answer traded the config screen's maintenance burden for the
  original problem's engineering-and-deploy tax, on a possibly different
  list next time. Named in "Approver's `changed` response" above as the
  trade the approver is accepting, not hidden here.
- **Nothing yet confirms whether `classifyStage()` has any other caller or
  test depending on it** — a grep before deletion is build-time work
  (step 6b of this loop), not a G1 concern, but named so whoever builds
  this doesn't assume a clean delete without checking.

## Cost (rescoped)

- **Build: `M`** — half a day to a couple of days, down from `L`. What
  earned the `L` — a net-new management screen, add/rename/reorder/remove
  endpoints, and a deletion-semantics question large enough to expect its
  own G2 — is exactly the scope the `changed` answer removed. What's left
  is close in shape to `ENG-013` itself: rewrite the `CHECK` constraint's
  literal list, delete `classifyStage()` instead of extending it, relabel
  the display array, and backfill every existing row to `Waitlisted`.
  **What would push it back up:** the dual-taxonomy reading (old six keep
  auto-classifying alongside the new nine) — that keeps `classifyStage()`
  alive and adds a real precedence question between two live systems.
- **What it displaces:** the single machine WIP slot, for a fraction of
  the run the original `L` would have asked for. `ENG-022` has since
  shipped and verified, so it no longer competes for the approver's
  attention — nothing currently on the board outranks this if the
  approver wants it started next.
- **Run: `$0`/month.** Unchanged — same Supabase project, same Cloudflare
  Worker deploy target, no new vendor, no new infrastructure.

## Recommendation (rescoped)

**Build the approver's version now, one ticket, `M`, and expect no G2.**
The scope that made this `L` and earned a G2 is gone; what remains is a
same-shaped, smaller sibling of `ENG-013`. **One thing flagged rather than
buried:** this rescope proposes retiring automatic classification outright
and resetting every existing listing to `Waitlisted` — the single answer
most worth the approver correcting on the fresh gate, since a "keep the
six auto-classifying too" answer would send this back up to `L` for a
materially different, dual-taxonomy ticket. The autopilot ask in the same
reply is real and has been shaped as its own ticket, `ENG-042`, rather than
folded in here or assumed to fit `ENG-017`.

## The 5-question filter, answered honestly (rescoped)

*(Board practice, per `ENG-027`'s PRD — same content as the standalone
filter check.)*

1. **Off the plate or onto it?** Off, on net, from where the original
   scope stood — no screen for anyone to own or maintain. Reintroduces the
   engineering-and-deploy tax the original ticket was trying to remove,
   for whichever list ships here; that trade is the approver's to accept,
   named above rather than hidden.
2. **Freedom created or removed?** Removed, compared to the config-screen
   version: staff can no longer add or rename stages themselves. Compared
   to *today* (six fixed stages), freedom is created once — a different,
   more useful fixed list — and then fixed again.
3. **Current or anticipated?** Current — a direct answer to a direct
   question, not speculative.
4. **What does it displace?** The single machine WIP slot, for roughly the
   same band `ENG-013` itself asked for. Nothing at the approver's desk
   competes for attention now that `ENG-022` has shipped.
5. **Would not building it be fine?** No — the six stages in code today are
   the ones the approver has twice said are wrong; this answer is how they
   get fixed, just not the way originally scoped.

**Filter verdict: build it, `M`, no G2 expected — and confirm the
automatic-classification call before starting, since it's the one thing
that would change the size again.**

## Decision

Filled in by the approver.

- **The approver's answer:**
- **Date:**
- **Notes:**
