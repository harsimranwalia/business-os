---
id: ENG-015
title: Agency/reseller (partner) users — brand-scoped locations and a working add-location path
project: aiorders-admin-hub
type: security
size: M
time_estimate: half a day to a day
time_spent: ~2h build, round-1 combined review/quality hop (fail), ~1h
  round-1-fix build hop, ~1h round-2 combined review/quality hop (pass),
  ~30m security gate (pass), ~30m release-readiness hop (two PRs opened)
time_remaining: none for the department. Waiting on the approver's own
  merge of both PRs, on their own schedule (L1). No approver time_impact
  beyond that merge.
severity: P1
priority:
state: blocked
owner: approver
lane: full
blocked_on: approver
blocked_from: ready-to-ship
source: approver
created: 2026-08-29
updated: 2026-09-03
branch: fix/ENG-015-agency-reseller-brand-scoping (same name, both repos)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md
  design: agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md
  adrs: [ADR-006]
  review: agents/principal-engineer/reviews/ENG-015.md
  test_plan: agents/qa/test-plans/ENG-015.md
  security_review: agents/security/reviews/ENG-015.md
  release:
  pr:
    aiorders-api: https://github.com/harsimranwalia/aiorders-api/pull/10
    aiorders-admin-hub: https://github.com/harsimranwalia/aiorders-admin-hub/pull/8
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

<!-- merge note: local (HEAD) recorded a 2026-08-29 `continue ENG-015` entry
  claiming design work was completed that pass. Remote's 2026-08-31
  `scheduled` entry below investigated and found zero trace-log evidence
  that pass ever ran and no design file on disk, directly contradicting
  the local claim; remote's later, corroborated account is kept and the
  local entry is dropped rather than merged in. -->
- `2026-08-31` `designed` (no state change), `scheduled` event pass, context
  `launchd`. Whole-board safety-net sweep. Mode check clean (business-os
  `.env` → `MODE=active`; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-015`) and whole-board: both exit 0, clean.

  **The 2026-08-29 re-fire, confirmed queued that day, never actually ran —
  same shape as `ENG-014`, found while investigating that ticket.** Grepped
  every `traces/eng-loop-*.log` this instance has ever written for `pass
  start: continue (ENG-015)`: zero matches, in any log, ever, against a
  confirmed-working format (`ENG-008`/`ENG-013` today). No design file
  exists at `agents/architect/designs/ENG-015-*.md`. This ticket is
  security-typed (`P1`, live cross-tenant data exposure — see this ticket's
  own Problem section) and has now sat undesigned for two full days behind
  a chain record that said otherwise. Not the known redundant-dispatch
  race (two events chasing a completed action) — the design was never
  written at all. Root cause not fully determined; see `ENG-014`'s own
  entry this same pass for the parallel reasoning, and
  `agents/eng-manager/proposals.md` (this pass) for the filed gap.

  **Action taken:** unlike `ENG-014` (already sitting queued at this pass's
  start), `continue ENG-015` was **not** in `traces/.pending` — re-fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  directly and confirmed rather than assumed: `traces/.pending` now carries
  `1 continue ENG-015`, queued behind this still-running pass (lock owner
  `34458`, this pass's own PID).

  `chained: ENG-015` — re-fired this pass and confirmed on the queue.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-015`) and whole-board: both exit 0, clean.

