---
id: ENG-014
title: Brand portal self-service — restaurant QR codes and marketing media downloads
project: restaurant-portal
type: feature
size: M
time_estimate: a day and a half to two days
time_spent:
time_remaining:
severity: P2
priority:
state: designed
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-31
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-014-restaurant-qr-media-self-service.md
  design: agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md
  adrs: [ADR-005]
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-on-the-brand-portal-restaurant-is-not-able-to-see-or-generea.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:20:42.534749+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # on the brand portal restaurant is not able to see or genereate the qr codes or the media downloads they have
>
> nor are they able to make changes to timing or anythings related to their
> website from the brand portal. all of this has be be done from admin
> portal which the restaurant owners dont have access to. aware that these
> are onboarding task but there can be no self onboarding if the restaurant
> owner/user is not able to do this.

## Readback

See
`agents/product-manager/specs/ENG-014-restaurant-qr-media-self-service.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Restaurant owners on the brand portal can't see, generate, or download their
own QR codes or marketing materials — confirmed in code as admin-only end to
end (UI and backend authorization both), not just a reported symptom. Every
restaurant's onboarding depends on staff doing this by hand and manually
sharing the result with the owner.

## Outcome

A restaurant/brand-manager user can view, generate, and download their own
restaurant's QR codes and marketing media (bag insert, A4 poster) from the
brand portal, with no admin-portal access and no staff hand-off required.

## Notes

**Severity called P2, not P1 or P3.** Calibrated against `ENG-013` (a
same-day "confirmed zero capability, not just a UI gap" ticket, called P2):
this ticket is the same shape — the backend path is hard-gated to admin,
not merely missing a frontend screen. Not P1: a workaround exists and is
presumably in active use (`Activation.tsx` step 8, "Share Bag Insert & QR
with Owner" — staff does this manually today), so it clears P0/P1's "no
workaround" bar.

**Evidence found, not assumed.** Full detail in the PRD's Readback section.
Summary: `restaurant-portal` (the brand portal — confirmed via its own
`brandPortalApi.ts`) has zero QR/media surface anywhere in `src/`. The two
live generators (`BagInsertGenerator.tsx`, `A4PosterGenerator.tsx`) and the
QR flow (`getRestaurantQR` → `url-shortener` function) exist only in
`aiorders-admin-hub`, reached from the staff-only `Activation.tsx` onboarding
checklist and `RestaurantDetails.tsx`. The `url-shortener` function itself
checks `profile.role === 'admin'` exactly — confirmed by reading
`aiorders-api/supabase/functions/url-shortener/index.ts` directly, not
inferred from the frontend gate — so this is a real backend authorization
gap, not a routing/UI-only fix. QR images come from a free public API
(`api.qrserver.com`); no recurring cost.

**Project scoping.** Primary project set to `restaurant-portal` (the brand
portal itself, where the acceptance criteria are observed), same split
precedent `ENG-003`/`ENG-008`/`ENG-011`/`ENG-013` used — the other repo's
work (`aiorders-api`, a new restaurant-scoped backend action) is named in
the PRD rather than inventing a multi-project ticket shape. No eng worktree
exists yet for `restaurant-portal` on this host
(`~/Documents/_eng/aiorders-admin-hub` and `~/Documents/_eng/aiorders-api`
do; `restaurant-portal` doesn't) — read from the human's checkout instead,
which `config/projects.md` records as a clean tree, for this pass's
research only; the worktree gets created at `building`, per
`config/projects.md`.

**One item intentionally not filed yet:** the website-settings/"timing"
half of the same request, and its own open question (how far "anythings
related to their website" should extend). Both readings flagged it as a
joint gap rather than resolving it — see the PRD's Readback and "Feature
shape and sequencing." Does not block this ticket.

**Found and left untouched, out of scope for this `intake` event's own
narrower contract.** Re-read `inbox/` fresh before raising this ticket's own
G1 (not trusting the board's cached header) and found all four previously
open items now answered: `inbox/2026-08-29-eng009-g1-scope.md` (approved
09:20:42), `inbox/2026-08-29-eng010-g1-scope.md` (approved 10:49:55),
`inbox/2026-08-29-eng012-g1-scope.md` (**rejected**), and
`inbox/2026-08-29-eng013-presignup-leads-question.md` (approved) — all
answered but none yet processed into their tickets' `state`/`owner`. Treated
as closed, not open, for this pass's own cap arithmetic per this board's
established convention (see `_index.md` header and prior board entries);
left unprocessed since acting on someone else's ticket is a `decision`
event's job, not this `intake` event's. This is now the fourth consecutive
pass to find this same backlog without it clearing — flagged more pointedly
than before in `observations.md`, since the pattern itself (not just the
individual items) now looks worth a dead-end sweep rather than another
re-verification. Nine-plus other requests still sit unshaped in
`agents/product-manager/inbox/` — untouched, each with its own `intake`
event already queued or pending.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, `intake`
  event pass, context this exact request file). Mode check clean
  (business-os `.env` →
  `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
  to scope to): exit 0, clean.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading plus a blind
  architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to this
  PM's own reading). **No material divergence** — both converged on the same
  shape: two portals for two audiences, QR/media already exist and are an
  access gap rather than a greenfield build, "timing" means operating hours.
  One joint gap both readings independently flagged rather than resolved:
  how far "anythings related to their website" extends — carried into item
  2's future scoping, not asked here since it doesn't gate this ticket.

  **Checked the live repos before proposing anything**, same practice
  `ENG-005`/`ENG-008`/`ENG-011`/`ENG-013` established — full detail in the
  PRD's Readback and this ticket's Notes above. Confirmed zero QR/media
  surface in `restaurant-portal`, confirmed the admin-only backend gate by
  reading `url-shortener/index.ts` directly rather than assuming from the
  frontend, confirmed the QR provider is a free API with no recurring cost,
  and confirmed the owner/admin role split is by design
  (`brand_managers`/`restaurant_managers` vs.
  `admin`/`sub-admin`/`partner-admin`/`partner-user`).

  **PRD written**:
  `agents/product-manager/specs/ENG-014-restaurant-qr-media-self-service.md` —
  acceptance criteria + non-goals naming the deferred website-settings item
  explicitly, plus a "Feature shape and sequencing" section (same pattern
  `ENG-008` used) naming it as item 2, `[proposed]`, to be filed once this
  ticket verifies.

  **G1 required** — full lane, not XS/bug/chore. Wrote
  `inbox/2026-08-29-eng014-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: restaurant-portal`, recommendation to build now). No
  separate standing-question file this time — unlike `ENG-008`/`ENG-011`/
  `ENG-013`, the one open gap (item 2's eventual scope) doesn't need an
  approver answer to move this ticket forward, so it stays inside the PRD's
  own "Feature shape and sequencing" section rather than spending an
  approval-cap slot on a question nothing is currently blocked on.

  Ran `departments/engineering/lib/eng-notify.sh raise` on the new file; see
  its own frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  the department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **Caps verified fresh from ground truth, not the cached board header** —
  see Notes above: all four previously-open inbox items are now answered,
  read as closed for this pass's cap arithmetic per established convention.
  Approver-facing WIP and approval cap both fully free (0/2, 0/3) before
  this ticket's own G1. **State:** `intake → shaped → awaiting-scope`,
  `owner` moves `product-manager → approver`, both in this pass, PRD written
  and G1 raised together per `templates/ticket.md`'s own convention.
  **Consequence:** approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 1/3.
  Machine WIP unaffected (still whatever `ENG-007`/`ENG-008`/`ENG-011`/
  `ENG-013` leave it at).

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — not run beyond the fresh cap-verification above. `ENG-007`
  through `ENG-013` otherwise untouched.

  **Notify sweep:** this pass's own new item raised and stamped above.
  Nothing else to nudge — the 24h nudge threshold doesn't apply to anything
  else on the board yet today. Approval cap 1/3, not full — no stall.

  **Observations filed** (`observations.md`): the confirmed admin-only
  backend gate on `url-shortener` grounding this PRD's Risks section; the
  free-QR-provider cost finding; the now-four-deep, four-pass-old
  answered-but-unprocessed inbox backlog, flagged more pointedly as a
  pattern.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: see pass notes.

- `2026-08-29` `awaiting-scope → designed` (product-manager → architect,
  `watch` event pass, context `schtasks`) — swept all three watched inboxes
  per the event's own contract; found `inbox/2026-08-29-eng014-g1-scope.md`
  answered (**approved**, `decided: 2026-08-29T15:54:50.916162+00:00`, no
  additional comment beyond the bare decision) since the last pass touched
  it. Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (multiple
  tickets touched this pass): exit 0, clean.

  PRD `status: approved`. Gate item moved to `inbox/_handled/` with a
  processed footer. Journaled in `agents/eng-manager/config/decision-journal.md`.

  **Handed to the architect at `designed`, design work itself not started
  this pass** — same reasoning `ENG-004`'s own `watch`-event G1 processing
  used: `designed`'s exit condition ("tech design written, ADRs logged") is
  the architect's own output, and the QR/media backend-authorization change
  this ticket needs (a new restaurant-scoped `url-shortener` action,
  possibly a new endpoint) is implementation-adjacent work against a project
  with real customer data, not board bookkeeping — it belongs in a
  dedicated `continue ENG-014` session.

  **Capacity freed, not spent on anything else this pass.** This G1 clearing
  frees one approver-facing WIP slot and one approval-cap slot; `ENG-015`'s
  G1 (processed in this same pass, below) frees the other of each. Per the
  same precedent (`ENG-004`'s `watch` entry), dispatching that freed capacity
  onto a *different* ticket waiting on it (`ENG-023`'s own G1, drafted and
  ready since it was held at `shaped` for exactly this) is left for the next
  `scheduled`/`watch`/`continue` pass — out of scope for a `watch` event
  scoped to the inbox items it found changed.

  **Dead-end sweep (scoped to this event):** no other action needed on
  `ENG-014` itself.

  `chained: ENG-014` — `designed`, owned by `architect`, an agent-owned
  state; firing
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-014`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

- `2026-08-29` `designed` (no state change), `decision` event pass, context
  `2026-08-29-eng014-g1-scope.md` — this event's own queued fire, drained
  from `traces/.pending` at 15:21 behind a `watch`/`schtasks` fire that had
  already reached this same gate item first. Mode check clean (`.env` →
  `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: exit 0, clean.

  **Verified fresh rather than trusted the entry above.**
  `inbox/2026-08-29-eng014-g1-scope.md` is gone from `inbox/`, sits in
  `inbox/_handled/` with its "Processed" footer intact; PRD `status:
  approved`; `decision-journal.md` carries the matching `ENG-014` G1 row
  with the same `decided:` timestamp. The prior pass's work checks out —
  nothing here to redo.

  **What that pass did not finish: its own recorded chain never actually
  fired.** The entry above reads `chained: ENG-014`, but
  `traces/eng-loop-2026-08-29.log` has no `pass start: continue (ENG-014)`
  anywhere in it, and `traces/.pending` carried no `continue ENG-014` line
  before this pass's own edit below — the fire was never made, not merely
  still queued. Root cause: that `watch` pass's own process (pid 36150,
  per `traces/.pass-out.36150`) never exited cleanly —
  `traces/eng-loop-2026-08-29.log` records `clearing stale lock (2103s old,
  owner 36150 gone)` shortly after — consistent with it dying at or near
  writing the log entry above, before the shell invocation that would have
  queued the next hop ever ran. The record of intent survived; the action
  it promised did not. Same class of failure `eng_build_loop.md` step 8
  names ("chaining is an instruction to a model, not a guarantee"), just
  wearing a different face than a missing record — here the record exists
  and the fire behind it is what's missing.

  **`ENG-015` carries the identical shape** (`chained: ENG-015`, same
  `watch` pass, same absence from both the trace log and the queue) — a
  second ticket, out of scope for this event's own narrow contract (named
  context is `ENG-014` only). Left untouched; flagged in
  `observations.md` instead of fixed here, so a `watch`/`scheduled`/
  `continue` pass picks it up without needing to rediscover it.

  **Action taken:** re-fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-014`
  directly. Confirmed rather than assumed: `traces/.pending` now carries
  `1 continue ENG-014`, and the trigger's own stderr read
  `lock is Ns old but PID 1909 is alive — not stealing` — it queued
  correctly behind this still-running pass instead of being silently lost
  a second time.

  **No state change made here, deliberately.** This pass does not attempt
  the architect's own design work inline — `designed`'s exit condition is
  that work's actual output, which belongs in the dedicated session the
  now-genuinely-queued chain will launch.

  **Dead-end sweep (scoped to this ticket only, per this event's own
  contract):** complete — the one broken chain this event could find is
  now repaired. Not extended to the rest of the board.

  `chained: ENG-014` — re-fired this pass and confirmed on the queue (see
  above); this line records that fire, not a restatement of the previous
  pass's unfulfilled one. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: exit 0, clean.

<!-- merge note: local (HEAD) recorded a 2026-08-29 `continue ENG-014` entry
  claiming design work was completed that pass. Remote's 2026-08-31
  `scheduled` entry below investigated and found zero trace-log evidence
  that pass ever ran and no design file on disk, directly contradicting
  the local claim; remote's later, corroborated account is kept and the
  local entry is dropped rather than merged in. -->
- `2026-08-31` `designed` (no state change), `scheduled` event pass, context
  `launchd`. Whole-board safety-net sweep. Mode check clean (business-os
  `.env` → `MODE=active`; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-014`) and whole-board: both exit 0, clean.

  **The 2026-08-29 re-fire, confirmed queued that day, never actually ran —
  a second, different break in the same chain.** Grepped every
  `traces/eng-loop-*.log` this instance has ever written for `pass start:
  continue (ENG-014)` (the exact format confirmed against `ENG-008`'s/
  `ENG-013`'s own known-good runs today): zero matches, in any log, ever.
  No design file exists at `agents/architect/designs/ENG-014-*.md`. This
  ticket's own architect-owned observation filed on `ENG-023` this same day
  ("`designed` conflates 'handed to architect, undesigned' and 'design
  complete, cap-held' — `ENG-014`/`ENG-015` turned out to be the former")
  independently corroborates the same finding from the other direction.
  This is not the known redundant-dispatch race (`observations.md`,
  multiple 2026-08-26/27 rows) — that race is two events chasing a
  **completed** action; here the action itself was never done. Root cause
  not fully determined — `traces/` is local and this instance runs on two
  hosts, and the 2026-08-29 confirmation only proves the append happened,
  not that the subsequent drain preserved or ran it.

  **Action taken:** did not re-fire — `continue ENG-014` already sits in
  `traces/.pending` at this pass's start (verified fresh, not assumed;
  likely the same entry `ENG-008`'s `continue` pass queued behind
  earlier today, though the log gives no way to distinguish that from a
  surviving remnant of the 2026-08-29 append). Firing a second `continue
  ENG-014` here would either collapse into it harmlessly or, if the
  existing entry is in fact stuck, double queue depth without fixing
  anything — left as one entry, to drain naturally behind `ENG-008`/
  `ENG-013` once this pass releases the lock.

  **Filed, not fixed here:** `agents/eng-manager/proposals.md` (this
  pass) — the dispatch gap itself (a confirmed-queued event that can
  vanish before draining, with no `eng-events-dropped`-style notice ever
  raised, unlike a pass that fails and is properly retried/dropped) is
  department machinery, not a ticket-shaped fix, and not P0 on an
  internal-lane process.

  `chained: none` — the ticket already has a queued fire; adding another
  is not a repair. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-014`) and whole-board: both exit 0, clean.

- `2026-08-31` `designed` (no state change — design work actually done this
  time), `continue` event pass, context `ENG-014`. Narrow scope per the
  event's own contract (resume this ticket from its current state; no
  board-wide sweep). This session is the dedicated `continue ENG-014` run
  three prior passes recorded chaining to and none of them actually reached —
  confirmed at pass start: `ENG-014` is absent from `traces/.pending`
  (already drained to launch this session), and the 2026-08-31 `scheduled`
  entry above independently found zero `pass start: continue (ENG-014)` lines
  in any trace log, ever, before now. Mode check clean (business-os `.env` →
  `MODE=active`; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: both exit 0, clean.

  **Design work done, for real this time.** Read the actual code across all
  three repos this ticket touches rather than trusting the PRD's own summary:
  `aiorders-api`'s `url-shortener/index.ts` (confirmed the blanket
  `verifyAdminAccess` gate and the existing `redirect` public carve-out),
  `_shared/restaurantAccess.ts` and `brand-portal/utils.ts` (two independent
  copies of `verifyRestaurantAccess`, confirmed why: `_shared`'s own comment
  says it exists so functions that deploy independently don't cross-import),
  `brand-portal/restaurants.ts` and `index.ts` (the `get_custom_reports`
  pattern this design's new action mirrors), and on the frontend side
  `qrUtils.ts`, `BagInsertGenerator.tsx`, and `A4PosterGenerator.tsx` in
  `aiorders-admin-hub` (found the same list-then-create QR logic hand-rolled
  three separate times, each building its own `destination_url`), plus
  `RestaurantDetails.tsx` (exact props passed to each generator) and
  `restaurant-portal`'s own `RestaurantContext.tsx`, `brandPortalApi.ts`, and
  `Sidebar.tsx`/`App.tsx` (confirmed `currentRestaurant` carries no
  `website`/`logo_url` today — a real gap the design has to close, not an
  assumption).

  **Design written:**
  `agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md`. One
  new restaurant-scoped action on `url-shortener`
  (`get_or_create_restaurant_qr`, gated by `verifyRestaurantAccess` instead of
  admin, computing its own `destination_url` server-side rather than trusting
  one from the caller — the detail that actually makes the scoping mean
  something); one new read action on `brand-portal`
  (`get_restaurant_media_info`) for the two fields the portal's existing
  restaurant data doesn't carry; both generator components ported into
  `restaurant-portal` (no shared package exists across these four repos to
  import from instead). `touches_data: false` — no migration, no new table or
  column. `touches_models: false` — no AI/LLM surface in this ticket.

  **One ADR, no G2.** `ADR-005` records narrowing `url-shortener`'s trust
  boundary per-action rather than per-function — a real "why on earth" a
  future engineer would ask, but reversible and following an existing
  in-repo pattern (`_shared/restaurantAccess.ts`), so decided and logged
  rather than escalated. No new datastore, vendor, or auth model; no one-way
  door. **Moves straight through `designed`, no G2** — same precedent
  `ENG-011`/`ENG-013` set.

  **Stays at `designed` anyway — held by the machine WIP cap, not a gate.**
  Verified fresh from each ticket's own frontmatter rather than the board's
  cached header: `ENG-008` (`in-qa`), `ENG-009` (`ready`), `ENG-010`
  (`ready`), and `ENG-013` (`ready-to-ship`) are all currently inside the
  counted `ready`..`ready-to-ship` range — **machine WIP 4/1, over cap** — and
  `_index.md`'s own header already names `ENG-014` through `ENG-025` as held
  by it until that count clears. This design does not attempt to push
  `ENG-014` into `ready` on top of that; per `eng_build_loop.md` step 6,
  shaping/design work is exempt from the cap, but entering `ready` is not.

  **Closes the specific ambiguity flagged against this ticket.** The
  architect's own `ENG-023` observation (2026-08-31) and the `scheduled`
  sweep above both named `ENG-014`/`ENG-015` as sitting at `designed`
  *un-designed*, not cap-held-after-completion — the two sub-states
  `designed` conflates. That's resolved for `ENG-014` specifically as of this
  pass: the design file now exists and is real; `ENG-014` is now genuinely in
  the cap-held-after-completion sub-state. `ENG-015` is untouched (out of
  scope — this event names `ENG-014` only) and remains in the other
  sub-state until its own `continue` pass runs.

  **Dead-end sweep (scoped to this ticket only, per this event's own
  contract):** none needed beyond the cap re-verification above.

  **Notify sweep:** nothing raised — no gate opened this pass (no G2), so
  nothing to notify or nudge. Approval cap unaffected.

  **Observations filed** (`observations.md`): closing the loop on the
  architect's own 2026-08-31 `ENG-023` observation for `ENG-014` specifically;
  the admin-hub QR/media destination-URL construction being hand-rolled three
  times independently, and this design adding a fourth (server-side, this
  time) rather than consolidating all four — named as a pre-existing,
  out-of-proportion-to-this-ticket pattern, not fixed here.

  `chained: none` — held by the machine WIP cap (4/1: `ENG-008`/`ENG-009`/
  `ENG-010`/`ENG-013` occupying), not waiting on the approver and not
  blocked, but explicitly one of the documented no-chain conditions
  ("held by a cap (WIP or approvals)"). Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.
