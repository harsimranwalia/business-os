---
ticket: ENG-025
project: restaurant-portal
status: approved
size: S
author: product-manager
created: 2026-08-29
decided: 2026-08-29T22:22:18.827452+00:00
---

# Recurring feedback issues, per restaurant, over time

## Readback

Not a fresh raw request — this ticket is the direct, previously-flagged
resolution of a non-blocking question raised alongside `ENG-023`
(`inbox/2026-08-29-eng023-frequency-question.md`), not a new ambiguous
input needing its own two-reading readback. The ambiguity that question
existed to resolve has already been resolved by the approver's own answer;
re-running the readback skill here would be re-litigating a closed
question, not detecting a new one.

**You said (on the original `ENG-023` request):** "...is this frequent what
are the bottomline issue that need to be resolved by the restaurant
location."

**The standing question asked:** whether this also wants the system itself
to compute recurrence (Reading B — counts of similar feedback, or a
called-out "these are your bottom-line issues" list) versus leaving it to a
human reading back through notes over time (Reading A).

**You answered:** "reading b, frequent is same restaurant over time" —
Reading B confirmed, explicitly scoped to one restaurant's own history, not
cross-restaurant patterns (the other candidate scoping the standing
question named).

## Problem

A restaurant using the brand portal's Feedback page has no way to see which
kinds of issues keep coming up for their own location — only a flat,
reverse-chronological list of individual items. Spotting a recurring
problem (e.g. repeated online-ordering complaints, or repeated cleanliness
complaints) today requires a human to read the whole list and notice the
pattern themselves.

## Why now

Directly answers a question the approver asked in their own words on the
original `ENG-023` request ("is this frequent"), now that they've confirmed
which reading they meant. Small and well-precedented once scoped — see
Evidence below for why this doesn't need new categorization work.

## Users

Restaurant owners/managers viewing their own Feedback page on the brand
portal (`restaurant-portal`).

## Proposed change

On the Feedback page, a restaurant can see a summary of which issue
categories recur most often for their own restaurant, across their
feedback history — separate from, and in addition to, the existing
flat list of individual items (which `ENG-023` is separately adding
status/notes to).

## Acceptance criteria

1. `[confirmed]` Given a restaurant with more than one feedback item, when
   they view the Feedback page, then they see a summary of recurring issues
   — feedback grouped by category and ranked by how often it recurs — for
   their own restaurant only.
2. `[confirmed]` The summary reflects that restaurant's own history over
   time, not a single-day or single-session snapshot — and never includes
   another restaurant's data, enforced server-side the same way
   `get_feedback` already scopes by `restaurant_id`.
3. `[inferred]` The grouping uses the feedback's existing `sub_type` /
   `nature` fields (see Evidence) rather than inventing a new taxonomy or
   re-reading free text — a restaurant with zero feedback, or feedback with
   no clear recurring pattern, sees a plain "not enough data yet" state
   rather than an empty or broken panel.
4. `[proposed]` Only actionable natures (`complaint`, `negative`,
   `suggestion`, `bug`) are surfaced as "issues" to recur — compliments
   aren't framed as a problem to resolve, even though the same grouping
   mechanically applies to them too.

## Non-goals

- Cross-restaurant comparison, benchmarking, or platform-wide trend
  analysis — the approver's own answer explicitly scoped this to one
  restaurant's own history, ruling out the standing question's other
  candidate reading.
- Any new free-text categorization, clustering, or AI/model-based analysis
  of feedback content — see Evidence: the categorization this needs already
  exists and is already populated.
- Automatic alerts or notifications when a new pattern emerges (a
  plausible future follow-on, not asked for here).
- Any change to `ENG-023`'s status/notes fields or write path — additive,
  read-only summary alongside it.

## Risks and unknowns

- **Windowing is a design-time call, not a PM one.** "Over time" could mean
  all-time, a rolling window (e.g. 90 days), or both — left to the
  architect at `designed`; acceptance criterion 2 only requires that it not
  be a single-snapshot read.
- Feedback volume per restaurant is currently low (platform-wide, the
  largest single `sub_type`/`nature` combination is 640 rows — see
  Evidence) — a naive in-memory grouping over an already-fetched list is
  plausible and would need no new backend endpoint or index, but that's the
  architect's call to confirm, not assumed here as final.

## Cost

- **Build:** Sized `S` — one clear surface (the existing Feedback page and
  its already-fetched data), no new interface, no new data model. Rough
  band: a few hours to half a day, same order of magnitude as `ENG-023` on
  the same page. Narrower than `size: M` was scoped at the standing
  question's own time of writing, now that Evidence below shows the
  categorization it needs already exists — it does not need the
  "AI-assisted categorization" the original question flagged as likely.
- **Run:** $0/month — no new dependency, no model calls, reuses the existing
  free-tier data path.

## Evidence checked, not assumed

Read live before sizing this, not inferred from the request text:

- **`restaurant_feedback`'s live schema** (Supabase project
  `bmnmnejwdxbcqinqkwko`, read-only `execute_sql` via the MCP path this
  instance's `ENG-011` pass already validated as safe — see
  `observations.md`): confirmed columns `type`, `sub_type`, `nature` are
  real, populated, structured fields — not free text needing new
  categorization. A live `GROUP BY sub_type, nature` returned 30 distinct,
  meaningful combinations (`sub_type` values include "Online ordering",
  "Food", "Service", "Staff attitude", "Cleanliness", "Order accuracy",
  "Portion size", "Delivery experience", "Wait time"; `nature` values
  include positive/negative/neutral/compliment/complaint/suggestion/bug/
  other), with real counts (largest: 640 rows). This directly overturns the
  standing question's own speculation that this "likely means AI-assisted
  categorization" — the categorization already happened at submission time,
  for every row.
- **Feedback page** (`restaurant-portal/src/pages/feedback/Index.tsx`):
  confirmed it renders a flat list plus exactly two aggregate stats (total
  count, average rating) — no per-category breakdown exists today. It
  already fetches the restaurant's **entire** feedback history in one call
  (no date filter), so "over time" in acceptance criterion 2 is already
  available in data the page already has.
- **Backend handler** (`aiorders-api/supabase/functions/brand-portal/feedback.ts`):
  confirmed exactly one action (`get_feedback`), returning the raw list.
  **Must not repeat `ENG-022`'s bug** if a new backend action is added here
  — that ticket found `verifyRestaurantAccess()` silently defeated in this
  same directory by checking a returned object's truthiness instead of its
  `.hasAccess` field. Model any new call on `catering.ts`'s confirmed-correct
  `update_catering_request`, per the same flag `ENG-023`'s own ticket
  already carries for its neighboring write path.

## Decision

Filled in after G1.

- **The approver's answer:** approved / rejected / changed to {…}
- **Date:**
- **Notes:**
