---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-006
recommendation: merge — code review, quality, security, and migration all passed; additive migration plus one new edge function with no live caller anywhere, so merging and deploying has zero production behavioral effect until a later ticket calls it
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/2
raised: 2026-08-28
notified: 2026-08-28T21:42:08
decision: approved
decided: 2026-08-29T02:59:33.281266+00:00
---

# Merge request — Add unified cross-restaurant customer identity

## What this does

`aiorders-api` gets a platform-level customer identity that spans
restaurants: a diner verifies a phone number once via Supabase's native
phone/OTP auth and is recognized as the same identity at every AIOrders
restaurant, with a maintained session. Two new additive tables
(`platform_customers`, `platform_customer_legacy_links`) link to, but never
replace, each restaurant's existing `customers` records. One new edge
function (`platform-customer-auth`) issues and verifies the OTP. No points,
redemption, config, or QR surface yet — this is the identity-foundation
slice of the five-ticket loyalty-program sequence the PRD proposed. No
frontend anywhere calls this yet, so there is no production blast radius
from merging.

## Gates passed

- Code review: **pass** — `agents/principal-engineer/reviews/ENG-006.md`
- Quality: **pass** — `agents/qa/test-plans/ENG-006.md` (AC3/4/7 fully
  covered by tests; AC1/2/5/6 only partially verifiable until Supabase's
  phone-auth provider and an SMS vendor are configured — not this ticket's
  scope, already named in the design's Risks)
- Security: **pass** — `agents/security/reviews/ENG-006.md` (every
  read/write keyed to the caller's own `auth.uid()`, checked in code and at
  the RLS layer; all negative/degraded-auth branches fail closed)
- Migration: **pass** — `agents/database/migrations/ENG-006-unified-customer-identity.md`
  (additive, rollback tested against a throwaway Postgres container)

## PR

https://github.com/harsimranwalia/aiorders-api/pull/2

`aiorders-api` is registered **L1** — this department opens the PR, a human
merges. Merge whenever suits you on GitHub directly; the next build-loop
pass detects the merge itself (local git ancestry check, no action needed
from you beyond the merge) and advances the ticket to `shipped`.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-29T02:59:33.281266+00:00

---

**Processed 2026-08-28 (`decision` event pass).** A "control center" dashboard
action had already flipped `ENG-006`'s `state:` straight from `blocked` to
`shipped` ahead of any build-loop pass reaching this item — the same shape
`ENG-002` hit first (`agents/eng-manager/proposals.md`, 2026-08-26 row), this
time with a written "approved" reply also arriving ~2m28s after the merge
rather than the tracked channel being bypassed outright. Neither signal taken
on its own text: independently re-derived via the loop's own merge-detection
check (`schedules/eng_build_loop.md` step 5) — `git fetch` in the
department's own worktree, `git merge-base --is-ancestor
origin/loyalty-system origin/main` confirmed MERGED, `40d7c36` (PR #2's own
merge commit) directly on top of `c3ab50c` with no intervening commits;
cross-checked against `gh pr view 2 --json state,mergedAt` (`MERGED`,
`2026-08-29T02:57:05Z`). Ticket advanced `shipped → verified` in this pass
(the `blocked → shipped` half was already done by the control center, and
independently confirmed correct here rather than redone) — see
`agents/eng-manager/board/ENG-006-unified-customer-identity.md` for the full
record and `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md` for
the release record (production deploy status not confirmed either way —
outside this department's visibility on an L1 project with no linked
Supabase CLI session; see that record's Deploy and Health notes). Journaled
in `agents/eng-manager/config/decision-journal.md`. Second occurrence of the
control-center-bypass gap noted as an addendum in `observations.md` rather
than a new proposal row, pointing back at the open 2026-08-26 proposal.
