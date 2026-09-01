---
id: ENG-023
title: Add status and internal notes to each brand-portal feedback item
project: restaurant-portal
type: feature
size: S
time_estimate: a few hours to half a day
time_spent:
time_remaining:
severity: P2
priority:
state: designed
owner: architect
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
  prd: agents/product-manager/specs/ENG-023-feedback-status-and-notes.md
  design: agents/architect/designs/ENG-023-feedback-status-and-notes.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T09:17:39.295756+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # the feedback board on the brand portal does not have status or notes
>
> what to do with the feedback, any actions taken is this frequent what are
> the bottomline issue that need to be resolved by the restaurant location.

## Readback

See `agents/product-manager/specs/ENG-023-feedback-status-and-notes.md` →
Readback — the full two-reading comparison and the divergence live there
rather than duplicated here.

## Problem

The brand portal's Feedback page (`restaurant-portal/src/pages/feedback/Index.tsx`)
is read-only display over `restaurant_feedback`, which has no `status` or
`notes` column at all — confirmed in schema, not just missing from the UI.
Restaurants get a real-time email per new item but have no durable record
afterward of what was done about it.

## Outcome

A restaurant can set a status and write an internal note on each of their
own feedback items, both persisting and scoped to their own restaurant only.

## Notes

**Investigated before writing anything**, same practice this board has used
throughout: read `restaurant-portal`'s Feedback page, its `brandPortalApi`
client, `aiorders-api`'s `brand-portal/feedback.ts` handler (only action
today: `get_feedback`), the `restaurant_feedback` table's real schema (no
status/notes columns), and the `notifications-handler`'s per-submission email
(confirmed feedback isn't missed on arrival, only unrecorded afterward).

**Filed alongside `ENG-022`, not folded into it.** Tracing this request's
backend surfaced a confirmed, unrelated security defect in the same
directory (`feedback.ts`'s existing `getFeedback` has a broken tenant-
isolation check) — filed as its own ticket
(`agents/eng-manager/board/ENG-022-brand-portal-tenant-isolation-broken.md`)
per `agents/product-manager/agent.md`'s `never_touches` list (security
findings aren't the PM's to fix or fold into a feature PRD). Cross-referenced
in both tickets' Risks/Notes: this ticket's new write path must be modeled on
`catering.ts`'s confirmed-correct `update_catering_request`, not on this
file's own broken `getFeedback` neighbor.

**Non-blocking question raised alongside this ticket**, not held for it:
`inbox/2026-08-29-eng023-frequency-question.md` — whether "is this frequent"
/ "bottomline issues" also wants a built cross-item aggregation view, per the
architect's blind reading diverging from this PM's own on exactly that point.
Same shape as `ENG-013`'s presignup-leads question → `ENG-017`: this ticket
ships the confirmed core regardless of the answer.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
reads 2/2 (conservative — `ENG-014`/`ENG-015`'s G1s are answered but not yet
processed by a `decision` pass; treated as still holding their slots, same
convention `ENG-021` used). G1 content (readback, both readings, non-goals,
recommendation) is fully drafted in the PRD's own Decision section, ready to
raise the moment a slot clears.

**Recommendation, for whenever this G1 raises:** build it. The core (status +
notes) is a small, well-precedented change — the department has shipped this
exact shape (new column + restaurant-scoped edit) three times this week
(`ENG-007`, `ENG-009`, `ENG-010`) — and it directly answers a question the
approver asked in their own words ("any actions taken").

## Log

