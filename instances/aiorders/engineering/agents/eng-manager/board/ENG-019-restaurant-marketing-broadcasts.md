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
priority:
state: shaped
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
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
