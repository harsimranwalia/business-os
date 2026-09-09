# Acceptance — ENG-027 (Loyalty points ledger, balances, and earn API — parent)

## Why this ran in full despite the ADR-003 exemption

`ENG-027` owes no receipts of its own — its evidence is its children's
(`ADR-003`; both `ENG-048` and `ENG-049` are `verified`, satisfying the
exemption). The `acceptance-check/SKILL.md` trigger has no parent carve-out,
same precedent `ENG-016`'s and `ENG-021`'s own closing checks already set —
this is a rollup and a fresh no-drift confirmation across the whole family,
not a gap-fill.

## Both children re-checked fresh off their own frontmatter

`ENG-048` and `ENG-049`: both `state: verified`, both `parent: ENG-027`,
neither `dropped`. Both actually shipped (well past the ADR-003 "at least
one" floor). `building → shipped`, no diff, review, QA, or security hop of
its own.

## Re-fetched the repo fresh rather than trusting either child's own notebook date

`aiorders-api` `origin/main` → `2e5333a8` (this pass, via the isolated
`_eng/aiorders-api` worktree). Both children's own acceptance notebooks
(`2026-09-08-eng048-acceptance.md`, `2026-09-08-eng049-acceptance.md`) were
themselves written against this same commit, checked this same pass — zero
drift between when each was walked and now.

## Walk all 18 PRD criteria — the full list, not just each child's owned subset

Both children already ran `acceptance-check` in full at their own shipping
point (neither took the `ENG-031`/`ENG-037`-style receipt-bookkeeping
shortcut). This is a rollup: every criterion cross-referenced from whichever
child's own notebook walked it, confirming no criterion is left with only
half its proof.

| AC | Owner(s) | Result |
|---|---|---|
| 1 (online fulfilled → credit) | `ENG-048` (guard/crediting) + `ENG-049` (webhook caller) | Pass — both halves walked in each ticket's own half-owned table |
| 2 (online cancelled → never credited) | `ENG-048` (guard: `status is distinct from 'cancelled'`) + `ENG-049` (sets `status='cancelled'` unconditionally) | Pass |
| 3 (sweep credits after window elapses) | `ENG-048` (`window_elapsed` reason handling) + `ENG-049` (sweep caller, `selectEligibleOrders`, 5/5 tests) | Pass |
| 4 (already-credited order, window elapses → no double credit) | `ENG-048`, owned in full | Pass |
| 5 (any sequence → credited at most once, ever) | `ENG-048`, owned in full | Pass |
| 6 (dine-in credits at dine-in rate) | `ENG-049`, owned in full | Pass |
| 7 (entry records full detail) | `ENG-048` (schema) + `ENG-049` (populates via `record_dine_in_earn`/crediting function) | Pass |
| 8 (rate = placement-time, not credit-time) | `ENG-048`, owned in full | Pass |
| 9 (later rate change doesn't alter written entry) | `ENG-048`, owned in full | Pass |
| 10 (balance = sum at that restaurant only) | `ENG-049`, owned in full — includes the caught-and-fixed 500-row cap regression | Pass |
| 11 (not enrolled → no credit, dine-in caller told why) | `ENG-048` (`skipped_not_enrolled`) + `ENG-049` (surfaces the reason) | Pass |
| 12 (no platform identity → no credit, no entry, order unaffected) | `ENG-048`, owned in full | Pass |
| 13 (loyalty failure never blocks webhook's own success) | `ENG-049`, owned in full | Pass |
| 14 (unknown order → accepted and ignored) | `ENG-049`, owned in full | Pass |
| 15 (sweep isolates one order's failure) | `ENG-048` (per-row processed marking) + `ENG-049` (catch-and-continue loop, isolation tests) | Pass |
| 16 (cancellation never deletes/rewrites a ledger row) | `ENG-048` (append-only schema, no update/delete path) + `ENG-049` (cancellation handler never touches the table, asserted) | Pass |
| 17 (no restaurant access → rejected, no entry) | `ENG-049`, owned in full | Pass |
| 18 (invalid amount → rejected, clear reason) | `ENG-049`, owned in full, 7/7 values | Pass |

**All 18: pass.** None left with an unproven half.

## Check the non-goals — whole-family sweep, not per-child

PRD's own assumptions section (`## Readback`) names what changes the build
if wrong, not a formal non-goals list, but states plainly: no backfill of
`cw_order_id`/`loyalty_processed_at` for pre-existing orders; ledger entries
never edited or deleted (correction is ticket 5's surface, not this one's);
balances never move between restaurants. Confirmed on the live migration and
both children's diffs: no backfill statement anywhere; no `update`/`delete`
against `loyalty_ledger_entries` in either ticket's diff; every balance read
filters by both `platform_customer_id` and `restaurant_id`. No scope creep
found — nothing resembling redemption, QR issuance, or an admin/support
surface (items 4 and 5 of the sequence) appears in either child's diff.

## Check the cost

PRD: no explicit `## Cost` section (unusual for this board — this PRD is a
rescope of an already-approved item, not a fresh one), but the "Assumed"
section and both children's own release-readiness hops independently landed
on `$0/month` (existing Supabase project, existing `pg_cron`/`pg_net`/Vault,
existing Edge Functions compute). Confirmed independently on both children's
own release records. Matches.

## Route

**All 18 criteria pass**, verified directly, cross-referenced from both
children's own fresh full walks rather than re-derived from scratch.
`shipped → verified`.

## Step 6b — continue an approved sequence?

**Condition met, unlike `ENG-016`'s and `ENG-021`'s own closing checks.**
This ticket's own `## Readback` names the sequence explicitly (`ENG-006`'s
`## Feature shape and sequencing`) and its own G1 history shows the standing
authorization to file incrementally: `ENG-006`'s G1 (2026-08-28) — "the
proposed five-ticket sequence stands as shape to file incrementally, not as
four pre-approved tickets" — and the answer that specifically named this
ticket (`inbox/2026-08-30-eng007-continue-sequence-question.md`, 2026-09-01,
"file ticket 3, same process as `ENG-007`"). `ENG-027` is item 3; item 4
("Redemption API and QR issuance/scanning... Depends on ENG-006 and (3)") is
now dependency-clear (`ENG-006` verified long since; `ENG-027` verified this
pass).

**Filed the stub (`ENG-051`), same pass, per step 1b only — not the full
PRD.** `chained: ENG-051` fired. Full reasoning for stopping at the stub,
including why it is not a model-tier deferral: `ENG-051`'s own board-file
log and `board/_index.md`'s `Next ID` note, same pass.

## Also worth recording

Both children's release records flag one still-open, non-blocking follow-up
each (the `loyalty-auto-complete-tick` cron's first live fire, expected
`18:30:00Z`, not directly observed as of this pass) — carried forward, not
re-litigated here; neither touches any of the 18 criteria this check owns.
