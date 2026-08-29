---
id: ENG-015
title: Agency/reseller (partner) users — brand-scoped locations and a working add-location path
project: aiorders-admin-hub
type: security
size: M
time_estimate: half a day to a day
time_spent:
time_remaining:
severity: P1
priority:
state: designed
owner: architect
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
  prd: agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-admin-portal-is-not-optimized-for-new-agency-users-resellers.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:22:19.014887+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # admin portal is not optimized for new agency users/ resellers of aiorders.
>
> they are not able to add locations , security issue if they go to
> /restaurant they can see all locations. they dashboard data is super admin
> data not just their brands. same for other tabs like influencer they are
> able to see all or user .

## Readback

See
`agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md` →
Readback — the full two-reading comparison and the code evidence live there
rather than duplicated here.

## Problem

A partner-admin/partner-user (this codebase's existing name for
"agency/reseller") sees every restaurant on the platform on the Restaurants
page, not just their own brand's — a live cross-tenant data exposure — and
cannot successfully add a new restaurant under their own brand at all (the
write is silently rejected).

## Outcome

A partner-admin/partner-user sees and can add only restaurants under brand(s)
assigned to them (`brands.partner_id`), enforced server-side. Staff
(`admin`/`sub-admin`) visibility and workflow are unchanged. The Dashboard,
Influencers, and Users pages are untouched — investigated and confirmed
already blocking partner roles outright today, not leaking.

## Notes

**Why `type: security` still got a G1, against the letter of
`definition-of-done.md`'s auto-skip list.** XS/bug/chore/security tickets
skip G1 by default because for most of them "should we build this" isn't a
real question. This one still has two: (1) a genuine, non-trivial policy
fork the request doesn't address — should a partner-created restaurant
auto-approve the way an admin-created one does today, or hold for review
(acceptance criterion 5, proposed default: held) — small enough not to
warrant its own standing-question gate item, per the same
order-of-magnitude test `ENG-011`/`ENG-013` used for theirs, but real enough
to want a tap; and (2) two of the four symptoms the approver named
(Dashboard, Influencers) do **not** reproduce on this branch — see PRD
Readback. Silently building only the two confirmed fixes without surfacing
that discrepancy risked either quietly under-delivering against what the
approver thinks they asked for, or (worse) "fixing" pages that already work,
against the standing instruction never to infer approval from silence. Full
readback still ran (this is not agent-originated work with its own
reproduction steps already attached — it arrived as a raw, imprecise human
report needing interpretation, exactly what the readback skill is for) and
this instance's own unbroken same-day precedent (`ENG-007` through
`ENG-014`, all `feature`-typed with a G1) is to keep the human tap for
anything with a real scope question, type label notwithstanding. Logged
here rather than silently overridden, per this instance's practice of
naming a deliberate departure from a mechanical default rather than either
blindly following or silently ignoring it.

