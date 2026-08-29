---
id: ENG-022
title: Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure
project: aiorders-api
type: security
size: M
time_estimate: half a day to a day
time_spent:
time_remaining:
severity: P0
priority:
state: shaped
owner: architect
lane: full
blocked_on:
blocked_from:
source: product-manager
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-022-brand-portal-tenant-isolation-broken.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`supabase/functions/brand-portal/`'s shared `verifyRestaurantAccess()` check
is silently defeated on 5 of 9 handler files, by two different mistakes:
wrong argument order combined with checking a returned object's truthiness
instead of its `.hasAccess` field (`feedback.ts`, `offers.ts`), and calling
the check but discarding its return value entirely (`customers.ts`,
`hiring.ts`, `website.ts`). Full evidence, file:line, and the confirmed
correct files for contrast are in the PRD (link above) — not duplicated here.

Net effect: any authenticated brand-portal user can read or write any other
restaurant's feedback, customers, offers, website content, or hiring data by
supplying a different `restaurant_id` — no exploit tooling needed, just a
different value already visible client-side.

## Outcome

Every `verifyRestaurantAccess` call site in `brand-portal/` correctly denies
access when the caller doesn't own the target restaurant, verified by a
negative-case test per site (wrong tenant → denied), not just the positive
case.

## Notes

**How this was found.** Not agent-initiated security sweep — discovered
mid-investigation while shaping `ENG-023` (the approver's "feedback board has
no status or notes" request), tracing `restaurant-portal`'s Feedback page to
its backend. Once the pattern showed up once (`feedback.ts`), grepped every
`verifyRestaurantAccess` call site in the directory (9 files, ~25 sites) and
read enough of each to classify it — see PRD for the full table.

**Filed directly, not via `agents/eng-manager/proposals.md`.** Per
`schedules/eng_build_loop.md` step 3's bypass ("A P0 on a registered project
that is not on the internal lane... becomes a ticket immediately, no
proposal and no G1") and `templates/ticket.md`'s `source:` field note ("The
exception is a P0 on a project not on the internal lane, which keeps its
agent source"). `aiorders-api` is registered `L1`, not internal
(`config/projects.md`), and is documented there as "Highest blast radius of
the set — shared backend for all four frontends."

**Why P0, not P1** (severity is the filing agent's call,
`definition-of-done.md`): `agents/eng-manager/config/security-baseline.md`
names "exposed data" as an active-security-incident example, on par with a
leaked credential or a live exploit; `agents/security/agent.md`'s own
`interrupt_rule` is "P0 only — active incident, leaked credential, or
**exposed data**." This is live, currently-reachable customer PII (feedback
and customer contact info) plus unauthorized cross-tenant *write* access
(offers, website content) in production, on the platform's highest-blast-
-radius project. Weighed directly against `ENG-015` (this board's other
confirmed cross-tenant exposure, rated P1): that one exposed restaurant/
location listings with no write path; this one exposes customer PII and
grants writes, across five files rather than one code path. Rated higher on
the merits, not assumed from precedent.

**`type: security` auto-skips G1** (`definition-of-done.md` ticket-states
table), so this does not wait on approver approval to be *designed* — the PRD
is written short-form per `templates/prd.md`'s rule for auto-approved types
and the ticket goes straight to `designed`. It does NOT skip the approver
being told: `security-baseline.md` — "Only two things reach the approver
directly: An active security incident... — P0." That notice is the separate
inbox item raised this same pass (`gate: incident`), not this ticket's
(nonexistent) G1.

**State chosen deliberately.** Landing this ticket at `state: shaped, owner:
architect` rather than attempting `designed` myself — `designed`'s exit
condition ("tech design written, ADRs logged") is the architect's own output,
not a PM's; the PM's job here is only to get the finding filed accurately and
handed off without waiting on a gate that doesn't apply. Chained below so the
architect's own pass performs `shaped → designed`.

**Cross-reference with `ENG-023`.** Both tickets touch
`supabase/functions/brand-portal/feedback.ts` — `ENG-023` (feedback status/
notes) is adding a new write action to that same file. Flagged explicitly on
`ENG-023` so its engineer models the new code on `catering.ts`'s
`update_catering_request` (confirmed correct) rather than copying this file's
existing (broken) `getFeedback`. Not a formal `depends_on` — `ENG-023` does
not need this ticket to ship first, only to not repeat its bug.

## Log

- `2026-08-29` `intake → shaped` (product-manager, `intake` event pass,
  context `agents/product-manager/inbox/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`
  — this finding is a byproduct of that pass, not its assigned subject; see
  `ENG-023` for the assigned work). Mode check clean (business-os `.env` →
  `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  PRD written short-form (auto-skip type, no readback — agent-originated
  finding with its own evidence, `skills/request-readback/SKILL.md`'s "when
  this does NOT run" list). Evidence gathered by reading
  `supabase/functions/brand-portal/utils.ts`'s real
  `verifyRestaurantAccess` signature against every call site in the same
  directory (`feedback.ts`, `offers.ts`, `customers.ts`, `hiring.ts`,
  `website.ts`, `catering.ts`, `restaurants.ts`, `menus.ts`,
  `onlineOrders.ts`) and classifying each by the code actually there, not by
  pattern-matching the call alone.

  Incident notice raised: `inbox/2026-08-29-eng022-p0-incident.md`
  (`gate: incident`, `agent: product-manager`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **State:** `intake → shaped`, `owner: product-manager → architect`.
  **Consequence:** does not consume approver-facing WIP or the approval cap
  — `security`-typed, auto-skip G1, nothing waiting at a gate. Machine WIP
  (6/6, at cap) also unaffected — `shaped` is short of the counted range
  (`ready` through `ready-to-ship`), same as `ENG-023`, `ENG-016`–`ENG-021`.

  `chained: ENG-022` — `shaped`, owned by `architect`, an agent-owned state;
  firing `lib/eng-trigger.sh continue ENG-022` before this pass exits so the
  design step starts without waiting for a scheduled sweep, given the
  severity. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-022`) and whole-board: see pass notes in
  `agents/eng-manager/board/_index.md`.
