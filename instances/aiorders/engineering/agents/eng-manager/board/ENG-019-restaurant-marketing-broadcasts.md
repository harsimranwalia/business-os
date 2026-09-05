---
id: ENG-019
title: Restaurant self-service marketing broadcasts — mass send and drip sequences, scheduled or immediate
project: restaurant-portal
type: feature
size: L
time_estimate: several days to a week+
time_spent:
time_remaining:
severity: P2
priority: now
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-05
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md
  design: agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md
  adrs: [ADR-018, ADR-019, ADR-020]
  review:
  test_plan:
  security_review:
  release:
  pr:
touches_data: true
touches_models: false
---

## Problem

Restaurant owners on the brand portal have no way to message their own
customers except when the platform's automatic triggers fire (welcome,
order, birthday, feedback). An owner who wants to announce a new menu item
or a holiday promotion — their own timing, their own reason — has no
in-product path to do it, and no way to see whether a past send produced any
orders.

## Outcome

An owner can compose a one-time message or a multi-step drip sequence,
choose to send to all customers or those inactive for a chosen number of
days, and either send immediately or schedule for later. Every send reuses
the platform's existing email/SMS delivery and is scoped strictly to that
owner's own restaurant. A campaign carrying a coupon code shows redemptions
and the revenue behind them.

## Notes

- **Naming collision, confirmed in code, not a guess.** The brand portal
  already has a nav item called "Campaigns" — it's about inviting
  influencers to visit and post (`influencer_campaigns` table,
  `pages/campaigns/*`, `services/campaignService.ts` →
  `restaurant-influencer-campaigns` edge function). This ticket is
  unrelated to that feature and proposes a different label ("Broadcasts",
  working name) for the new one — correctable at G1, but whoever designs
  this should not reuse the `campaigns` table/route names.
- **Where this plugs in.** The brand portal's existing `Automations` page
  (`pages/autopilot/Automations.tsx`) is the closest existing surface — it
  already shows send stats and a communication history table for the
  reactive triggers. The natural home for the new composer is a new tab
  alongside "Automation Flows" / "History" on that same page, since the
  raw request itself frames this as a gap *in* autopilot, not a request for
  an unrelated nav item.
- **Reusable prior art, confirmed by reading the code, not assumed:**
  - `outgoing-communications`'s `services/email.ts` / `sms.ts` /
    `template.ts` — the actual send layer, actor-routed
    (`aiorders-api/supabase/functions/outgoing-communications/index.ts`).
  - `communication_templates` / `communication_log` — the existing
    trigger/template/log pattern (`restaurant-portal/src/types/autopilot.ts`),
    scoped to `restaurant_id` and a closed set of lifecycle `trigger_type`s.
    This ticket's campaign/audience/scheduling model is parallel to that,
    not an extension of it — same shape `ENG-017` used for lead nurture,
    for the same reason (a chosen-audience blast doesn't fit a
    single-customer lifecycle trigger).
  - `offers.coupon_code` — already wired into `welcome_offer` /
    `first_order` / `every_order`; this ticket's proposed ROI mechanism
    (acceptance criterion 4) reuses it rather than building new tracking.
  - `20260217000001_platform_analytics_cron.sql` — proves `pg_cron` is
    already in use in this database, useful precedent for the
    scheduled-send/drip dispatch mechanism.
- **Cross-tenant scoping risk, named because it has already happened on
  this codebase.** `ENG-015` found a handler (`admin-portal/handlers/
  restaurants.ts`) that forgot the role/brand check its sibling handler
  had. Acceptance criterion 7 in the PRD exists specifically because of
  that precedent — whoever builds this should read `ENG-015`'s review
  before writing the audience-query code.
- **CASL context, not a resolved answer.** This audience is existing
  customers with a prior order, unlike `ENG-017`'s cold leads — materially
  better consent footing, but still worth a real legal check. Baseline:
  every send carries an unsubscribe path regardless (acceptance criterion
  6).

## Breakdown

Decomposed 2026-09-04 (`work-breakdown/SKILL.md`) into three sub-tickets, one
per surface, sequenced by the design's own Rollout order (migration before
functions before frontend):

