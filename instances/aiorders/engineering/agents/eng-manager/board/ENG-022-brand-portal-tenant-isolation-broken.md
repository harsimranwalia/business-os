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
state: designed
owner: eng-manager
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
  design: agents/architect/designs/ENG-022-brand-portal-tenant-isolation-broken.md
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

- `2026-08-29` `shaped → designed` (architect, `continue` event pass, context
  `ENG-022` — this fire's own turn at the front of `traces/.pending`,
  reached after the approver's plain "approved" acknowledgement on the P0
  incident notice, `inbox/_handled/2026-08-29-eng022-p0-incident.md`; no
  priority change requested, nothing else to act on there). Narrow scope
  per this event's own contract — this ticket only. Mode check clean
  (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  whole-board: exit 0, clean.

  Read the real code before designing against it, per
  `agents/architect/agent.md` ("match the codebase"): the department's own
  `aiorders-api` worktree (`~/Documents/_eng/aiorders-api`, confirmed clean —
  no uncommitted changes from a prior dead pass) rather than the PRD's
  summary alone. Confirmed all 19 broken call sites and the 4 correct
  contrast files match the PRD's table exactly (grep + targeted reads, all
  9 files). One thing the PRD didn't surface: `utils.ts:116` already
  contains `verifyRestaurantAccessLegacy`, a correctly-implemented throwing
  wrapper around `verifyRestaurantAccess`, exported but called from
  **nowhere** in the repo (confirmed by grep across the whole worktree) —
  changes the design from "invent a fix" to "promote the unused correct one
  already sitting here."

  Design written: `agents/architect/designs/ENG-022-brand-portal-tenant-isolation-broken.md`.
  Approach: the 9 files already split into two pre-existing, still-valid
  error conventions (throw vs. return `{success:false}`); fixed each broken
  file per its *own* convention rather than unifying all 9 (that's a
  refactor bundled into a bug fix — refused per `agents/architect/agent.md`'s
  own "what you refuse" list) — `feedback.ts`/`customers.ts`/`hiring.ts`/
  `website.ts` (11 sites) get the promoted `requireRestaurantAccess`
  (renamed from the dead legacy helper, `@deprecated` dropped, one
  `console.warn` denial log added per `security-baseline.md` A09);
  `offers.ts` (8 sites) fixed in place — correct argument order and
  `.hasAccess` check, matching its own already-correct siblings
  (`catering.ts`/`menus.ts`/`restaurants.ts`) — no new helper, since its
  surrounding code already returns `{success:false}` and switching it to
  throw would change its response shape for no reason. Full alternatives,
  the two response-shape risk, and the rollout plan (qualifies for the P0
  hotfix exception to the release window, security gate still applies) are
  on the design doc, not repeated here.

  Test plan for acceptance criterion 4: `Deno.test` files colocated per
  fixed source file, using a stubbed `SupabaseClient` (no live project, no
  network) to prove the negative case per call site — real automated
  coverage, not a manual-verification fallback, and does not need the
  repo-wide test-harness ticket `config/projects.md` frames for
  `restaurant-portal` (different stack, different gap; Deno's built-in
  runner needs no scaffolding).

  **No one-way door.** Renaming a zero-external-caller internal function and
  correcting call sites to an existing primitive's real signature are both
  fully reversible — no new datastore, vendor, auth model, or public
  contract. No ADR written (`adrs: []` in the design's own frontmatter).
  `awaiting-decision` (G2) does not apply; per `definition-of-done.md` the
  ticket moves straight to `ready` next.

  **State:** `shaped → designed`, `owner: architect → eng-manager` — the
  next state's owner per `definition-of-done.md`'s table (`ready |
  eng-manager`), mirroring how this ticket's own prior entry named the next
  actor rather than the current one. **Consequence:** stays short of the
  counted `ready..ready-to-ship` machine-WIP range (6/12 unaffected);
  `security`-typed, no G1/G2 raised, approver-facing WIP and approval cap
  both unaffected (1/2, 1/3, unchanged).

  One observation filed (`agents/eng-manager/observations.md`): the two
  pre-existing, unrelated error-response conventions living side by side in
  `brand-portal/` — noted so a future ticket doesn't mistake it for
  something this fix introduced.

  This pass does not attempt the eng-manager's own `ready` sequencing work
  inline, matching this board's own established practice for a
  `shaped→designed` (and `designed`-adjacent) hop — see `ENG-014`'s
  2026-08-29 log ("this pass does not attempt the architect's own design
  work inline... belongs in the dedicated session the now-genuinely-queued
  chain will launch"), same principle applied one hop later.

  `chained: ENG-022` — `designed`, owned by `eng-manager`, an agent-owned
  state; firing `/bin/sh
  departments/engineering/lib/eng-trigger.sh continue ENG-022` before this
  pass exits. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-022`) and whole-board: see pass notes in
  `agents/eng-manager/board/_index.md`.

- `2026-08-29` no state change (eng-manager, `decision` event pass, context
  `2026-08-29-eng022-p0-incident.md` — this event's own turn at the front of
  `traces/.pending`, drained immediately behind the `continue ENG-022`
  design pass directly above: `traces/eng-loop-2026-08-29.log` — `pass end:
  continue (exit 0, 1286s)` 16:25:37 → `queue: collapsed 5 duplicate
  event(s)` → `draining queued event: decision
  (2026-08-29-eng022-p0-incident.md)` 16:26:33, no gap). Mode check clean
  (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  whole-board: exit 0, clean.

  Verified fresh rather than trusted before concluding no-op: the incident
  item already sits in `inbox/_handled/2026-08-29-eng022-p0-incident.md`
  carrying its own "Processed" footer — an earlier `watch`/`schtasks` pass
  had already fully actioned it (nothing to decide per the item's own text,
  no `priority` set); `decision-journal.md` row 34 already records this
  exact decision and timestamp; this ticket's own immediately-preceding log
  entry already ends at `designed` with `chained: ENG-022`, and
  `traces/.pending` confirms that fire is still genuinely queued (`1
  continue ENG-022`) — not lost or stale. This is the well-documented
  decision-races-a-prior-pass shape `observations.md` has logged over a
  dozen times on this board, the clean variant this time (chain genuinely
  fired and queued), not the broken-chain one (`ENG-014`/`ENG-015`'s rows,
  where the record existed but the fire never reached the trigger).

  **No state change.** `chained: none` — already correctly chained by the
  immediately-preceding pass, confirmed still live in `traces/.pending`;
  re-firing `continue ENG-022` here would only queue a duplicate for the
  collapse logic to clean up, not fill a real gap. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean — unchanged from pre-pass since no edit was made. One observation
  filed (`observations.md`) corroborating the open `proposals.md` race fix
  (2026-08-27 row: skip the launch when a `decision` event's named gate item
  is already in `_handled/`).

- `2026-08-29` no state change (eng-manager, `continue` event pass, context
  `ENG-022` — this fire's own turn at the front of `traces/.pending`, drained
  after `continue ENG-013`). Narrow scope per this event's own contract —
  this ticket only. Mode check clean (business-os `.env` → `MODE=` empty;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  Ticket sits at `designed`, owner `eng-manager`; per the design's own
  no-one-way-door finding the next step is straight to `ready` (G2 doesn't
  apply). Checked whether a machine-WIP slot is actually free rather than
  trusting the board index: read `ENG-008`, `ENG-009`, `ENG-010`, `ENG-013`
  frontmatter directly — `state: building`, `ready`, `ready`, `building`
  respectively, all unchanged. Machine WIP is still 4/1, over the
  2026-08-29-corrected cap of 1, none of the four has reached `shipped` yet.
  The board's own header already names `ENG-022` inside the range
  (`ENG-014` through `ENG-025`) that stays at its current backlog state
  until the count drains — this pass's read matches that instruction exactly,
  so `designed → ready` does not happen this pass.

  Checked all three inboxes for anything filed against `ENG-022` specifically:
  both prior gate items for this ticket (`2026-08-29-eng022-p0-incident.md`,
  and `ENG-023`'s G1 which cross-references it) are already in `_handled/`.
  One live item in `agents/eng-manager/inbox/`
  (`2026-08-29-restaurant-detail-write-partner-exposure.md`) names `ENG-022`
  only as a comparison point for a different file/ticket (`aiorders-admin-hub`
  `restaurants.ts`, filed during `ENG-015`'s design) — already classified
  out of scope by the `ENG-010` continue pass; re-confirmed, still correct,
  not this event's ticket, left untouched.

  **0 transitions.** State stays `designed`, owner stays `eng-manager`.
  **Consequence:** machine WIP unaffected (still 4/1, over cap, draining
  naturally); approver-facing WIP and approval cap both unaffected — no gate
  touched.

  **Dead-end sweep (scoped to this event):** nothing to resume — this is a
  deliberate wait on a re-verified cap, not a stall. **Notify sweep:**
  nothing to raise (no new gate item); nothing to nudge.

  `chained: none` — held by the machine WIP cap (4/1, over cap; no new
  ticket enters `ready` until it drains to ≤1). Re-check once one of
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` reaches `shipped`. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.
