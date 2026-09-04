---
id: ENG-022
title: Fix broken restaurant-scoped access check on 5 brand-portal handlers — cross-tenant PII/write exposure
project: aiorders-api
type: security
size: M
time_estimate: half a day to a day
time_spent: build, code review, QA, security, and release-readiness (PR opened, merge request raised) complete this pass, not itemized against a pass-start clock (same pre-existing gap ENG-010's frontmatter named rather than backfilled with an invented figure)
time_remaining: nothing left for the department — waiting on the approver to merge the PR; already inside the original half-day-to-a-day band, not separately re-banded
severity: P0
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: product-manager
created: 2026-08-29
updated: 2026-09-03
branch: fix/ENG-022-brand-portal-tenant-isolation (aiorders-api@d5078c5)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-022-brand-portal-tenant-isolation-broken.md
  design: agents/architect/designs/ENG-022-brand-portal-tenant-isolation-broken.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-022.md
  test_plan: agents/qa/test-plans/ENG-022.md
  security_review: agents/security/reviews/ENG-022.md
  release: agents/devops/releases/2026-09-03-aiorders-api-ENG-022.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/9
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

- `2026-09-03` `designed → ready` (eng-manager, `scheduled` event pass,
  context `manual-drain`, whole-board dispatch step). Re-checked machine WIP
  fresh from frontmatter rather than the board header: `ENG-008`, `ENG-009`,
  `ENG-010`, `ENG-013` are all `blocked`/`blocked_on: approver` — none
  occupies the counted `ready`..`ready-to-ship` range. **0/1, free** — the
  first time since this ticket reached `designed` on 2026-08-29 (5 days
  ago, held the whole time by the machine WIP cap alone, per this ticket's
  own immediately-preceding log entry).

  **This ticket is the only fully gate-clear candidate on the board right
  now**, checked against every other `designed`/`shaped` ticket, not
  assumed: `ENG-014`/`ENG-017`/`ENG-023`/`ENG-025` are `type: feature`, full
  lane, still owe an unraised G2 (or G1); `ENG-015` (`type: security`, also
  G1-auto-skip, also decided-not-escalated at its own design gate per
  `ADR-006`) is gate-clear too but ranks below this ticket on severity (P1
  vs `P0`); `ENG-024` (`type: bug`, fast lane, G1 auto-skip) is also
  gate-clear but ranks below on severity (P1). Both noted in the board
  index as the next candidates once a slot frees again. Priority is unset
  on all of them (never inferred, per `eng_build_loop.md` step 6), so
  severity is the actual tie-break, and this ticket's `P0` — live,
  currently-reachable cross-tenant PII exposure plus unauthorized writes —
  outranks every other candidate outright.

  **File-level sequencing confirmed, not just assumed clean:** nothing else
  is currently `building` (machine WIP was 0/1 before this dispatch), so no
  active edit touches this design's file set
  (`supabase/functions/brand-portal/{feedback,offers,customers,hiring,
  website,utils}.ts`). `ENG-023` shares `feedback.ts` but is only
  `designed`, not building, and was already flagged (this ticket's own
  Notes, above) so its own future build models the fix rather than
  repeating the bug — no live conflict to resolve here.

  Work is already broken down and sequenced in
  `agents/architect/designs/ENG-022-brand-portal-tenant-isolation-broken.md`
  (two fix groups by existing error convention, the promoted
  `requireRestaurantAccess` helper, a colocated `Deno.test` per fixed file)
  and no G2 applies (no one-way door, logged above) — nothing further for
  this hop to produce beyond the state move itself.

  **1 transition** (`designed → ready`). **Consequence:** machine WIP
  `0/1 → 1/1`, the counted range now occupied by this ticket. Approver-facing
  WIP and approval cap both unaffected — no gate touched.

  **Dead-end sweep, notify sweep:** nothing else to resume or raise from
  this specific action; see this pass's own dated entry in
  `agents/eng-manager/board/_index.md` for the rest of the whole-board
  sweep.

  `chained: ENG-022` — `ready`, owned by `eng-manager`, an agent-owned state
  whose next hop (`ready → building`) is new implementation work and
  therefore belongs in its own dedicated session, not this sweep. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: see board index.

- `2026-09-03` `ready → building`: built per the design, single repo
  (`aiorders-api`) (backend, `continue` event pass, context `ENG-022` — this
  ticket's own turn at the front of the queue). Narrow scope per the event's
  own contract — this ticket only.

  **Worktree confirmed clean before branching.** `~/Documents/projects/_eng/aiorders-api`
  was sitting on `ENG-008`'s own branch (`feat/ENG-008-influencer-admin-management`,
  no uncommitted changes — that ticket's own build long finished, now
  `blocked`/`blocked_on: approver`). `git fetch origin` confirmed no drift
  against `origin/main` (`93617c6`). Branched
  `fix/ENG-022-brand-portal-tenant-isolation` off `origin/main` directly —
  this ticket has no dependency on any other in-flight ticket's branch.

  **Live code re-read before editing, not trusted from the design's summary.**
  All 5 broken files (`feedback.ts`, `offers.ts`, `customers.ts`, `hiring.ts`,
  `website.ts`) and `utils.ts` matched the design's own table exactly — same
  line numbers, same two bug shapes, `verifyRestaurantAccessLegacy` still at
  `utils.ts:116`, still called from nowhere.

  **Built exactly what the design named.** `utils.ts`: renamed
  `verifyRestaurantAccessLegacy` → `requireRestaurantAccess`, dropped
  `@deprecated`, forwarded the `options` param the design's Interfaces section
  added (no existing call site passes one — backward compatible), added one
  `console.warn` denial log line (`user=<id> restaurant=<id>`) before the
  throw per `security-baseline.md` A09. `feedback.ts`/`customers.ts`/
  `hiring.ts`/`website.ts` (11 call sites): switched onto `requireRestaurantAccess`,
  one line each, no other change. `offers.ts` (8 call sites): fixed in
  place — `verifyRestaurantAccess(restaurant_id, supabase, user)` (correct
  order) and `if (!access.hasAccess)` — no new helper, matching its own
  already-correct siblings.

  **One addition beyond the design's literal text, flagged rather than taken
  silently.** The design's A09 log line was scoped to `requireRestaurantAccess`
  only (`utils.ts`'s own Components row); `offers.ts`'s in-place fix wasn't
  named for it. Added the identical log line to all 8 `offers.ts` sites too —
  `security-baseline.md`'s A09 control ("authz denial" logged) applies
  regardless of which response convention denies the request, and this is the
  "design silent, standards apply" case `agents/backend/agent.md` names
  directly, not new scope: no behaviour or response-shape change, purely
  additive.

  **Artifact-enumeration grep (step 6b) run before closing out this hop.**
  `grep -rn "verifyRestaurantAccess\|requireRestaurantAccess\|brand-portal/{feedback,offers,customers,hiring,website}.ts"`
  across `departments/` and every instance agent/config/inbox dir. One real
  hit worth checking: `agents/architect/designs/ENG-023-feedback-status-and-notes.md`
  already names `requireRestaurantAccess` explicitly (its own Approach section
  anticipated this exact rename and states the resolution rule for whichever
  of the two tickets builds second — "call `utils.ts` at build time to see
  which name is live"). Already correct, a `map` that agrees with what was
  just built; nothing to fix. Everything else was historical narrative
  (PRDs, board logs, ADRs, `observations.md`/`proposals.md` rows) describing
  the bug as found — `location` class, not live instructions.

  **New tests: 5 files, 24 `Deno.test` cases** (colocated `*.test.ts`, not
  the design's literal `*_test.ts` — this repo already has 5 existing test
  files, all `*.test.ts`; matched the actual repo convention over the
  design's guess, per `engineering-standards.md`'s "first rule," flagged
  here rather than taken silently). Per file: a minimal fake
  `.from().select().eq()...single()`/thenable stub (no live Supabase project,
  no network — matches the design's own Test approach), a negative case per
  call site (19 total — the case that was actually broken: a caller who
  manages restaurant A is denied for restaurant B), plus one positive case
  per file (5 total) proving the stub isn't just failing every call — without
  that, a negative test alone can't tell "correctly denied" from "stub is
  broken." `feedback.ts`/`customers.ts`: `assertRejects` (access check throws
  uncaught). `hiring.ts`/`website.ts`: resolved-value assertion
  (`{success:false,...}` — both wrap the whole function body in a local
  `try/catch`, so the throw never reaches the caller, exactly as the design's
  own Interfaces section describes). `offers.ts`: resolved-value assertion
  (return idiom, never throws).

  **Self-tested.** `deno check` on the 6 changed files: **19 pre-existing
  errors → 10**, confirmed by `git stash -u` against the original tree before
  attributing any of it. All nine eliminated were `TS2345` — `SupabaseClient`
  passed where `verifyRestaurantAccess`'s first parameter expects a
  restaurant-id string, i.e. the wrong-argument-order bug itself, already
  visible to the compiler and never once looked at (no CI wiring on this
  project). The remaining 10 are pre-existing, in code this ticket didn't
  touch (`utils.ts`'s unused `getUserAccessibleRestaurants`, `website.ts`'s
  untouched catch blocks and a supabase-js generic-select quirk) — confirmed
  line-for-line against the stashed original, not assumed. My own 3 new
  narrowing errors (union return types on `handleCustomers`/`handleHiring`/
  `handleWebsite`) fixed with a local result-shape cast in the test file, the
  standard move for loosely-typed production return values. `deno test
  --no-check *.test.ts` (`--no-check` only to route around the *pre-existing*
  10, confirmed above — none introduced by this ticket): **24 passed, 0
  failed**. Full observed denial-log line for every throw-idiom negative
  test, `offers.ts`'s own new log line likewise visible on its negative-test
  runs — both confirmed firing, not just present in the diff.

  **`deno.lock` generated by this pass's own `deno check`/`deno test` runs —
  deliberately not committed.** First one anywhere in this repo (checked
  every function directory); adopting Deno lockfiles repo-wide isn't this
  bug-fix ticket's call. Observation filed (`observations.md`).

  **Committed and pushed**, single repo: `aiorders-api@d5078c5`
  (`fix/ENG-022-brand-portal-tenant-isolation`, tracking
  `origin/fix/ENG-022-brand-portal-tenant-isolation`); no PR opened yet —
  devops's release-readiness hop, same precedent `ENG-008`/`ENG-009`/`ENG-010`
  each set. PR body drafted here:

  *aiorders-api* — title: `Fix broken restaurant-scoped access checks in
  brand-portal (ENG-022)`. Body: the two bug shapes (wrong-order +
  truthy-object check on `feedback.ts`/`offers.ts`; discarded return value on
  `customers.ts`/`hiring.ts`/`website.ts`) and net effect (cross-tenant
  PII read + write exposure); the fix (`requireRestaurantAccess` promoted
  from the dead `verifyRestaurantAccessLegacy` for the 4 throw-convention
  files, `offers.ts` fixed in place matching its own correct siblings, A09
  denial logging on both paths); the 24-test suite (19 negative + 5
  positive) and what it proves; the `deno check` before/after (19 → 10,
  the 9 eliminated being `TS2345` on the exact bug); out of scope (the 4
  already-correct files, unifying response shapes, CI wiring). Single repo,
  no cross-ticket branch dependency.

  **1 transition** (`ready → building`; the build itself happened inside
  it), same as every other ticket's own building hop on this board — the
  next hop (review + quality, combined) is a fresh session's work by design.
  **Consequence:** machine WIP unaffected (`1/1`, unchanged — `building` is
  still inside the counted `ready..ready-to-ship` range, already counted at
  `ready`). Approver-facing WIP and approval cap both unaffected — no gate
  touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing raised this pass — a build hop doesn't notify.
  **Observations filed** (`observations.md`, 2 rows): the `deno.lock`
  decision above, and the `TS2345`-was-the-bug finding as concrete evidence
  for the already-known no-CI-wiring gap in `config/projects.md` (not
  re-proposed — already named there).

  `chained: ENG-022` — `building`, owned by `backend`, an agent-owned state;
  not the approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: see board index.

- `2026-09-03` `building → in-review → in-qa`: code review + quality,
  combined hop, round 1 — **both PASS** (principal-engineer + qa,
  `continue` event pass, context `ENG-022`, this fire's own turn at the
  front of the queue). Narrow scope per the event's own contract — this
  ticket only. Mode check clean (business-os `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: both exit 0, clean.

  **Ran both gates this session** (`config.yaml` →
  `machine_gates.combined_hop: [code_review, quality]` — they read the same
  diff and don't depend on each other), genuinely fresh: neither receipt
  existed at pass start (`agents/principal-engineer/reviews/ENG-022.md`,
  `agents/qa/test-plans/ENG-022.md` both absent). Worktree
  (`~/Documents/projects/_eng/aiorders-api`) confirmed on
  `fix/ENG-022-brand-portal-tenant-isolation@d5078c5`, matching this
  ticket's own frontmatter, no drift after `git fetch`.

  **Code review: automatic-failure scan 0/10 open.** Diff matches the
  design's Approach/Interfaces sections exactly, independently re-checked
  rather than assumed — including verifying by direct code read (not the
  design's word alone) that `feedback.ts`/`customers.ts` have no local
  `try/catch` around their call sites (so a denial reaches `index.ts`'s
  top-level catch as a 500) while `hiring.ts`/`website.ts` do (denial
  becomes `{success:false}` at 200), exactly as the design's Interfaces
  section describes. One non-blocking finding: `offers.ts`'s 8 call sites
  repeat an identical two-line denial block that a small local helper could
  collapse — not blocking (matches the file's own pre-existing repetition
  level), logged to the notebook as a first occurrence. Full detail:
  `agents/principal-engineer/reviews/ENG-022.md`.

  **Verified fresh rather than trusted from the build pass's own log.**
  `deno check` on the 6 changed files (run from
  `supabase/functions/brand-portal/` — running from the repo root hits a
  byonm/node_modules resolution error even though the same `deno.json` is
  picked up either way; noted in the QA plan's `suite_command` so the next
  pass doesn't rediscover this): **10 errors**, independently confirmed all
  pre-existing and outside this diff's changed lines (line-for-line, not
  just count-for-count). `deno test --no-check` on the 5 new test files:
  **24 passed, 0 failed**, matching the build pass's own claim exactly.

  **Executed a real mutation check, not a hand-trace.** Disabled the access
  check at one throw-convention site (`customers.ts:73`) and one
  return-convention site (`offers.ts:80`), reran both test files: exactly
  the two matching negative tests went red, every other test in both files
  (untouched call sites included) stayed green. Reverted immediately after;
  `git status --short` confirmed the worktree matched the recorded commit
  again, only the pre-existing untracked `deno.lock` remaining. This is the
  regression evidence acceptance criterion 4 asks for, executed directly
  this round rather than carried from the build pass's own account.

  **QA plan written**: `agents/qa/test-plans/ENG-022.md` — one row per
  acceptance criterion (all four covered). AC3 (legitimate access
  unchanged) is covered by 5 positive tests, one per file/code-path shape,
  rather than one per all 19 call sites — reasoned explicitly in the plan
  as deliberate sampling (every site in one file shares the identical
  access-check substitution, so the property AC3 is actually about lives at
  the per-file/per-helper level) rather than left as an unexplained gap. No
  open P0/P1 bug on this board (`agents/qa/bugs/_index.md`: one open item,
  `BUG-001`, P2, unrelated project area). Verdict: pass.

  **Both receipts written** (pass-verdict-only, per `config.yaml` →
  `machine_gates.receipts.pass_verdict_only`):
  `agents/principal-engineer/reviews/ENG-022.md`,
  `agents/qa/test-plans/ENG-022.md`. `links.review`/`links.test_plan` set
  on this ticket in the same edit as the state change. `time_spent`/
  `time_remaining` updated in frontmatter.

  **Stopped at `in-qa`, not carried further to `in-security` this pass —
  deliberate, not the transition cap.** 2 transitions used
  (`building→in-review→in-qa`), well under 4.
  `sequential_after_quality: [security, release_readiness]` keeps security
  a separate hop on purpose — it needs QA's *finished* plan to check
  negative-authz coverage against, and that plan didn't exist until this
  pass wrote it moments ago. Same precedent this board's own `ENG-013`
  round-2 review+quality pass set (2026-08-31 entry on that ticket's board
  file) for the identical situation.

  **Step 6b not run** — this is a review+quality hop, not a build hop; step
  6b names itself as build-hop-specific, and nothing this pass wrote
  establishes a new rule about an artifact path, state name, or config key.

  **Consequence:** `machine_wip` unaffected — `ENG-022` was and remains
  inside the counted `ready`..`ready-to-ship` range (`in-qa` is inside it),
  still `1/1`. Approver-facing WIP and approval cap both unaffected — no
  gate raised or resolved this pass.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise — `in-qa` needs no approver gate.
  Nothing to nudge.

  `chained: ENG-022` — `in-qa` is agent-owned (security next), not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: see board index.

- `2026-09-03` `in-qa → ready-to-ship`: **security gate — PASS** (security,
  `continue` event pass, context `ENG-022` — this fire's own turn at the
  front of the queue, per the prior pass's own `chained: ENG-022`). Narrow
  scope per the event's own contract — this ticket only. Mode check clean
  (business-os `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: both exit 0, clean.

  **Re-derived from disk rather than trusted from the prior hops' own
  accounts.** Worktree (`~/Documents/projects/_eng/aiorders-api`) confirmed
  clean but for the pre-existing untracked `deno.lock`, on
  `fix/ENG-022-brand-portal-tenant-isolation@d5078c5`, `git fetch` +
  `merge-base` confirmed no drift against `origin/main@93617c6`. Read all
  six changed source diffs directly (`git diff origin/main...HEAD`) rather
  than taking the design/review's word for what shipped — all 19 call sites
  match the design's Approach/Interfaces sections exactly, independently
  confirmed, not just spot-checked.

  **Threat-modelled the change** (4 questions, full detail in the receipt).
  The load-bearing fact, confirmed by reading `brand-portal/index.ts` directly
  (unchanged by this diff): every handler in this directory runs on a
  **service-role** Supabase client, so RLS is bypassed entirely and
  `verifyRestaurantAccess`/`requireRestaurantAccess` is the *only* access
  control standing between an authenticated brand-portal user and any
  restaurant's data — not one layer of defense-in-depth. This is why the five
  broken call sites were a full P0 rather than a partial one, and confirms
  this diff is sufficient to close the hole rather than a partial mitigation
  awaiting a second layer. Logged to the security notebook as a standing fact
  for future `brand-portal` reviews, not a fresh finding.

  **OWASP A01–A10 walked**, each marked applicable or `n/a` with a reason;
  full table in the receipt. A01 (the ticket's own class): all 19 sites
  independently re-confirmed corrected, object access scoped by owner via
  `restaurant_managers`/`brand_managers` keyed on `user_id`, never by id
  alone. **Zero blocking findings.**

  **Negative-case tests re-run fresh, not taken from the QA/review accounts**:
  `deno test --no-check` on all 5 test files — **24 passed, 0 failed**, all 19
  negative cases confirmed individually **by name** against the PRD's own
  19-action enumeration (one-for-one, counted side by side), denial log line
  visible on every one. `deno check` on the 6 changed files: **10 errors**,
  independently re-derived as the identical pre-existing set both the build
  and review passes already found (3× `hiring.ts`, 3× `utils.ts`'s
  unrelated `getUserAccessibleRestaurants`, 4× `website.ts`), none on a
  changed line.

  **Secrets**: the branch's single commit scanned for key/secret/token/
  password/bearer/PEM/service-role patterns — none. The new `console.warn`
  denial lines carry only `user.id`/`restaurantId` (opaque UUIDs), not PII or
  a credential. **Dependencies**: none new — confirmed directly, no
  `package.json`/`deno.json`/lockfile among the 11 changed files (the
  untracked `deno.lock` is a pre-existing local artifact, not part of this
  diff). **PII handling**: `feedback.ts`/`customers.ts` carry Restricted-tier
  data (name/email/phone/message) per `security-baseline.md`; this diff
  narrows exposure, adds no PII to logs, and the new test fixtures use
  synthetic placeholder values (spot-checked `customers.test.ts`: `name:
  "Jo"`), not realistic data. **LLM checklist**: n/a, `touches_models: false`
  confirmed against the diff directly — no model/agent/tool/MCP touched.

  **Two non-blocking findings, neither introduced by this diff, both
  routed rather than left implicit.** (1) `verifyRestaurantAccess`'s own
  catch-all (`utils.ts`, unchanged) can surface a raw `error.message` to the
  client on its internal-error path — the same finding class already
  three-struck on `ENG-009` (2026-09-02) and carried on `ENG-010` without a
  new proposal; same disposition here, **not re-proposed**, logged to
  `agents/security/notebook/2026-09-03-findings.md` as another occurrence.
  (2) `verifyRestaurantAccess`'s admin/sub-admin/partner-admin/partner-user
  bypass (`utils.ts:27-37`, unchanged, out of this ticket's scope per the
  PRD's own non-goals) grants any of those four roles full cross-restaurant
  access with no further scoping — not asserted as a defect, but worth a
  deliberate confirmation given this ticket's own root cause was an
  *assumed*-correct check elsewhere in the same file. Filed as a proposal
  (`agents/eng-manager/proposals.md`, 2026-09-03 row), not a blocking finding
  — no evidence of an actual defect, and the function is outside this diff
  entirely.

  **SOC 2 evidence trail checked complete**: ticket → PRD → design → code
  review (pass) → QA (pass) → this verdict → release record (pending). No
  gap.

  **Receipt written**: `agents/security/reviews/ENG-022.md` (verdict
  `pass`). `links.security_review` set on this ticket in the same write.
  `time_spent`/`time_remaining` updated in frontmatter in the same edit —
  only devops's release-readiness hop remains.

  **1 transition** (`in-qa → ready-to-ship` — `SKILL.md` step 9 writes
  `ready-to-ship` directly on a pass; `in-security` is never itself persisted
  to frontmatter, same precedent `ENG-009`'s own security-gate pass set),
  well under the cap of 4. **Consequence:** `machine_wip` unaffected —
  `ENG-022` stays inside the counted `ready`..`ready-to-ship` range, still
  `1/1`. No approver-facing or approval-cap change — a security-gate pass
  isn't a gate item to the approver, and `owner` moving to `devops` is an
  agent-to-agent handoff.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise this pass (a security pass isn't a gate
  item to the approver); nothing to nudge. **Decision journal:** not
  written — a machine security-gate verdict is not one of the three approver
  gates (`config/decision-journal.md`'s own scope), so no entry applies.
  **Observations/proposals filed:** the two findings above (notebook entry
  plus the one new proposal); no `observations.md` entry — both routed
  through the security-specific channel the skill's own Outputs table names,
  which is the more specific home for a security finding than a generic
  observation.

  `chained: ENG-022` — `ready-to-ship`, owned by `devops` (release-readiness:
  open the PR), an agent-owned state; not the approver, not blocked, not
  terminal, not held by a cap (still inside the same counted machine-WIP
  range this ticket already occupied). Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-022`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: see board index.

- `2026-09-03` `ready-to-ship → blocked`: **release-readiness — PR opened,
  merge request raised** (devops, `continue` event pass, context `ENG-022` —
  this fire's own turn at the front of the queue, per the prior pass's own
  `chained: ENG-022`). Narrow scope per the event's own contract — this
  ticket only. Mode check clean (business-os `.env` → `MODE=active`).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-022`) and whole-board: both exit 0, clean.

  **Verified all three upstream gates fresh from the receipt files**, not
  assumed from the frontmatter alone: code review
  (`agents/principal-engineer/reviews/ENG-022.md`, `verdict: pass`), quality
  (`agents/qa/test-plans/ENG-022.md`, `last_result: pass`), security
  (`agents/security/reviews/ENG-022.md`, `verdict: pass`). No migration
  applies — this diff has no schema or data-model change. Worktree
  (`~/Documents/projects/_eng/aiorders-api`) confirmed clean but for the
  pre-existing untracked `deno.lock`, on
  `fix/ENG-022-brand-portal-tenant-isolation@d5078c5` (matching this
  ticket's own frontmatter); `git fetch` plus an ahead/behind check against
  `origin/main` confirmed 1 ahead, 0 behind — no drift. `gh pr list --search
  ENG-022 --state all` confirmed no PR already existed for this ticket — not
  a duplicate open.

  **Project registered L1** (`config/projects.md`) — step 1's window check
  does not apply. **Step 3 readiness checks**, same interpretation this
  board already established for `ENG-007`/`ENG-008`/`ENG-013`:
  - Rollback: no migration, no stored-state change — reverting the single
    commit (or the merge, once merged) fully and safely undoes this diff.
    Simpler than every prior ticket's readiness check on this board, all of
    which carried a migration.
  - Observability: both fix paths log via `console.warn` before denying
    (confirmed directly in the security review's A09 line), surfaced through
    Supabase's existing function logs — no new mechanism needed.
  - Cost: **$0/month delta** — no new dependency, no new vendor (security
    review's own Dependencies section, re-confirmed here).
  - Window: n/a, L1.

  **Opened the PR**: `aiorders-api` #9
  (https://github.com/harsimranwalia/aiorders-api/pull/9). Body states the
  two bug shapes, net effect, the fix, the 24-test suite and what it proves,
  the `deno check` before/after (19 → 10, the 9 eliminated being the exact
  bug), the three gates passed, and what's out of scope — same content this
  ticket's own `building`-hop log entry drafted, written out in full this
  hop rather than left as a draft.

  **Wrote the L1 merge-request item**
  (`inbox/2026-09-03-eng022-merge-request.md`), plain `pr_url:` string per
  `skills/release-runner/SKILL.md` step 4 (single repo, no `pr_urls:` list
  needed). Also set `time_estimate:` on the item, mirroring the ticket's own
  field, per `definition-of-done.md`'s Time tracking section ("every
  `type: eng-decision` inbox item... carries `time_estimate`") — flagged
  here rather than taken silently, since none of this board's prior merge-
  request items (`ENG-006`, `ENG-008`, `ENG-009`, `ENG-010`) actually carry
  this field; not fixing those retroactively, just not repeating the gap on
  a fresh one. Ran `departments/engineering/lib/eng-notify.sh raise` — sent
  cleanly (`traces/eng-notify-2026-09-03.log`: `sent: active
  2026-09-03-eng022-merge-request.md`, 01:26:47); stamped `notified:
  2026-09-03T01:26:47` on the item by hand, since the script itself doesn't
  write its own frontmatter back.

  State `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, owner `devops → approver`. `links.pr` set
  to the PR URL. No release record yet, per `release-runner`'s own step
  7/step 4 split — that's written only once the build loop's merge-detection
  confirms the PR merged, same as `ENG-008`/`ENG-009`/`ENG-010`'s current
  position.

  **1 transition** (`ready-to-ship → blocked`). **Consequence:**
  `machine_wip` `1/1 → 0/1` — `ENG-022` leaves the counted
  `ready`..`ready-to-ship` range, freeing the machine-WIP slot (not acted on
  this pass — narrow scope per this event's own contract; a fresh start into
  the freed slot is the next `scheduled`/`continue`-elsewhere pass's work,
  not this one's). Approver-facing WIP `7/2 → 8/2` (still over cap; already
  over before this item — a continuing ticket reaching its own next gate is
  not gated by this cap, only a fresh To-do-column start is, per this
  board's own established reading, same precedent `ENG-008`'s own
  release-readiness entry set).

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** this pass's own item raised and
  stamped above; nothing else to nudge. **Observations/proposals filed:**
  none new — every named gap (verbose-error-message finding, admin-bypass
  scoping question) was already routed to its own channel at the security
  gate, one hop back.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human
  gate the whole hop was driving toward; firing `continue ENG-022` again
  would only queue against a ticket with nothing left for a machine to do,
  same reasoning `ENG-008`'s own release-readiness entry already recorded at
  this identical state. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
  whole-board: see below.

- `2026-09-03` `blocked → shipped → verified` (eng-manager, `scheduled`
  event pass — whole-board sweep, step 5 merge detection). `git fetch
  origin` in `~/Documents/projects/_eng/aiorders-api` (clean, no drift),
  then `git merge-base --is-ancestor d5078c5 origin/main`: **YES** — PR #9
  merged. Given the severity (P0, cross-tenant PII/write exposure),
  cross-checked beyond the local-git-only floor with `gh pr view 9 --repo
  harsimranwalia/aiorders-api`: `state: MERGED`, `mergedAt:
  2026-09-04T02:03:48Z`, merge commit `78194da8` — exactly `origin/main`'s
  current tip. `git diff` between the branch tip and `origin/main` over the
  changed files: empty — the merged tree is byte-identical to what passed
  all three gates, no drift. `decision:` on
  `inbox/2026-09-03-eng022-merge-request.md` stayed blank — merged directly
  on GitHub, same shape `ENG-007`/`ENG-011`/`ENG-024`/`ENG-031` already
  established for this approver.

  **Not advanced past a state that owes gates** (step 5's own "a merge is
  not a gate" clause): re-read all three receipts directly before writing
  `shipped` — `agents/principal-engineer/reviews/ENG-022.md` (`verdict:
  pass`), `agents/qa/test-plans/ENG-022.md` (`last_result: pass`),
  `agents/security/reviews/ENG-022.md` (`verdict: pass`); no migration
  applies (confirmed no `*.sql` in the diff). Independently re-verified the
  fix on the merged tree itself rather than trusting the receipts' word
  alone: `grep`'d all 5 fixed files on `origin/main` (`feedback.ts`,
  `offers.ts`, `customers.ts`, `hiring.ts`, `website.ts`) — all 19 call
  sites call `requireRestaurantAccess`/corrected `verifyRestaurantAccess`,
  and `utils.ts` exports the promoted `requireRestaurantAccess`. All 4
  acceptance criteria re-confirmed against `origin/main`. Release record
  written: `agents/devops/releases/2026-09-03-aiorders-api-ENG-022.md`,
  `links.release` set in the same edit. `state: blocked → verified`,
  `owner: approver → eng-manager`, `blocked_on`/`blocked_from` cleared.

  Merge-request item moved to `inbox/_handled/`. Journal entry added
  (`decision-journal.md`) — silent GitHub merge, no written reply, same
  shape as `ENG-007`/`ENG-011`/`ENG-024`/`ENG-031`'s own rows.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — pure receipt-confirmation and bookkeeping, no new
  implementation work, same precedent `ENG-024`'s identical scheduled-sweep
  discovery already set. **Consequence:** ticket leaves the board's
  in-flight table entirely (terminal); does not affect machine WIP (already
  outside the counted `ready..ready-to-ship` range since its own
  `ready-to-ship → blocked` hop); drops off the approver-facing "Waiting on
  the approver" count (no open inbox item remains for it).

  `chained: none` — `verified` is terminal; the chaining guard never fires
  on a terminal ticket.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.
