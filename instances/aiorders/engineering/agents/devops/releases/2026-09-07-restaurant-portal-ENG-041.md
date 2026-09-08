---
ticket: ENG-041
project: restaurant-portal
released: 2026-09-07T06:18:50Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: f649583 (merge of 01c6ddb, PR #5)
environment: production (Cloudflare Pages). **Confirmed deployed, not just
  merged** — "Deploy to Cloudflare Pages" run at this commit completed
  successfully 3 seconds after the merge. See Deploy below.
rollback_tested: not drilled — no migration, no stored-state change of its
  own; reverting the merge commit fully undoes this diff and `deploy-cf.yml`
  re-triggers on the revert (reasoned, not rehearsed — same posture this
  repo's prior releases, ENG-032/ENG-039/ENG-040, already used).
health_check: partial — the one new failure path (`ai_conversations` query)
  logs `error.code` and shows a distinct error card with retry; no
  client-side runtime error tracking service exists anywhere in this repo
  (pre-existing gap, already accepted at this gate on ENG-002/ENG-032/ENG-039).
cost_delta_monthly: 0
---

# Release — Customer Questions page + FAQ self-service editor (ENG-041)

## What shipped

A new `/questions` page on `restaurant-portal` lists a restaurant's own
chat-bar questions (newest first, keyset-paginated, `role: 'user'` turns
only), with a distinct empty state and a distinct error state. A third
"FAQs" tab on the existing Website page adds/edits/removes entries against
`restaurant_website.faqs` through `ENG-040`'s widened
`update_website_content` action. A per-row "Add to FAQs" hand-off carries
the question text from the Questions page to a pre-filled FAQ entry via
react-router state, scoped to the originating restaurant (round-1 review
fix for a cross-restaurant leak). Sub-ticket 2 of 2 under `ENG-021`
(chat-bar engagement + FAQ self-service) — the family's last child. Full
detail: `ENG-041`'s own board file,
`agents/frontend/notebook/2026-09-06-eng041-build.md`.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-06-eng041-merge-request.md`, `decision:` still blank).
`restaurant-portal` PR #5 was merged directly on GitHub instead, base
`main`, no stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-041-customer-questions-and-faq-editor origin/main
MERGED (is ancestor)
$ gh pr view 5 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-041-customer-questions-and-faq-editor",
 "mergeCommit":{"oid":"f64958393eb55b726a3d3c036160dc86c3d0312d"},
 "mergedAt":"2026-09-07T06:18:50Z","state":"MERGED"}
```

Merge commit has two parents (`8eea8f1` — `main`'s tip at merge time,
`ENG-020`'s already-verified state; `01c6ddb` — this ticket's own
QA-reviewed tip, the AC1 mutation-verified test commit). `git diff 01c6ddb
origin/main --stat` is empty — the merged tree matches the reviewed tip
exactly, no drift.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass (round 2 — round 1 found and blocked a cross-restaurant FAQ-draft leak, fixed and re-traced) | principal-engineer | 2026-09-06 |
| Quality (QA) | pass, 4/4 owned ACs | qa | 2026-09-06 |
| Security | pass, zero blocking/new findings | security | 2026-09-06 |
| Migration | n/a — no schema or data-model change | database | n/a |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-07 |

Re-read all three receipts directly before writing this record:
`agents/principal-engineer/reviews/ENG-041.md` (`Verdict: PASS`, round 2,
regression test independently re-verified by swapping in pre-fix code),
`agents/qa/test-plans/ENG-041.md` (`last_result: pass`, all 4 owned ACs
covered), `agents/security/reviews/ENG-041.md` (`verdict: pass`, full OWASP
walk, `ENG-022`'s ownership-check fix re-confirmed live on `aiorders-api`).

## Deploy

- **Method: push-triggered CI, confirmed run, not assumed.** `deploy-cf.yml`
  fires on every push to `main`.
- **What actually happened, checked live this pass:** `gh run list --branch
  main` shows "Deploy to Cloudflare Pages" at `head_sha f649583`,
  `createdAt: 2026-09-07T06:18:53Z` (3 seconds after `mergedAt`),
  `status: completed`, `conclusion: success`.
- **Migration:** none — no schema or data-model change in this diff.
- **Feature flag:** none.
- **Duration:** n/a — CI-run, not run by this department.

## Verification

Read directly from the merged, live source (`git show f649583:...`), not any
gate's own account: `questions/Index.tsx`'s query is scoped
`.eq('restaurant_id', currentRestaurant.id)`; the empty/error states are
distinct branches; `handleAddToFaqs` hands off via `navigate(..., {state:
{faqDraft: {question, restaurantId}}})`, never a URL parameter;
`WebsiteFaqForm`'s consuming effect discards a draft whose `restaurantId`
doesn't match the currently-open restaurant (the round-1 leak fix, present
in the shipped code); the FAQ tab's `Save FAQs` submits through
`saveMutation` → `brand-portal`'s `update_website_content` action, the same
real write path `ENG-040` already verified. Full walk:
`agents/product-manager/notebook/2026-09-07-eng041-acceptance.md`.

## Acceptance criteria

Full `acceptance-check/SKILL.md` walk run this pass (not receipt-bookkeeping)
— this ticket owns AC1, AC2, AC6 in full, plus the UI half of AC3, per
`ENG-021`'s work-breakdown AC-mapping. All 4 owned criteria: **pass**. AC4/AC5
and AC3's write half are `ENG-040`'s, already verified 2026-09-06 — not
re-claimed here. Full walk:
`agents/product-manager/notebook/2026-09-07-eng041-acceptance.md`.

## Rollback

- **Path:** no migration, no stored-state change of any kind — reverting the
  merge commit and letting `deploy-cf.yml` redeploy from the prior build
  fully undoes this diff.
- **Tested:** not drilled — nothing destructive to rehearse; the diff is
  additive.
- **Used:** no.

## Health note

The one new failure path (the `ai_conversations` query) already surfaces a
distinct error card with a retry action and logs `error.code` only (no
customer text logged). No new application-level check needed beyond that.

## Observability

No new gap introduced. The pre-existing "no client-side runtime error
tracking anywhere in this repo" condition is unchanged (already accepted at
this gate on `ENG-002`/`ENG-032`/`ENG-039`). The one non-blocking finding
carried at release-readiness (A04 write-payload shape/size validation)
traces to an already-logged `ENG-040` finding, not a fresh occurrence here.

## Cost

$0/month delta — no new dependency, no new infrastructure; matches the
ticket's own estimate.

## Follow-ups

**This was `ENG-021`'s last sub-ticket.** Both children (`ENG-040`,
`ENG-041`) are now `shipped`/`verified` — the parent's own `ADR-003`-class
exemption (all children settled, at least one shipped) is satisfied.
`continue ENG-021` fired this same pass rather than processing the parent's
own no-diff shipped transition inline, same handoff shape `ENG-016`'s and
`ENG-019`'s own closing passes already used. No other ticket unblocked
(`ENG-041`'s `blocks: []`).
