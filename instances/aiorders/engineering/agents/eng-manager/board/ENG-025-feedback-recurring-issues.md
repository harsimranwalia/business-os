---
id: ENG-025
title: Recurring feedback issues, per restaurant, over time
project: restaurant-portal
type: feature
size: S
time_estimate: a few hours to half a day
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
  prd: agents/product-manager/specs/ENG-025-feedback-recurring-issues.md
  design: agents/architect/designs/ENG-025-feedback-recurring-issues.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Not a fresh raw request — the direct resolution of the non-blocking
standing question raised alongside `ENG-023`
(`inbox/2026-08-29-eng023-frequency-question.md`, now
`inbox/_handled/`), itself sourced from
`agents/product-manager/inbox/_handled/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`,
filed by the approver, `via: control-center`. Verbatim, from that original
request:

> the feedback board on the brand portal does not have status or notes
>
> what to do with the feedback, any actions taken is this frequent what are
> the bottomline issue that need to be resolved by the restaurant location.

The standing question's own answer, verbatim, from
`inbox/_handled/2026-08-29-eng023-frequency-question.md`'s `## Decision`:

> reading b, frequent is same restaurant over time

## Readback

See `agents/product-manager/specs/ENG-025-feedback-recurring-issues.md` →
Readback for why this ticket does not re-run the full request-readback
skill (the ambiguity it exists to catch was already resolved by the
standing question this ticket answers).

## Problem

A restaurant on the brand portal's Feedback page can't see which issues
recur for their own location — only a flat list of individual items, with
no way to tell "is this frequent" without reading every entry by hand.

## Outcome

A restaurant sees a summary of their own recurring feedback issues —
grouped by category, ranked by frequency, reflecting their history over
time — on the same Feedback page, alongside (not replacing) the existing
list.

## Notes

**Confirmed NOT AI/categorization work, against the standing question's own
speculation.** The question that produced this ticket guessed Reading B
"likely means AI-assisted categorization, not just a count" — live schema
evidence (below) shows `restaurant_feedback` already carries populated
`type`/`sub_type`/`nature` columns for every row, so this is a `GROUP BY`
over data that's already categorized, not a new classification system.
Sized `S`, not the `M` the standing question assumed, on that basis.

**Evidence checked, not assumed.** Full detail in the PRD's own Evidence
section. Summary: live `execute_sql` against the real `aiorders-api`
Supabase project (`bmnmnejwdxbcqinqkwko`, read-only, same MCP path
`ENG-011` validated — see `observations.md`) confirmed `sub_type`/`nature`
are real, structured, populated columns (30 distinct combinations, largest
640 rows) — not free text. `restaurant-portal/src/pages/feedback/Index.tsx`
already fetches each restaurant's entire feedback history in one call, so
"over time" (acceptance criterion 2) needs no new backend query at all on
current evidence — confirmed at design time, not assumed here.
`aiorders-api/supabase/functions/brand-portal/feedback.ts` has exactly one
action (`get_feedback`) today.

**Cross-reference with `ENG-022` and `ENG-023`.** Same directory
(`brand-portal/feedback.ts`) `ENG-022` found broken
(`verifyRestaurantAccess()`'s return value checked as truthy instead of
`.hasAccess`). If this ticket's design ends up needing a new backend
action rather than a pure frontend aggregation over the existing
`get_feedback` response, it must model the access check on `catering.ts`'s
confirmed-correct `update_catering_request`, same flag already carried on
`ENG-023`. Not a formal `depends_on` on either ticket — this one doesn't
need `ENG-023`'s status/notes columns, and doesn't need `ENG-022`'s fix to
ship first, only to not repeat its bug if it touches the same file.