- `2026-08-31` `designed` (no state change), `continue` event pass, context
  `ENG-015`. Narrow scope per the event's own contract (resume this ticket
  from its current state; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-015`) and whole-board: both exit 0, clean.

  **This is the design work three prior passes recorded chaining to and none
  of them actually reached** — same shape as `ENG-014`'s own dedicated
  session and the immediately-preceding `scheduled` sweep's finding: at pass
  start, `continue ENG-015` absent from `traces/.pending` (already drained
  to launch this session); no design file existed at
  `agents/architect/designs/ENG-015-*.md`.

  Read the real code across both repos this ticket touches — not the PRD's
  summary — before designing anything: `aiorders-api`'s
  `admin-portal/handlers/restaurants.ts` (all four functions, not only
  `getRestaurants()`), `brands.ts` (the pattern the PRD suggested mirroring),
  `_shared/restaurantAccess.ts` and `proxy-login/index.ts` (existing
  brand-ownership-check precedents), every migration touching `restaurants`'
  or `brands`' RLS (not just the initial one the PRD cited), and
  `admin-portal/index.ts`'s auth middleware (confirms `auth.user.profile`
  shape). On `aiorders-admin-hub`: `AddRestaurantModal.tsx`,
  `AuthContext.tsx`, `Brands.tsx`, `PartnerBrandAssignment.tsx`,
  `Restaurants.tsx`.

  **Tracing the RLS history changed the design from what the PRD proposed.**
  The PRD suggested fixing `getRestaurants()` "the same way `brands.ts`
  already does it" (branch to the RLS-scoped client for non-admin). Three
  migrations after the one the PRD cited (`20250814065341` through
  `20250814065606`) already locked `restaurants`' public SELECT down to
  `USING (false)` and moved public reads to a separate `restaurants_public`
  view — so that branch would return **zero rows** for a partner today, not
  their own brand's rows; no live policy grants a partner anything on this
  table. Separately, `brands` — the table `brands.ts`'s own version of this
  pattern depends on — has **zero RLS policies in tracked migration history
  at all** (`git grep -n "ON public.brands"` across every migration: no
  matches), the same untracked-schema-history gap the PRD already names for
  `profiles`/`influencers`, now confirmed for a second table. Designed
  around both findings instead of building on either: brand scoping is
  enforced in code (service-role client, explicit `brand_id` filter/check),
  not by trusting either table's RLS. Recorded as `ADR-006` — reversible, not
  a one-way door, same precedent `ADR-004`/`ADR-005` set for deciding and
  logging rather than escalating to G2.

  **Extended the fix to two functions the PRD's Evidence section didn't
  name.** `getRestaurantById()` and `updateRestaurant()` share the identical
  unconditional-service-role defect `getRestaurants()` has, on the same
  file, the same resource, reachable today by a partner via a direct
  `GET`/`PUT /admin-portal/restaurants/:id` call — squarely inside AC2's own
  wording ("enforces the same brand scoping itself... not just a UI
  filter") and the PRD's Outcome, even though the Evidence section named
  only the list endpoint. Logged as a deliberate scope decision rather than
  silently expanded or silently left as a same-severity gap in a ticket
  about exactly this gap — same practice this ticket's own G1 notes already
  modeled.

  **Found a third, unrelated defect in the same file, filed rather than
  fixed.** `updateBrandOwner()` uses the service-role client with no role or
  ownership check at all — any partner can rewrite any brand's owner
  contact info (`profiles.name/email/phone`) platform-wide. Different
  resource and failure mode than this PRD's Problem/Outcome/AC describe
  (brand-owner profile data, not restaurant visibility/add-location) — not
  folded in here. Filed as a proposal, `agents/eng-manager/proposals.md`
  (architect-originated finding, `schedules/eng_build_loop.md` step 3), not
  a ticket and not a silent fix.

  **Design written:**
  `agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md`. One
  new local helper pair in `restaurants.ts` (`isStaff`,
  `getPartnerBrandIds`) applied to all three read/write functions; one new
  migration (`INSERT` policy on `restaurants`, brand-scoped, `WITH CHECK
  (approved = false)` — makes AC5's default un-bypassable by a client rather
  than trusting the frontend alone); one small `AddRestaurantModal.tsx`
  change (send `approved: false` for a partner caller — required for AC3 to
  work at all once the new policy lands, not only for AC5's default to be
  honest). `ADR-006` recorded for the RLS-vs-code-side-scoping call. Ticket
  frontmatter updated: `links.design`, `links.adrs: [ADR-006]`.

  **Stays at `designed` regardless — held by the machine WIP cap, not a
  gate.** Re-verified fresh from each ticket's own frontmatter, not the
  board index: `ENG-008` (`in-qa`), `ENG-009`/`ENG-010` (`ready`), `ENG-013`
  (`ready-to-ship`) — four tickets inside the counted `ready`..`ready-to-ship`
  range against a cap of 1, unchanged from this morning's `scheduled` sweep.
  Design work itself is exempt from this cap; entering `ready` is not, so
  this pass does not attempt it — no branch created in either worktree, no
  code written, per the same precedent `ENG-014`'s dedicated design session
  set.

  **0 transitions** — ticket stays at `designed`; the cap, not the hop
  budget, is what stopped it. Machine WIP unaffected (still 4/1, `ENG-015`
  was never inside the counted range). Approver-facing WIP and approval cap
  both unaffected — no gate raised.

  **Dead-end sweep (scoped to this ticket only, per this event's own
  contract):** complete for `ENG-015` — the chain gap the `scheduled` sweep
  flagged this morning is now closed by this pass actually reaching the
  design work. Not extended to the rest of the board.

  `chained: none` — held by the machine WIP cap (4/1:
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` occupying), one of the documented
  no-chain conditions. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-09-03` **cap cleared — `designed → ready`** (eng-manager, `scheduled`
  event pass, context `auto-drain` — whole-board sweep). Mode check clean
  (`MODE=active`). Pre-pass `eng-gate-check.sh`, whole-board: exit 0, clean.

  Machine WIP re-verified fresh from frontmatter, not the board index:
  `ENG-022` (this same pass-chain's own release-readiness hop, tonight)
  vacated the sole slot — `blocked` sits outside the counted
  `ready`..`ready-to-ship` range — leaving it genuinely `0/1`, free. Named
  as this board's own two next-candidates, both checked fresh rather than
  taken on the board index's citation: `ENG-015` (this ticket — `designed`,
  no G2 owed, `ADR-006` already recorded in place of one) and `ENG-024`
  (`shaped`, fast lane, G1 auto-skipped). Equal severity (`P1`) and equal
  (unset) `priority` on both — tie-break to the lower ticket id, per
  `eng_build_loop.md` step 6. `ENG-015` wins it.

  **Nothing else re-litigated.** The design, the RLS-vs-code-side-scoping
  call (`ADR-006`), and every finding already on this ticket's own log
  stand as written — this hop's only job is the mechanical transition the
  cap was the sole thing blocking. `links.design`/`links.adrs` unchanged.
  No branch cut yet, no code written — that is `building`'s own work, a
  fresh session's job by this loop's own design (each heavy step gets
  fresh context), not crammed into an already-large whole-board sweep.

  **1 transition** (`designed → ready`). **Consequence:** machine WIP
  `0/1 → 1/1`, at cap (not over) — no other `designed`/`shaped` ticket may
  enter `ready` until this one reaches `shipped`. Approver-facing WIP and
  approval cap both unaffected — no gate touched, `ready` needs no
  approver.

  **Dead-end sweep (whole-board, this pass):** covered in full at the
  board-index entry for this pass — clean, no broken chains, no
  unprocessed drops. **Notify sweep:** nothing to raise (no gate item);
  nothing to nudge (checked all eight pending items fresh this pass, none
  past 24h).

  `chained: ENG-015` — `ready` is agent-owned and chains immediately once
  nothing else holds it (the cap that was suppressing this ticket
  specifically is now the thing that just cleared). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits. Post-pass `eng-gate-check.sh`, scoped
  (`ENG-015`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-09-03` **`ready → building` — the actual build, both repos**
  (`continue` event pass, context `ENG-015`, its own turn at the front of
  `traces/.pending` reached). Narrow scope per the event's own contract
  (resume this ticket from its current state; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Gate check, scoped (`ENG-015`) and
  whole-board: both exit 0, clean (run mid-pass rather than strictly
  before the first edit — this pass's own frontmatter/proposals.md edits
  below were already made when it ran; noted rather than mis-labeled
  pre-pass).

  **Worktrees.** Both `~/Documents/projects/_eng/aiorders-api` and
  `~/Documents/projects/_eng/aiorders-admin-hub` already existed on this
  host, sitting on other tickets' branches (`fix/ENG-022-...`,
  `feat/ENG-008-...` respectively) — each clean but for `aiorders-api`'s
  pre-existing untracked `supabase/functions/brand-portal/deno.lock`
  (already named on `ENG-022`'s own log; not touched, not carried onto
  this ticket's branch). `git fetch` both, then re-verified the three
  target files fresh against `origin/main` (`git diff origin/main --
  <file>`, empty on all three) before trusting anything read from the
  design/PRD against a checkout that wasn't actually on `main` — no
  drift found; both `restaurants.ts` and `AddRestaurantModal.tsx` match
  the design's Evidence section verbatim, byte for byte. Branched both
  repos fresh off `origin/main` as `fix/ENG-015-agency-reseller-brand-scoping`,
  same name both repos, same convention `ENG-011`/`ENG-013` used (`fix/`
  prefix rather than `feat/`, matching `ENG-022`'s own precedent for a
  security-typed ticket).

  **Re-verified the design's and `ADR-006`'s schema claims directly against
  tracked migrations, rather than trusting either document's own citations**
  — no live Postgres or Supabase MCP connection reachable this pass
  (narrower than `ENG-007`/`ENG-011`/`ENG-013`'s own build passes, which had
  a working read-only MCP fallback; `deno`/`docker`/`supabase` binaries are
  present on this host but no authenticated/linked session was available).
  Read `20250729143357_initial_restaurant_rls.sql` in full: confirmed
  "Admins can manage all restaurants" (`role IN ('admin','sub-admin')`,
  `FOR ALL`) and "Restaurant owners can manage their own restaurant"
  (`auth.uid() = id`, `FOR ALL`) are the only two `INSERT`-capable policies
  on `restaurants` today — neither grants a partner anything. Read all
  three RLS-lockdown migrations `ADR-006` cites
  (`20250814065341`/`065439`/`065606`) in full: confirmed the `USING
  (false)` public-SELECT lockdown and `restaurants_public` view exist
  exactly as described. Grepped for a policy already named "Partners can
  add restaurants to their assigned brands" (none — no collision) and for
  `brands`' own `CREATE TABLE` or any index on `partner_id` in tracked
  migration history (neither exists — independently confirms `ADR-006`'s
  untracked-schema-history claim for this table, not just trusted it).
  Nothing here had drifted since the design was written on 2026-08-31.

  **Built per the architect's design
  (`agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md`) and
  `ADR-006`, read fresh at the start of this pass:**

  - **`aiorders-api`** (`b6b3024`) —
    `admin-portal/handlers/restaurants.ts`: added `isStaff(profile)`
    (admin/sub-admin, checked in `role` or `additional_roles`) and
    `getPartnerBrandIds(partnerId, adminSupabase)` (one query,
    `brands.select('id').eq('partner_id', partnerId)`, service-role client
    per `ADR-006` — bypasses `brands`' own untracked RLS deliberately, not
    an oversight). Applied to all three functions the design named:
    `getRestaurants` filters `.in('brand_id', brandIds)` for non-staff, or
    returns `{success:true, data:[], count:0}` immediately if the caller
    owns no brand yet (a valid state, not an error); `getRestaurantById`
    and `updateRestaurant` both check the target row's `brand_id` against
    the caller's owned-brand set before returning/writing, 403 `Access
    denied to this restaurant` on mismatch (wording matches
    `_shared/restaurantAccess.ts`'s existing equivalent, confirmed by
    reading that file this pass, not invented fresh). `updateRestaurant`
    needed one extra read (`select('brand_id')` before the update) the
    design's Interfaces section implied but didn't spell out as a
    separate query — noted here since the design text alone left it to
    the build hop, same category of gap `ENG-013`'s own build pass logged
    for its response-shape ambiguity. New migration
    `20260903120000_partner_restaurant_insert_scoping.sql`: the one
    `INSERT` policy verbatim from the design, `WITH CHECK (approved =
    false AND ...)`. Full schema reasoning, index check, and rollback:
    `agents/database/migrations/ENG-015-agency-reseller-brand-scoping.md`
    (written this pass).
  - **`aiorders-admin-hub`** (`8c0db46`) — `AddRestaurantModal.tsx`: added
    `useAuth()` (confirmed `profile.role`'s exact type union in
    `AuthContext.tsx` this pass rather than assuming it), changed the
    new-restaurant insert's hardcoded `approved: true` to a conditional
    (`false` for `partner-admin`/`partner-user`, `true` otherwise) — the
    only way a partner's insert lands held instead of being rejected
    outright by the new RLS policy once both repos' branches merge
    together. The `update`-mode branch (existing-restaurant Google-Place
    connect) is untouched — confirmed it never sets `approved`.
  - **Out of scope, unchanged, per the design's own Out-of-scope section:**
    `updateBrandOwner()` (same file) — no role/ownership check at all, a
    real but distinct-resource finding already on `proposals.md`
    (2026-08-31 row), not this ticket's to fix.

  **Self-tested, per this state's own exit condition and
  `engineering-standards.md`'s checklist:**
  - `deno check supabase/functions/admin-portal/handlers/restaurants.ts` —
    clean, no errors. No `deno.json` in this repo (already-named gap,
    `config/projects.md`), so a direct single-file check, same as
    `ENG-013`'s own precedent.
  - `npm run lint` in `aiorders-admin-hub` — repo-wide, 150 pre-existing
    errors / 31 warnings (identical count to `ENG-013`'s own build pass,
    confirming nothing here shifted the baseline). Grepped the output for
    `AddRestaurantModal.tsx` specifically: one pre-existing
    missing-dependency warning (line 132, `searchPlaces`) and four
    pre-existing `no-explicit-any` errors (lines 276/310/318/334) — each
    individually re-read against the current file and confirmed to be a
    prior `: any` annotation shifted by exactly +2 lines (this diff's own
    2-line insertion: one import, one `useAuth()` call), not a new one.
    Zero new lint issues introduced.
  - `npm run build` in `aiorders-admin-hub` — clean, 3340 modules, same
    pre-existing large-chunk warning `ENG-011`'s/`ENG-013`'s own
    verification already named.
  - No live Postgres reachable to execute the migration itself (see
    schema-verification paragraph above); full detail and gate verdict
    (**pass**) in the migration doc.

  **Artifact enumeration run before finishing** (step 6b):
  `grep -rn "restaurants\.ts"` and `grep -rln "ENG-015"` across both roots'
  `agents/`, `skills/`, `lib/`, `docs/`. Most hits are **location**
  references (other tickets' designs/reviews citing this file, or a
  same-named-but-different file under `brand-portal/`,
  `restaurant-portal-onboarding/`, or `restaurant-marketplace/` — confirmed
  by path, not by filename alone, that these are different files) or
  historical record (observations.md's own account of what `ENG-015`'s
  design pass found, still accurate as history regardless of this pass's
  fix). One real conflict found and fixed in this hop:
  **`agents/eng-manager/proposals.md`'s 2026-08-29 row** (architect-filed)
  still named `updateRestaurant()` as open, future S–M work, filed two days
  *before* the 2026-08-31 design deliberately pulled that exact function
  into `ENG-015`'s own scope (a reasoned, logged exception to the PRD's
  general "no full audit" non-goal — same resource, same AC2 wording, not
  a different page found by auditing). Now that this pass has actually
  shipped that fix, the row was stale in a way that would have asked the
  approver to approve future work already done. Corrected in place
  (inline addendum, matching this file's own established correction style
  — see its 2026-09-02 row): narrowed the row to `updateBrandOwner()`
  alone, which now **fully overlaps** the 2026-08-31 row below it (already
  flagged as merely "overlapping" in `observations.md`, 2026-09-01 — this
  correction closes that gap the rest of the way) — cross-referenced both
  rows to each other rather than deleting either (proposals rows aren't
  this pass's to remove unilaterally, per that same observation). One
  `ENG-019` citation of `restaurants.ts` (forward-looking: "read `ENG-015`'s
  review before writing the audience-query code") checked and left alone —
  prospective advice about a review that will exist once this ticket
  reaches `in-review`, not a claim this pass's diff contradicts.

  **Branches committed and pushed, both repos**:
  `fix/ENG-015-agency-reseller-brand-scoping` — `aiorders-api` (`b6b3024`,
  2 files: the handler + the migration), `aiorders-admin-hub` (`8c0db46`,
  1 file: the modal). Both `git push -u origin ...` succeeded; no PR opened
  yet (devops's release-readiness step, per the pipeline).

  **PR body, both repos** (`building`'s own exit condition):

  ***`aiorders-api`***
  - *What it does:* Brand-scopes `getRestaurants`/`getRestaurantById`/
    `updateRestaurant` in `admin-portal/handlers/restaurants.ts` to a
    partner's own `brands.partner_id` set, enforced in code (service-role
    client, explicit filter/check — not RLS, see `ADR-006`). Adds one RLS
    `INSERT` policy letting a partner add a restaurant under their own
    brand, hard-held for review (`WITH CHECK (approved = false)`).
  - *What it deliberately does not do:* Touch `updateBrandOwner()` (same
    file, different resource, filed separately in `proposals.md`); add a
    partner-scoped `SELECT` policy on `restaurants` (code-side filter is
    the enforcement boundary per `ADR-006`, not RLS); change staff
    (`admin`/`sub-admin`) behavior at all.
  - *Uncertainties:* Neither the handler diff nor the new policy has
    executed against any live Postgres this pass — verified instead by
    re-reading every relevant tracked migration directly (no read-only MCP
    fallback available this time, unlike `ENG-007`/`ENG-011`/`ENG-013`).
    Full reasoning: `agents/database/migrations/ENG-015-*.md`.
  - *What to review hardest:* The `updateRestaurant` ownership check runs
    *before* the update, on a freshly-fetched `brand_id` — not the
    post-update row — so a partner cannot use this endpoint to move a
    restaurant they own into a brand they don't (the check would already
    have rejected the call). Also: the new policy's `approved = false`
    clause is what makes `AddRestaurantModal.tsx`'s matching change
    load-bearing, not cosmetic — the two must ship together (named as a
    sequencing risk in the design, not an open one, since both are in this
    same ticket's branch).

  ***`aiorders-admin-hub`***
  - *What it does:* `AddRestaurantModal.tsx` now sends `approved: false`
    for a partner-admin/partner-user's new-restaurant insert instead of
    the unconditional `true` every caller got before.
  - *What it deliberately does not do:* Touch the `update`-mode branch
    (Google-Place reconnect for an existing restaurant) — confirmed it
    never sets `approved` either way. No UI change communicating "pending
    review" to the partner — not asked for by any acceptance criterion.
  - *Uncertainties:* None functional. Four pre-existing `no-explicit-any`
    lint errors and one pre-existing missing-dependency warning in this
    file, all confirmed unchanged by this diff (see Self-tested above).
  - *What to review hardest:* That this change alone, without the paired
    `aiorders-api` migration, would make every partner-attempted insert
    silently *succeed* as auto-approved (today's actual bug) rather than
    fail — the two repos' PRs must land together, not independently, for
    AC3/AC5 to both hold.

  **1 transition this pass** (`ready → building`), well under the cap of
  4 — `in-review`+`in-qa` (combined hop, this board's established
  convention) is a fresh session's work, per `eng_build_loop.md`'s "a pass
  stops after `building` on purpose." **Consequence:** no machine-WIP
  change — `ENG-015` was already the sole occupant of the counted
  `ready`..`ready-to-ship` range; `building` is still inside it.
  Approver-facing WIP and approval cap both untouched — no gate raised
  this pass. `time_spent`/`time_remaining` set in frontmatter (~2h this
  pass; review/QA/security/release-readiness hops remain).

  **Dead-end sweep (scoped to this event):** no other ticket touched,
  per this event's own narrower contract.

  **Notify sweep:** nothing to raise — `building` needs no approver gate.
  Nothing to nudge (out of this event's scope; the whole-board nudge
  check ran fresh in the immediately-prior `scheduled` pass).

  **Observations:** none new beyond the `proposals.md` correction above
  (logged there, not duplicated here).

  `chained: ENG-015` — `building` transitions to the combined review+QA
  hop next, owned by `principal-engineer`/`qa`, not the approver, not
  blocked, not terminal, not held by a cap (machine WIP unaffected, still
  `ENG-015`'s own slot). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits. Post-pass `eng-gate-check.sh`, scoped
  (`ENG-015`) and whole-board: both exit 0, clean.

  business-os itself left uncommitted — same standing default every prior
  pass has used; the commit-convention question
  (`[[project-buildloop-instance-repo-commit-gap]]`) remains open, not
  re-decided here.

- `2026-09-03` **code review round 1: FAIL — automatic-failure #3/#10 (zero
  test coverage, third occurrence this week), plus a real authorization bug
  the missing tests let through** (principal-engineer, `continue` event
  pass, context `ENG-015` — this ticket's own turn at the front of
  `traces/.pending`, per the prior `continue ENG-015` (build) pass's own
  `chained: ENG-015`). Narrow scope per the event's own contract (resume
  this ticket only; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=active`; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-015`) and whole-board: both exit 0, clean.

  **Combined review + quality hop**, per `eng_build_loop.md` step 6 — both
  gates read the same diff in one session. Reviewed `git diff
  origin/main...HEAD` on both worktrees (fresh `git fetch` first),
  confirmed each matches the ticket's own recorded commits exactly
  (`aiorders-api@b6b3024`, `aiorders-admin-hub@8c0db46` — `git status`/`git
  log -1` on both, no drift, both clean but for `aiorders-api`'s
  pre-existing untracked `deno.lock`, already named on `ENG-022`'s log).
  `aiorders-api`: 2 files, 93 insertions / 4 deletions (`restaurants.ts`,
  one new migration). `aiorders-admin-hub`: 1 file, 7 insertions / 1
  deletion (`AddRestaurantModal.tsx`).

  **Automatic-failure scan (`engineering-standards.md`):**

  | # | Check | Result |
  |---|---|---|
  | 1 | Secret/credential/token/key committed | Clean |
  | 2 | Silent exception swallow | Clean — `getPartnerBrandIds`'s thrown error propagates to each caller's existing `catch`, which logs (`console.error`) and returns 500; not swallowed |
  | 3 | Missing test on a bug fix | **Hit** — see below |
  | 4 | Untyped public interface, undocumented | Clean — `getPartnerBrandIds`'s `adminSupabase: any` matches the file's pre-existing `AuthenticatedRequest.adminSupabase: any` shape, not a fresh violation |
  | 5 | Unbounded query / missing pagination | Clean — `getPartnerBrandIds` is scoped to one partner's own rows; the unpaginated `getRestaurants` query predates this diff |
  | 6 | New dependency, no justification | Clean |
  | 7 | Unrelated refactor bundled in | Clean — diff is exactly the three functions/helpers/migration/modal-field the design describes |
  | 8 | Commented-out code / unowned `TODO` | Clean |
  | 9 | Datastore write bypassing the data layer | Clean — no new write path beyond the design's own migration and the pre-existing `updateRestaurant`/insert calls |
  | 10 | Auth path changed, no failure-case test | **Hit** — same gap as #3, from the auth-path angle |

  **#3/#10 — zero test coverage, third occurrence of this exact shape in one
  week.** Neither `isStaff`/`getPartnerBrandIds` nor any of the three
  brand-scoping branches in `getRestaurants`/`getRestaurantById`/
  `updateRestaurant` has a test. No test proves a partner sees only their
  own brand's restaurants (AC1/2), no test proves a partner is denied a
  restaurant outside their brand on the by-id or update paths (AC2/4), no
  test proves the empty-brand-list early return. Direct precedent sits in
  the same directory today: `brands.test.ts`, `loyalty-config.test.ts` —
  and `ENG-022`, this same board, same day, shipped 24 tests for the
  identical class of fix (tenant-scoped access control) in a sibling
  handlers directory. This is the **third** occurrence of automatic-failure
  #10 on this exact `admin-portal/handlers/` family this week — `ENG-013`
  round 1 (2026-08-29) and `ENG-008` round 1 (2026-08-30), both explicitly
  logged as "not yet a third" in
  `agents/principal-engineer/notebook/2026-08-29-review-log.md` and
  `.../2026-08-30-review-log.md`, waiting for exactly this. Crosses
  `skills/code-review-gate/SKILL.md` step 10's promotion threshold — flagged
  below rather than actioned directly (see Observations).

  **Blocking correctness finding, independent of the missing tests and more
  serious: `updateRestaurant` lets a partner bypass AC5 and reassign a
  restaurant to a brand they don't own.**
  `supabase/functions/admin-portal/handlers/restaurants.ts:207–232`. The new
  ownership check (207–223) validates only that the restaurant's *existing*
  `brand_id` belongs to the caller; line 225 (`const { brand_owner,
  ...updates } = body;`) then passes every other field in the request body
  — unchecked — straight to `adminSupabase.from('restaurants').update
  (updates)`, the **service-role** client, so RLS provides no backstop here
  the way it does on the INSERT path (frontend conditional *and* the new
  `WITH CHECK` clause). Concretely:
  - **AC5 bypass.** A partner creates a restaurant under their own brand
    (correctly held, `approved: false`, per this same ticket's own fix),
    then immediately calls `PUT /admin-portal/restaurants/{id}` with
    `{approved: true}`. The ownership check passes (it's their restaurant),
    `updates` includes `approved: true` unfiltered, and the write lands —
    self-approving a row this ticket's entire AC5/migration exists to keep
    held for staff review. Not a hypothetical UI gap: AC2's own wording
    ("enforces the same brand scoping itself... not just a UI filter") is
    this ticket's own stated reason the API must be safe independent of
    what any current frontend happens to send, and that reasoning applies
    here exactly as it does to the read paths.
  - **Brand reassignment.** The same call with `{brand_id: <a brand the
    caller does not own>}` succeeds for the same reason — the check never
    inspects the *incoming* `brand_id`, only the row's current one.
  - The build hop's own PR body ("What to review hardest") claims "a
    partner cannot use this endpoint to move a restaurant they own into a
    brand they don't (the check would already have rejected the call)" —
    checked directly against the code, and this is incorrect: the check
    inspects `existing.brand_id` (line 217) and never touches
    `updates.brand_id` or `updates.approved` at all.
  - **Fix shape** (for the next build hop, not applied here): when
    `!isStaff(user.profile)`, strip `approved` and `brand_id` from `updates`
    before the write (or 403 if either is present) — the same "server
    enforces it, not just the client" principle this ticket already applies
    to the INSERT path.

  **Verified independently, not trusted from the build hop's own claims:**
  `deno check supabase/functions/admin-portal/handlers/restaurants.ts` —
  clean, matches the build log; typecheck cannot catch either finding above
  (both are authorization-logic gaps, not type errors). Confirmed the
  `AddRestaurantModal.tsx` `update`-mode branch (Google-Place reconnect)
  never sets `approved`, matching the build log's own claim. Confirmed
  `AuthContext.tsx`'s `Profile['role']` union includes the exact literals
  (`'partner-admin' | 'partner-user'`) the modal's new conditional checks
  against — no typo. `admin-portal/index.ts`'s `authenticate()` confirms
  `user.profile` (the shape both `isStaff` calls and this review's own
  reasoning depend on) is `{role, additional_roles}`, matching the design.
  Wording of the new 403 (`'Access denied to this restaurant'`) matches
  `_shared/restaurantAccess.ts`'s existing convention verbatim. No migration
  name collision (`grep -rln` across `supabase/migrations/`: one match,
  this ticket's own file).

  **Verdict: FAIL, round 1.** No receipt written
  (`agents/principal-engineer/reviews/ENG-015.md` stays absent, per
  `skills/code-review-gate/SKILL.md` step 8 — a receipt is written on `pass`
  only). QA's hop not run this round — discarded per the combined-hop
  design (the code is about to change); no
  `agents/qa/test-plans/ENG-015.md` written.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`), same precedent `ENG-008`'s and `ENG-013`'s own round-1
  entries set. `machine_wip` unaffected, still 1/1 (`ENG-015`).
  Approver-facing WIP and approval cap both unaffected — a code-review
  failure is not an approver-facing gate. `time_spent`/`time_remaining`
  updated in frontmatter.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** nothing raised — a review
  failure routes back to `building`, not to the approver.

  **Observations filed** (`observations.md`): the third-occurrence
  standards-promotion flag for `engineering-standards.md` step 10 (file
  lives in the read-only department tree — noted, not edited, same
  precedent `ENG-010`'s 2026-09-02 security-gate entry set for exactly this
  situation); and, unrelated to this ticket's own diff, a discrepancy
  noticed while reading instance config for this hop —
  `config/config.yaml`'s `wip.approver_limit` reads `unlimited` (raised
  2026-09-02, per the file's own comment) while this board's own header and
  every dated entry since have kept computing and enforcing an `8/2, over
  cap` limit of 2 — flagged, not resolved, since it's outside this
  narrowly-scoped ticket and touches board-wide accounting this event's own
  contract doesn't cover.

  `chained: ENG-015` — `building` is agent-owned (round 1's two findings
  are the next hop's own work: strip the mass-assignment gap, add the
  missing tests), not the approver, not blocked, not terminal, not held by
  a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

  business-os itself left uncommitted — same standing default every prior
  pass has used; the commit-convention question
  (`[[project-buildloop-instance-repo-commit-gap]]`) remains open, not
  re-decided here.

