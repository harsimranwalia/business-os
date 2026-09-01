---
id: ADR-007
title: Recurring feedback summary uses an all-time window and a >1 threshold for "recurring"
project: restaurant-portal
ticket: ENG-025
status: accepted
decided_by: architect
date: 2026-08-31
supersedes:
superseded_by:
---

# ADR-007: Recurring feedback summary uses an all-time window and a >1 threshold for "recurring"

## Context

The PRD (`ENG-025`) explicitly left two calls to design time rather than
deciding them itself: whether "over time" (AC2) means all-time or a rolling
window, and — since AC1 asks for issues "ranked by frequency" without saying
how many occurrences make something "recurring" — what to do with a category
that appears only once. Both need an answer before the component in
`agents/architect/designs/ENG-025-feedback-recurring-issues.md` can be
written, and both are exactly the kind of thing a future engineer reading
that design would ask "why on earth" about if left silent.

## Decision

**Window: all-time, no rolling cutoff.** `get_feedback` already fetches the
restaurant's entire history with no date filter (confirmed in
`aiorders-api/supabase/functions/brand-portal/feedback.ts`), and per-restaurant
volume is low today (PRD Evidence: platform-wide largest `sub_type`/`nature`
combination is 640 rows, across all restaurants combined). A rolling window
would need either a new query parameter or a client-side date cutoff for no
present benefit, and AC2 only requires "not a single-day/session snapshot" —
all-time satisfies that with the data already on the page.

**Threshold: a category must appear at least twice to count as "recurring."**
A count of one is, definitionally, not a recurrence — showing it as a ranked
"issue" would present every distinct complaint a restaurant has ever received
as a pattern. The threshold is also what makes AC3's "no clear recurring
pattern" empty-state state reachable at all: without it, any restaurant with
even one piece of actionable feedback would always show a (misleading)
one-item summary instead of "not enough data yet."

## Alternatives

| Option | Why not |
|---|---|
| Rolling window (e.g. last 90 days) | No stated need (AC2 only rules out single-snapshot), and it would require either a new backend query parameter or discarding rows the page already fetched for free — added complexity with no acceptance criterion asking for it. |
| No threshold — show every category, including count-of-one | Fails to distinguish an actual recurring pattern from a single incident, which is the entire premise of AC1 ("recurring") and leaves AC3's empty-state condition ("no clear recurring pattern") unreachable in practice. |
| Threshold higher than 2 (e.g. 3+) | No evidence for where a meaningful pattern starts at this restaurant's current, low feedback volumes (PRD Evidence) — a higher bar would likely show "not enough data yet" for every restaurant on the platform today, defeating the feature at launch. |

## Consequences

**Accepted:** a restaurant with exactly two same-category actionable items
sees that category as "recurring" — a low bar, deliberately, given today's
volumes.

**Gained:** AC3's empty-state is reachable and meaningful (it will actually
render for low-volume restaurants at launch, rather than being dead code), and
the summary never overstates a single incident as a pattern.

**Reversibility:** both the window and the threshold are one constant each,
entirely client-side, in `computeRecurringIssues`. Changing either is a
one-line code change with no data migration and no backend deploy — not a
one-way door, decided and logged rather than escalated per the same precedent
`ADR-005`/`ADR-006` set.

## Review trigger

If per-restaurant feedback volume grows enough that a count-of-2 category
becomes routine noise rather than a signal, revisit the threshold — and if a
restaurant ever asks to see trend-over-a-specific-period rather than all-time,
revisit the window using the same live-schema check this ticket's PRD already
ran.
