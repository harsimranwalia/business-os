---
id: ENG-006
title: Introduce a unified cross-restaurant customer identity with phone/OTP auth and legacy-customer mapping
project: aiorders-api
type: feature
size: L
severity: P3
priority:
state: verified
owner: product-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-08-27
updated: 2026-08-28
branch: loyalty-system
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-006-unified-customer-identity.md
  design: agents/architect/designs/ENG-006-unified-customer-identity.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-006.md
  test_plan: agents/qa/test-plans/ENG-006.md
  security_review: agents/security/reviews/ENG-006.md
  release: agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/2
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-27-i-want-to-be-able-to-give-the-customers-points-for-online-or.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver via the
control center, received 2026-08-27T20:19:21Z — preserved here per
`skills/request-readback/SKILL.md` step 1, never edited:

> I want to be able to give the customers points for online ordering and dine
> in they do at a restaurant and the points would be restaurant specific only
> but all of them would have the same naming in the frontend. For now we are
> just going to build the backend to support this.
>
> Add a new table that saves points per customer per restaurant, api to add
> points, redeem points. Save redemption history, spent history for dine-in
> that led to points. We also need a way to manage how much %age points to be
> give by each restaurant and separate for online ordering and dine in
> configs. We are also introducing the concept of a foodswipe customer who
> will be identified by a unique phone number and they will be authenticated
> through an sms otp and session would be maintained. Currently each
> restaurant has its own customer even though its the same physical human
> being which will now be identified in the system as a xxx customer (do no
> use the name xxx anywhere in db and code thats more for branding). We can
> map the new foodswipe customer to the legacy restaurant customer but for
> loyalty it will be one user but collecting and redeeming points for
> multiple restaurants and see all of them on one ui. and one qr code of the
> user would be scanned by all restaurants to add and redeem points. Define
> the feature and we may have to split this into multiple tickets that can be
> delivered individually one after another instead of full feature being just
> one bug ticket. Also create this int a separate branch of loyalty-system and
> backend and supabase migrations go in aiorders-api. Frontend stories/tasks
> can be written but they will be done later on in a separate discussion. as
> the frontend goes in multiple repos restaurant-marketplace for the
> customer, restaurant-portal for the restaurant and admin-hub for our
> internal use

## Readback

See `agents/product-manager/specs/ENG-006-unified-customer-identity.md` →
Readback — the full two-reading comparison and the proposed five-ticket
feature shape live there rather than duplicated here.

## Problem

Every restaurant on AIOrders holds its own separate customer record for the
same diner, so nothing recognizes one physical person across restaurants —
there's no way to run a reward program broader than a single restaurant, and
dine-in spend is entirely outside the system today. This ticket is the
identity foundation the approver's full loyalty request depends on; it is one
slice of a five-ticket sequence, not the whole feature.

## Outcome

A diner can verify a phone number once via SMS OTP and be recognized as the
same identity at every AIOrders restaurant, with a maintained session; their
existing per-restaurant order history and legacy customer records are
preserved and linked to that identity rather than replaced. No points, config,
redemption, or QR surface exists yet — those are later tickets in the
sequence.

## Notes

**Sized `L`, not `XL`, because the ticket is deliberately scoped to one
slice.** The full request (identity + ledger + config + redemption + QR +
admin surfaces, backend across a new auth model and a new data model) is
unambiguously `XL` as one ticket — `config/definition-of-done.md`'s size table
is explicit that an `XL` "must be split before it leaves intake" and is never
itself a ticket. This ticket is the first of five proposed slices; see the
PRD's "Feature shape and sequencing" for the other four, none of which have
ticket IDs yet — they get allocated as each is actually started, not
speculatively now, so an unapproved shape doesn't manufacture four tickets'
worth of board presence before the approver has seen it.

**`severity: P3` is a statement about urgency, not importance.** Nothing here
is broken — this is opportunity work, not incident response — so by
`definition-of-done.md`'s own rubric (severity measures how bad a *problem*
is) P3 is the honest bucket even though the initiative itself is substantial.
If this should jump the queue ahead of other work, that's exactly what
`priority` is for, and it's the approver's field to set, not this pass's.

**Branch deviates from the standard one-ticket-one-branch convention, by
explicit instruction.** `engineering-standards.md` names `{type}/{ENG-NNN}-{slug}`
per ticket as the default. The approver asked for all tickets in this
sequence to share one branch, `loyalty-system`, in `aiorders-api` — so
whoever picks this ticket up at `building` should branch `loyalty-system`
directly rather than cutting `feat/ENG-006-...`, and every later ticket in
this sequence branches from and merges back into that same branch, not from
`main`. `branch:` in this ticket's frontmatter is left empty per the
template's own lifecycle (set by the engineer at `building`) but will be
`loyalty-system` when it is.

**Migrations:** Supabase migrations for this and every ticket in the sequence
belong in `aiorders-api`, per the approver's explicit instruction — matches
`ADR-003`'s existing rule that `aiorders-api` is authoritative for migrations,
so no deviation needed there.

