---
type: eng-decision
agent: eng-manager
gate: merge
project: restaurant-marketplace
ticket: ENG-047
recommendation: merge — code review, quality, and security all passed (security: zero findings); no migration owed (frontend-only); last sub-ticket of the ENG-026 family, closes AC4's UI half (chip + status render). Safe to merge before or after ENG-045 — additive only, no runtime break either order.
time_estimate: a few hours to half a day
pr_url: https://github.com/harsimranwalia/restaurant-marketplace/pull/1
raised: 2026-09-07
notified: 2026-09-07T13:16:15
nudged:
decision: merged
---

# Merge request — FoodSwipe Open Now filter and channel display, consumer marketplace (ENG-047)

Sub-ticket of `ENG-026` (FoodSwipe channel-visibility toggles and
capability-based discovery), sequence 4 of 4, last of the family — depended
on `ENG-045` alone (PR #20 open on `aiorders-api`, not yet merged).

## What this does

- New "Open Now" filter chip on all three channel tabs (Order Food / Dine
  In / Catering), default off — unlike the existing Offers/Rating 4+ chips,
  which only show on two of the three, since Catering restaurants close
  too.
- Threads `openNow` through to the `open_now` query param (snake_case on
  the wire, confirmed to match `ENG-045`'s shipped handler exactly).
- Renders a closed-restaurant `status` label in the existing card meta row
  when the backend provides one — no client-side hours logic, pure render
  of what `ENG-045`'s handler computes (`ADR-010`).
- `openNow` deliberately survives a tab switch (standing intent, per
  design) but resets on "Clear All", same as its siblings.

## Gates passed

- **Code review: pass, round 1** — `agents/principal-engineer/reviews/ENG-047.md`.
  0/10 automatic failures; wire contract independently confirmed against
  `ENG-045`'s shipped code.
- **Quality: pass** — `agents/qa/test-plans/ENG-047.md`. Owns AC4's UI half
  only, covered by inspection; no suite exists for `restaurant-marketplace`
  (proposal filed this date).
- **Security: pass, zero findings** — `agents/security/reviews/ENG-047.md`.
  No new route, no new dependency, no secret, no PII beyond an
  already-intended business-status label.
- No migration owed — confirmed no `ENG-047-*.md` migration file exists.

## Release readiness

- **Rollback:** no migration, no stored-state change — reverting the merge
  (once merged) fully undoes this diff.
- **Observability:** rides `useRestaurants.tsx`'s existing generic
  try/catch + error-state path, unchanged by this diff.
- **Cost:** $0/month — no new dependency, no new infrastructure.
- **Window:** n/a — `restaurant-marketplace` is registered L1; opening a PR
  is not a release. `deploy-cf.yml` triggers on push to `master` only (no
  `pull_request` trigger) — opening this PR carries no auto-deploy risk.

## PR

https://github.com/harsimranwalia/restaurant-marketplace/pull/1

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Out of scope

- `ENG-045`'s own filtering/status-computation logic (parked on you, PR
  #20, `aiorders-api`).
- `ENG-046`'s own admin-hub toggle UI (parked on you, PR #10,
  `aiorders-admin-hub`).
- The broken `.eslintrc.cjs` and missing `package-lock.json` on this repo
  (already an open proposal, not this diff's to fix).

Last of `ENG-026`'s four sub-tickets — with this PR open, every child is
now off the machine's own queue and the parent is eligible to close out via
its own `ADR-003`-class exemption once all four are settled.
