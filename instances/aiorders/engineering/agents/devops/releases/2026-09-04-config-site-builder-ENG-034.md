---
ticket: ENG-034
project: config-site-builder
released: 2026-09-04T17:09:10Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 40cfc55 (merge of 62b3ca0, PR #4)
environment: production (Cloudflare Pages, config-site-builder). Merge confirmed on `origin/main`; no CI/CD auto-deploy workflow exists on this repo (`.github/workflows/` absent, confirmed directly), and `deploy-cf`/`deploy-all` are manual, explicitly-invoked `npm` scripts — whether/when this specific commit has actually been built and pushed live for any given restaurant's site is unknown from this department's vantage point. See Deploy section.
rollback_tested: false — reasoned, not drilled (no test command exists on this project at all, same position `ENG-005` already established for this stack shape). Reasoning: single commit, no migration, no stored-state change — reverting the merge commit on `main` fully and safely undoes it.
health_check: not checked — no dashboard/API access to this Cloudflare Pages project from this department's worktree; see Health note
cost_delta_monthly: 0
---

# Release — Public catering form: category-grouped dish picker (ENG-016 Piece 1, sub-ticket 4 of 4 — last)

## What shipped

A restaurant that opts in (`config.catering.orderFormEnabled`) now shows a
category-grouped dish picker on its public catering page — customers pick
items with a quantity and an optional note each, then either submit a quote
request or ask for a callback instead, with no dish required either way.
Every restaurant that hasn't opted in (the overwhelming majority today) sees
the exact form it renders now, byte for byte. This is the fourth and last
sub-ticket of `ENG-016`'s Piece 1 (catering quote generator); all four
surfaces (`ENG-031` database, `ENG-032` restaurant-portal, `ENG-033`
aiorders-api, this ticket the public form) are now shipped or verified.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-04-eng034-merge-request.md`, `decision:` still blank).
`config-site-builder` PR #4 was merged directly on GitHub instead, base
`main`:

```
$ git merge-base --is-ancestor 62b3ca0 origin/main && echo YES
YES
$ gh pr view 4 --repo harsimranwalia/config-site-builder --json state,mergedAt,mergeCommit,baseRefName,headRefOid
{"baseRefName":"main","headRefOid":"62b3ca0f19b0c519be9f2dc641618db792be18fd","mergeCommit":{"oid":"40cfc55f66b2c04d08f5f49f6e587cfc58fe99a4"},"mergedAt":"2026-09-04T17:09:10Z","state":"MERGED"}
```

Branch tip (`62b3ca0`) matches this ticket's own frontmatter exactly, no
drift between what passed every gate and what merged. Base is `main`
directly — no stacking, so none of the `ENG-009`/`ENG-010` branch-tip
contamination shape applies here. Single repo, no cross-ticket branch
dependency of its own (this ticket depended on `ENG-033`, already shipped;
nothing depends on this one — it's the last in the sequence).

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass, round 1 | principal-engineer | 2026-09-04 |
| Quality (QA) | pass, round 1 (`no suite` — expected, no test runner on this project) | qa | 2026-09-04 |
| Security | pass, round 1, zero findings | security | 2026-09-04 |
| Migration | n/a — frontend-only diff, no schema/data-layer surface | database | — |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-04 |

Re-read all three receipts directly before writing this record, not taken
from the ticket's own narrative: `agents/principal-engineer/reviews/ENG-034.md`
(`verdict: pass`), `agents/qa/test-plans/ENG-034.md` (`last_result: no
suite`, every AC manually verified with a reason), `agents/security/reviews/ENG-034.md`
(`verdict: pass`, zero findings). No `agents/database/migrations/ENG-034-*.md`
— correct, confirmed no `*.sql`/schema change in the diff.

## Deploy

- **Method:** merge to `main` only. `git ls-tree -r origin/main --name-only
  | grep -i workflow`: no hits — no GitHub Actions auto-deploy exists on this
  repo (confirmed directly by the release-readiness hop before opening the
  PR, re-confirmed here). `deploy-cf` (`generate-wrangler && build && wrangler
  pages deploy`) and `deploy-all` are manual, explicitly-invoked `npm`
  scripts — nothing fires them on a merge.
- **Why this department didn't run one:** `config-site-builder` is registered
  **L1** — a human merges, and this department's own action boundary at L1
  stops at confirming the code landed on `main`, same posture already
  recorded on this exact question for `aiorders-api` (`ENG-033`'s own release
  record: "why this department didn't run it: L1 — a human merges. What
  actually happened: unknown from here.") and, differently but for the same
  reason, `restaurant-portal` (`ENG-032`'s: the workflow "runs unattended on
  GitHub's side once merged, outside this department's own action"). This is
  the first release on `config-site-builder` specifically, and the
  precedent from both sibling repos in this same `ENG-016` family points the
  same direction regardless of whether CI/CD exists on the repo or not:
  running `wrangler pages deploy` from this worktree would be this
  department publishing to production on its own initiative, past the point
  L1 draws the line, not a mechanical continuation of a decision the human
  already made by merging.
- **What actually happened:** unknown from here — no Cloudflare Pages
  dashboard or API access from this department's worktree, and this repo is
  per-restaurant config-driven (`VITE_RESTAURANT_SLUG`/`VITE_BRAND_ID` in
  `.env`), so even "deployed" doesn't resolve to one single site to check.
- **Migration:** none.
- **Feature flag:** none — `orderFormEnabled` defaults off per-restaurant
  (`ADR-009`), opted in individually, not a global flag.
- **Duration:** n/a — no deploy run by this department.

## Verification

Re-verified directly against the merged tree, not just the receipts' own
account: `git show origin/main:src/components/CateringMenuSelector.tsx`
confirms the component exists as reviewed; `git show
origin/main:src/components/CateringForm.tsx` confirms the `orderFormEnabled`
gate expression, the `CateringMenuSelector` mount, both submit actions, and
the email-required/requirements-optional swap are all present exactly as
reviewed. Health checks: not run — see `health_check` above.

## Acceptance criteria

Independently re-walked against the merged `origin/main` tree by this
release's own acceptance-check (not re-derived from the review's account) —
full criterion-by-criterion evidence in
`agents/product-manager/notebook/2026-09-04-acceptance.md`. All eight
criteria this ticket owns (AC-1 narrowed, AC-2, AC-3, AC-4, AC-5 client half,
AC-6 client half, AC-9, AC-11) verified **pass** by direct source reading.
Production/live-user-path verification is not available for the reason
named in `environment:` above — named as a real, honestly-reported gap, not
rounded up to a full click-through that didn't happen.

## Rollback

- **Path:** revert the single merge commit — no migration, no stored-state
  change; fully undoes the diff. No CI to re-trigger on the revert (see
  Deploy) — a human would need to re-run whichever deploy path (`deploy-cf`
  or the FTP `deploy` script) publishes this repo's live sites, same as the
  forward direction.
- **Tested:** not drilled — see `rollback_tested` above.
- **Used:** no.

## Health note

No dashboard/monitoring access to this Cloudflare Pages project or its
deploy pipeline from this department's worktree — same standing boundary
`ENG-032`'s own release record already named for this project family,
compounded here by there being no CI run to even check the status of.

## Observability

No new fetch/network call of its own (security gate's own grep, zero hits) —
POSTs through `ENG-033`'s already-shipped, already-observed
`catering-request` endpoint unchanged. The one new client-side failure mode
(code review Finding F1 — `SubmitEvent.submitter` has no fallback) fails
open silently; a named, accepted gap, not a monitored path — no
client-side error tracking exists anywhere in this repo family, a
pre-existing condition not introduced or worsened here.

## Cost

$0/month delta — no new dependency (`lucide-react` confirmed pre-existing at
both the code-review and security gates), no new infrastructure, no new
vendor.

## Follow-ups

**This is the last of `ENG-016`'s four sub-tickets to ship** — `ENG-031`,
`ENG-032`, `ENG-033` already `verified`; this ticket's own acceptance-check
(see notebook) routes it to `verified` too. Per the parent's own `##
Breakdown` (ADR-003-class exemption), `ENG-016` itself is now eligible to
move `building → shipped` directly, without its own review/QA/security hops,
since every child is `shipped`/`verified`/`dropped` with at least one
actually shipped. Not processed inline this pass — chained (`continue
ENG-016`) for a dedicated session, same handoff shape this family's own
prior shipping passes already used for their successors. Four non-blocking
code-review findings and two named pre-existing conditions remain open,
carried on the ticket's own log, none gating anything
(`agents/principal-engineer/reviews/ENG-034.md`).
