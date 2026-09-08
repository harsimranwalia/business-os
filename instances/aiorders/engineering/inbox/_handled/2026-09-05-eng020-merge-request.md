---
type: eng-decision
agent: eng-manager
gate: merge
project: restaurant-portal
ticket: ENG-020
time_estimate: a day and a half to two days
recommendation: merge — code review (3 rounds, pass), quality (3 rounds, pass, all 5 acceptance criteria), security (round 1, pass, access control mutation-verified), and migration (pass, rollback tested against a disposable replica) all passed on both repos; additive-only (no existing behaviour touched, no new dependency, no schema removal); one non-blocking security finding and a few known, by-design limitations named below, none blocking
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/17
  - repo: restaurant-portal
    url: https://github.com/harsimranwalia/restaurant-portal/pull/4
raised: 2026-09-05
notified: 2026-09-05T13:40:18
nudged:
decision:
---

# Merge request — Marketing ROI reporting, acquisition-channel breakdown (ENG-020)

Two-repo ticket, both PRs opened this pass.

## What this does

A restaurant owner can now see, on their own brand portal ("Customer
Sources" in the nav, `/acquisition`), their own customers/orders/revenue
broken down by acquisition channel (organic, direct, social, referral, paid,
QR/in-store, etc.) over a selectable time range — framed honestly rather than
as a number that claims to isolate AI SEO's effect alone.

- `aiorders-api`: new `brand-portal` action `get_acquisition_report`, a new
  read-only `get_acquisition_breakdown` SQL function (migration, additive
  only), and channel classification in TypeScript.
- `restaurant-portal`: new acquisition report page, channel-breakdown table +
  chart, selectable date range, nav entry.

## Gates passed

- **Code review: pass, round 3** (three consecutive passing rounds) —
  `agents/principal-engineer/reviews/ENG-020.md`. 0/10 automatic failures;
  access control and the two new test assertions both mutation-verified, not
  read-and-trusted.
- **Quality: pass, round 3** — `agents/qa/test-plans/ENG-020.md`. All 5
  acceptance criteria (AC1–AC5) pass.
- **Security: pass, round 1** — `agents/security/reviews/ENG-020.md`. OWASP
  A01–A10 walked; no secrets; no new dependency; the one attacker-reachable
  text (an unrecognised UTM source) is stored-but-inert, not stored XSS.
- **Migration: pass** —
  `agents/database/migrations/ENG-020-marketing-roi-attribution-reporting.md`.
  Verified against a disposable Postgres replica, which caught and fixed a
  real `FULL JOIN` bug before it ever reached a PR. Rollback (`DROP FUNCTION`)
  actually run against the same replica, not just asserted.

## PRs

- `aiorders-api` (backend action + RPC): https://github.com/harsimranwalia/aiorders-api/pull/17
- `restaurant-portal` (report page): https://github.com/harsimranwalia/restaurant-portal/pull/4

Both projects are registered **L1** — this department opens the PR, a human
merges. The design's recommended order is `aiorders-api` first, then
`restaurant-portal`, but either order is safe: if the portal ships first, it
renders an explicit "Acquisition report is not available yet" state (tested),
not a blank or a crash. The next build-loop pass detects each merge itself
(local git ancestry check, no reply needed from you) and advances the ticket
once both are in.

## Named gaps and known limitations, carried forward rather than hidden

- **Restaurant-existence oracle** (security, non-blocking) — the shared
  `verifyRestaurantAccess` helper (unchanged, used by every other
  `brand-portal` handler) lets a caller distinguish "that restaurant doesn't
  exist" from "that restaurant isn't yours." Pre-existing, not introduced or
  worsened here; low exploit value (a restaurant UUID isn't a credential).
- **Cross-domain attribution coverage varies per restaurant** — the
  online-ordering-side tracking install is manual per deployment, not
  guaranteed live everywhere. This is exactly why the report always shows a
  `coverage` percentage and a `direct_unknown` bucket rather than hiding the
  gap — by design, not an oversight.
- **No historical baseline** — the report is range-scoped only; no all-time
  total or trend line that would read as a causal claim.
- **`analytics/index.ts` has no access check** (unauthenticated cross-tenant
  data exposure) — found as a byproduct of this ticket's design work, already
  **filed and resolved separately as `ENG-030`**. Not touched by this diff.
- Deliberately out of scope (named in the design, not silently dropped):
  Microsoft Clarity integration, a true ROI ratio isolating AI-SEO from
  organic traffic, a staff-facing all-restaurants rollup, the
  `user_tracking` cookie-scope mismatch between the standalone and React
  tracking implementations, and a consent gate for first-party tracking
  cookies (PIPEDA / Quebec Law 25) — the last two are capture-side and need a
  legal answer this department doesn't have.

## Decision

No written reply — both PRs merged directly on GitHub instead, together, 94
seconds apart (`aiorders-api` PR #17 `672dfa77` at `2026-09-06T00:41:23Z`,
`restaurant-portal` PR #4 `8eea8f15` at `00:42:57Z`), same standing pattern
this approver has used for every prior L1 merge on this board. Found by this
`scheduled` event pass's own step-5 re-check. All four gate receipts
re-read fresh and confirmed `pass`; a full acceptance-check (all 5 owned
criteria) run against the merged, now-live tree — see the ticket's own
board-file log and
`agents/devops/releases/2026-09-05-ENG-020-aiorders-api-and-restaurant-portal.md`.
Carried `blocked → shipped → verified` this pass. `blocks: []` — nothing
else unblocked.
