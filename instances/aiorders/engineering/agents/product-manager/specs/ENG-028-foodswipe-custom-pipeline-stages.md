---
ticket: ENG-028
project: aiorders-admin-hub
status: awaiting-scope
size: L
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

## Proposed change

After this ships, a staff member can open the Foodswipe funnel's stage
configuration, add a stage, rename an existing one, change the order
stages appear in, and remove one — and the funnel page immediately
reflects that set for every staff member, with no engineering change and
no deploy. The six stages the board shows today are there when it ships,
in the order they are in now, with the same listings sitting in them, and
each still classified automatically by the same underlying signal as
before. A stage staff add beyond those six is reachable by a staff member
setting a listing's stage by hand, using the control `ENG-013` already
built. Whatever happens to a stage that has listings in it, no listing is
ever left assigned to a stage that isn't on the board.

## Acceptance criteria

1. `[stated]` Given the Foodswipe funnel, when an authorised staff member
   defines a new stage, then it appears as a stage on the funnel page for
   all staff, with no code change and no deploy.
2. `[stated]` Given an existing stage, when an authorised staff member
   renames it, then the funnel page shows the new name everywhere, and no
   listing's stage assignment changes as a result.
3. `[stated]` Given the configured stages, when an authorised staff member
   changes their order, then the funnel page presents the stages in that
   order for all staff.
4. `[proposed]` Given the six stages that exist today, when this ships,
   then all six are present with their current names, in their current
   order, and every listing sits in the stage it sat in before — this is
   a migration, not a reset.
5. `[proposed]` Given one of the six original stages and a listing with no
   manual override, when that listing's underlying data meets the
   condition that stage is classified on today, then the listing is still
   assigned that stage automatically, exactly as before.
6. `[proposed]` Given a staff-defined stage that is not one of the
   original six, when any listing without a manual override is
   classified, then it is never assigned that stage automatically — such
   a stage is reachable only by a staff member setting a listing's stage
   by hand.
7. `[inferred]` Given a listing whose stage was set manually under
   `ENG-013`, when the stage set is changed afterwards in any way, then
   that listing still resolves to a stage that exists on the board — no
   listing anywhere references or displays a stage that is not defined.
8. `[proposed]` Given a stage that has listings assigned to it, when an
   authorised staff member attempts to remove it, then either the removal
   is refused, or every affected listing is moved to a defined stage as
   part of the same action — no listing is silently stranded. (*Which* of
   those two, and whether a third option applies, is a design question,
   not answered here.)
9. `[proposed]` Given a staff-defined stage, when the funnel page renders,
   then it is visually distinguishable as its own column without an
   engineer having authored anything specific for it.
10. `[inferred]` Given a request to define, rename, reorder, or remove a
    stage from a caller without admin access to this page, then it is
    rejected by the same authorisation gate the funnel page's existing
    endpoints already use.

## Non-goals

- **Making the automatic classifier itself configurable.** Staff define
  stage *names, order and existence*; they do not define the conditions
  under which a stage is auto-assigned. There is no generic rule
  mechanism in the system today and building one is a different, larger
  ticket. Named in the readback as the assumption most worth correcting.
- **Changing how a listing's stage is set per card.** `ENG-013` built that
  and it is not reopened.
- **Deciding what the right stages actually are.** This ticket ships the
  capability; choosing the pipeline is the team's to do afterwards. No
  stage names are proposed here.
- **A pre-signup / cold-lead pipeline.** Adding a stage called "Lead" does
  not create records for restaurants that haven't signed up — there is no
  `profiles` row to hang one off. That remains `ENG-017`'s territory.
- **Automations, notifications, or nurture sequences triggered by a
  stage.** `ENG-017` again.
- **Editing a listing's underlying details** (name, phone, email,
  restaurant info) — inherited unchanged from `ENG-013`.
- **Per-user, per-role, or multiple parallel pipelines.** One shared stage
  set.
- **Any other board's stage concept**, including the Brands page's
  client-stage work. Different page, different object, no unification
  here.
- **A history or audit trail of stage-set changes** — who renamed what,
  when. Not asked for; a real feature if wanted later.
- **Backfilling or reclassifying existing listings** beyond preserving
  where they already sit.

## Risks and unknowns

- **A custom stage has nowhere to come from automatically, and that is a
  real limitation, not a detail.** `classifyStage()` maps each of the six
  stages to one specific, hardcoded real-world signal. There is no
  table-driven engine to extend. Criterion 6 proposes that the originals
  stay automatic and anything new is manual-only — which is a coherent
  reading of "the stage updates per card can be manual or automatic," but
  it is a reading. If the approver expects to define a stage *and* tell
  the system when to put cards in it, this ticket is materially larger
  and should be split rather than stretched. Cheapest possible moment to
  find that out is this G1.
- **The `foodswipe_stage_override` CHECK constraint cannot stay what it
  is.** Its own migration comment already predicted this ticket: *"If a
  future ticket changes that stage set, this constraint needs updating in
  the same change or an override could reference a stage that no longer
  classifies automatically."* A constraint hardcoding six literals is
  incompatible with a stage set staff can edit. How integrity is
  preserved instead is the architect's call at `designed`; that it must
  change is not optional, and it is the single concrete reason this
  ticket is bigger than "add a table."