**Investigated before writing anything**, same practice `ENG-011`/`ENG-013`/
`ENG-014` established. Confirmed the `partner-admin`/`partner-user` role
pair already exists (`aiorders-admin-hub`'s `AuthContext.tsx`), already has
a real brand-ownership relationship (`brands.partner_id`, live schema column,
backing a working `/partners/:id/assign-brands` screen) — so this is a
propagation gap in an existing model, not a net-new access-control system.
Traced the two confirmed defects to exact code:
`admin-portal/handlers/restaurants.ts`'s `getRestaurants()` always uses the
service-role client with no role branch at all (contrast `brands.ts`, which
already branches service-role-only-for-`admin`); and the `restaurants`
table's only `INSERT`-capable RLS policy is `role IN ('admin', 'sub-admin')`
(`20250729143357_initial_restaurant_rls.sql`), which is why
`AddRestaurantModal.tsx`'s direct client-side `.insert()` silently fails for
a partner caller. Also traced the two non-reproducing claims to exact code:
`Dashboard.tsx` returns a placeholder before ever fetching stats for
`partner-admin`/`partner-user`; `ProtectedRoute.tsx` explicitly denies those
same two roles on `/influencers` (also hidden from `AppSidebar`) and,
separately, requires `role === 'admin'` exactly for `/users` (frontend and
the backend's own `verifyAdminAccess()`). Correcting my own first-pass
misread here: I initially took `AppSidebar.tsx`'s
`item.url === '/influencers' && (hasRole('partner-admin') ...)` conditional,
seen in isolation, to imply partners could reach that page — only reading
`ProtectedRoute.tsx` and the rest of `AppSidebar.tsx` in full showed both
actually **hide/deny** it. Left in the log rather than quietly fixed,
because it's exactly the kind of misread this instance's own practice of
"verify against the filesystem before building on a claim" exists to catch,
and it applies to a PM's own mid-investigation inference as much as to a
prior pass's artifact.

**Project scoping.** Primary `aiorders-admin-hub` (the literal admin panel,
where acceptance criteria are observed), same split precedent
`ENG-003`/`ENG-008`/`ENG-011` used — the `aiorders-api` backend handler fix
and RLS migration are named explicitly above rather than inventing a
multi-project ticket shape. Both worktrees already exist on this host
(`_eng/aiorders-admin-hub`, `_eng/aiorders-api`).

**One ticket, not split.** Both confirmed defects (read-scoping,
write-rejection) trace to the same root cause — the partner role was added
to the top-level `admin-portal` gate and to the Brands page, but never
propagated to the `restaurants` handler or its RLS insert policy — and touch
adjacent, small surfaces (one handler function, one migration). Unlike
`ENG-014`'s two-item split, there's no natural, independently-shippable
boundary here worth the ceremony of a second ticket.

**No standing question filed separately.** The auto-approve-on-create fork
(acceptance criterion 5) is bundled into this G1 rather than given its own
gate item — it's a single default, doesn't change file/repo scope or size,
and doesn't block the rest of the fix, unlike `ENG-011`'s "tickets" or
`ENG-013`'s presignup-leads forks, which could each roughly 10x their
ticket's cost depending on the answer. A bare "approved" on this G1 is
informed consent to the proposed default (held for review); a one-line
rider is enough to flip it.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, `intake`
  event pass, context this exact request file). Per this event's own
  narrower contract, worked only this one request end to end — did not
  sweep the rest of `agents/product-manager/inbox/` (seven other unshaped
  requests untouched, each with its own `intake` event already queued or
  pending).

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket
  yet to scope to): exit 0, clean.

  **Caps verified fresh from `inbox/` directly, not the (stale) board
  index**, before raising: `ENG-009`'s, `ENG-010`'s G1s and `ENG-013`'s
  standing question all carry a `decision:` already (approved, approved,
  approved respectively) but sit unprocessed — treated as closed for cap
  arithmetic per this board's established convention (an answered gate item
  is off the count immediately). `ENG-012`'s G1 likewise carries `decision:
  rejected`, also closed. Only `ENG-014`'s G1 is genuinely open. Read this
  way: approver-facing WIP 1/2, approval cap 1/3 — one WIP slot and two
  approval-cap slots free before this ticket's own G1.

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's own reading plus a blind architect reading (subagent, `opus`,
  raw request + `knowledge/business-profile.md` only, no repo access, no
  exposure to this PM's own reading). **No material divergence on intent** —
  both converged on a systemic, data-layer tenancy-scoping gap rather than
  isolated page bugs, and the architect's reading additionally,
  independently guessed that an agency→brand→location ownership relationship
  would have to already exist for the request to make sense at all —
  confirmed true against the live schema (see PRD Readback and Evidence).

  **Real investigation against both live repos before proposing anything**,
  same practice `ENG-005`/`ENG-007`/`ENG-008`/`ENG-011`/`ENG-013`/`ENG-014`
  established — full trace in Notes above and the PRD's own Evidence
  paragraph. Found the two reported symptoms (locations visible platform-wide,
  can't add a location) are real and precisely reproducible; found two of the
  four originally-named symptoms (Dashboard, Influencers) do not reproduce on
  this branch, already hard-blocked rather than leaking. Resolved the "or
  user" ambiguity in the raw text by checking `/users` directly rather than
  asking the approver to choose a reading — also already hard-blocked.

  **PRD written**:
  `agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md`.

  **G1 required** — deliberately not relying on the `security`-type auto-skip;
  see Notes above for the reasoning. Wrote
  `inbox/2026-08-29-eng015-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: aiorders-admin-hub`, recommendation to build now, with
  the Dashboard/Influencers discrepancy and the auto-approve default both
  surfaced in the readback for a one-tap confirm-or-correct). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  the department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  1/2 → 2/2 (at cap, not over); approval cap 1/3 → 2/3 (one slot free);
  `machine_wip` unaffected.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract (act on the named request; don't sweep the whole board) — not run
  beyond the fresh cap-verification above. `ENG-007` through `ENG-014`
  untouched. The four-deep answered-but-unprocessed backlog
  (`ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question) is now five consecutive
  `intake` passes old without a `decision` event or dead-end sweep picking
  any of them up — re-flagged in `observations.md`, not fixed here, same as
  every pass before this one.

  **Notify sweep:** this pass's own G1 raised and stamped above. Nothing
  else to nudge — `ENG-014`'s G1, the only other genuinely-open item, was
  `notified: 2026-08-29T12:08:45`, well under the 24h nudge threshold.
  Approval cap 2/3, not full — no stall.

  **Observations filed** (`observations.md`): the confirmed root causes for
  both real defects; the three-of-four-symptoms-already-partially-fixed
  pattern (page-by-page "block outright" rather than real scoping); the
  corrected first-pass misread of `AppSidebar.tsx` in isolation.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: see pass notes.

