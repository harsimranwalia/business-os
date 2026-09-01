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
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-014-restaurant-qr-media-self-service.md
  design: agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md
  adrs: []
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

- `2026-08-29` `designed` (no state change — exit condition now met),
  `continue` event pass, context `ENG-014` — this fire's own turn, resuming
  the ticket from its current state per the event's own narrower contract
  (no board-wide sweep). Mode check clean (business-os `.env` → `MODE=`
  empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
  whole-board: both exit 0, clean.

  **Design work done this pass** — the immediately preceding entry named
  exactly why it wasn't done inline ("designed's exit condition is the
  architect's own output... belongs in a dedicated continue ENG-014
  session"); this is that session. Read both repos fresh from the worktrees
  rather than trusting the PRD's summary: `restaurant-portal`
  (`~/Documents/_eng/restaurant-portal`, clean, `eng/base`) and `aiorders-api`
  (`~/Documents/_eng/aiorders-api`, clean, sitting on `ENG-008`'s branch —
  confirmed via `git diff origin/main...HEAD --stat` that branch touches
  only `admin-portal`'s influencer handler, nothing this design reads, so
  safe to read from without switching branches).

  **Traced the actual code, not just the PRD's summary of it**:
  `url-shortener/index.ts` (the exact `verifyAdminAccess` gate and the
  `list`/`create` shapes), `_shared/restaurantAccess.ts` (already exists,
  already used by `api-key-auth` for the identical "restaurant-scoped path
  alongside an admin-gated function" shape — direct precedent, not a novel
  pattern), and all three existing client call sites that each do their own
  "list, filter, create-if-absent" (`qrUtils.ts`, `BagInsertGenerator.tsx`,
  `A4PosterGenerator.tsx`) — confirmed the latter two's embedded QR and the
  standalone Bag-Insert QR all resolve to the same `destination_url` (no
  `utm_source`), so the new action's `qr_type` only needs two values,
  matching the PRD's non-goal of no new QR type.

  **Design written**:
  `agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md`.
  One new restaurant-scoped action on `url-shortener`
  (`get_or_create_restaurant_qr`), inserted before the existing admin gate,
  touching none of that function's existing actions; two ported (not
  shared) frontend generator components with their admin-only QR auto-load
  effect rewritten to call the new action instead of `list`; one new page +
  nav entry + route in `restaurant-portal`. No new table, column, vendor, or
  migration — `touches_data: false`, `touches_models: false`.

  **No one-way door, no G2** — precedented by `api-key-auth`'s identical use
  of `_shared/restaurantAccess.ts`; every existing `url-shortener` action
  untouched; fully reversible. No ADR needed (`adrs: []`).

  **Two pre-existing findings surfaced during research, neither new**: the
  `verifyRestaurantAccess` misuse in `brand-portal`'s `website.ts` (result
  discarded) and `feedback.ts`/`offers.ts` (wrong argument order) are
  already tracked in `aiorders-api/supabase/functions/README.md`'s "Known
  issues" — named in the design's Risks section only as the mistake this
  new code must not repeat, not filed again as a fresh finding.

  **AC5 (checklist auto-completion) scoped out** — the PRD itself flags it
  `[proposed]`/possibly-fast-follow and leaves the mechanism to this design;
  doing it well means reaching into `admin-portal`'s
  `restaurant_activations`, untouched by everything else here, to answer a
  question (does viewing count, or only first generation?) this ticket
  doesn't need answered. Recommended as its own fast-follow once this ticket
  verifies — see the design's "Out of scope".

  **State stays `designed`.** The exit condition
  ("Tech design written; ADRs logged; one-way doors either decided or
  escalated", `definition-of-done.md`) is now met, but the mechanical flip
  to `ready` is that state's own owner's job ("Work broken down, sequenced,
  assigned; WIP slot available"), not this pass's. **`owner: architect →
  eng-manager`** — naming the next actor rather than the current one, same
  convention `ENG-022`'s own design-done entry used, citing the same
  `definition-of-done.md` `ready | eng-manager` row.

  **Not advanced to `ready`, and not chained, for the same reason.**
  Verified fresh from `agents/eng-manager/board/_index.md` (read this pass,
  not trusted from memory) that machine WIP is currently 5/1 — over the
  1-ticket cap corrected earlier today — and the board's own header names
  `ENG-014` explicitly among the tickets held at
  `designed`/`shaped`/`awaiting-scope` until that count clears. This differs
  from `ENG-022`'s own design-done pass, which chained immediately after
  design — but at that moment machine WIP was 6 against the *old* 12-ticket
  cap, genuinely not capped, so chaining could plausibly make progress.
  Right now it provably cannot: the next hop would re-verify the same 5/1
  cap and record the same hold, spending a full pass to reconfirm a fact
  already on the board. Per `eng_build_loop.md` step 9 ("Do NOT chain when
  the ticket is: ... held by a cap"), that is exactly the condition here.

  **Dead-end sweep (scoped to this ticket only, per this event's own
  contract):** nothing else outstanding on `ENG-014` itself.

  **Observations filed** (`observations.md`): one — this is the second
  same-day design-done pass to fork on the machine-WIP-cap question
  (`ENG-022` chained, not yet capped at its moment; `ENG-014` here does not,
  now capped) — worth eng-manager's dispatch pass confirming `ready`-entry
  actually resumes once `ENG-007`/`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013`
  drain, rather than this ticket silently waiting past that point.

  `chained: none` — held by the machine WIP cap (5/1, over the 1-ticket
  limit; `_index.md` names `ENG-014` by name as parked at `designed` until
  it clears). Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-014`) and whole-board: see pass notes in
  `agents/eng-manager/board/_index.md`.