- `2026-08-29` `intake → shaped` (product-manager, `intake` event pass,
  context this exact request file). Per this event's own narrower contract,
  worked only this one request end to end — did not sweep the rest of
  `agents/product-manager/inbox/` (`fix-the-location-bug-on-foodswipe`
  untouched, its own `intake` event presumably already queued or pending).

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Caps checked fresh from `inbox/` directly**: `ENG-014`'s and `ENG-015`'s
  G1s both still sit in `inbox/` (not yet moved to `_handled/`) with
  `decision: approved` — answered but unprocessed, held conservatively as
  still occupying their approver-facing WIP slots pending a `decision` pass,
  same reasoning the board index and `ENG-021` already used. Approver-facing
  WIP treated as 2/2 for this ticket's own purposes.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  live code across `restaurant-portal` and `aiorders-api`, plus a blind
  architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to this
  PM's own reading). Strong convergence on the core (status + notes per
  item); one material divergence on the "is this frequent" /
  "bottomline issues" phrase — see PRD Readback. Not held up: confirmed core
  shaped now, divergence raised as its own non-blocking question, per the
  `ENG-013`/leads-question precedent.

  **Investigated all relevant code before proposing anything**: see Notes
  above.

  **Found and filed `ENG-022` as a separate ticket** — a confirmed P0
  security defect discovered while tracing this request's backend, out of
  scope for a PM to fix or fold in. Full reasoning on `ENG-022`'s own PRD and
  ticket log.

  **PRD written**:
  `agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`.

  **No G1 raised this pass** — approver-facing WIP at cap (2/2, conservative
  count above). G1 content fully drafted in the PRD, ready the moment a slot
  clears.

  **Non-blocking question raised**:
  `inbox/2026-08-29-eng023-frequency-question.md` (`agent: product-manager`,
  `gate: intake-question`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **State:** `intake → shaped`. `owner` stays `product-manager` — nothing
  handed off yet, no gate open. **Consequence:** no cap numbers change —
  `shaped` counts toward neither approver-facing WIP nor machine WIP (still
  6/6).

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract beyond the fresh cap-verification above.

  **Observations filed** (`observations.md`): none beyond what's captured on
  `ENG-022` and this ticket directly.

  `chained: none` — `ENG-023` sits at `shaped`, held by the approver-facing
  WIP cap, not genuinely blocked or waiting on a human for this ticket
  specifically; firing `continue ENG-023` now would only re-discover the
  same cap with no new work to do. Re-check once a
  `decision`/`watch`/`scheduled` pass actually clears `ENG-014` or
  `ENG-015`. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-023`) and whole-board: see pass notes in
  `agents/eng-manager/board/_index.md`.

- `2026-08-29` `shaped → awaiting-scope` (product-manager → approver,
  `scheduled` event pass, context `schtasks`) — the four-times-daily
  safety-net sweep. Mode check clean (business-os `.env` → `MODE=` empty;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Re-check from the top, not trusted from the cached header.** Processing
  `ENG-025`'s answered G1 this same pass (see that ticket's own log) freed
  both the approver-facing WIP slot and the approval-cap slot this ticket's
  own prior log entry was waiting on. `_index.md`'s own "Waiting on the
  approver" section names this exact ticket by id as the one to raise "the
  moment a `scheduled`/`watch`/`continue` pass picks it up" — this is that
  pass.

  **No new drafting needed** — G1 content (readback, both readings,
  evidence, non-goals, recommendation) was already fully drafted in the
  PRD's own Decision section at `shaped` time. Wrote
  `inbox/2026-08-29-eng023-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: restaurant-portal`, recommendation to build now) from
  that drafted content, not written fresh. Ran
  `departments/engineering/lib/eng-notify.sh raise` on it — logged
  `SLACK_WEBHOOK_URL unset — cannot notify` (`traces/eng-notify-2026-08-29.log`,
  15:55:43), same open, already-tracked notify-channel gap every gate item
  today has hit; stamped `notified: 2026-08-29T15:55:43` into the item's
  frontmatter directly, per this instance's established practice of
  stamping regardless of whether the push itself succeeds.

  **State:** `shaped → awaiting-scope`, `owner` moves `product-manager →
  approver`. **Consequence:** approver-facing WIP 0/2 → 1/2 (after
  `ENG-025`'s own G1 freed it earlier this same pass); approval cap 0/3 →
  1/3. Two approver-facing slots and two approval-cap slots remain free —
  `ENG-016` through `ENG-021` (also G1-drafted) deliberately left for a
  future pass; see `ENG-025`'s own log entry for why only this one ticket's
  freed capacity was reused rather than filling every open slot.

  **Dead-end sweep:** no other action needed on `ENG-023` itself; the
  broader whole-board sweep this event ran is recorded on `ENG-025`'s own
  log entry and the board index, not repeated here.

  **Notify sweep:** this pass's own new item raised and stamped above.
  Nothing else to nudge.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

<!-- merge note: local (HEAD, `schtasks` context) and remote (`launchd`
  context) independently recorded the same `awaiting-scope -> designed`
  handoff for the same decided G1 (identical `decided:` timestamp) — a
  duplicate-dispatch race on two hosts, not contradictory content. Kept
  remote's entry (fuller: also flags a stash-pop investigation) and
  dropped local's redundant duplicate rather than logging the same
  transition twice. -->
- `2026-08-29` `awaiting-scope → designed` (product-manager → architect,
  `watch` event pass, context `launchd`) — swept all three watched inboxes
  per the event's own contract; found `inbox/2026-08-29-eng023-g1-scope.md`
  answered (**approved**, `decided: 2026-08-29T23:38:32.834274+00:00`, no
  additional comment beyond the bare decision) since the last pass touched
  it. Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` not checked to override — falls through).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-023`) and whole-board: both exit 0, clean.

  **Found the repo mid-recovery from an unrelated, unresolved `git stash
  pop` conflict** (`stash@{0}: On main: local instance state before
  marketing port pull`, touching `_index.md`, `_index-archive.md`,
  `observations.md`) — resolved by someone/something else to a clean
  working tree matching `HEAD` (`ad4c6c4`) between this pass's first and
  second `git status` check, stash left intact and untouched. Not this
  pass's to resolve — out of scope for a `watch` event, and the stash's own
  survival looks deliberate. Flagged in `observations.md`, not acted on
  further.

  PRD `status: approved`
  (`agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`),
  Decision section filled in. Gate item moved to `inbox/_handled/` with a
  processed footer. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **Handed to the architect at `designed`, design work itself not started
  this pass** — same reasoning `ENG-014`'s own `watch`-event G1 processing
  used: `designed`'s exit condition ("tech design written") is the
  architect's own output, and this ticket's write path (a new
  `update_feedback` action modeled on `catering.ts`'s
  `update_catering_request`, plus two new columns on `restaurant_feedback`)
  is implementation-adjacent work against a project with real customer
  data, not board bookkeeping — it belongs in a dedicated `continue
  ENG-023` session.

  **Worth flagging for that session directly: machine WIP is currently
  5/1, over the board's own cap.** Per `_index.md`'s own header and the
  `ENG-014`/`ENG-015` precedent already sitting at `designed` for the same
  reason, even a clean design with no one-way door should hold at
  `designed` rather than advance to `ready` until the count clears —
  `designed` and `awaiting-scope` aren't gated by this cap, `ready` is.

  **Capacity freed, not spent on anything else this pass** — same
  precedent `ENG-014`'s `watch` entry set: dispatching the freed
  approver-facing WIP/approval-cap slot onto a different waiting ticket is
  left for a future `scheduled`/`watch`/`continue` pass, out of scope for a
  `watch` event scoped to the inbox items it found changed. `ENG-011`'s L1
  merge request, the board's other open gate item, remains unanswered
  (`decision:` empty) — checked fresh, nothing to act on, never inferring
  approval from silence.

  **Dead-end sweep (scoped to this event's own contract):** the other two
  watched inboxes (`agents/product-manager/inbox/`,
  `agents/eng-manager/inbox/`) hold only `.gitkeep` — nothing new. No
  broken chain found on this ticket's own prior log entries.

  `chained: ENG-023` — `designed`, owned by `architect`, an agent-owned
  state; firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-023`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