| Sub-ticket | Surface | Repo | Depends on | State |
|---|---|---|---|---|
| `ENG-037` | database | `aiorders-api` | — | `building` |
| `ENG-038` | backend | `aiorders-api` | `ENG-037` | `ready` |
| `ENG-039` | frontend | `restaurant-portal` | `ENG-038` | `ready` |

This parent carries no diff of its own from here on — its evidence is its
children's (ADR-003-class exemption). It moves directly to `shipped` once
every child reaches `shipped`/`verified`/`dropped` with at least one
`shipped`/`verified`, without itself passing through `in-review`/`in-qa`/
`in-security`. Full reasoning — the surface split, why `backend` wasn't
split further, ADR/AC mapping per child, and sizing — is in
`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`.

## Log

- 2026-08-29 `intake → shaped` (product-manager) — sized L, project
  `restaurant-portal` (`aiorders-api` also touched, named in the PRD).
  Ran the full request-readback (`skills/request-readback/SKILL.md`): this
  PM's own reading, grounded in `restaurant-portal` and `aiorders-api` code
  read directly (created this host's missing `restaurant-portal` worktree
  to do so — `config/projects.md`'s "all five already exist" is stale for
  this Windows host, same gap the architect already flagged 2026-08-29 for
  `aiorders-api`), plus a blind architect reading (subagent, `opus`, raw
  request + `knowledge/business-profile.md` only, no repo access, no
  exposure to this PM's own reading). No material divergence — see PRD
  Readback for the full comparison and the risks the architect raised
  unprompted (CASL, cross-tenant scoping, durable scheduling, approval
  posture — the last resolved as a non-issue, not a real fork).
  PRD: `agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`.
  **Held at `shaped`, not advanced to `awaiting-scope`** —
  approver-facing WIP cap (2) re-verified fresh from `inbox/` immediately
  before this decision: `ENG-014`'s and `ENG-015`'s G1s both still read
  `decision:` empty, at cap, same as this board's own header going into
  this pass. G1 content is fully drafted in the PRD's own Decision section
  and ready to raise the moment a slot frees. **1 transition**
  (`intake → shaped`), well under the cap of 4. No cap numbers change —
  `shaped` counts toward neither approver-facing WIP nor machine WIP.
  No `inbox/` item raised this pass (no G1 to notify on yet), so no
  `lib/eng-notify.sh` call.
  `chained: none` — sits at `shaped`, held by the approver-facing WIP cap
  rather than genuinely blocked or waiting on a human for this ticket
  specifically; firing `continue ENG-019` now would only re-discover the
  same cap with no new work to do. Re-check once a
  `decision`/`watch`/`scheduled` pass clears `ENG-014` or `ENG-015`, or via
  a dedicated `continue ENG-019` once either does.

## 2026-09-03 — scheduled: G1 raised — `shaped → awaiting-scope`

The premise every prior hold on this ticket cited — approver-facing WIP
cap (2), full — is stale. `agents/eng-manager/config.yaml` (department
template) still says `approver_limit: 2`, but this instance's own override,
`config/config.yaml` (read fresh this pass, not previously checked by any
pass that held this ticket): `approver_limit: unlimited # was 2. Raised to
no-cap 2026-09-02 by the approver` — a real, dated, reasoned policy change,
not a gap. No decision-journal or exceptions.md entry names it (checked
both, zero hits), because it isn't a gate answer or a process exception —
it's a standing config override, same shape as `wip.machine_limit`'s own
inline history in the same file. Nothing further to design or confirm: the
PRD's readback already converged (PM + blind architect, no material
divergence), so this went straight to G1 rather than a fresh question.

Wrote `inbox/2026-09-03-eng019-g1-scope.md` (recommendation: build now,
scoped to one-time + drip broadcasts, all/inactive-N-days audience,
coupon-code ROI, exactly as the PRD proposes). `lib/eng-notify.sh raise`
called, exit 0 (logged `sent: active`, the already-tracked `MODE`-clobber
bug — `proposals.md`, 2026-08-25 row — not re-filed). Stamped
`notified: 2026-09-03T11:51:25`.