- **Deletion with live data is genuinely unspecified.** Refuse, reassign,
  archive-but-keep-history — each has different consequences for
  listings, for manual overrides, and for anything that later reads a
  stage by name. Criterion 8 constrains the outcome (nothing is stranded)
  without picking the mechanism, deliberately, because the decision that
  spawned this ticket explicitly deferred it. Expect this to be the
  substance of G2.
- **`ENG-017` acquires a moving target.** It is `designed` and nurtures
  leads "to next stages automatically." A stage taxonomy staff can edit
  means the stage a nurture rule points at can be renamed or deleted
  underneath it. Whichever of the two ships second inherits the coupling;
  worth the EM sequencing them consciously rather than by whichever is
  picked up first.
- **`ENG-013`'s PRs are not merged yet.** This ticket builds directly on
  the override column and the funnel write path they introduce. If it
  starts before they land on `main`, it branches from an unmerged sibling
  — and this loop's own review tooling diffs against `main`, not against
  the sibling, so the staleness would not be caught automatically.
- **The strongest argument against this ticket, stated rather than
  buried: nobody has said which stages are wrong.** If the real need is
  three specific extra stage names, adding three literals is hours of
  work and this is days. A configuration capability is the more expensive
  answer to a problem that has never been described in specifics. The
  counter — and the reason the recommendation is still "build" — is that
  the approver asked for the *capability* in those words, twice, and
  building the cheap thing on an inference is precisely what produced
  this ticket in the first place.
- **`aiorders-admin-hub` had 64 uncommitted files in the human checkout as
  of 2026-08-23** (`projects.md`). Merge friction on the frontend half is
  expected, and this ticket rewrites a page `ENG-013` has just also
  rewritten.

## Cost

- **Build: `L`** — several days to a week or more. Two triggers from the
  size table independently: a new data model, and cross-project
  (`aiorders-api` for the taxonomy, the constraint, the classifier's
  output type and the management endpoints; `aiorders-admin-hub` for
  data-driven columns plus a management screen that does not exist in any
  form today). Strictly larger than `ENG-013` (`M`), which extended an
  existing screen with an additive column and one write endpoint. **What
  pushes it to `XL` — i.e. back to the EM to be split:** requiring the
  classifier itself to become rule-configurable; requiring a
  data-migration path for existing override values on deletion; or
  requiring the built-in six to be fully severable from their automatic
  signals.
- **What it displaces:** the single machine WIP slot, currently 1/1 with
  `ENG-024`, for the whole of its run — and at `L` that is the longest
  single occupancy any ticket on this board has asked for. Four tickets
  already at `designed` (`ENG-014`, `ENG-017`, `ENG-023`, `ENG-025`) sit
  behind it. Approver-facing WIP is uncapped since 2026-09-02, so nothing
  is gated at the approver's desk. The honest competitor for attention is
  `ENG-022` — `type: security`, `severity: P0`, cross-tenant PII and write
  exposure on five live handlers, already `designed` and owing only a G2.
- **Run: `$0`/month.** Same Supabase project, same Cloudflare Worker
  deploy target, no new vendor and no new infrastructure — both repos are
  existing L1 registrations with existing deploy paths. Nothing here
  calls a metered API or a model.

## Recommendation

**Build now, one ticket, `L`, and expect a G2.** The temptation is to
build something smaller — and it should be resisted, because the smaller
thing is exactly what `ENG-013` was, and the approver has now said in
their own words that it wasn't what they meant. Repeating that pattern a
second time on the same page would cost more than the difference in size.
Two things flagged rather than buried: **first**, the assumption that
staff-defined stages are manual-only is the single answer most worth
correcting at this gate — if the approver expects to define auto-assignment
conditions too, this becomes a rules engine and should come back to be
split, not stretched. **Second**, this is not the most urgent item on the
board; `ENG-022` (`P0`, live cross-tenant exposure) outranks it, and
`ENG-013`'s two PRs should land on `main` before anyone starts building on
top of them. If the approver's attention is scarce this week, approving
the scope here and sequencing the build behind `ENG-022` costs nothing.

## The 5-question filter, answered honestly

*(Board practice, per `ENG-027`'s PRD — same content as the standalone
filter check.)*

1. **Off the plate or onto it?** Both. Adds a decision someone owns
   forever; removes an engineering tax where a pipeline change today
   means four bindings across two repos and two deploys. Net direction is
   the one that was asked for.
2. **Freedom created or removed?** Creates real freedom and removes some
   permanently — three things that are compile-time-safe today (the CHECK
   constraint, the classifier's output type, hand-authored display
   metadata) become runtime concerns, and `ENG-017` gets a moving target
   underneath it.
3. **Current or anticipated?** Current, and raised twice — obliquely in
   `ENG-013`'s original request ("proper peipleine stages") and
   explicitly in the merge reply.
4. **What does it displace?** The single machine WIP slot for the longest
   run any ticket has asked for, ahead of four `designed` tickets. Nothing
   at the approver's desk (WIP uncapped). Real competitor: `ENG-022`.
5. **Would not building it be fine?** No. Not building it makes Reading A
   a bad decision retroactively and ships a capability the approver has
   already rejected the shape of.

**Filter verdict: build it, and say out loud that it's the biggest ticket
on the board and not the most urgent one.**

## Decision

Filled in by the approver.

- **The approver's answer:**
- **Date:**
- **Notes:**