- `2026-09-03` **round-1-fix build hop: mass-assignment bug closed, 22 tests
  added** (eng-manager, `continue` event pass, context `ENG-015` — this
  ticket's own turn at the front of `traces/.pending`, per the round-1
  review's own `chained: ENG-015`). Narrow scope per the event's own contract
  (resume this ticket only; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-015`) and whole-board: both exit 0, clean. Both worktrees
  already on `fix/ENG-015-agency-reseller-brand-scoping`, clean but for
  `aiorders-api`'s pre-existing untracked `brand-portal/deno.lock` (same one
  named on every prior pass's log, still not this ticket's).

  **Fix (`aiorders-api`, `admin-portal/handlers/restaurants.ts`).** Read
  round 1's own finding fresh against the live file rather than trusting the
  review's prose alone — confirmed line-for-line: the ownership check at
  what was then lines 207–223 validated only `existing.brand_id`, then
  `const { brand_owner, ...updates } = body` let every other field, including
  `approved`/`brand_id`, reach the service-role `.update(updates)`
  unfiltered. Applied the review's own first-listed fix shape (strip, not
  403) over the "or 403 if either is present" alternative it also named:
  a partner caller that merely echoes back a restaurant's current
  (unchanged) `approved`/`brand_id` value — a realistic shape for a form that
  round-trips the full record — would be rejected outright under a
  presence-based 403, where stripping harmlessly no-ops on an unchanged
  value and still blocks a changed one. No existing precedent in this
  codebase settles it either way (`brand-portal/profiles.ts`'s own
  update-field handling is an allow-list building `updateData` field-by-field,
  not a strip/reject-on-forbidden-field pattern, and doesn't even guard
  `role` — a distinct, real gap, out of scope, not filed here since it isn't
  this pass's own diff to extend into). Added `isStaff`'s companion,
  `stripPartnerRestrictedFields(updates)`, deleting `approved`/`brand_id`
  from a shallow copy; `updateRestaurant` now computes `staff =
  isStaff(user.profile)` once (previously called twice) and applies the
  strip only on the non-staff branch — staff behavior (AC6) byte-for-byte
  unchanged. Exported both `isStaff` and the new helper (previously
  module-private) to unit-test them directly, matching this file family's
  own convention (`brands.ts`'s exported `deriveStage`/`deriveHealth`,
  `loyalty-config.ts`'s exported `hasLoyaltyConfigAccess`) rather than only
  exercising them indirectly through the HTTP handler.

  **Tests added:** `admin-portal/handlers/restaurants.test.ts`, new file, 22
  `Deno.test` cases — zero existed before this hop, the exact gap round 1's
  #3/#10 automatic-failure hit named. Modeled the fake-Supabase-client shape
  directly on `ENG-022`'s reviewed `offers.test.ts` (this same board, same
  day, the review's own cited precedent for this class of fix): a
  `.from(table)` router over per-table resolvers supporting
  `select`/`update`/`eq`/`in`/`order`/`single`/`maybeSingle`/`then`, with
  every `.update()` call recorded so a test can assert on the exact payload
  that would have reached Postgres — not just on the HTTP response. Coverage,
  mapped to what round 1 named as missing: `isStaff` (7 cases: admin,
  sub-admin, partner-admin, partner-user, `additional_roles` both ways, a
  missing `additional_roles` not throwing) and the new strip helper (2
  cases) as direct pure-function tests; `getRestaurants` — staff unfiltered
  (AC6), partner sees only their own brand (AC1/AC2), a brand-less partner
  gets `{success:true,data:[],count:0}` **without the `restaurants` table
  ever being queried** (proved by a `from()` override that throws if that
  table is touched on this branch — the specific "empty-brand-list early
  return" gap round 1 named, same throw-on-unstubbed-table technique
  `loyalty-config.test.ts`'s `uncalledAuth` already established for this
  repo); `getRestaurantById` — staff unrestricted, partner allowed within
  brand, partner denied (403) outside it, partner denied on a
  `brand_id: null` row (AC2); `updateRestaurant` — staff can still set
  `approved`/`brand_id` (AC6), partner can update an unrelated field on
  their own restaurant, partner denied (403) outside their brand with **zero
  `.update()` calls recorded** (proves the ownership check still runs before
  any write), plus the three cases naming round 1's own findings directly:
  self-approve blocked, brand reassignment blocked, and both stripped
  together while an accompanying legitimate field (`name`) still lands in
  the same write — proving this is a strip, not a full-body rejection.

  **Mutation check, executed, not hand-traced — same rigor `ENG-022`'s own
  round-1 review used and was praised for in its own verdict.** Temporarily
  reverted the fix line (`const updates = rest` — the exact pre-fix
  behavior) and re-ran the suite: **exactly** the three tests naming round
  1's findings by name went red (`self-approve`, `brand reassignment`, `both
  stripped together`); all other 19 stayed green, confirming those three are
  wired to this specific fix and not vacuous, and that nothing else changed
  behavior. Restored the fix; `diff` against a pre-mutation backup confirmed
  byte-identical restoration; re-ran clean.

  **Self-tested:**
  - `deno check supabase/functions/admin-portal/handlers/restaurants.ts` —
    clean, no errors.
  - `deno test --no-check supabase/functions/admin-portal/handlers/restaurants.test.ts`
    — **22 passed, 0 failed.**
  - `deno test --no-check supabase/functions/admin-portal/handlers/` (whole
    directory, checking for cross-file interference) — first run: **77
    passed, 1 failed**
    (`brands.test.ts`: "deriveHealth: exactly 14 days ago is still active
    (boundary is inclusive)"). Investigated rather than dismissed:
    `brands.ts`/`brands.test.ts` are untouched by this diff
    (`git diff --stat origin/main -- ...brands.ts ...brands.test.ts` empty on
    both), the same file passed 12/12 twice in isolation immediately after,
    and a second full-directory run passed **78/78** with no code change in
    between — a pre-existing, wall-clock-boundary-sensitive flake in a test
    literally named "boundary is inclusive" comparing against `Date.now()`,
    not a regression this diff introduced. Filed to `observations.md`, not
    fixed — different file, different ticket, and file-touch is the
    documented boundary for what a build hop corrects in passing (step 6b),
    not open-ended flake-hunting.
  - No live Postgres reachable this pass either (same gap the original build
    hop logged); nothing in this hop's diff touches schema or the migration,
    so nothing new to re-verify there.

  **Artifact enumeration run before finishing (step 6b):** `grep -rln
  "updateRestaurant\|mass-assignment\|mass assignment\|AC5-bypass\|AC5 bypass"`
  across `agents/` and `inbox/` (both roots) and the department tree. Every
  hit is either this ticket's own artifacts (this file, the PRD, the design,
  `ADR-006` — updated by this same entry) or already-correct history: the
  2026-08-29 and 2026-08-31 `proposals.md` rows about this file's
  `updateRestaurant()`/`updateBrandOwner()` pair were already corrected by
  the prior build hop (2026-09-03) to say `updateRestaurant()` "is no longer
  open" and narrow both rows to `updateBrandOwner()` alone — re-read fresh
  this pass, still accurate: neither row claims anything about the
  mass-assignment gap specifically that this hop's fix would contradict, and
  `updateBrandOwner()` (the only thing either row still calls open) is
  untouched by this hop, correctly. The original filed finding,
  `inbox/_processed/2026-08-29-restaurant-detail-write-partner-exposure.md`,
  is frozen history in `_processed/` per step 3's own convention — not
  re-edited. Nothing to correct this round.

  **0 transitions** — `state`/`owner` unchanged (`building`/`eng-manager`),
  same shape as every round-1-fix hop on this board that doesn't itself
  reach the next gate. Machine WIP unaffected, still 1/1 (`ENG-015`).
  Approver-facing WIP unaffected — no gate raised. `time_spent`/
  `time_remaining` updated in frontmatter.

  **Committed and pushed, `aiorders-api` only** (`aiorders-admin-hub` has no
  round-1 findings — both were backend-only — so it's untouched this hop):
  `99ea353` on `fix/ENG-015-agency-reseller-brand-scoping`, 2 files (378
  insertions, 3 deletions — the handler fix plus the new test file). Pushed
  clean: `b6b3024..99ea353`. No PR exists yet for either repo (devops's
  release-readiness step, unchanged from the original build hop).

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise or nudge — `building` needs no
  approver gate.

  **Observations filed** (`observations.md`): the pre-existing
  `brands.test.ts` `deriveHealth` boundary-timing flake found while
  self-testing (above) — unrelated file, not this ticket's to fix, flagged
  for whoever next touches that file's health-bucket thresholds.

  `chained: ENG-015` — `building` → combined review+QA hop next (round 2),
  owned by `principal-engineer`/`qa`, not the approver, not blocked, not
  terminal, not held by a cap (machine WIP unaffected, still `ENG-015`'s own
  slot). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

  business-os itself left uncommitted — same standing default every prior
  pass has used; the commit-convention question
  (`[[project-buildloop-instance-repo-commit-gap]]`) remains open, not
  re-decided here.

- `2026-09-03` **code review + QA round 2: PASS — `building → in-security`**
  (principal-engineer/qa, `continue` event pass, context `ENG-015`, its own
  turn at the front of `traces/.pending`). Both round-1 findings verified
  fixed, independently re-derived (mutation check re-run fresh, not
  trusted from the fix hop). Automatic-failure scan: clear. Receipts:
  `agents/principal-engineer/reviews/ENG-015.md`,
  `agents/qa/test-plans/ENG-015.md`. Full reasoning, non-blocking notes,
  and QA's one named coverage gap (AC3/4/5 — the add-location write path
  rests on the new RLS policy + a frontend conditional, neither
  automatable this pass — no live Postgres, no test runner on
  `aiorders-admin-hub`; de-risked by a full policy-history static trace,
  manual staging smoke-test recommended, not gated on):
  `agents/principal-engineer/notebook/2026-09-03-review-log.md`,
  `agents/qa/notebook/2026-09-03-coverage-gaps.md`. **1 transition**
  (`building → in-security`). Machine WIP unaffected (still `ENG-015`'s own
  slot — `in-security` is inside the counted `ready`..`ready-to-ship`
  range). Approver-facing WIP/approval cap untouched — no gate raised.
  `time_spent`/`time_remaining` updated in frontmatter. Pre/post-pass
  `eng-gate-check.sh`, scoped and whole-board: both exit 0, clean.

  `chained: ENG-015` — `in-security` is agent-owned (security), not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits.

- `2026-09-03` **security gate: PASS — `in-security → ready-to-ship`**
  (security, `continue` event pass, context `ENG-015` — this ticket's own
  turn at the front of `traces/.pending`, per the prior `continue ENG-015`
  (review+QA round 2) pass's own `chained: ENG-015`). Narrow scope per the
  event's own contract (resume this ticket only; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: both exit 0, clean.

  **Threat-modeled the change** (four questions, `security-gate/SKILL.md`
  step 2) before walking the checklist: no new attacker-controlled input: (
  the caller's own `restaurant_id`/`brand_id`/`approved` claims are no
  longer trusted at face value); no new capability granted (this diff
  *revokes* platform-wide reach, and the one new working path —
  add-restaurant — lands explicitly held for review); no new data exposed
  (narrows exposure, this is the fix for the ticket's own P1 leak); blast
  radius of a compromised partner session now bounded to that partner's own
  brand(s), against platform-wide reach before this diff.

  **Independently re-ran rather than trusted the round-2 review's/QA's own
  accounts:** `deno check restaurants.ts` clean; `deno test --no-check
  restaurants.test.ts` — 22/22, matched test-by-test by name against both
  prior hops' own logs. Did not re-run the mutation check a third time
  (round-1-fix and round-2 review each already executed and reported it
  independently same day — re-deriving again adds no material confidence).
  Read the full current `restaurants.ts` and the new migration in full, not
  only their diffs.

  **Walked OWASP A01–A10 per `security-baseline.md`**, each marked
  applicable or `n/a` with a reason (full table:
  `agents/security/reviews/ENG-015.md`). A01 (this ticket's own category):
  all three functions re-confirmed correctly brand-scoped; both round-1
  findings (self-approve, brand-reassignment) re-verified closed by reading
  the live diff directly, not only the receipts. A03/A04 reasoned through
  explicitly rather than assumed: the query builder is used throughout (no
  raw SQL), and the new INSERT policy's `WITH CHECK` fails closed on an
  omitted/null `approved` (Postgres evaluates `WITH CHECK` after column
  defaults apply, and treats `NULL` as a failed check the same as `false`).
  A05/A09 non-blocking notes only, both pre-existing and unchanged by this
  diff. Secrets scan (diff and branch history, both repos): clean. No new
  dependencies.

  **One new finding, more specific than anything named so far, non-blocking
  — RLS activation on `public.restaurants` itself is unverified from this
  repo**, a layer beneath the policy-*logic* trace QA already ran assuming
  RLS is active. No migration in tracked history creates the table or
  enables RLS on it — the same untracked-schema-history gap `ADR-006`
  already names for `brands`, now confirmed at the RLS-toggle level for
  `restaurants` too. Reasoned, not asserted as a live defect: this table's
  own multi-migration public-SELECT lockdown history would be pointless
  theatre unless RLS has been enforced throughout, and no incident in this
  business's history suggests otherwise. Not fixed blind — a defensive
  `ENABLE ROW LEVEL SECURITY` would be an unbounded-blast-radius change
  across all four frontends' direct-client callers, considered and
  rejected, same reasoning that kept `updateBrandOwner()` out of this
  ticket. Folded into a sharpened version of QA's own already-planned
  manual staging smoke test (confirm a test partner's insert/update is
  actually rejected or held, never unrestricted) rather than filed as a
  new proposal. Full reasoning and a second, pre-existing, already-tracked
  finding (verbose `error.message` in this file's catch blocks, not
  re-proposed): `agents/security/reviews/ENG-015.md`, Findings #1–2; also
  logged to `agents/security/notebook/2026-09-03-findings.md`.

  **Verdict: PASS.** Zero blocking findings. Receipt written
  (`agents/security/reviews/ENG-015.md`); `links.security_review` set on
  this ticket in the same edit, per `security-gate/SKILL.md` step 9 (a
  receipt is written on `pass` only).

  **1 transition** (`in-security → ready-to-ship`). **Consequence:** no
  machine-WIP change — `ready-to-ship` is still inside the counted
  `ready`..`ready-to-ship` range, `ENG-015` remains the sole occupant.
  Approver-facing WIP unaffected — this hop raises no gate; the L1 merge
  request is devops's own next hop. `time_spent`/`time_remaining` updated
  in frontmatter; `owner` moves `security → devops`.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise or nudge this hop —
  `ready-to-ship` needs no approver gate yet; that comes from devops's own
  release-readiness hop next. **Observations:** none beyond what's already
  in the two notebook entries above (both are security findings, filed to
  the security notebook per convention, not `observations.md`).

  `chained: ENG-015` — `ready-to-ship` is agent-owned (devops), not the
  approver, not blocked, not terminal, not held by a cap (machine WIP
  unaffected, still `ENG-015`'s own slot). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

  business-os itself left uncommitted — same standing default every prior
  pass has used; the commit-convention question
  (`[[project-buildloop-instance-repo-commit-gap]]`) remains open, not
  re-decided here.

  business-os itself left uncommitted — same standing default; commit
  question remains open, not re-decided here.

- `2026-09-03` **release-readiness: PASS — `ready-to-ship → blocked`, both
  PRs opened** (devops, `continue` event pass, context `ENG-015` — this
  ticket's own turn at the front of `traces/.pending`, per the prior
  `continue ENG-015` (security gate) pass's own `chained: ENG-015`). Narrow
  scope per the event's own contract (resume this ticket only; no
  board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-015`) and
  whole-board: both exit 0, clean.

  **Ran `skills/release-runner/SKILL.md` steps 1–4.** Step 1 (window check):
  both `aiorders-api` and `aiorders-admin-hub` are registered **L1**
  (`agents/eng-manager/config/projects.md`) — per the skill, step 1 does not
  apply to L1 and this pass went straight to step 4. Step 2 (upstream
  gates): all four receipts re-confirmed present and `pass` — code review
  round 2 (`agents/principal-engineer/reviews/ENG-015.md`), quality
  (`agents/qa/test-plans/ENG-015.md`), security
  (`agents/security/reviews/ENG-015.md`), migration
  (`agents/database/migrations/ENG-015-agency-reseller-brand-scoping.md`).
  Step 3 (readiness gate): **rollback** — the migration doc's own rollback
  (`DROP POLICY IF EXISTS "Partners can add restaurants to their assigned
  brands" ON public.restaurants;`) is written and reasoned through as
  independent of the handler-code changes in the same ticket, same bar this
  instance's own precedent (`ENG-007`'s 2026-08-29 release-readiness entry)
  already accepted given the standing no-live-DB constraint; the
  `aiorders-admin-hub` side has no migration, rollback is reverting the one
  commit. **Observability** — both functions' errors already propagate to
  each caller's existing `catch` (`console.error` + Supabase function logs,
  confirmed clean on the automatic-failure scan, round 1) and the new 403
  denials are consistent with this codebase's own existing convention
  (`_shared/restaurantAccess.ts`); nothing new and silent. **Cost** — no new
  service, dependency, or infra: one additive RLS policy plus a code branch
  and a one-field frontend conditional, $0/month; no cost notice required.
  **Window** — n/a, both repos L1 (step 1 doesn't apply).

  **Worked in the department's own worktrees, not the human's**
  (`~/Documents/projects/_eng/aiorders-api`,
  `~/Documents/projects/_eng/aiorders-admin-hub`), per skill step 4b.
  Verified fresh rather than trusted the prior hops' own accounts: both
  already on `fix/ENG-015-agency-reseller-brand-scoping`; `git status
  --short --branch` clean but for `aiorders-api`'s pre-existing untracked
  `supabase/functions/brand-portal/deno.lock` (same one named on every
  earlier hop of this ticket, not this ticket's own file); `git log -1`
  matches the ticket's own recorded commits exactly (`99ea353`, `8c0db46`).
  `git fetch origin` both, then `git merge-base --is-ancestor
  origin/fix/ENG-015-agency-reseller-brand-scoping origin/main` on each —
  **not an ancestor on either repo**, confirming neither branch is merged
  yet. `gh pr list --head fix/ENG-015-agency-reseller-brand-scoping --state
  all` on both repos, before opening anything — empty on both, confirming no
  PR already existed for this branch (unlike a same-named-branch collision,
  not a concern here since both repos share the ticket's own branch name by
  convention, not by accident).

  **Opened both PRs** (skill step 4, L1 route — "any day, any time," not
  gated by the window check): `aiorders-api` first (the backend the
  frontend depends on, same ordering `ENG-013` used) —
  https://github.com/harsimranwalia/aiorders-api/pull/10 — then
  `aiorders-admin-hub` — https://github.com/harsimranwalia/aiorders-admin-hub/pull/8.
  Each PR body states what it does, what it deliberately doesn't, the gates
  it passed, and — in both directions — that the two must merge together,
  not independently (the backend's new `approved = false` INSERT policy is
  what makes the frontend's conditional load-bearing rather than cosmetic;
  either alone leaves AC3/AC5 only half-satisfied, in opposite failure
  directions). `links.pr` set on this ticket as a `{project: url}` map, same
  format `ENG-013`'s own two-repo precedent established.

  **Raised one L1 merge-request item covering both PRs**
  (`inbox/2026-09-03-eng015-merge-request.md`), `pr_urls:` as a YAML list of
  `{repo, url}` pairs per the current skill format (not the single
  delimited-string format `ENG-011` used before the approver corrected it).
  Named both round-1 findings' resolution, the security review's one
  non-blocking RLS-activation finding and its folded-in staging-smoke-test
  recommendation, and the already-tracked verbose-error-message finding
  (not re-proposed). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it — exit 0 — and
  stamped `notified: 2026-09-03T10:03:53` in its frontmatter (the script
  sends the notification; stamping the field is this pass's own job, per
  `eng_build_loop.md` step 7).

  **1 transition** (`ready-to-ship → blocked`). **Consequence:** no
  machine-WIP change — `blocked` sits outside the counted
  `ready`..`ready-to-ship` range, so this pass **frees** `ENG-015`'s slot
  (machine WIP `1/1 → 0/1`) for the next To-do-column candidate on a future
  pass; not spent here, per the same precedent `ENG-004`/`ENG-022` set of
  not dispatching newly-freed capacity onto a different ticket within the
  pass that freed it. Approver-facing WIP: this ticket's blocked-on-approver
  slot is held (per the Guards section, a `blocked` ticket on
  `blocked_on: approver` counts against the approver-facing WIP limit too,
  not only an open gate) — moot this instance, since `wip.approver_limit` is
  currently `unlimited` (raised 2026-09-02; the board header's own `8/2,
  over cap` text is the stale, unconverted accounting already flagged as a
  discrepancy in this ticket's own round-1 review entry, not re-litigated
  here). `owner` moves `devops → approver`. `time_spent`/`time_remaining`
  set in frontmatter.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** this pass's own merge-request item raised and stamped
  above; nothing else to nudge — out of this narrowly-scoped event's own
  contract to sweep the rest of the approver's queue.

  **Observations:** none new — the `wip.approver_limit`
  unlimited-vs-board-header discrepancy noted above is the same one already
  filed in this ticket's own round-1 code-review entry, not a fresh finding.

  `chained: none` — **blocked on the approver**
  (`blocked_on: approver`), one of the documented no-chain conditions per
  `eng_build_loop.md` step 9 and the Guards section. The next hop is a human
  merging both PRs on GitHub; the build loop detects each merge itself by
  local git ancestry on a future pass (`scheduled`, `watch`, or a `decision`
  event once the approver answers) and advances the ticket to `shipped`
  only once **both** repos' branches have merged — no action to fire here.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-015`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

  business-os itself left uncommitted — same standing default every prior
  pass has used; the commit-convention question
  (`[[project-buildloop-instance-repo-commit-gap]]`) remains open, not
  re-decided here.
