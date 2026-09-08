---
ticket: ENG-040
project: aiorders-api
released: 2026-09-06T16:11:40Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 5e36648b (merge of 104b057, PR #18)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). **Confirmed
  deployed, not just merged** — `brand-portal` at version 84,
  `UPDATED_AT 2026-09-06T16:29:25Z`, ~18 minutes after merge. See Deploy below.
rollback_tested: n/a — no migration, no stored-state change; reverting the
  merge fully undoes this diff (asserted, nothing to rehearse).
health_check: partial — both handler paths already log via `console.error` on
  failure, generic over every `EDITABLE_PAGES` key including the new one; no
  new application-level check added or needed.
cost_delta_monthly: 0
---

# Release — Brand-portal FAQ write path (ENG-040)

## What shipped

`aiorders-api`'s `brand-portal/website.ts` gains a third `EDITABLE_PAGES` key,
`faqs`, alongside the existing `catering`/`careers`. `update_website_content`
persists it via the handler's existing generic per-key loop (no new branch);
`get_website_content` returns it; a new `WebsiteFaq` export documents the
shape. Sub-ticket 1 of 2 under `ENG-021` (chat-bar engagement + FAQ
self-service) — unblocks `ENG-041` (the FAQ editor UI), which has nothing to
save to without this. Full detail: `ENG-040`'s own board file,
`agents/backend/notebook/2026-09-05-eng040-build.md`.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-05-eng040-merge-request.md`, `decision:` still blank).
`aiorders-api` PR #18 was merged directly on GitHub instead, base `main`, no
stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-040-brand-portal-faq-write-path origin/main
MERGED (is ancestor)
$ gh pr view 18 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-040-brand-portal-faq-write-path",
 "mergeCommit":{"oid":"5e36648b08c32443e287ea75fc2d5877124a75e5"},
 "mergedAt":"2026-09-06T16:11:40Z","state":"MERGED"}
```

Merge commit has two parents (`672dfa77` — `main`'s tip at merge time,
carrying `ENG-020`'s already-verified `get_acquisition_report` addition to
the same shared README; `104b057` — this ticket's own QA-reviewed tip). `git
diff 104b057 origin/main --stat` shows only that unrelated, already-shipped
README line beyond this ticket's own commit — `website.ts` itself lands
byte-identical to what every gate reviewed.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass (round 1) | principal-engineer | 2026-09-05 |
| Quality (QA) | pass (round 1), 6/6 | qa | 2026-09-05 |
| Security | pass (round 1) | security | 2026-09-05 |
| Migration | n/a — no schema/data-model change | database | n/a |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-06 |

Re-read all three receipts directly before writing this record:
`agents/principal-engineer/reviews/ENG-040.md` (`pass`, round 1),
`agents/qa/test-plans/ENG-040.md` (`pass`, 6/6, both owned ACs plus AC5
structural), `agents/security/reviews/ENG-040.md` (`pass`, round 1, full OWASP
walk, `ENG-022`'s fix confirmed live on this branch independently).

## Deploy

- **Method: unknown to this department, but confirmed to have happened.** No
  `.github/workflows/` on this repo, same as every prior `aiorders-api`
  release.
- **What actually happened, checked live this pass:** `supabase functions
  list` shows `brand-portal` at version 84, `UPDATED_AT 2026-09-06T16:29:25Z`
  — ~18 minutes after this PR's own `mergedAt` (`16:11:40Z`). Reads as the
  approver deploying by hand shortly after merging, consistent with every
  other release on this board's own deploy pattern.
- **Migration:** none — no schema or data-model change in this diff.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

Read directly from the merged, live source
(`git show origin/main:supabase/functions/brand-portal/website.ts`), not any
gate's own account: `EDITABLE_PAGES` includes `faqs`; the per-key `updates`
loop uses `page in content` (not truthiness) so `faqs: []` persists rather
than being dropped; both `getWebsiteContent`/`updateWebsiteContent` call
`requireRestaurantAccess` (the throwing, post-`ENG-022` version) before
touching any row. Cross-repo check: every chat-bot search function
(`ai-search`, `ai-search-intelligent`, `ai-search-openrouter`) and the
existing staff-only admin-hub editor (`RestaurantAIWebsite.tsx`) all read/write
the same `restaurant_website.faqs` column — no divergent second store. Full
walk: `agents/product-manager/notebook/2026-09-06-eng040-acceptance.md`.

## Acceptance criteria

Full `acceptance-check/SKILL.md` walk run this pass (not receipt-bookkeeping)
— this ticket owns AC4 and AC5 in full, plus the write half of AC3, per
`ENG-021`'s work-breakdown AC-mapping. All 3 owned criteria: **pass**. AC3's
UI half and AC1/AC2/AC6 are `ENG-041`'s to establish, not claimed here. Full
walk: `agents/product-manager/notebook/2026-09-06-eng040-acceptance.md`.

## Rollback

- **Path:** no migration, no stored-state change of any kind — `git revert`
  the merge and redeploy `brand-portal` from the prior commit fully and
  safely undoes this diff.
- **Tested:** not drilled — nothing destructive to rehearse; the diff is
  additive to an existing generic loop.
- **Used:** no.

## Health note

Both handler paths log failures generically over every `EDITABLE_PAGES` key,
including the new one, with no code change needed. No new application-level
health check added or required.

## Observability

No new gap introduced. Two pre-existing, non-blocking findings carried
forward from the security gate (A04 shape-validation gap on
`EDITABLE_PAGES` values, tenant-confined, first occurrence; A05 verbose
error message in `requireRestaurantAccess`, already three-struck and
tracked in an open proposal) — neither re-proposed here.

## Cost

$0/month delta — no new dependency, no new infrastructure; matches the
ticket's own estimate.

## Follow-ups

**Unblocks `ENG-041`** (`depends_on: [ENG-040]`) — the family's last
sub-ticket, `restaurant-portal` frontend FAQ editor. `continue ENG-041`
fired this same pass rather than building it inline. `ENG-021` (parent)
still cannot reach `shipped` until `ENG-041` is settled too (`ADR-003`).
`catering`/`careers`' own write-path test-coverage gap (pre-existing, not
introduced here) remains an open proposal
(`agents/eng-manager/proposals.md`, 2026-09-05 row).
