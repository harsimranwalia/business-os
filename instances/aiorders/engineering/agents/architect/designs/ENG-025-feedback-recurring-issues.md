---
ticket: ENG-025
project: restaurant-portal
author: architect
created: 2026-08-31
adrs: [ADR-007]
<!-- merge note: local claimed created 2026-08-29 / adrs: [], remote claimed created 2026-08-31 / adrs: [ADR-007] (more recent), kept remote -->
one_way_doors: []
touches_data: false
touches_models: false
---

# Recurring feedback issues, per restaurant, over time — technical design

## Approach

Pure client-side aggregation — no backend or data-model change. Confirmed by
reading the real code rather than trusting the PRD's summary:
`aiorders-api/supabase/functions/brand-portal/feedback.ts`'s `getFeedback`
already does `select('*')` on `restaurant_feedback` with no date filter,
ordered `created_at desc`, so `type`/`sub_type`/`nature` for the restaurant's
entire history are already in the payload; `restaurant-portal/src/services/brandPortalApi.ts`'s
`RestaurantFeedback` interface already carries all three fields; and
`restaurant-portal/src/pages/feedback/Index.tsx` already holds the full list
in `feedbackList` before this ticket. A new presentational component computes
the recurring-issue summary from that already-fetched array via `useMemo` and
renders alongside the existing list — zero new queries, zero new endpoints.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `restaurant-portal/src/pages/feedback/RecurringIssuesSummary.tsx` | new — presentational, `feedback: RestaurantFeedback[]` in, ranked category list or empty-state out | frontend |
| `restaurant-portal/src/pages/feedback/Index.tsx` | modify — render `<RecurringIssuesSummary feedback={feedbackList} />` above the existing list/empty-state block | frontend |

## Interfaces

```ts
interface RecurringIssuesSummaryProps {
  feedback: RestaurantFeedback[];
}

const ACTIONABLE_NATURES = ['complaint', 'negative', 'suggestion', 'bug'];

// category = sub_type, falling back to type when sub_type is null —
// schema allows null even though live data (PRD Evidence) has none today.
function computeRecurringIssues(feedback: RestaurantFeedback[]) {
  const counts = new Map<string, number>();
  for (const f of feedback) {
    if (!ACTIONABLE_NATURES.includes((f.nature ?? '').toLowerCase())) continue;
    const category = f.sub_type ?? f.type;
    counts.set(category, (counts.get(category) ?? 0) + 1);
  }
  return [...counts.entries()]
    .filter(([, count]) => count >= 2)   // ADR-007: "recurring" means >1
    .sort((a, b) => b[1] - a[1]);
}
```

No failure response to define — entirely client-side over data the page
already holds, no new network call to fail. Empty result (zero feedback, or
zero categories reaching the threshold) renders a "Not enough data yet" card,
matching `Index.tsx`'s own existing empty-state visual language (icon +
heading + description inside a `Card`) — satisfies AC3's two named triggers
with one state.

## Alternatives considered

1. **A new backend action** (`get_recurring_issues`, `GROUP BY sub_type,
   nature` in Postgres). Rejected — `get_feedback` already returns every
   field this needs, in the one call the page already makes on mount; a
   second endpoint would add a network round trip and a new access-check
   call site (the exact surface `ENG-022` is already fixing elsewhere in this
   same file) for data already sitting in memory.
2. **Group by `(sub_type, nature)` pair** instead of `sub_type` alone.
   Rejected — AC1 asks for "category," which reads as `sub_type` (the issue
   itself: "Cleanliness," "Order accuracy"); `nature` is the sentiment/
   actionability tag AC4 already uses as the filter, not a second grouping
   axis. Pairing them would fragment one real recurring issue into
   "Cleanliness/complaint" and "Cleanliness/negative" rows instead of one.

## One-way doors

None. One new file, one new render call, zero backend or data surface.
Deleting the component and the render line fully reverts this.

## Risks

- **`sub_type` is typed nullable; live data shows it always populated.** The
  PRD's live-schema check found no null rows, but the interface still allows
  it. Falls back to `type` (non-null on every row) so a null `sub_type` can't
  silently drop a row from the count.
- **Inherits `ENG-022`'s access-check gap, unchanged.** `getFeedback`'s
  `verifyRestaurantAccess` call is the same one `ENG-022` is fixing elsewhere
  in this file. This ticket adds no new backend call, so it neither worsens
  nor depends on that fix landing first — same carry-forward note `ENG-023`'s
  own design already made for this read path.

## Rollout

One repo (`restaurant-portal`), straight, no flag. Branch → PR → gates →
human merge (L1) → Cloudflare deploy. Rollback: revert the merge commit —
nothing else to unwind, no schema or backend change.

## Out of scope

Cross-restaurant comparison (PRD non-goal). Any AI/clustering categorization
(PRD non-goal — the categorization already exists and is already populated).
Alerts on new patterns (PRD non-goal). Any change to `ENG-023`'s status/notes
columns or write path (PRD non-goal — this stays read-only and additive).

## Prior pass (superseded)

An earlier pass (2026-08-29) reached the same core algorithm (group by
`sub_type` falling back to `type`, filter to the same four actionable
natures, count ≥ 2 threshold, sort descending) but packaged it differently
and with additional reasoning worth keeping:

- **Put the aggregation inline in `Index.tsx`** as a new exported pure
  function `groupRecurringIssues(feedback)`, called via `useMemo`, rather
  than extracting a separate `RecurringIssuesSummary.tsx` component. It
  explicitly considered and rejected the separate-file shape the newer pass
  uses: "`feedback/` has exactly one file today, and that file already keeps
  its own display-logic helpers... local rather than extracted. A new file
  for one more function of the same kind breaks this file's own convention
  for a size-S ticket." `export` alone was judged sufficient to make the
  function unit-testable without a render.
- **Named the count ≥ 2 threshold as its own explicit architect judgment
  call**, with a specific fallout worth preserving: because a restaurant
  with 0 or 1 total feedback items can never produce a count-≥-2 group, AC1
  ("a restaurant with more than one feedback item") needs no special-casing
  — it lands on the AC3 empty state for free.
- **Justified the all-time (unwindowed) aggregation** with a concrete data
  point not repeated in the newer pass: the largest single `sub_type`/
  `nature` combination is 640 rows platform-wide across every restaurant
  combined, so a single restaurant's own history is smaller still — inventing
  a rolling window (e.g. 90 days) would need a new date-filtered query the
  PRD's own Risks section already flagged as unconfirmed and unnecessary at
  current volumes.
- **Spelled out a concrete Vitest test plan** for the aggregation function:
  empty list → `[]`; all-compliments → `[]`; two "Cleanliness" complaints
  plus one "Wait time" complaint → `[{category: "Cleanliness", count: 2}]`;
  natures in mixed case still match — narrower and cheaper than a
  render-and-mock test, since the aggregation logic is what needs a
  correctness proof, not the render tree.