**Possible one-way door.** A new customer-facing auth/identity model is the
kind of decision the architect may need to escalate at G2 once designed — not
predicted further here; the PRD's Risks section flags it for that step.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-27` `intake → shaped → awaiting-scope` (product-manager,
  `intake` event pass — the approver's request, shaped as far as it goes per
  the event's own contract: shape the new request and carry it as far as it
  goes, don't sweep the whole board). Mode check clean (business-os `.env` →
  `MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
  through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  whole-board (ticket didn't exist yet to scope to): exit 0, clean.

  **Confirmed this request was this event's to act on, not `watch`'s.** An
  earlier `intake`-vs-`watch` race the same day
  (`agents/eng-manager/observations.md`, 2026-08-27) already reasoned through
  this exact file: it arrived `via: control-center` with a correctly-typed
  `intake` event already queued for it, so the `watch` pass that found it
  first correctly left it untouched rather than shaping it under the wrong
  contract. This pass is that queued `intake` event.

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's independent reading plus a blind architect reading, both as
  separate opus subagents (per the skill's own model direction), each given
  only the raw request verbatim and `knowledge/business-profile.md` — neither
  saw the other's reading, and the architect saw no PM interpretation.
  **Compared and found no material divergence** — both converged on the core
  shape (platform-level phone identity, additive legacy-customer mapping,
  restaurant-scoped balances under one shared display name, manual dine-in
  entry with no POS integration assumed, restaurant-scoped QR authorization,
  and a near-identical proposed ticket sequence). Differences were additive
  detail from different lenses (the architect's ledger/RLS/race-safety
  texture; this PM's read on the cross-restaurant-identity-vs-"own your
  customer" positioning tension) rather than disagreement about scope or what
  the request is for — per the skill's own classification table, that's
  "fine, proceed," not a fork to ask about. No question was put to the
  approver as a result; every load-bearing gap either reading flagged alone
  (chiefly: what a point is worth on redemption) was resolved by proposing a
  requirement rather than guessing a number or spending this ticket's one
  allowed clarifying question on it. Full comparison and both readings'
  content are summarized in the PRD's Readback section.

  **Sized `L`, scoped to the identity/auth/mapping slice only** — the full
  request is `XL` and cannot be one ticket per `definition-of-done.md`'s size
  table. PRD written:
  `agents/product-manager/specs/ENG-006-unified-customer-identity.md`,
  including the full proposed five-ticket feature shape (this PM's job per
  the approver's own "define the feature" ask), acceptance criteria for this
  slice only, and non-goals naming every later slice explicitly so scope
  doesn't creep into this ticket by default.

  **G1 required — `size: L` always requires it**, no judgement call needed
  (unlike `ENG-005`'s deliberate override at a smaller size). Checked caps
  fresh before raising: `wip.approver_limit` (2) at 0, `wip.approval_cap` (3)
  at 0/3 — both fully free, `ENG-005` (the only other in-flight ticket) holds
  neither. Wrote `inbox/2026-08-27-eng006-g1-scope.md`
  (`agent: product-manager`, `gate: scope`, `project: aiorders-api`,
  recommendation to build this slice now and treat the four follow-on slices
  as proposed shape open to correction), readback first per the skill's own
  ordering. Ran `departments/engineering/lib/eng-notify.sh raise
  inbox/2026-08-27-eng006-g1-scope.md` (exit 0; `traces/eng-notify-2026-08-27.log`
  logged `sent: active`, not `sent: raise` — the same `MODE`-collision bug
  every gate raised on this instance has hit; eighth corroborating
  occurrence, not a new finding, still the open `proposals.md` row from
  2026-08-25); stamped `notified: 2026-08-27T13:47:31` in the gate item's own
  frontmatter. PRD `status: draft → awaiting-scope`.

  **State:** `intake → shaped → awaiting-scope`, all in this pass — nothing
  here needed a second pass to reach the gate. `owner` moves
  `product-manager → approver` per `definition-of-done.md`'s state table.
  **Consequence:** approver-facing WIP 0 → 1 (cap 2, room for one more);
  approval cap 0/3 → 1/3. `machine_wip` (`ready`..`ready-to-ship`) unaffected
  — this ticket doesn't enter that range. **1 transition-worthy stop** (one
  gate reached); did not proceed further, since `awaiting-scope` is a human
  stop by design.

  **Dead-end sweep (scoped to this event):** this ticket's log ends in a
  valid, accounted-for state with a chain record below. `ENG-005` untouched —
  out of scope for an `intake` event naming this ticket; it already carries
  its own valid `chained: ENG-005` from the immediately preceding `decision`
  pass.

  **Notify sweep:** this pass's own gate item was raised and stamped above.
  Nothing to nudge (brand new). Approval cap 1/3, not full — no stall.

  `chained: none` — sitting at `awaiting-scope`, owned by the approver; the
  chaining guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
  whole-board: both exit 0, clean.

- `2026-08-28` `awaiting-scope → designed → awaiting-decision` (this pass,
  `decision` event, context `inbox/2026-08-27-eng006-g1-scope.md`). Mode
  check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.

  **Found in a partially-processed state, not a clean unanswered gate.** An
  earlier `watch` pass the same day (08:35–08:44) had already read the
  approver's hand-edited G1 answer and started acting on it — it edited this
  ticket's own PRD (`status: draft → designed`, filled in the `## Decision`
  section with a full two-instruction reading) — then hit the account's
  monthly spend limit mid-sequence and died. Its automatic retry then failed
  on a network error (`ENOTFOUND`) and the event was dropped after two
  attempts per `lib/eng-trigger.sh`'s own bounded-retry design
  (`inbox/2026-08-28-eng-events-dropped.md`, 10:42:17 entry — its
  `ticket: unknown` is this ticket; not edited, since that file is an
  automated append-only log, but the gap is closed by this ticket's own log
  and the observation below). This `decision` pass reached the item through
  a manual re-fire of `eng-trigger.sh decision` (confirmed via `ps` — the
  process chain holding `traces/.loop.lock` traces back to a manual
  `eng-trigger.sh decision 2026-08-27-eng006-g1-scope.md` invocation, not a
  scheduled fire), not the race pattern `observations.md` already documents
  repeatedly (two queued events both finding nothing left to do) — this was
  the opposite: real, undone work behind a claim that it was already done.
  **Verified rather than trusted:** the PRD's Decision section claimed
  `agents/product-manager/specs/loyalty-program-frontend-understanding.md`
  was "Done" — it did not exist (`ls` confirmed empty). Wrote it for real
  rather than leaving the false claim standing.

  **Design work done fresh against the live repo**, not inferred from the
  PRD alone (this ticket is `L`, flagged with a possible one-way door — the
  PRD's own bar for "actually investigate the schema" before deciding).
  `~/Documents/projects/_eng/aiorders-api` has **no schema in version
  control at all** (no migrations dir, no types file) — read the edge
  functions that query `customers` instead
  (`crm/customers.ts`, `crm/utils.ts`, `website-submissions/customer-signup.ts`)
  to confirm its real columns and matching behavior. Found and corrected one
  PRD assumption in the process: "restaurant means one location, not a
  multi-location brand" is not what the live schema says — `customers` is
  already scoped by `restaurant_id` **or** `brand_id`, and `proxy-login`
  confirms a real `brands`/`brand_managers` structure exists above
  individual restaurants. This design's legacy-link table carries both
  columns rather than assuming restaurant-only scoping. Also checked
  `outgoing-communications/services/sms.ts` (SMS is currently mocked behind
  a `SMS_PROVIDER` switch with Twilio/MessageBird/Vonage all stubbed
  `// TODO`) and `proxy-login/index.ts` (existing precedent for a
  hand-rolled Supabase-compatible JWT, used here as a reason to *prefer*
  Supabase's native phone/OTP auth instead, not to copy the pattern — native
  auth means no custom OTP storage, hashing, expiry, or JWT signing for this
  ticket to get wrong). Full design:
  `agents/architect/designs/ENG-006-unified-customer-identity.md` — two new
  tables (`platform_customers`, `platform_customer_legacy_links`), both
  purely additive, `customers` untouched.

  **One-way door: escalated, not decided.** The PRD flagged this twice for
  the architect to evaluate at G2 rather than settle quietly. Reasoned
  through it in full in the design doc's own One-way-doors section: the
  *schema* is reversible (both new tables are additive and droppable without
  touching `customers`), but *adoption* isn't — once real diners have
  verified a phone and linked history across restaurants, unwinding is a
  user-facing regression, not a clean migration. Given the repeated explicit
  flag, the stakes (the department's largest new subsystem so far), and no
  G2 precedent yet on this board to lean on, chose to put the actual
  question to the approver rather than decide it unilaterally. Raised
  `inbox/2026-08-28-eng006-g2-oneway-door.md` (`agent: eng-manager`, `gate:
  one-way-door`, per `schedules/eng_build_loop.md`'s own convention that
  G2/G3 are raised in the EM's name). Deliberately did **not** re-ask the
  PRD's separate "marketplace owns the identity" positioning tension — that
  was already logged at G1 as "on the record, not a fork to ask about," and
  reopening it here would contradict that already-passed classification.
  Ran `lib/eng-notify.sh raise inbox/2026-08-28-eng006-g2-oneway-door.md`
  (exit 0); stamped `notified: 2026-08-28T20:04:15` by hand (the
  already-open `MODE`-collision proposal, `proposals.md` 2026-08-25 row,
  means the script's own logged status label isn't trustworthy — not a new
  finding).

  **Both of the approver's G1 riders acted on for real:** (1) wrote
  `agents/product-manager/specs/loyalty-program-frontend-understanding.md`
  — knowledge capture only, drawn from the PRD's existing readback and
  feature-shape sections, explicitly not scoped, sized, or scheduled. (2)
  carried the resolved SMS-vendor-cost note into the design's Risks, with
  the honest caveat added that delivery still isn't wired to any real
  vendor in code regardless of the commercial deal being settled — worth
  keeping distinct from the marketing-SMS module's own separate mock.

  **2 transitions this pass** (`awaiting-scope → designed → awaiting-decision`),
  under the cap of 4. `machine_wip` unaffected (neither state is in the
  counted `ready..ready-to-ship` range). Approver-facing WIP and approval
  cap both net unchanged at 1/2 and 1/3 — G1 closed, G2 opened, same ticket.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for state with a chain record below.

  **Notify sweep:** this pass's own gate item raised and stamped above.
  Nothing to nudge (brand new). Approval cap 1/3, not full — no stall.

  **Observation filed** (`agents/eng-manager/observations.md`): a pass
  crashing mid-edit-sequence can leave on-disk artifacts partially updated
  and self-contradictory (here, a PRD claiming finished work that hadn't
  happened) — distinct from the already-documented duplicate-event race,
  and worth a name of its own since this is the first occurrence caught.

  `chained: none — awaiting-decision (G2), waiting on the approver.` Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
  whole-board: both exit 0, clean.

- `2026-08-28` `awaiting-decision → ready` (this pass, `scheduled` event,
  context `launchd`). Narrow scope per the event contract for a `scheduled`
  fire (safety-net, sweep the whole board). Mode check clean (business-os
  `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

  **Found this ticket's G2 already answered** while sweeping `inbox/` for
  gate returns — exactly the class of thing a scheduled sweep exists to
  catch, since neither `watch` (not wired on this instance per
  `schedules/eng_build_loop.md`'s own note) nor a reply through the tracked
  notify channel (this approver answers by hand-editing the gate file
  directly, every time so far — `decision-journal.md`) had a live path to
  fire on this answer before this pass found it. `traces/.pending` held `1
  watch launchd` then `1 decision 2026-08-28-eng006-g2-oneway-door.md` at the
  time of reading — this pass reached the file first; the two queued behind
  it will find it already in `_handled/` and no-op, which is the
  already-documented duplicate-event race (`observations.md`, ten-plus prior
  occurrences), not a new failure, so not re-logged as its own row.

  **The answer:** `decision: approved`, `decided:
  2026-08-28T20:09:06.151165+00:00`, a full paragraph in the approver's own
  words rather than a bare approval — read in full on
  `inbox/_handled/2026-08-28-eng006-g2-oneway-door.md`. Its core claim
  (reversibility rests on the legacy per-restaurant flow and the new platform
  identity continuing to run side by side, not on the schema alone) restates,
  rather than changes, the design's own One-way-doors reasoning — both the
  "legacy `customers` untouched" and "unified order view is later-ticket
  scope" points it makes are already true of
  `agents/architect/designs/ENG-006-unified-customer-identity.md` and the
  PRD's Outcome/Non-goals. Treated as a full approval of the recommendation
  to proceed, not a partial answer needing a follow-up question — unlike
  `ENG-005`'s two-part G1, every part of this gate's actual question
  (adoption-reversibility) came back addressed. Processed footer appended to
  the gate item; moved to `inbox/_handled/`. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **`ready` per `config/definition-of-done.md`'s ticket-states table ("work
  broken down, sequenced, assigned; WIP slot available"), not `building`** —
  entering `building` is new implementation work and this event's dispatch
  step stops before it by design, leaving it for a fresh chained session.
  The breakdown itself is already on record rather than invented here: the
  design's own Components table sequences cleanly as (1) the additive
  migration for `platform_customers` + `platform_customer_legacy_links` with
  their RLS policies, (2) the new `platform-customer-auth` edge function, (3)
  Supabase Auth phone-provider + SMS vendor configuration, (4) the stricter
  phone validator ahead of the OTP call (AC7) — all four assigned `backend`
  (one, Auth settings, jointly with `devops`) in that table already. No
  further split needed at this size (`L`, within
  `definition-of-done.md`'s size table; only `XL` forces a split, and this
  ticket is already the one bounded slice of the five-ticket sequence the PRD
  proposed). Per the ticket's own Notes, `branch:` stays empty here and
  becomes `loyalty-system` when the next session actually reaches `building`.

  **Caps checked fresh before advancing:** `wip.machine_limit` (6, counts
  `ready`..`ready-to-ship`) was 0/6, → 1/6. `wip.approver_limit` (2) was 1/2
  (this ticket's own G2), → 0/2 — this ticket no longer runs through the
  approver. `awaiting_approver_cap` (3) was 1/3 (same G2), → 0/3. No cap
  was at or near its limit either before or after.

  **1 transition this pass** (`awaiting-decision → ready`), well under the
  cap of 4 — the next state needs new implementation work, so this pass
  stops here by design rather than spending more of the budget.

  **Dead-end sweep (whole-board, per the `scheduled` event contract):**
  `ENG-001` through `ENG-005` are all terminal (`verified` ×4, `dropped` ×1)
  with valid closing log lines — nothing to resume. `ENG-006` (this ticket)
  now ends in a valid, accounted-for state with the chain record below.
  `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
  `inbox/requests/` all swept fresh and empty (bar `.gitkeep`/already-`_handled/`
  entries). `inbox/2026-08-28-eng-events-dropped.md` (an incident notice, not
  a ticket) has no `decision:` yet and is not P0 — left waiting on the
  approver per the constitution's "do not surface anything that isn't a P0";
  it was already notified once at creation (`drop_notice`'s own
  once-per-day-when-fresh rule in `lib/eng-trigger.sh`), so no re-notify due.

  **Notify sweep:** no new gate item raised this pass (this pass closed one,
  raised none). Nothing older than 24h with no `nudged:` and no `decision:`
  — the only other inbox item is today's incident notice, not yet a day old.
  Approval cap 0/3, not full — no stall.

  **Observations/exceptions:** none filed — the duplicate-event race behind
  this pass is corroborating, not new (see above), and everything else swept
  clean.

  `chained: ENG-006` — `ready` is an eng-manager-owned state, not the
  approver, not blocked, not terminal; fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-006`) and whole-board: both exit 0, clean.

- `2026-08-28` `ready → building → in-review → in-security → ready-to-ship`
  (backend, then principal-engineer + qa combined, then security, then
  devops — `continue ENG-006` event pass, attempt 2/2 after a timeout).
  Narrow scope per the event contract (resume this ticket from its current
  state; no board-wide sweep). Mode check clean (business-os `.env` →
  `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped and whole-board: both exit 0, clean.

  **Recovered an unrecorded build, same shape as ENG-002 and ENG-005's own
  precedent for this exact failure mode.** `traces/eng-loop-2026-08-28.log`:
  the first dispatch of `continue ENG-006` today timed out at 14:04:25 after
  1800s mid-verification and was killed; `lib/eng-trigger.sh` re-queued it as
  attempt 2/2 (not consumed); the queue drained that retry at 14:21:32 and
  launched this session. `traces/.hops-2026-08-28-ENG-006` reads `2`,
  confirming this is the second dispatch today. Ruled out a live concurrent
  session before trusting any of it: the lock at `traces/.loop.lock` (pid
  50311, the trigger/wrapper process) and the running `claude` process (pid
  50904, `ps aux`) both trace to this exact invocation — the launched
  command's own argument text is this pass's own prompt, word for word — and
  `traces/.pass-out.50311` is this session's own narration being mirrored to
  disk in real time (confirmed live: it changed on disk mid-read, showing
  lines this session had just written), not a second session's output.

  The dead attempt had, before its timeout, already: created and checked out
  branch `loyalty-system` in the `_eng/aiorders-api` worktree; written the
  migration (`supabase/migrations/20260828120000_platform_customer_identity.sql`)
  and verified it for real against a throwaway Postgres container (documented
  in full, with concrete pass/fail results per check, in
  `agents/database/migrations/ENG-006-unified-customer-identity.md` —
  **this doc was read and found genuinely complete this time**, unlike the
  false "Done" claim this same ticket's G2 pass caught on 2026-08-28 earlier
  today); written the `platform-customer-auth` edge function (4 source
  files), found and fixed a real bug during its own build (a too-lenient
  regex silently stripping non-digit characters instead of rejecting them,
  letting `"+1647abc7545"` collapse into a different valid-looking number);
  refactored `index.ts` into a thin entrypoint plus a testable `handler.ts`
  (mirroring this repo's own `crm/index.ts` + `crm/customers.ts` split) to
  close the gap named by automatic-failure #10 (auth path changed, no
  failure-case test); and written 3 test files. All of it sat uncommitted —
  the timeout hit mid-way through re-verifying tests/typecheck/lint after
  that refactor, per `traces/.pass-out.50311`'s own narration.

  **Independently re-verified rather than trusted, this pass, before
  committing anything.** Deno isn't installed on this host (`which deno`:
  not found; no `~/.deno`, no version manager) — the dead attempt must have
  used Docker, so this pass did the same:
  `docker run --rm -v $(pwd)/supabase/functions/platform-customer-auth:/app
  -w /app denoland/deno:latest sh -c "deno test --allow-env && deno check
  *.ts && deno lint"`. Result: **27 passed, 0 failed** (5 handler + 9 linking
  + 13 validation), `deno check` clean on all 4 source files, `deno lint`
  clean on all 7. Read all 4 source files and the migration SQL directly
  rather than trusting the migration doc's or the dead session's own
  narration; ran the automatic-failure scan fresh (0/10 — detailed in the
  code-review receipt below). Did **not** re-run the Postgres verification —
  it predates and is untouched by the later handler refactor, and is already
  documented with concrete, checkable results rather than a bare claim.

  **`building` exit condition met.** Staged and committed
  (`c3ab50c`, "Add unified cross-restaurant customer identity (ENG-006)",
  commit message checked against this repo's own convention — imperative
  subject, why-focused body, `Co-Authored-By` footer — against its 4 most
  recent commits before writing it) and pushed:
  `origin/loyalty-system`. `supabase/functions/README.md`'s catalog entry
  for the new function was already updated in the same commit, per this
  repo's own `CLAUDE.md` instruction. Per this instance's own precedent
  (`ENG-005`), `building`'s documented exit condition is read in practice as
  "branch pushed, self-tested" — the PR itself, and its body, are devops's
  distinct work at the merge-request step, not written as a separate draft
  here.

  **`in-review` (combined review + quality hop).** Acted as
  principal-engineer: automatic-failure scan clean (0/10 —
  `agents/principal-engineer/reviews/ENG-006.md`), design conformance
  checked line-by-line against
  `agents/architect/designs/ENG-006-unified-customer-identity.md` (tables,
  RLS policy set, the `verify` interface, linking semantics, the validator's
  own rationale) — no divergence found. Two non-blocking gaps named rather
  than hidden: no automated test reaches past the first `createClient()`
  call (a repo-wide limitation — zero precedent anywhere in this repo's 46
  functions for mocking a Supabase client, not a shortcut unique to this
  ticket) and one unbounded-but-low-cardinality query against `customers`.
  Verdict **pass**, `links.review` set. Acted as qa: wrote
  `agents/qa/test-plans/ENG-006.md`, mapping all 7 PRD acceptance criteria.
  AC3/4/7 fully covered by unit tests plus code/migration-doc verification.
  **AC1/2/5/6 are only partially verifiable** — each depends on Supabase's
  phone-auth provider and an SMS vendor being configured, and neither is
  done yet, so this ticket's own OTP-issuance/session behavior cannot be
  exercised end to end by any test this pass could write. Not a new
  finding — already on record in the design doc's Risks and restated here
  so the quality gate's record doesn't imply a stronger claim than the code
  supports. Verdict **pass** on the code as written, `links.test_plan` set.
  Per `skills/code-review-gate/SKILL.md` step 9, both clearing together
  advances straight to `in-security` — no separate `in-qa` sit-state, same
  as `ENG-005`.

  **`in-security`.** Threat-modelled the new endpoint: every write and read
  in the diff is keyed to the caller's own `auth.uid()`, both in application
  code and independently at the RLS layer (belt-and-suspenders); no
  caller-suppliable id, restaurant, or phone parameter exists to act on
  anyone else's data. Traced all 7 negative/degraded-auth branches in
  `handler.ts` directly — every one fails closed with a generic message and
  a server-side log carrying `userId`, no internal detail leaked. OWASP
  walk: A01 and A04 reviewed as real content (access control confirmed;
  the two known design-level risks — phone-number recycling and unwired
  consent capture — confirmed **deliberately** unaddressed by this diff,
  matching the architect's own explicit scoping in the design's Risks
  section rather than a gap this review discovered), rest `n/a` with
  reasons or reviewed clean. No secrets. PII handling assessed: consent
  for the new cross-restaurant correlation isn't captured yet
  (`consent_recorded_at` exists, unpopulated by this diff) — named, not
  hidden, and explicitly the approver's/counsel's call per the design, not
  this gate's. SOC 2 trail complete. Verdict **pass** —
  `agents/security/reviews/ENG-006.md`, `links.security_review` set.

  **`ready-to-ship`.** Acted as devops. Migration gate already cleared —
  `agents/database/migrations/ENG-006-unified-customer-identity.md`'s own
  verdict (`pass`: additive, rollback tested for real against a throwaway
  Postgres container, indexes present, no backfill needed). Release plan:
  additive migration plus one new edge function with **no live caller
  anywhere** (frontend work is an explicit PRD non-goal, deferred to a
  later, unscheduled ticket) — merging and deploying this has zero
  behavioral effect on production until something calls it. Rollback:
  migration rollback already tested; the edge function itself is new,
  stateless, and trivially reversible by not deploying/redeploying it.
  Observability: every failure branch logs server-side with `userId` and
  error context (confirmed in the security review), visible through
  Supabase's own function logs — the same mechanism every other function in
  this repo already relies on, no new gap. Cost: **$0/month delta** — same
  Supabase project, two new empty tables, no new service; the SMS vendor's
  real recurring cost is pre-approved by the approver (G1 note, carried in
  the design's Risks) and is not triggered by this diff alone, since no SMS
  sends occur until the phone provider is separately configured. Confirmed
  `aiorders-api` has no `.github/workflows/` — no CI/CD auto-deploy exists,
  same shape as every other registered project, so a human merge is the
  full extent of this department's autonomy here regardless of timing.
  Release window checked for completeness though not acted on this pass:
  Friday 2026-08-28, 14:33 PDT (before the 15:00 cutoff), `MODE=active`, no
  `ENG_RELEASE_FREEZE` found — to be re-checked fresh by whichever session
  actually opens the PR, since that's a later hop.

  **Three items carried forward, stated once and plainly rather than
  re-derived by the next reader:** (1) Supabase phone-auth provider + SMS
  vendor configuration is still open — this ticket's entire attack surface
  and its OTP-dependent acceptance criteria are unreachable until it's
  done; (2) consent capture for the new cross-restaurant correlation isn't
  wired (`consent_recorded_at` unpopulated) — the approver's/counsel's call
  per the design, not built here; (3) the phone-recycling mitigation the
  design proposed is deliberately not implemented — a build-time
  refinement per the architect, not a requirement of this ticket. None of
  these block this verdict; all three are pre-existing, already-named
  design-level decisions this pass confirmed the code matches rather than
  gaps discovered here.

  **4 transitions this pass** (`ready→building`, `building→in-review`,
  `in-review→in-security`, `in-security→ready-to-ship`), at the cap of 4 —
  same count and same stopping point as `ENG-005`'s precedent for a full
  end-to-end `continue` session. Opening the PR and moving to `blocked`
  (`blocked_on: approver`) is real, distinct devops work for the next hop,
  deliberately not started here. `machine_wip` (`ready`..`ready-to-ship`)
  unaffected — same ticket, still inside the counted range, net 1/6.
  Approver-facing WIP and approval cap both unaffected — no gate raised
  this pass.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in
  a valid, accounted-for state with the chain record below.

  **Notify sweep:** no new gate item raised this pass — the merge request
  (the next hop's PR-open) is what will actually need the approver.
  Nothing to nudge. Approval cap unaffected, not full — no stall.

  **Observations/exceptions:** none filed. The recovered-unrecorded-build
  shape is corroborating (`ENG-002`, `ENG-005` precedent), not new.

  `chained: ENG-006` — `ready-to-ship` is a devops-owned state, not the
  approver, not blocked, not terminal; fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-006`) and whole-board: both exit 0, clean.

- `2026-08-28` `ready-to-ship → blocked` (devops — `continue ENG-006` event
  pass, context `ENG-006`, the dedicated session the preceding pass chained
  specifically to open the L1 PR). Narrow scope per the event contract
  (resume this ticket from its current state; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance `config/config.yaml`
  → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.

  **Release window re-checked fresh, as the preceding pass explicitly asked
  the next session to do** rather than trusting its own earlier
  informational read: `date` → Friday 2026-08-28, 14:40 PDT, before the
  15:00 cutoff; business-os `.env` → `MODE=active`, no `ENG_RELEASE_FREEZE`
  set; instance `config/config.yaml` carries no `release_freeze` override.
  Inside the window — proceeded.

  **Checked for an already-opened PR before creating one**, same discipline
  `ENG-005` applied at this identical boundary: `gh pr list --repo
  harsimranwalia/aiorders-api --head loyalty-system --state all` returned
  empty. None existed. Confirmed the worktree state first too —
  `~/Documents/projects/_eng/aiorders-api` clean, `loyalty-system` up to
  date with `origin/loyalty-system` at `c3ab50c`, `git merge-base
  --is-ancestor origin/loyalty-system origin/main` → not merged.

  **Opened the real PR** (`gh pr create`, title "Add unified cross-restaurant
  customer identity (ENG-006)"):
  https://github.com/harsimranwalia/aiorders-api/pull/2. Body states what
  changed, why, the four gate verdicts (code review, quality, security,
  migration) by file reference, and the three carried-forward items
  (SMS/phone-provider configuration, consent capture, phone-recycling
  mitigation) so the approver sees them at the point of the actual merge
  decision, not just buried in a design doc. Wrote the L1 merge-request item
  (`inbox/2026-08-28-eng006-merge-request.md`, `gate: merge`, `agent:
  eng-manager`) carrying the PR link and the same four gate verdicts by file
  reference. Ran `departments/engineering/lib/eng-notify.sh raise` —
  reproduced the already-filed `MODE`-collision bug
  (`traces/eng-notify-2026-08-28.log`, 14:42:22: `sent: active`, not `sent:
  raise`) — corroborating the open 2026-08-25 `proposals.md` row, not a new
  finding. Stamped `notified: 2026-08-28T21:42:08` by hand, since the script
  never reliably writes back to the item either way. State → `blocked`,
  `blocked_on: approver`, `blocked_from: ready-to-ship`, owner `devops →
  approver`, `links.pr` set — the same design `config.yaml`'s
  `gates.merge_request` describes, and the one `ENG-002`/`ENG-005` both used
  at this identical boundary.

  **Cap check before this transition, read fresh rather than trusted from
  the board header.** `wip.approver_limit` (2) was at 0/2; `awaiting_approver_cap`
  (3) was at 0/3 — `ENG-006` is the only in-flight ticket and nothing else
  is open. Advancing brings `approver_limit` to 1/2 and `awaiting_approver_cap`
  to 1/3 — neither at or over its limit.

  **1 transition this pass** (`ready-to-ship → blocked`), well under the cap
  of 4 — opening the PR and writing the gate item is itself the real work of
  this hop, same as `ENG-002`/`ENG-005`'s precedent. `machine_wip` 1/6 → 0/6
  (`blocked` sits outside the `ready`..`ready-to-ship` range). Approver-facing
  WIP 0 → 1; approval cap 0/3 → 1/3.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for state with the chain record below. No other ticket is
  in flight to check.

  **Notify sweep:** this pass's own gate item raised and stamped above.
  Nothing to nudge (brand new). Approval cap 1/3, not full — no stall.

  **Observations/exceptions:** none filed — the `MODE`-collision reproduction
  is corroborating, not new.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
  the whole hop was driving toward; firing `continue ENG-006` again would
  just re-queue against a ticket with nothing left for a machine to do until
  the approver merges the PR or replies to the gate item. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
  whole-board: both exit 0, clean.

- `2026-08-28` `blocked → shipped` (control center, merge detected) — `loyalty-system` is an ancestor of `origin/main`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree. The release record and `verified` still belong to a pass — this marks the merge, not the verification.

- `2026-08-28` `shipped → verified` (devops, then product-manager —
  `decision` event pass, context `inbox/2026-08-28-eng006-merge-request.md`).
  Narrow scope per the event contract (act on the answered gate item, advance
  only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean.

  **Found the ticket already past this gate item, not sitting cleanly behind
  it.** The gate item carried `decision: approved`,
  `decided: 2026-08-29T02:59:33.281266+00:00`, text "approved" — the tracked
  channel. But the ticket's own `state:` was already `shipped`, set by the
  same "control center" dashboard action documented in the row immediately
  above this one, ahead of any build-loop pass. This is the second time that
  mechanism has preempted a pass (`ENG-002` first, `proposals.md` 2026-08-26
  row) — this time with a hybrid shape: unlike `ENG-002` (gate item left open
  indefinitely, no reply at all), the tracked item *did* get answered, just
  minutes after the merge rather than in place of it. Addendum filed in
  `observations.md` rather than a new proposal row.

  **Neither signal taken on its own text.** Re-ran the loop's own
  merge-detection check (`schedules/eng_build_loop.md` step 5) from scratch
  in the department's own worktree (`~/Documents/projects/_eng/aiorders-api`,
  never the human's checkout): `git fetch origin`; `git merge-base
  --is-ancestor origin/loyalty-system origin/main` → MERGED; `git log
  origin/main --oneline -3` showed `40d7c36` (PR #2's own merge commit)
  directly on top of `c3ab50c` (this ticket's commit) on top of `5b3bac2` —
  no intervening commits, `git diff origin/loyalty-system origin/main` empty.
  Cross-checked independently via `gh pr view 2 --json state,mergedAt`:
  `MERGED`, `2026-08-29T02:57:05Z`. The merge commit's own timestamp lands
  ~2m28s before the gate item's `decided:` stamp — same "merge, then record
  the decision in the same sitting" shape `ENG-005` showed, a slightly wider
  gap. Both routes agree with the control center's claim: genuinely merged.
  The `blocked → shipped` transition above is confirmed correct; not redone.

  **Acted as devops, closing out `shipped`'s exit condition**
  (`config/definition-of-done.md`: "Deployed, health checks green, release
  record written") **for what an L1 project with no CI/CD can actually
  attest to.** `.github/workflows/` absent from `origin/main` — no
  auto-deploy. `git ls-tree -r origin/main --name-only` confirms both the
  migration file and all 7 `platform-customer-auth` source/test files are
  present on `origin/main` under the paths already reviewed; since the
  branch-to-main diff is empty, the 27/27 Deno test result and clean
  `check`/`lint` already documented at `in-review` necessarily still hold —
  re-running an identical suite against provably identical source would add
  no new information, so it wasn't re-run. Checked whether this department
  could even confirm a live Supabase deploy: `supabase/config.toml` points
  at the registered project (`bmnmnejwdxbcqinqkwko`), but the worktree isn't
  linked and no `SUPABASE_ACCESS_TOKEN` is available — a read-only `supabase
  migration list --linked` returned "Cannot find project ref" rather than a
  status. Recorded `health_check: not checked` and `rollback_tested: true
  (drilled pre-merge against a throwaway Postgres container; not against the
  live project)` honestly rather than inferring a status unavailable to
  observe — same discipline `ENG-005` used for its own Cloudflare gap. Wrote
  the release record from what was actually found:
  `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`, `links.release`
  set.

  **Acted as product-manager, confirming acceptance criteria against the live
  (merged) tree** (`agents/product-manager/specs/ENG-006-unified-customer-identity.md`):
  AC3 (legacy-record linking), AC4 (cross-restaurant resolution to one
  platform customer), and AC7 (phone-normalization rejection) all confirmed
  directly — each is exercised by `linking.ts`/`validation.ts`'s unit tests,
  re-confirmed present and unchanged on `origin/main`, none needing a live
  OTP call to exercise. **AC1, AC2, AC5, AC6 remain not verified live** —
  each depends on Supabase's phone-auth provider and an SMS vendor being
  configured, neither of which is done; this is not a new gap, it's the same
  one QA named at `in-qa` and the same one the approver read and approved in
  the merge-request item's own text. Carried forward explicitly rather than
  silently claimed or allowed to block: applying the same "pass on the code
  as written, gap named and not hidden" standard used at every gate on this
  ticket so far, rather than a stricter one invented only at this last step.
  PRD `status: designed → verified`.

  **Gate item closed out.** `inbox/2026-08-28-eng006-merge-request.md` moved
  to `inbox/_handled/` with a processed footer. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **1 transition this pass** (`shipped → verified`; the `blocked → shipped`
  half was already on record from the control center), well under the cap of
  4. **Approval cap:** `ENG-006` no longer counts (was the only item on both
  approver-facing WIP and the approval cap, as `blocked_on: approver`) —
  `verified` is terminal and owes nothing to either cap. Approver-facing WIP
  1 → 0; approval cap 1/3 → 0/3. `machine_wip` unchanged at 0/6 — neither
  `shipped` nor `verified` sits inside the counted `ready`..`ready-to-ship`
  range.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for terminal state. No other ticket is in flight.

  **Notify sweep:** nothing to raise this pass (`verified` raises no gate
  item). Nothing to nudge — the merge-request item is now answered and
  closed, not sitting open. Approval cap now 0/3, not full — no stall.

  `chained: none` — `verified` is a terminal state. Nothing left for a
  machine or the approver to do on this ticket. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.

- `2026-08-28` (no-op) `continue ENG-006` event pass, context `ENG-006`. Mode
  check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.

  **Nothing to resume — `state: verified` since 20:12:38, independently
  reconfirmed** against this ticket's own frontmatter/log, the board index,
  and `decision-journal.md` (all three gates journaled). Mid-pass, commit
  `3c3dcd0` landed (Harsimran, 2026-08-28T21:09:07-07:00): the approver ran
  `supabase db push` / `supabase functions deploy` directly against
  production and updated the release record's frontmatter accordingly,
  outside this department's own L1 workflow — a concrete, plausible source
  for this event's own external fire, though not confirmed as the literal
  cause. Full reasoning, including why this fire doesn't match the
  instance's documented duplicate-queued-event race, is on
  `board/_index.md`'s dated entry for this pass rather than repeated here.
  Observations filed (`observations.md`): this fire's shape, and a
  frontmatter/body inconsistency that same commit left in the release
  record, found while checking it.

  **0 transitions.** No cap affected (machine WIP 0/6, approver WIP 0/2,
  approval cap 0/3 — unchanged).

  `chained: none` — `verified` is terminal; nothing for a machine to resume.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean.
