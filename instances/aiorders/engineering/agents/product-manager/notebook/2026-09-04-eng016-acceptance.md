# Acceptance — ENG-016 (catering quote generator, Piece 1 — parent)

## Why this ticket's own check is not a rubber stamp

`ENG-016` has no diff of its own — the `ADR-003`-class parent exemption
means it is never itself reviewed, tested, or security-scanned. But
`acceptance-check/SKILL.md`'s trigger is "a ticket enters state `shipped`,"
with no parent carve-out, and its purpose ("confirm the shipped thing does
what the PRD promised... checked against the live result, not the proxies
that are themselves upstream evidence someone *intended* it to work") applies
with more force here, not less: this is the one point where anyone checks
whether Piece 1 *as a whole* — all four sub-tickets, three repos — does what
the PRD promised, rather than each surface in isolation.

That matters concretely because three of the four children (`ENG-031`,
`ENG-032`, `ENG-033`) reached `verified` via the receipt-bookkeeping shortcut
named in `ENG-034`'s own notebook (`2026-09-04-acceptance.md`) — review/QA/
security receipts re-read fresh, but no criterion individually walked against
live code. `ENG-034` alone got the full walk, for the eight criteria it
owns, and its own notebook explicitly deferred the rest: *"Whether to raise
Piece 2 is `ENG-016`'s own question to answer once it reaches its own
acceptance-check, not this ticket's."* Taking the parent exemption to mean
"nothing left to check" would let AC-5/6's storage half and AC-7/8/10/12/13
go from never-individually-verified straight to permanently-closed with
nobody ever having read the live code for them. So this entry does two
things: closes that specific gap for this family (not the general ten-ticket
drift already covered by the open `proposals.md` row, which this doesn't
re-litigate), and then runs steps 4–6b properly.

## Scope

All 13 acceptance criteria in the PRD
(`agents/product-manager/specs/ENG-016-catering-quote-generator.md`), Piece 1
only (Pieces 2/3 are explicitly out of scope, not filed).

| AC | Owner | This pass |
|---|---|---|
| 1 (narrowed), 2, 3, 4, 5 (client half), 6 (client half), 9, 11 | `ENG-034` | Cross-referenced from `ENG-034`'s own notebook — each already checked line-by-line against `origin/main` at the merged commit, not re-derived |
| 5 (storage half), 6 (storage half), 10, 13 | `ENG-033` (`aiorders-api`) | Walked fresh against live code this pass — never individually checked before (receipt-bookkeeping shortcut) |
| 7, 8, 12 | `ENG-032` (`restaurant-portal`) | Walked fresh against live code this pass — same gap |

## Check against the live result — not the proxies

`git fetch origin main` on both `aiorders-api` (`5415ef0`) and
`restaurant-portal` (`5276a53`) fresh this pass, then `git show origin/main:
{path}` for every file below — the same substitute `ENG-034`'s own entry
used and named as the standard for this board (no throwaway environment,
no browser).

## Walk every criterion not already covered

| AC | Criterion | Checked against | Result |
|---|---|---|---|
| 5 (storage) | Stored with `action_type = QUOTE_SUBMITTED` and its selections (category, item ref, name, quantity, note) | `aiorders-api/supabase/functions/catering-request/validation.ts` `deriveActionStatus()`: `QUOTE_SUBMITTED` + valid selections → `{ actionType: 'QUOTE_SUBMITTED', selections, status: 'Quote Generated' }`; `isValidSelections()` requires integer `quantity > 0`, string `name`, optional `note` ≤500 chars — `category`/`item_id` pass through unvalidated, matching the migration's own documented shape. `index.ts` inserts `action_type: normalizedActionType, selections: normalizedSelections` directly | **Pass** |
| 6 (storage) | Stored with `action_type = MANUAL_CONTACT_REQUESTED` and no selections | Same function: `MANUAL_CONTACT_REQUESTED` branch force-nulls `selections` regardless of what was sent (comment: "discard on purpose, not an omission — ENG-033 quality-gate finding") | **Pass** |
| 7 | `QUOTE_SUBMITTED` → board column `Quote Generated`; `MANUAL_CONTACT_REQUESTED` → `Contact Requested`, no staff action needed | `deriveActionStatus()` writes exactly those two `status` strings server-side; `restaurant-portal/src/components/catering/CateringKanban.tsx` `statusConfig`/`columns` (lines 39–80, `origin/main`) carry both as first-class columns with their own color config | **Pass** |
| 8 | Existing requests in the five current stages are unchanged and stay visible when the two new stages are added | Same file: `New Enquiry`, `Contacted`, `Not Interested`, `Finalized`, `Completed` all still present in both `statusConfig` and `columns`, same keys, same colors as the pre-ticket shape — the two new columns are inserted, nothing removed or renamed | **Pass** |
| 9 | (owned by `ENG-034`, cross-referenced) | — | Pass (see `ENG-034`'s notebook) |
| 10 | An existing caller sending today's payload with no new fields succeeds unchanged, row stored as today | `index.ts`: `action_type`/`selections` destructured from the body but never required; when absent, `deriveActionStatus(undefined, undefined)` falls through to `{ actionType: null, selections: null, status: undefined }` — the insert's `...(derivedStatus !== undefined ? { status: derivedStatus } : {})` spread contributes nothing, so `status` is omitted from the insert entirely and the column keeps using its pre-existing default, exactly as before this ticket. The two new columns are nullable (migration: `add column if not exists ... text` / `... jsonb`, no `not null`, no default) and no old caller (`CateringForm.tsx`'s existing POST shape, confirmed in the PRD's own Evidence section; GoHighLevel; `restaurant-marketplace`) sends either field | **Pass** |
| 12 | Owner's detail modal renders fulfillment option, guest count, and itemized selections (quantities, notes) readably | `restaurant-portal/src/components/catering/CateringDetailModal.tsx`: `Number of Guests` row renders `request.number_of_guests` unconditionally; `Delivery Method` badge renders `request.delivery_method`; an "Order Selections" block (guarded on `selections.length > 0`) groups by `category`, rendering `{quantity}× {name}` plus `— {note}` when present | **Pass** |
| 13 | Any read/write of the new selection data by a non-owning caller is refused by the existing authorization path | `aiorders-api/supabase/functions/brand-portal/catering.ts`: `get_catering_requests`, `create_catering_request`, `update_catering_request` (the only read/write paths that touch the new `action_type`/`selections` columns — `select('*')` and `update(updateData)`) all call `verifyRestaurantAccess(restaurant_id, supabase, user)` and return `Access denied` on failure, before touching the table. No new or separate authorization path was added for the two new columns — they ride the same gate every other field on this endpoint already used | **Pass** |

**All 13 criteria: pass.** No criterion required rework; nothing routes back
to `building`.

## Check the non-goals (whole-family sweep)

Re-scanned all four merged diffs (not just `ENG-034`'s, already checked by
its own entry) for anything on the PRD's non-goals list: pricing/packages/
tiers/upcharges, "Edit Quote"/resend, `Quote Viewed`/tokenized links,
autopilot wiring, collapsing the eight hardcoded status-string copies,
`restaurant-marketplace`/CloudWaitress paths, payment/deposits, reordering
the meaning of the five existing stages.

None present. One thing worth naming rather than silently passing over:
`CateringDetailModal.tsx` carries an `onEdit` prop and an "Edit" button —
not new scope creep, since `ENG-016`'s own ticket Notes already named this
exact surface ("a small addition to the already-shipped
`CateringDetailModal`") and the design's own component table only ever
listed a ~100-line addition, not a new flow; it opens a plain field-edit
form, unrelated to Piece 3's "edit an already-priced quote and resend it" —
there is no price anywhere in this diff to edit. The seven-column board
layout change (two new columns inserted between `New Enquiry` and
`Contacted`) is the one named, accepted risk from the PRD's own Risks
section, not an undisclosed one.

## Check the cost

PRD estimate: `$0/month` run cost, no new vendor/service. Each child's own
release record already confirmed this independently (`ENG-031`/`032`/`033`/
`034`, all "no new dependency, no new service"); nothing in this pass's own
review of the merged code (nullable-column migration, no new external call)
contradicts that. Matches.

## Route

**All 13 criteria pass.** State → `verified`, owner → `eng-manager` — see
`ENG-016`'s own board-file log for the transition
(`building → shipped → verified`, the `ADR-003`-class exemption for the
`shipped` half).

## Step 6b — continue the approved sequence?

PRD names two next items with real shape: Piece 2 (package/price-book,
`L`) and Piece 3 (owner edit/resend + view tracking, `M`–`L`). Condition 1
(enough shape to draft from) is met for Piece 2.

**Condition 2 is not met.** `ENG-016`'s own G1 answer was "Lets start with
piece 1" (2026-09-03T15:47:46) — already read, on this ticket's own board
log at the time it was answered and again at its `designed → ready`
hand-off, as confirming build *order*, not pre-authorizing the rest of the
sequence. That reading doesn't clear 6b's bar (`ENG-006`'s recorded answer,
*"the proposed five-ticket sequence stands as shape to file incrementally"*
— an explicit sequence sign-off, which this G1 is not). Per 6b's own
instruction for exactly this case: ask a targeted follow-up question rather
than assume the rest was approved by implication — same shape
`ENG-007`→`ENG-027`'s own continue-sequence question already set precedent
for on this board.

**Not a plain yes/no, unlike that precedent.** The PRD's own Recommendation
section holds Piece 2 on one more named condition beyond "continue the
sequence": *"who maintains each restaurant's price book"* — an ongoing
operator-time cost with no owner named anywhere in the approver's original
rewrite. Filing Piece 2 on a bare "yes, continue" would still leave that
unanswered, so the question raised this pass
(`inbox/2026-09-04-eng016-continue-piece2-question.md`) bundles both: continue
to Piece 2 at all, and if so, who owns keeping each restaurant's price book
in sync with its menu. Not filed as a ticket — per 6b, filing only starts
once both conditions hold, and they don't yet.

## What the estimate got right

`time_estimate: several days to a week` (parent, `L`) held almost exactly —
sum of the four children's own estimates (~3–4 days raw build,
`2026-09-03-eng016-work-breakdown.md`'s own Sizing section) plus gate
rounds landed inside the band, first-precedent decomposition included.

## What it missed

The rewrite's own G1 (the approver's `changed` answer) asked for three
target stages but its own enum-update instruction named only two — resolved
as a rider (`Quote Viewed` deferred to Piece 3) rather than a blocking
question, and that resolution held with no rework needed once building
started. Worth noting for the next PRD: a spec's own internal
inconsistency, caught and resolved at G1 time as a named rider, is cheaper
than the same inconsistency surviving into a design or a build.

## Also worth recording

**This entry is also the backfill point for `ENG-032`/`ENG-033`'s own
un-walked criteria**, not just Piece 1's aggregate check — a reusable shape
worth naming since this is the first parent ticket this board has run
through its own acceptance-check: when some children in a family shipped
via the receipt-bookkeeping shortcut, the parent's own acceptance-check
(which cannot itself be shortcut away — its trigger has no parent carve-out)
is the last point before the family goes terminal, and the natural place to
walk whatever criteria were never individually checked, rather than
inheriting the children's `verified` label as a proxy. Flagged as an
observation (`observations.md`) rather than written as a new rule — one
family isn't enough to generalize from, and the standing proposal on the
broader ten-ticket gap already covers the general case.