- `2026-08-29` `awaiting-scope → designed` (product-manager → architect,
  `watch` event pass, context `schtasks`) — swept all three watched inboxes
  per the event's own contract; found `inbox/2026-08-29-eng015-g1-scope.md`
  answered (**approved**, `decided: 2026-08-29T16:12:24.708073+00:00`, no
  additional comment — bare approval of the proposed default that a
  partner-created restaurant is held for staff review) since the last pass
  touched it. Mode check clean. Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (multiple
  tickets touched this pass): exit 0, clean.

  PRD `status: approved`. Gate item moved to `inbox/_handled/` with a
  processed footer. Journaled in `agents/eng-manager/config/decision-journal.md`.

  **Handed to the architect at `designed`, design work itself not started
  this pass** — same reasoning as `ENG-014` directly above and `ENG-004`'s
  precedent: the actual fix (a role branch in `getRestaurants()`, an RLS
  policy change on `restaurants`' `INSERT`, plus the held-for-review default
  on partner-created rows) is real design/implementation-adjacent work
  against a live cross-tenant security gap, not board bookkeeping — belongs
  in a dedicated `continue ENG-015` session, not folded into this
  narrowly-scoped `watch` pass.

  **Capacity freed, not spent on anything else this pass.** Combined with
  `ENG-014`'s G1 clearing above, both approver-facing WIP slots (2/2 → 0/2)
  and both of the two remaining approval-cap slots this pass found occupied
  (→ 0/3) are now free. `ENG-023`'s own G1 (drafted, held at `shaped`
  waiting exactly for this) is the natural next thing to raise, but per the
  `ENG-004` precedent that is dispatching newly-freed capacity onto a
  *different* ticket than the one this event found changed — left for the
  next `scheduled`/`watch`/`continue` pass rather than done here.

  **Dead-end sweep (scoped to this event):** no other action needed on
  `ENG-015` itself.

  `chained: ENG-015` — `designed`, owned by `architect`, an agent-owned
  state; firing
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

- `2026-08-29` `designed` (no state change), `decision` event pass, context
  `2026-08-29-eng015-g1-scope.md` — this event's own queued fire, drained
  from `traces/.pending` at 15:34:45, behind (after one collapsed
  duplicate) the `decision (2026-08-29-eng014-g1-scope.md)` repair pass
  immediately before it (`pass end: decision (exit 0, 685s)` at 15:33:53 →
  `draining queued event: decision (2026-08-29-eng015-g1-scope.md)`,
  15:34:45, no gap). Mode check clean (`.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: exit 0, clean.

  **Verified fresh rather than trusted the entry above.**
  `inbox/2026-08-29-eng015-g1-scope.md` is gone from `inbox/`, sits in
  `inbox/_handled/` with its "Processed" footer intact; PRD `status:
  approved`; `decision-journal.md` carries the matching `ENG-015` G1 row
  with the same `decided:` timestamp. The prior `watch` pass's substantive
  work checks out — nothing here to redo.

  **What that pass did not finish: its own recorded chain never actually
  fired** — exactly the gap the immediately-preceding `decision ENG-014`
  pass found and repaired on the sibling ticket, and named in its own log
  and in `observations.md` as applying identically here.
  `traces/eng-loop-2026-08-29.log` has no `pass start: continue (ENG-015)`
  anywhere in it, and `traces/.pending` carried no `continue ENG-015` line
  before this pass's own edit below — the fire was never made, not merely
  still queued. Same root cause as `ENG-014`: the `watch` pass that
  processed both G1s (pid 36150, per `traces/.pass-out.36150`) never
  exited cleanly — `clearing stale lock (2103s old, owner 36150 gone)`
  shortly after — consistent with it dying before the shell invocation for
  either ticket's next hop ever ran. The record of intent survived; the
  action it promised did not.

  **Action taken:** re-fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  directly. Confirmed rather than assumed: `traces/.pending` now carries
  `1 continue ENG-015`; `traces/.loop.lock/pid` reads `1909`, confirmed
  alive via `ps -W` (a live `/usr/bin/sh`, not a stale MSYS PID `tasklist`
  fails to resolve) — it queued correctly behind this still-running pass
  instead of being silently lost a second time.

  **No state change made here, deliberately.** This pass does not attempt
  the architect's own design work inline — `designed`'s exit condition is
  that work's actual output, which belongs in the dedicated session the
  now-genuinely-queued chain will launch.

  **Dead-end sweep (scoped to this ticket only, per this event's own
  contract):** complete — the one broken chain this event names is now
  repaired. Not extended to the rest of the board.

  `chained: ENG-015` — re-fired this pass and confirmed on the queue (see
  above); this line records that fire, not a restatement of the previous
  pass's unfulfilled one. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: exit 0, clean.
