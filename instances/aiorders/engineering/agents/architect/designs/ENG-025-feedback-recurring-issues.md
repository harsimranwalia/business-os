---
ticket: ENG-025
project: restaurant-portal
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: false
touches_models: false
---

# Recurring feedback issues, per restaurant, over time — technical design

## Approach

Pure frontend aggregation over the feedback list the page already fetches —
no new backend action, no new endpoint, no schema change. `Index.tsx` gains
one new pure function and one new UI section rendered above the existing
flat list.

`restaurant_feedback` rows already carry populated, structured `type`,
`sub_type`, and `nature` columns (confirmed live, per the PRD's Evidence),
and the page's existing `get_feedback` call already returns a restaurant's
**entire** history in one round trip (`brandPortalApi.getFeedback`, no date
filter, no pagination). Both facts together mean acceptance criteria 1–3 are
answerable entirely from data already in the browser: group by category
(`sub_type`, falling back to `type` for the rare row with no `sub_type`),
restrict to actionable natures (AC4: `complaint`, `negative`, `suggestion`,
`bug`, case-insensitive — same four values, same `.toLowerCase()` casing
convention `getNatureColor`/`getTypeColor` already use in this file), count,
keep only categories with count ≥ 2, sort descending.

The count-≥-2 threshold is this design's own call (the PRD leaves "over
time" windowing and volume assumptions to the architect; the same paragraph
that does so implies a threshold decision belongs here too, since AC3
requires a "no clear recurring pattern" empty state to exist at all — a
single occurrence isn't a pattern to have detected). One useful fallout: AC1
("a restaurant with more than one feedback item") needs no special-casing —
a restaurant with 0 or 1 total feedback items can never produce a count-≥-2
group, so it lands on the AC3 empty state for free.

Zero backend risk: `get_feedback`'s existing access-check defect (confirmed
live during design — the call passes arguments in the wrong order and checks
the returned object's truthiness instead of `.hasAccess`, the same bug class
`ENG-022` is already scoped to fix across 5 handlers) is untouched by this
design. Nothing here changes what data reaches the browser, only how the
already-arrived, already-scoped rows are displayed — so this ticket neither
depends on `ENG-022` landing first nor risks colliding with its diff.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `src/pages/feedback/Index.tsx` (`restaurant-portal`) | modify — add an exported pure function `groupRecurringIssues(feedback)` plus a new "Recurring Issues" `Card` section, rendered above the existing feedback list | frontend |

One file. No backend, no migration, no new page, no new route.

## Data

No new table, column, or migration. Reuses fields already present in the
`RestaurantFeedback` type the existing `get_feedback` action already returns
(`src/services/brandPortalApi.ts`): `type` (non-null), `sub_type` (nullable),
`nature` (nullable).

```ts
function groupRecurringIssues(
  feedback: RestaurantFeedback[],
): { category: string; count: number }[] {
  const ACTIONABLE_NATURES = new Set(['complaint', 'negative', 'suggestion', 'bug']);
  const counts = new Map<string, number>();

  for (const item of feedback) {
    const nature = item.nature?.toLowerCase();
    if (!nature || !ACTIONABLE_NATURES.has(nature)) continue;
    const category = item.sub_type || item.type;
    counts.set(category, (counts.get(category) ?? 0) + 1);
  }

  return [...counts.entries()]
    .filter(([, count]) => count >= 2)
    .map(([category, count]) => ({ category, count }))
    .sort((a, b) => b.count - a.count);
}
```

