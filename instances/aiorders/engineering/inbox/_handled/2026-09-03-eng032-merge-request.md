---
type: eng-decision
agent: eng-manager
gate: merge
project: restaurant-portal
ticket: ENG-032
recommendation: merge — code review (round 2), quality, and security all passed; no migration (pure UI/render change plus an existing-jsonb-column save-path fix, no schema or data change); read-only additive feature (two new stage strings, an itemized-selections render block, an owner-side switch defaulted off), single repo, no cross-ticket branch dependency (ENG-033 depends on this shipping, not the reverse)
time_estimate: ~1 day
pr_url: https://github.com/harsimranwalia/restaurant-portal/pull/2
raised: 2026-09-03
notified: 2026-09-04T04:27:45
decision:
---

# Merge request — Catering board: two new stages, itemized owner view, order-form enable switch (ENG-032)

## What this does

The catering board now knows about the two new outcomes Piece 1 introduces
(`Quote Generated`, `Contact Requested`) — appended immediately after `New
Enquiry` across all nine files that hold a hardcoded copy of the stage list.
An existing request in any of the five current stages is unaffected and
stays visible (AC-8).

The owner's detail modal (`CateringDetailModal`) gains a read-only
itemized-selections block — one line per selection (quantity, name, note),
grouped by category, the raw stored `name` rendered as-is (AC-12, narrowed to
this ticket's own `restaurant-portal` slice per the design).

The owner-side catering editor gains an `orderFormEnabled` switch (default
off, ADR-009) and a per-fulfillment-option copy editor (`fulfillmentCopy`),
and fixes a real, live bug in the same save path: it now spreads `...content`
before its normalised fields, so keys outside the known field list survive a
save instead of being silently dropped the next time the owner saves any
other catering-page edit.

Out of scope: no pricing (Piece 2), no Edit Quote/resend (Piece 3), the
duplicated status literals and `CateringRequest` redeclarations stay
duplicated (PRD's own non-goal, overlaps `ENG-013`).

## Gates passed

- Code review: **pass**, round 2 — `agents/principal-engineer/reviews/ENG-032.md` (round 1's sole finding, a missing regression test on the save-path fix, closed with a mutation-verified test)
- Quality: **pass** — `agents/qa/test-plans/ENG-032.md` (AC-8 and AC-12 each covered by a dedicated, mutation-verified test; 4/4 tests green)
- Security: **pass** — `agents/security/reviews/ENG-032.md` (no new route/query/write path; the itemized block renders an already-fetched, already-authorized prop; one non-blocking finding routed to `proposals.md`, not held against this ticket)
- Migration: n/a — no schema or data change

## PR

https://github.com/harsimranwalia/restaurant-portal/pull/2

`restaurant-portal` is registered **L1** — this department opens the PR, a
human merges. Merge whenever suits you on GitHub directly; the next
build-loop pass detects the merge itself (local git ancestry check, no action
needed from you beyond the merge) and advances the ticket to `shipped`.

## Decision

Filled in by the approver.
