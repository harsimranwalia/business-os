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
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-03
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