**Project scoping.** `restaurant-portal`, matching `ENG-023` (same page,
same audience) — same split precedent as `ENG-003`/`ENG-008`/`ENG-011`/
`ENG-013`/`ENG-014`/`ENG-015`: the other repo's work, if the design needs
any, is named in the PRD rather than inventing a multi-project ticket
shape.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, `watch`
  event pass, context `schtasks`) — direct resolution of
  `inbox/2026-08-29-eng023-frequency-question.md`, found answered
  (**approved**, "reading b, frequent is same restaurant over time",
  `decided: 2026-08-29T17:41:07.724420+00:00`) while sweeping all three
  watched inboxes. Per the item's own text ("Once answered, 'yes' becomes
  its own new ticket"), shaped end to end in this pass — same pattern
  `ENG-013`'s presignup-leads question used toward `ENG-017`.

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (multiple
  tickets touched this pass): exit 0, clean.

  **No fresh request-readback run** — see PRD Readback for why: the
  divergence this skill exists to catch was already caught and resolved by
  the standing question itself; re-running it would re-litigate a closed
  answer, not detect a new one.

  **Investigated live before sizing or writing acceptance criteria** — see
  PRD Evidence and Notes above. This overturned the standing question's own
  assumption (AI-assisted categorization likely needed) and sized this `S`
  instead of the `M` that assumption would have implied.

  **PRD written**:
  `agents/product-manager/specs/ENG-025-feedback-recurring-issues.md`.

  **G1 required** — `feature` type, not XS/bug/chore. Wrote
  `inbox/2026-08-29-eng025-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: restaurant-portal`, recommendation to build now). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's
  own frontmatter for the result and `notified:` timestamp.

  **Capacity used, not "another ticket" per the `ENG-004` precedent this
  same pass applied to `ENG-023`.** This ticket is the direct object of the
  inbox item this `watch` pass found changed, not a different, older ticket
  opportunistically dispatched onto freed capacity — see `ENG-014`'s and
  `ENG-015`'s own log entries this same pass for that distinction. Caps
  verified fresh immediately before raising: `ENG-014`'s and `ENG-015`'s
  G1s both processed earlier in this same pass (approver-facing WIP 2/2 →
  0/2, approval cap → 0/3) and nothing else consumed either in between.
  **State:** `intake → shaped → awaiting-scope`, `owner` moves
  `product-manager → approver`, all in this pass. **Consequence:**
  approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 1/3. `ENG-023`'s own
  still-undrafted G1 is explicitly NOT raised in this same pass — see
  `ENG-015`'s log entry for why (left for the next
  `scheduled`/`watch`/`continue` pass, per the `ENG-004` precedent).

  **Dead-end sweep (scoped to this event):** no other action needed on this
  new ticket.

  **Notify sweep:** this pass's own new item raised and stamped above.
  Nothing else new to nudge this pass.

  **Observations filed** (`observations.md`): the confirmed
  already-populated `sub_type`/`nature` taxonomy overturning the standing
  question's own AI-categorization assumption, in case a future ticket
  makes the same assumption about this table.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-025`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

- `2026-08-29` `awaiting-scope → designed` (approver → architect, `scheduled`
  event pass, context `schtasks`) — the four-times-daily safety-net sweep,
  not a narrow event; swept the whole board per this event's own contract.
  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  Found `inbox/2026-08-29-eng025-g1-scope.md` answered (**approved**,
  `decided: 2026-08-29T22:22:18.827452+00:00`, no additional comment beyond
  the bare decision) — the only file in `inbox/` this pass. PRD `status:
  approved`. Gate item moved to `inbox/_handled/` with a processed footer.
  Journaled in `agents/eng-manager/config/decision-journal.md`.

  **Handed to the architect at `designed`, design work itself not started
  this pass** — same reasoning `ENG-014`'s and `ENG-015`'s own G1 processing
  used: `designed`'s exit condition (tech design written) is the architect's
  own output, not board bookkeeping, so it belongs in a dedicated `continue
  ENG-025` session.

  **Capacity freed, partly reused in this same pass.** This G1 clearing
  freed one approver-facing WIP slot and one approval-cap slot (both back to
  0/2, 0/3). Unlike a narrowly-scoped `watch`/`decision` event, this
  `scheduled` pass's own contract is a whole-board sweep, not one ticket —
  so, per `_index.md`'s own standing note ("`ENG-023`'s own G1 is drafted
  and ready to raise... the moment a `scheduled`/`watch`/`continue` pass
  picks it up"), this same pass used the freed capacity to raise `ENG-023`'s
  G1 (see that ticket's own log). Approver-facing WIP 0/2 → 1/2; approval
  cap 0/3 → 1/3 after that second action — full detail on `ENG-023`'s own
  entry and the board index. No further capacity spent: `ENG-016` through
  `ENG-021` (also G1-drafted and ready) were deliberately left for a future
  pass rather than filling the second approver-facing WIP slot on a judgment
  call not anchored to an explicit pointer the way `ENG-023`'s was.

  **Dead-end sweep (whole board, per this event's own contract):**
  `ENG-007` (`ready-to-ship`) confirmed still correctly held —
  `chained: none`, release window still closed (Saturday); `ENG-009` and
  `ENG-010` (`ready`) confirmed still correctly held pending `ENG-008`
  reaching `in-review` or later; `ENG-011`'s `chained: ENG-011` already
  fired and sits genuinely queued in `traces/.pending`. No broken chain
  found on any of the four. Also found this instance's own git tree
  carrying several passes' worth of legitimate, verified, uncommitted work
  (spanning the `continue ENG-008`, `continue ENG-013`,
  `decision ENG-014`/`ENG-015` and incident-repair passes) — the
  `eng-loop-halted` repair pass's own log claimed to have committed three of
  those files but a fresh `git status` this pass shows otherwise; full
  detail and the resolution on the board index's dated entry for this pass
  rather than repeated here.

  **Notify sweep:** nothing to raise for this ticket itself (its own gate is
  now closed, not open); `ENG-023`'s fresh G1 raised and stamped this same
  pass, see its own entry. No item found with `notified:` older than 24h and
  no `decision:` — nothing to nudge. Approval cap 1/3, not full — no stall.

  **Dead-end sweep:** no other action needed on `ENG-025` itself.

  `chained: ENG-025` — `designed`, owned by `architect`, an agent-owned
  state; firing
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-025`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-025`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

- `2026-08-29` `designed → designed` (architect, `continue` event pass,
  context `ENG-025`) — narrow scope per this event's own contract (resume
  this ticket from its current state; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-025`) and whole-board: both exit 0, clean.

  **Incidental discovery, not reconciled here.** `ENG-007`'s own ticket file
  now reads `state: shipped` (`blocked → shipped`, "control center, merge
  detected... recorded on Harry's say-so; ancestry not consulted") though
  `_index.md`'s header and In-flight table still show it `blocked` — that
  transition happened outside this pass, by a human dashboard action, not by
  a build-loop write. `inbox/2026-08-29-eng007-merge-request.md` carries no
  `decision:` field, so its gate item is also not yet resolved/archived to
  match. Same shape as the `ENG-011` discovery `ENG-007`'s own pass logged
  earlier today — flagged as an observation (`observations.md`) rather than
  reconciled, out of scope for a ticket-scoped `continue ENG-025` pass; pre-
  and post-pass whole-board gate checks both ran clean regardless.

  Did the architect's design work this ticket's prior entry deferred to a
  dedicated session. Read `restaurant-portal` fresh from its `_eng` worktree
  (`eng/base`, clean, 2 commits behind `origin/main` — both unrelated CI/
  deploy-workflow commits, confirmed via `git log b3a81ef..origin/main`
  before fast-forwarding; safe, no risk to this design). Read
  `src/pages/feedback/Index.tsx` in full: confirmed the PRD's Evidence
  claims firsthand — flat list plus exactly two aggregate stats (total
  count, average rating), fetches the restaurant's entire feedback history
  in one call, no per-category breakdown exists today. Read
  `src/services/brandPortalApi.ts`'s `RestaurantFeedback` interface:
  `sub_type`/`nature` both nullable, `type` non-null — confirms a `sub_type
  ?? type` fallback is needed for grouping. Read `aiorders-api`'s
  `brand-portal/feedback.ts`, `catering.ts`, and `utils.ts` (worktree
  sitting on `ENG-008`'s branch; `git diff origin/main...HEAD --stat`
  confirmed that branch touches only `admin-portal/handlers/influencers.ts`
  and its own migration, nowhere near `brand-portal/`, so safe to read
  without switching branches) to confirm the PRD's access-check warning
  firsthand rather than trusting its wording: `feedback.ts`'s `getFeedback`
  calls `verifyRestaurantAccess(supabase, user.id, restaurant_id)` (wrong
  argument order against `utils.ts`'s real signature) and checks the
  returned object's truthiness (`if (!hasAccess)`, always false on an
  object) instead of `.hasAccess` — confirmed live, same bug class
  `ENG-022` is already scoped to fix, and confirmed **not** one this
  design's own change touches or depends on (see below).

  **Design conclusion: no backend change needed.** All three acceptance
  criteria are answerable from data the page already has in the browser —
  `sub_type`/`nature`/`type` are already present on every fetched row, and
  the existing call already returns full history with no date filter. Wrote
  `agents/architect/designs/ENG-025-feedback-recurring-issues.md`: one new
  exported pure function (`groupRecurringIssues`) plus one new "Recurring
  Issues" `Card` section, both in `Index.tsx`, no new file, no new backend
  action, no new table/column/migration, no one-way door, no G2, no ADR.
  Documented three of my own design calls the PRD explicitly left open
  (count-≥-2 recurrence threshold, all-time windowing, keeping the helper
  inline rather than a new module) under Approach/Alternatives rather than
  deciding them silently.

  **State stays `designed`** — exit condition (tech design written) is now
  met, but the flip to `ready` belongs to whichever pass finds machine WIP
  clear, same convention `ENG-014`'s and `ENG-015`'s own entries used.
  **`owner: architect → eng-manager`.** **Not chained** — machine WIP
  verified fresh immediately before this decision, each ticket's own
  `state:` field read directly rather than trusting `_index.md`'s header:
  `ENG-007` `shipped` (outside range, see discovery above), `ENG-008`
  `building`, `ENG-009` `ready`, `ENG-010` `ready`, `ENG-011` `blocked`
  (outside range), `ENG-013` `building` — 4/1 (`ENG-008`, `ENG-009`,
  `ENG-010`, `ENG-013`), still over the one-ticket cap. `chained: none` —
  held by the machine WIP cap.

  **0 net board consequence**: `machine_wip` unaffected (still 4/1 —
  `designed` sits outside the counted `ready`...`ready-to-ship` range);
  approver-facing WIP and approval cap both unaffected by this ticket's own
  transition (this pass did not touch either cap's count — the `ENG-007`
  discovery above is noted, not acted on). In-flight table's `ENG-025` row:
  Owner column updated to `eng-manager`, State unchanged.

  **Dead-end sweep (scoped to this event):** no other action needed on
  `ENG-025` itself.

  **Notify sweep:** nothing to raise — this pass produced a design doc, not
  a gate item. Nothing with `notified:` older than 24h and no `decision:`
  found in this event's narrow scope — nothing to nudge.

  **Observation filed** (`observations.md`): the `ENG-007`/control-center
  discovery above.

  `chained: none` — `designed`, held by the machine WIP cap (4/1). Resume
  happens when a future pass finds the cap clear. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-025`) and
  whole-board: both run clean, no `WAIVED:` lines. Board holds four dated
  entries once this one is added — oldest (`ENG-014`) moved to
  `_index-archive.md`, per the keep-three rule.