<!-- merge note: local (HEAD) recorded a 2026-08-29 `continue ENG-023` entry
  claiming the design was completed that pass and owner handed off to
  eng-manager. Remote's entries below (2026-08-30/08-31) show that chain
  actually failed twice (auth-token and DNS errors) before ever writing a
  design, and the design was only genuinely written on 2026-08-31 with
  owner staying `architect` — directly contradicting the local claim.
  Remote's later, verified account is kept and the local entry dropped. -->
- `2026-08-30` (broken chain, no state change) `scheduled` event pass,
  context `launchd` — the safety-net sweep this exact scenario exists for.
  This ticket's own `continue ENG-023` chain, fired at the end of the entry
  above, did run — twice — but never got past reading files: attempt 2
  (02:13:55) failed with `401 OAuth access token has been revoked` before
  touching any file; attempt 3 (09:31:19) read this ticket, the board index,
  and two other files, then failed with a DNS error (`ENOTFOUND`) before
  writing anything. **No tech design was produced by either attempt** — the
  frontmatter and this log are unchanged from the `designed`/`architect`
  state the prior entry left them in. Event dropped after 3 attempts total
  (`inbox/2026-08-30-eng-events-dropped.md`, notified this same pass).
  Root-caused before re-firing, per that item's own recommendation: both
  failures are infra-level (auth token, DNS), neither implicates this
  ticket's own content, and this pass's own working tool access suggests
  both have since cleared. Re-firing:
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-023`.
  `chained: ENG-023`.

- `2026-08-31` (no state change — held at `designed` by the machine WIP cap)
  `continue` event pass, context `ENG-023` — resuming this ticket's own
  design work per the prior pass's explicit hand-off (the 2026-08-29
  `designed`-entry note: "design work itself not started this pass... belongs
  in a dedicated `continue ENG-023` session"). Narrow scope per this event's
  own contract (resume this ticket from its current state; no board-wide
  sweep). Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: both exit 0, clean.

  **Investigated the live code before designing, same practice this board
  uses throughout**: read `restaurant-portal`'s `src/pages/feedback/Index.tsx`,
  `src/services/brandPortalApi.ts` (the `RestaurantFeedback` interface,
  `callApi`, the existing `getCateringRequests`/`updateCateringRequest` pair
  as the closest client-side precedent), `src/components/catering/CateringRequestCard.tsx`
  (status-badge UI precedent); `aiorders-api`'s `brand-portal/feedback.ts`,
  `catering.ts`, `utils.ts`, and `index.ts`'s routing switch; the
  `restaurant_feedback` table's migration history (no tracked `CREATE TABLE`,
  same untracked-base-schema gap every prior ticket touching this table has
  found) and the closest sibling precedent,
  `20260807000006_restaurant_claim_documents.sql` (`status TEXT NOT NULL
  DEFAULT '...'` + `notes TEXT`, RLS enabled with no policies since access is
  service-role-only — the exact shape this design reuses); and `ENG-022`'s
  own design doc (same directory, unshipped) for its file-by-file convention
  classification.

  **Confirmed the `getFeedback` bug `ENG-022` already found**, first-hand:
  `feedback.ts` calls `verifyRestaurantAccess(supabase, user.id,
  restaurant_id)` — arguments in the wrong order against `utils.ts`'s real
  signature `(restaurantId, supabase, user, options)` — and checks `if
  (!hasAccess)` against the whole returned object rather than `.hasAccess`,
  which is always truthy. Not this ticket's bug to fix; confirmed only so
  the new `updateFeedback` path does not reuse this call site.

  **Wrote the tech design**:
  `agents/architect/designs/ENG-023-feedback-status-and-notes.md`. Summary:
  two new columns (`status text not null default 'new'`, `notes text`) on
  `restaurant_feedback`, modeled on the `restaurant_claim_documents`
  precedent; one new `update_feedback` action in `feedback.ts` following
  `catering.ts`'s `update_catering_request` *data-access shape* (fetch
  record → resolve `restaurant_id` → verify access → update → return) while
  keeping `feedback.ts`'s own **throw** convention for failures, rather than
  importing `catering.ts`'s return-idiom wholesale — reasoned explicitly in
  the design's Approach section, since the PRD's literal wording ("model it
  on catering.ts") and `ENG-022`'s file classification (`feedback.ts` is a
  throw-convention file) point in different directions until read together.
  Flagged a real but non-blocking sequencing note: the correct access-check
  helper exists today as `verifyRestaurantAccessLegacy`, becomes
  `requireRestaurantAccess` once `ENG-022` ships — whichever ticket builds
  second checks `utils.ts` for the live name, no `depends_on` needed (per the
  PRD's own instruction on this point).

  **One-way doors: none** — decided, not escalated. Two design questions the
  PRD left open were resolved directly rather than punted: status vocabulary
  is `new | in_progress | resolved` (the PRD's own suggested example), and no
  per-change audit/attribution log — no sibling status field in this
  codebase has one, and it's a pure additive table later if it turns out to
  matter (design's Alternatives #2). Both reversible, so decided here rather
  than raised as G2. **No ADR written** — no one-way door, no deviation from
  `engineering-standards.md`, no accepted security risk; a small,
  well-precedented additive change doesn't meet the architect's own bar for
  a record (`agents/architect/agent.md`).

  **State: unchanged, `designed` / `architect`.** The exit condition for
  `designed` (tech design written; ADRs logged — none apply; one-way doors
  decided — none exist) is now met, and with no one-way door this ticket's
  next stop in the full lane is `ready` directly, no G2. **Not advanced there
  this pass.** Re-verified machine WIP fresh from every ticket file's own
  frontmatter rather than trusting the board index's cached header
  (`ENG-008`/`ENG-013` `building`, `ENG-009`/`ENG-010` `ready` — 4/1,
  confirmed, still over the cap and still draining naturally). Same
  precedent this ticket's own prior log entry already flagged for
  `ENG-014`/`ENG-015`: a clean design with no one-way door still holds at
  `designed` rather than advancing to `ready` until the count clears —
  `ready` is gated by the cap, `designed` is not. `ENG-023` now joins
  `ENG-014`/`ENG-015`/`ENG-025` at `designed`, fully or partly design-ready,
  queued behind the same cap.

  **Dead-end sweep, scoped to this event's own contract**: no broken chain on
  this ticket's own prior entries beyond the one this pass exists to resume
  (already closed by writing the design). No new observation beyond what's
  captured in the design doc itself.

  **Notify sweep**: nothing raised this pass — no gate opened (no one-way
  door), nothing to nudge on this ticket.

  `chained: none` — `designed`, held by the machine WIP cap (4/1, re-verified
  fresh above), not genuinely blocked and not waiting on a human for this
  ticket specifically, but firing `continue ENG-023` now would only
  re-discover the same cap with no new work to do, same reasoning this
  ticket's own 2026-08-29 `shaped`-state entry used. Re-check once a
  `scheduled`/`watch`/`continue` pass drains `ENG-008`/`ENG-009`/`ENG-010`/`ENG-013`
  below the cap. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-023`) and whole-board: both exit 0, clean, no `WAIVED:` lines.