Windowing: all-time, matching what the page already fetches. AC2 only
requires the summary not be a single-snapshot read — it doesn't ask for a
rolling window, and inventing one (e.g. 90 days) would need a new
date-filtered query the PRD's own Risks section already flags as unconfirmed
and unnecessary at current volumes (largest single `sub_type`/`nature`
combination is 640 rows **platform-wide**, across every restaurant
combined — a single restaurant's own history is smaller still).

## Interfaces

No API change. `groupRecurringIssues` is a new pure, exported function local
to `Index.tsx` — `(feedback: RestaurantFeedback[]) => { category: string;
count: number }[]` — called from a `useMemo(() => groupRecurringIssues(feedbackList), [feedbackList])`
inside the existing component. Exported (not module-private) specifically so
a test file can import and assert on it without rendering the page or
mocking Supabase.

UI: a new `Card` titled "Recurring Issues," rendered between the existing
header/stats block and the flat list. Empty state (zero groups after
filtering): a plain "Not enough data yet" message, matching AC3, styled
consistently with the existing empty-state `Card` this file already renders
when `feedbackList.length === 0` (same icon/copy pattern, not a new one).
Non-empty state: one row per category, category label plus count, sorted
descending — no new component library, reuses `Card`/`CardContent`/
`CardHeader`/`CardTitle`/`Badge`, all already imported in this file.

## Alternatives considered

1. **New backend action** (e.g. `get_recurring_feedback`) doing the
   `GROUP BY` in Postgres. Rejected: the PRD's own Risks section flags this
   as unconfirmed-necessary, and design-time evidence confirms it's
   unnecessary — the page already fetches the complete history in one call,
   and a new action would duplicate a round trip for data already in hand
   while adding a second call site that has to get `feedback.ts`'s access
   check right (see Approach — the existing one doesn't). Revisit only if
   per-restaurant feedback volume grows enough that shipping full history to
   the browser becomes the actual bottleneck; not evidenced today.
2. **Separate helper module** for `groupRecurringIssues` (e.g.
   `pages/feedback/recurringIssues.ts`). Rejected: `feedback/` has exactly
   one file today, and that file already keeps its own display-logic
   helpers (`getRatingStars`, `getNatureColor`, `getTypeColor`,
   `getAverageRating`) local rather than extracted. A new file for one more
   function of the same kind breaks this file's own convention for a
   size-S ticket; `export` alone is enough to make it testable in isolation.
3. **No minimum-count threshold** — show every category regardless of count,
   ranked by frequency. Rejected: AC3's "no clear recurring pattern" empty
   state implies some feedback sets shouldn't show a recurring-issues panel
   at all. Showing every singleton category "ranked by frequency of 1" isn't
   a recurring-issues summary, it's the existing list re-grouped with extra
   steps.
4. **Include all natures**, not just the four AC4 names. Rejected — AC4 is
   explicit and gives the reason (compliments aren't a problem to resolve);
   the mechanism (grouping) does apply to them unchanged, only the nature
   filter set would need to change, which is exactly what AC4 pins down.

## One-way doors

None. Purely additive UI over already-fetched, already-scoped data — fully
reversible by deleting the new function and the new `Card` section. No new
datastore, endpoint, dependency, or public contract.

## Risks

- **Threshold (count ≥ 2) is this design's own call, not literal PRD text**
  — named explicitly here (Approach, Alternatives) rather than assumed
  silently, since the PRD left it open.
- **Inherits `get_feedback`'s existing access-check defect unchanged** (see
  Approach, and `ENG-022`). This ticket neither fixes nor worsens it — no
  ordering dependency either way, since `ENG-022`'s fix lands inside
  `feedback.ts` (backend) and this design touches only `Index.tsx`
  (frontend); the two diffs don't overlap.
- **`sub_type` is displayed as-is, no normalization.** Live data is
  consistently Title Case today ("Online ordering", "Cleanliness," etc.),
  but the column isn't schema-enforced (free-ish text set at submission
  time), so a future differently-cased value would count as a separate
  category rather than merging with an existing one. Not a new risk this
  design introduces — the existing flat list already renders `sub_type`
  as-is with no normalization (`Index.tsx`, current `Badge` rendering).

## Rollout

Straight, no flag. Branch → PR → gates → human merge (`restaurant-portal` is
L1). `npm run lint` + `npm run build` (registered commands) plus
`npm run test` (Vitest, `ENG-002`'s harness) — `groupRecurringIssues` is
exported specifically so a new `src/pages/feedback/Index.test.tsx` can unit
test the grouping/filtering/threshold logic directly (empty list →
`[]`; all-compliments → `[]`; two "Cleanliness" complaints plus one
"Wait time" complaint → `[{category: "Cleanliness", count: 2}]`; natures in
mixed case still match) without rendering the full page or mocking
Supabase — a narrower, cheaper test than `App.test.tsx`'s render-and-mock
approach, appropriate because the thing that actually needs correctness
proof here is the aggregation logic, not the render tree.

Rollback: revert the one commit. No data migrated, nothing to clean up.

## Out of scope

- Cross-restaurant comparison or platform-wide trend analysis (PRD
  non-goal).
- Any AI/model-based categorization or free-text clustering (PRD non-goal;
  not needed — the data is already categorized).
- Alerts or notifications when a new pattern emerges (PRD non-goal).
- `ENG-023`'s status/notes fields and write path (separate ticket, same
  page, additive alongside — no shared code path).
- Fixing `get_feedback`'s access-check defect (`ENG-022`'s scope; see
  Risks).