**1 transition** (`shaped → awaiting-scope`). **Consequence:** no machine-
WIP change (`awaiting-scope` is outside the counted range). Approver-facing
WIP: uncapped per the override above, so this adds to the queue without
displacing anything — `owner` moves `product-manager → approver`.

`chained: none` — `awaiting-scope` is one of the documented no-chain
conditions (waiting on the approver). The next hop is the approver's
answer; a future `decision` pass acts on it.

## 2026-09-03 — decision: G1 approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-03-eng019-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus step 6 (this answer
advances the ticket into a machine-owned state) and the not-negotiable set
(step 1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
*Guards*). Mode check clean (repo-root `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls back to the global switch).
Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board: both
exit 0, clean.

**The answer:** `approved` (`decided: 2026-09-03T15:52:30.648626+00:00`).
No additional comment. Read as accepting the recommendation exactly as
scoped — one-time and drip broadcasts, all-customers/inactive-for-N-days
audience, coupon-code redemption/revenue as ROI, owner-authored content,
owner/manager access only — and as accepting every item in the readback's
"Assumed, correctable here" list as proposed, since none was corrected.

PRD `status: approved`, `decided:` stamped
(`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`,
`## Decision` section filled in). Journal entry written
(`agents/eng-manager/config/decision-journal.md`). Gate item's own `##
Decision` footer appended with a processed note and moved
`inbox/2026-09-03-eng019-g1-scope.md` → `inbox/_handled/`.

**Risks named in the PRD are not resolved by this approval and stay open,
inherited by the architect at `designed`:** durable scheduling/drip
infrastructure (the PRD notes a cron precedent exists,
`platform_analytics_cron`, but a multi-day drip on top of it is real design
work); whether the existing send services need changes for a
chosen-audience fan-out versus today's single-recipient trigger sends (if
so, this ticket's cost grows — PRD Risks); and the CASL consent posture
(better footing than `ENG-017`'s cold leads — an existing order
relationship rather than a cold lead — but still worth a real check, and
acceptance criterion 6's unsubscribe path is the baseline regardless of how
that check lands). Restated here so the `continue ENG-019` hop below
doesn't have to re-derive them from the PRD alone.

**Priority column corrected while already touching this row**: this
ticket's own frontmatter has carried `priority: now` since the G1 was
raised; the board index's In-flight table still cached `next` (the same
drift the `ENG-016` decision pass's own observation flagged for this row
without fixing it) — fixed here as part of this pass's board update.

**Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached board header:** `1/1`, occupied by `ENG-024` (`ready-to-ship`, not
yet `shipped`). Irrelevant to this transition — `designed` sits outside the
counted `ready`..`ready-to-ship` range; shaping/design work is backlog
grooming regardless of who holds the slot (`eng_build_loop.md` step 6).

**1 transition** (`awaiting-scope → designed`), well under the cap of 4 —
the actual design work is the architect's own next hop, not attempted
inline here, same precedent `ENG-026`'s, `ENG-016`'s and `ENG-015`'s
identical G1-approved hand-offs already set. **Consequence:** ticket now
owned by `architect`, outside both the machine-WIP and approver-WIP counted
ranges. Approver-facing WIP uncapped (`wip.approver_limit: unlimited`);
this G1 drops off the "Waiting on the approver" list.

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract (act on the answered gate item, advance
only the ticket it belongs to).

**Notify sweep:** nothing raised this pass — no new gate item written.
Nothing else nudged — out of this event's own scope.

**Observations/proposals filed:** none this pass.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board: both
exit 0, clean.

`chained: ENG-019` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver,
not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-019`
before this pass exits.

## 2026-09-03 — scheduled: dead-end sweep found and re-fired a broken chain

`scheduled` event pass (whole-board safety-net sweep), step 8's broken-chain
check. This ticket's own last log line above (`chained: ENG-019`) reads as
healthy by itself — exactly the trap step 8 names ("a chain that was fired
is not the same as a chain that ran"). Cross-referencing against
`traces/eng-loop-2026-09-03.log` found the `continue ENG-019` fire it
recorded (14:25:46) really did launch and run (`pass start: continue
(ENG-019)` ... `pass end: continue (exit 0, 1768s)`), but the architect's
own tech-design work never landed: the pass delegated the actual design to
a background subagent, then that subagent was still running past the
session's own 600s internal budget and was terminated
("Background tasks still running after 600s; terminating") before it wrote
anything. Exit 0, so this was never a failed-pass retry and never a
dropped event — no `*-eng-events-dropped.md` file exists for today, checked
directly. To every mechanical check this looked like a clean chain; it
wasn't.

**Already caught once, not resumed.** The very next `continue ENG-020`
design pass (same evening) independently found the identical gap while
cross-checking `ENG-019` for file collisions — `links.design` blank, no
file at `agents/architect/designs/ENG-019-*.md`, log stops at `chained:
ENG-019` with nothing after — and filed it as an observation
(`observations.md`, "This continue ENG-020 pass's design work
cross-checked ENG-019..."), explicitly left for "the dead-end sweep's own
'broken chains' check" rather than resumed inline, since fixing a sibling
ticket is outside a `continue ENG-020` pass's own narrow contract. No later
pass re-ran `continue ENG-019` in the meantime (verified: the only other
`ENG-019`-tagged pass-start line in today's log is this `scheduled` pass's
own context tag, not a resumption) — genuinely still open until now, not a
stale observation.

**Verified clean before re-firing**, not just re-triggered on faith:
`links.design`, `adrs: []` still both empty on this ticket's own
frontmatter; no `ENG-019-*` file anywhere under `agents/architect/designs/`
or `agents/architect/notebook/` (tracked or untracked — `git status`
checked directly); `agents/architect/decisions/_index.md`'s `next_id`
shows no partial/orphaned allocation from the dead attempt. Nothing to
clean up — the killed subagent left no partial artifact, so a fresh
`continue ENG-019` starts from exactly the same clean state the 14:25:46
fire did.

**No state or owner change** — `designed`/`architect` is still the
technically-correct next step (the state name is applied at G1-approval
time on this board, same convention every sibling G1 this evening used;
`ENG-020`'s and `ENG-021`'s own design work completed *after* their
identical decision-pass transitions, so the gap here is specific to this
one attempt dying, not a wrong state).

Re-fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-019` this pass —
`continue` outranks `scheduled`/`watch` under the 2026-09-02 priority rule,
so this jumps ahead of the six `scheduled`/`watch` events already queued
and gets the next available session. `chained: ENG-019` (remediation of a
broken chain, not a fresh dispatch — see `_index.md`'s own dated entry for
this pass's full board-wide account).

## 2026-09-03 — continue ENG-019: tech design complete — held at `designed`, machine-WIP slot full

`continue` event pass, resuming the chain the prior `scheduled` sweep
re-fired after finding the last attempt's background design subagent killed
at its own 600s timeout with nothing written. Reading map for `continue`:
steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*) — step 2's mid-PRD checkpoint note
doesn't apply, the PRD is already `approved`. Mode check clean (repo-root
`.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-019`) and whole-board: both exit 0, clean.

**Ran `skills/tech-design/SKILL.md` directly in this session — no
background subagent delegated for the substantive work this time**, given
what killed the last attempt. Read the PRD, this ticket's own Notes, the
prior design/decision-journal/observations context, `config/projects.md`,
and — the bulk of the work — `origin/main` directly across `aiorders-api`
(`outgoing-communications`, `autopilot`, `brand-portal`, `_shared/
restaurantAccess.ts`, `cloudwaitress-middleware`, `external-integrations/
handlers/cloudwaitress.ts`) and `restaurant-portal` (`pages/autopilot/
Automations.tsx`), plus `ADR-011`/`012`/`015`/`016`/`017` (this evening's
sibling designs and the P0 auth-cascade) before writing anything.

**Three real decisions found, all reversible, all logged as ADRs rather
than escalated** — resolving the three risks the PRD's own G1 approval
named as "the architect's to resolve":

- **`ADR-018`** — durable scheduling/mass dispatch is a `pg_cron` poller
  (`platform_analytics_cron`'s own structural precedent) claiming bounded
  batches of due rows every 5 minutes, not per-recipient `autopilot`-style
  QStash scheduling. QStash is proven at one-message-per-event scale;
  broadcasts introduce one-action-enrolls-thousands scale, which a poller
  fits and per-recipient publish calls don't. Resolves the PRD's
  scheduling/drip-infrastructure risk.
- **`ADR-019`** — the PRD's own Assumed section reads AC4 as reusing an
  existing redemption-tracking mechanic; reading the code directly finds no
  such mechanic exists (`offers.coupon_code` is a plain display string
  everywhere). What does already exist and already gets captured, since
  before this ticket: CloudWaitress's `order_new` webhook already reports
  applied promos, and `external-integrations/handlers/cloudwaitress.ts`
  already persists them onto `orders.promos`/`total_amount`. AC4 is a read
  against data already captured, not a new capture path — a correction to
  the PRD's own framing, not just a design choice. Resolves the "do the
  send services need changes" risk in the negative: they don't, only a new
  orchestration layer above them is new.
- **`ADR-020`** — opt-out reuses `customers.consent_email`/`consent_sms`
  (already written on every customer at creation, already the exact
  "implied consent from an existing order relationship" the PRD's CASL risk
  argues in prose) via a new small public `broadcast-unsubscribe` function,
  rather than a new column or a hole cut into `outgoing-communications`'
  just-tightened auth gate (`ADR-016`/`ADR-017`, same evening). Resolves
  the CASL risk.

No one-way door found — checked explicitly against all five categories
(new datastore, new vendor, auth-model change, public contract, painful
migration, recurring cost) in the design's own One-way doors section; none
qualify. `pg_cron` and `outgoing-communications` are both already-live
primitives reused, not new infrastructure.

**Design written:** `agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md`.
Three new tables (`broadcast_campaigns`, `broadcast_campaign_steps`,
`broadcast_campaign_recipients`), one new `brand-portal` action file
(`broadcasts.ts`, `ADR-011`'s own precedent), one new dispatcher function,
one new public unsubscribe function — full component list and failure-mode
reasoning (idempotent claiming, opted-out-between-steps re-check,
empty-audience no-op, mid-flight-edit rejection) in the design itself.
`touches_data: true` (new tables only, `database` owns the migration
detail — this design states intent/constraints, per `tech-design`'s own
step 7); `touches_models: false` (owner-authored content throughout, no
model call anywhere in this design).

**Routing (step 11): would be `ready` — held at `designed` instead.**
Neither an L0 project nor a one-way door, so the skill's own routing table
reads `ready`, `owner: eng-manager`. **Machine WIP re-checked fresh from
every ticket's own frontmatter this pass, not the cached board header:**
still `1/1`, the `ENG-016` family (`ENG-016` `building`; `ENG-032`
`blocked`/approver; `ENG-033`/`ENG-034` `ready`, both still behind their own
unmet `depends_on`). Per this board's own established precedent for exactly
this situation — set today on `ENG-014`/`ENG-017`/`ENG-020`/`ENG-021`/
`ENG-023`/`ENG-025`/`ENG-026`, all `designed` with a completed design and no
one-way door, all held rather than written to `ready` — `ENG-019` joins the
same held-for-slot pool: `state`/`owner` **unchanged** (`designed`/
`architect`), not written to `ready`/`eng-manager`, because entering `ready`
is what claims the one slot, not being designed. Whichever ticket in this
pool the slot's own priority order picks (`now` first, then lowest id among
ties — this ticket, `ENG-020` and `ENG-021` all currently carry `priority:
now`, so id order decides among them: `ENG-019` first) gets it once the
`ENG-016` family reaches `shipped`.

**0 transitions** — `state`/`owner` deliberately unchanged this pass, only
`links.design`/`links.adrs`/`touches_data`/`touches_models` populated.
Well under the cap of 4; no machine-WIP or approver-WIP consequence either
way (`designed` sits outside both counted ranges).

**Dead-end sweep (scoped to this event):** no other ticket touched, per
this event's own narrower contract. Machine-WIP occupancy check above
doubled as a sanity check that the `ENG-016` family's own four rows are
still internally consistent (they are — matches `_index.md`'s own most
recent account exactly).

**Notify sweep:** no gate item raised this pass (no one-way door). Swept
`inbox/`'s 11 open items fresh against the 24h threshold (current
`2026-09-03T22:55:24-07:00`): `eng015-merge-request` (~12h51m),
`eng027-g1-rescope` (~9h40m), `eng028-g1-scope` (~6h45m),
`eng032-merge-request` (~1h28m, UTC-stamped unlike its siblings — read
against its own log-recorded local time) all comfortably under 24h;
`eng008`/`009`/`010` already carry their one-time `nudged:`; the four P0
incident notices (`eng029`/`030`/`035`/`036`) left un-nudged, same standing
informational treatment prior passes established. Nothing due.

**Observation filed** (`observations.md`): `supabase/functions/README.md`'s
"Known issues" section still describes `brand-portal/offers.ts`/
`feedback.ts` calling `verifyRestaurantAccess` with the wrong argument
order — reading `offers.ts` directly for this design's own Interfaces work
shows correct argument order today, consistent with `ENG-022` (merged this
evening) having fixed it without the doc catching up. Not this ticket's to
fix.

**Step 6b:** no rule about a shared artifact path/state name/config key was
written or relied on this hop — the tables/functions this design names are
new, nothing existing instructs another agent to produce them under a name
this hop could conflict with.

**Journal:** n/a — no G1/G2/G3 or merge request answered this pass.

**Board update:** `agents/eng-manager/board/_index.md`'s In-flight row for
`ENG-019` — no state/priority/owner change, `Updated` column unchanged
(already `2026-09-03`).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board: both
exit 0, clean.

`chained: none` — held by the machine-WIP cap (`1/1`, the `ENG-016`
family), one of the documented no-chain conditions (held by a cap). Firing
`continue ENG-019` again now would only re-discover the same full slot with
no new work to do. Re-check via a `decision`/`watch`/`scheduled` pass once
the `ENG-016` family reaches `shipped`, or via a dedicated `continue
ENG-019` once it does.

## 2026-09-04 — scheduled: dispatched into the freed slot — `designed → ready`

`scheduled` event pass (whole-board safety-net sweep), context `launchd`.
Reading map for `scheduled`: the whole document. Mode check clean
(business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-019`) and
whole-board: both exit 0, clean.

**Why this ticket, verified fresh rather than trusted from the board
index's own cached narrative.** Machine WIP re-checked off every ticket's
own frontmatter this pass: the whole `ENG-016` family (`ENG-016` itself
plus `ENG-031`–`034`) now reads `verified`, and no other ticket sits inside
the counted `ready`..`ready-to-ship` range — **machine WIP `0/1`, free**.
To-do-column scan (`intake`/`shaped`/`awaiting-scope`) found nothing
eligible to start fresh (`ENG-018` is `priority: hold`; `ENG-027`/`ENG-028`
are `awaiting-scope`/`owner: approver`, both genuinely waiting on the
approver, not machine-actionable). Per this ticket's own prior entry
(2026-09-03, immediately above), it is not a *new* start but a **deferred**
one: design already complete, no one-way door, routing already determined
(`tech-design/SKILL.md` step 11) — held only by the cap. Among the
`priority: now` pool held in the same position (`ENG-019`, `ENG-020`,
`ENG-021` per this ticket's own prior entry; `ENG-026` also currently
carries `priority: now` but was not part of that enumerated pool — not
chased further, since it is a higher id than all three and so does not
change the outcome either way), lowest id decides: `ENG-019`.

**Re-verified the design is still what it was, not re-derived.**
`links.design` still points at
`agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md`,
`links.adrs: [ADR-018, ADR-019, ADR-020]` still populated, file still
present on disk. No edits to the ticket's scope, PRD, or design this pass —
this is the deferred bookkeeping transition the 2026-09-03 entry already
earned, not a fresh design review.

**State/owner: `designed`/`architect` → `ready`/`eng-manager`.** Per
`tech-design/SKILL.md` step 11 ("Otherwise: state `ready`, owner
`eng-manager` (work-breakdown next)") — no G2, no one-way door, not an L0
project. **1 transition**, well under the cap of 4. **Consequence:**
machine WIP `0/1 → 1/1`, occupied by `ENG-019` alone. Approver-facing WIP
unaffected (uncapped; `ready` was never counted there).

**Stops here, deliberately — does not attempt work-breakdown or building
inline.** Both are new implementation work (or the judgment call that leads
directly to it), and this board's own established precedent throughout
today (`ENG-031`→`ENG-032`→`ENG-033`→`ENG-034`→`ENG-016`, each a `continue`
dispatch rather than inline building on a `scheduled`/`watch` pass) treats
that as out of scope for this event type. Chained instead — see below.

**Dead-end sweep (whole board, per this event's own contract):** found and
fixed two stale `owner` fields (`ENG-014`, `ENG-025`, both `eng-manager` →
`architect` — see their own board files and this pass's `_index.md` entry
for the full finding); no ticket sits without an owner; no ticket is
`blocked` at all right now (confirmed off every ticket's own frontmatter);
no broken chain found — `traces/eng-loop-2026-09-04.log` shows a clean,
continuous chain through today with no `DROPPED` lines and no
`*-eng-events-dropped.md` file for today, and an earlier pass today
(`traces/eng-loop-2026-09-04.log` ~line 1173) already re-verified all
twelve `designed`-state tickets are genuinely in the
"design-complete-but-capped" sub-state, not stalled.

**Notify sweep:** `inbox/`'s three open items (`ENG-027`, `ENG-028`,
`ENG-016`'s Piece-2 question) re-checked against the 24h threshold —
`ENG-027`/`ENG-028` already carry their one-time `nudged:`; the `ENG-016`
question is ~13 minutes old (`notified: 2026-09-04T10:58:06` vs. this
pass's start), nowhere near due. Nothing raised or nudged this pass — this
ticket's own transition opened no gate.

**Observations/exceptions (8b):** none new beyond the two owner-field
corrections logged above and on `_index.md`. No `exception-request:` found
on any ticket log.

**Journal (8c):** n/a — no G1/G2/G3 or merge request answered this pass.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-019`) and whole-board: both exit 0, clean.

`chained: ENG-019` — `ready` is agent-owned (`eng-manager`, work-breakdown
next), not the approver, not blocked, not terminal, not held by a cap
(this ticket now holds the cap itself). Fired `/bin/zsh
/Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-019` before this pass exits.

- 2026-09-04 **`ready → building`, work-breakdown run** (eng-manager,
  `continue` event pass, context `ENG-019`, `work-breakdown/SKILL.md`).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*) — step
  2's mid-PRD checkpoint doesn't apply. Mode check clean (`MODE=active`).
  Gate-check, scoped (`ENG-019`) and whole-board: both exit 0, clean (run
  fresh against the resulting board state, including the three new tickets
  below).

  **Autonomy check:** both touched projects (`aiorders-api`,
  `restaurant-portal`) are L1. Proceeds. **WIP check:** SKILL.md's own text
  names a stale config key (`wip.limit`); read the current authoritative
  value instead — `machine_limit: 1`, `1/1`, held by this ticket's own
  family, not a second occupant. Observation filed (stale key name in a
  skill file — not edited here, skill files go through Fable only).

  Split into three sub-tickets by surface, sequenced per the design's own
  Rollout order (migration → functions → frontend): `ENG-037` (database, no
  dep, dispatched to `building`), `ENG-038` (backend, depends_on `ENG-037`),
  `ENG-039` (frontend, depends_on `ENG-038`) — both held at `ready`. Considered
  and rejected splitting `backend` further (CRUD vs. dispatch/unsubscribe) —
  same agent, same WIP slot either way, no parallelism gained. See
  `## Breakdown` above; full reasoning, ADR/AC mapping per child, and sizing
  in `agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`.

  **1 transition** on this ticket (`ready → building`). Machine WIP: still
  `1/1`, same family (`ENG-019` + `ENG-037`..`039`), not 2/1 — applying the
  `ENG-016`/`ENG-031` precedent, not re-litigating it. No G1/G2/G3, no
  one-way door, nothing raised to the approver.

  `chained: ENG-037` — the only child with a met dependency and something
  agent-actionable now. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-037` before this pass exits. `chained: none` on `ENG-019`
  itself (parent has no action until a child reports back) and on
  `ENG-038`/`ENG-039` (each waiting on an unmet dependency) — recorded on
  each ticket's own log.

  business-os itself left uncommitted — same standing default every pass on
  this board has used; the commit-convention question remains open, not
  re-decided here.

- `2026-09-05` **`building → shipped → verified`** (eng-manager/
  product-manager, `continue` event pass, context `ENG-019`,
  `acceptance-check/SKILL.md`). Reading map for `continue`: steps 6 and 6b,
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*,
  *The four lanes*, *Guards*) — step 2's mid-PRD checkpoint doesn't apply,
  the PRD has been `approved` since 2026-09-03. Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`,
  scoped (`ENG-019`) and whole-board: both exit 0, clean.

  **All three children verified**, re-checked fresh off each one's own
  frontmatter rather than trusted from `_index.md`'s cached narrative:
  `ENG-037`, `ENG-038`, `ENG-039` all `state: verified`, all `parent:
  ENG-019`, none dropped. `ADR-003`-class exemption met (every child
  settled, all three actually shipped — well past the "at least one"
  floor). `building → shipped`, no diff, review, QA, or security hop of its
  own — same handoff shape `ENG-016`'s own parent transition used
  2026-09-04.

  **Ran `acceptance-check/SKILL.md` in full despite the exemption** — the
  skill's trigger has no parent carve-out. Re-fetched both repos fresh
  rather than trusting either child's own notebook date: `aiorders-api`
  `origin/main` → `89c6fdb1`, `restaurant-portal` `origin/main` → `aeeb7b9`
  — both identical to the commits `ENG-038`'s and `ENG-039`'s own
  acceptance-checks already walked, zero drift. Unlike `ENG-016`'s family
  (3 of 4 children shipped via the receipt-bookkeeping shortcut, leaving
  criteria never individually walked until the parent's own check), both of
  this family's non-schema children already ran acceptance-check in full at
  their own shipping point, so this pass is a rollup and a fresh no-drift
  confirmation, not a gap-fill. All 7 PRD criteria pass (cross-referenced
  from `ENG-038`'s and `ENG-039`'s own notebooks); no scope creep found in
  a whole-family non-goals sweep; cost `$0/month` as estimated, confirmed
  independently on all three children's own release records. `shipped →
  verified`. Full reasoning:
  `agents/product-manager/notebook/2026-09-05-eng019-acceptance.md`.

  **2 transitions**, under the cap of 4. **Machine WIP: `1/1 → 0/1`, free**
  — the whole `ENG-019` family (parent plus `ENG-037`–`039`) is now
  terminal.

  **Step 6b: neither condition met** — the PRD's Non-goals section names
  deferred ideas in prose (deeper ROI/attribution, a fuller segment
  builder, AI-generated content) but no "Feature shape and sequencing"
  section with a named next ticket, and the G1 answer was a bare
  "approved" with no explicit sequence sign-off. Nothing filed.

  **Two observations filed** (`observations.md`): this family as the first
  on the board where the parent's own acceptance-check found zero backfill
  work (contrast with `ENG-016`), not treated as closing the standing
  receipt-bookkeeping proposal; and a stale citation in
  `lib/eng-gate-check.sh`'s own comments pointing at
  `agents/architect/decisions/ADR-003-parent-ticket-receipts.md`, which
  does not exist on this instance (this instance's real `ADR-003` is
  `aiorders-api-authoritative-for-migrations`, an unrelated decision) —
  likely a life-os-origin citation that never resolves for any instance
  forked from that template. Not fixed inline — out of scope for this
  ticket's own `continue` pass, and `lib/` scripts are outside the
  Fable-only authoring rule but still not this pass's work to do.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract.

  **Notify sweep:** no gate item raised this pass (no one-way door, no G1/
  G2/G3, no merge request). Nothing nudged — out of this event's own scope.

  **Journal (8c):** n/a — no G1/G2/G3 or merge request answered this pass.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-019`) and whole-board:
  both exit 0, clean.

  `chained: none` — terminal (`verified`), `blocks: []`. The freed machine-
  WIP slot is for the next dispatch-scoped pass (`scheduled`, or a
  qualifying `decision`/`watch`) to pick up, not this one — `continue`'s
  own single-ticket scope, same precedent `ENG-016`'s own shipping pass
  already set.

  business-os itself left uncommitted — same standing default every pass on
  this board has used; the commit-convention question remains open, not
  re-decided here.
