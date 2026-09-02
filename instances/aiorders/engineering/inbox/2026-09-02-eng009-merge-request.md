---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-009
recommendation: merge — migration, code review (round 2), quality, and security all passed; additive-only change (two new nullable columns, a write path on two previously-unwritten existing columns, one new read-only admin-gated route, no schema removal, no new dependency). Both PRs are stacked on ENG-008's still-open branch, not main — see Sequencing below before merging.
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/7
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/6
raised: 2026-09-02
notified: 2026-09-02T10:51:07
nudged:
decision:
---

# Merge request — Influencer engagement info (ENG-009)

Fourth two-repo ticket on this board (after `ENG-011`, `ENG-013`, `ENG-008`)
— one ticket, two PRs, both opened this pass.

## What this does

Staff can now see an internally-derived signal of how active an influencer
is on AIOrders, and can manually enter/update a social-media engagement
figure — both were the standing answer to the question raised while shaping
`ENG-008` ("both reading A and reading B", the approver's own words).

- `aiorders-api`: two new nullable columns on `influencers`
  (`social_stats_updated_at`, `social_stats_platform`); a write path on the
  existing, previously-unwritten `followers`/`engagement` columns via
  `PATCH admin-portal/influencers/{id}` (extends `ENG-008`'s handler); new
  `GET admin-portal/influencers/activity` (admin/sub-admin gated,
  service-role client) returns a per-influencer activity aggregate derived
  from invitation history — no external API call, no stored derived data.
- `aiorders-admin-hub`: edit form gains followers/engagement/platform
  inputs; table gains an Activity column, dialog gains an Activity block;
  Followers/Engagement now show "Not set" instead of a fabricated `0`/`0.0%`
  before staff enter a value.

**Not the Meta API integration** — the approver's own words defer that
("later we can connect"); this ticket ships the staff-manual version only.

## Sequencing — read before merging

**Both PRs are based on `feat/ENG-008-influencer-admin-management`, not
`main`**, because this ticket extends the exact handler file and edit form
`ENG-008` adds, and its round-1 code review failed specifically because this
branch had forked *before* `ENG-008`'s own bug fix landed (see Gates
passed). The diff on each PR is ENG-009's own change only — `ENG-008`'s
commits are not duplicated into these PRs' review surface.

`ENG-008`'s own merge request (`inbox/2026-08-31-eng008-merge-request.md`)
is still open and unanswered. Two ways to sequence:
- Merge `ENG-008`'s two PRs first. If you delete its branch on merge (GitHub's
  default prompt), GitHub auto-retargets these PRs to `main`, and they
  merge cleanly from there.
- Or merge these first — GitHub allows merging into a non-default base
  branch directly; `ENG-008`'s own PRs are unaffected either way. Its
  branch keeps carrying these commits until `ENG-008` itself merges.

No functional dependency forces one order — this is purely a review-surface
choice already made at build time, not a new constraint from this pass.

## Gates passed

- Migration: **pass** — `agents/database/migrations/ENG-009-influencer-engagement-info.md`. Two nullable columns, no default, no backfill.
- Code review: **pass, round 2** — `agents/principal-engineer/reviews/ENG-009.md`. Round 1 failed: this branch forked before `ENG-008`'s own fix landed on both repos and still shipped an already-fixed bug (a defensive auth gap on `aiorders-api`; a real null-coalescing bug on `aiorders-admin-hub` that fabricated `accepts_paid`/`accepts_barter` on an unset preference). Closed by rebasing onto `ENG-008`'s current tip — one real test-file conflict resolved by hand on `aiorders-api`, zero-conflict clean auto-merge on `aiorders-admin-hub`, both independently re-verified by reading the merged result in full.
- Quality: **pass** — `agents/qa/test-plans/ENG-009.md`. All 4 acceptance criteria covered. `deno test` actually executed for the first time on this repo: 34 passed, 0 failed.
- Security: **pass** — `agents/security/reviews/ENG-009.md`. OWASP A01–A10 walked; negative-auth cases (missing profile, wrong role, allowlist enforcement) independently re-verified, not taken on the review's word; no secrets, no new dependency, no PII in the new activity aggregate.

## Named gaps, carried forward rather than hidden

- **Raw `error.message` returned on a 500** in the new activity-endpoint catch block — **3rd tracked occurrence** of this finding class at the security gate (after `ENG-013`, `ENG-008`). Not blocking. Proposed to principal-engineer as a three-strike standards question rather than fixed here: `agents/principal-engineer/notebook/2026-09-02-security-proposal-verbose-error-response.md`.
- `getInfluencerActivity`'s query carries no `.limit()` — 4th occurrence of this accepted class on this board (cardinality bounded by real row counts today, architect-evaluated).
- `social_stats_updated_at` stamps on "present," not "present and changed" as the design literally worded it — a deliberate, tested simplification (avoids a read-modify-write race nothing else in this handler has).
- Setting `social_stats_platform` alone (no `followers`/`engagement`) persists but doesn't render anywhere yet. P3, has a workaround (enter a number too).
- No live Postgres reachable from the build host — verified instead via read-only Supabase MCP against the real production schema, same standing gap every prior migration on this board carries.

## Decision

Filled in by the approver.
