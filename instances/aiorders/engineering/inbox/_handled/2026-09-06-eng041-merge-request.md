---
type: eng-decision
agent: eng-manager
gate: merge
project: restaurant-portal
ticket: ENG-041
recommendation: merge — code review (round 2, round 1's cross-restaurant FAQ-draft leak fixed and re-traced), quality, and security all passed; no migration; the ENG-021 family's last child, unblocking the parent's own ADR-003-class close-out
time_estimate: ~1 to 1.5 days
pr_url: https://github.com/harsimranwalia/restaurant-portal/pull/5
raised: 2026-09-06
notified: 2026-09-06T11:16:37
nudged:
decision:
---

# Merge request — Customer Questions page and self-service FAQ editor (ENG-041)

Sub-ticket of `ENG-021` (chat-bar engagement + FAQ self-service), sequence 2
of 2 — the family's last child. Depended on `ENG-040` (merged, verified,
deployed) for the widened `update_website_content` action.

## What this does

- New `/questions` page: lists the restaurant's own chat-bar questions,
  newest first, keyset-paginated, with a distinct empty state and a distinct
  error state.
- Third "FAQs" tab on the existing Website page — add/edit/remove entries
  against `restaurant_website.faqs`, mirroring `CateringPageForm`'s existing
  idiom.
- Per-row "Add to FAQs" hand-off from the Questions page pre-fills a new FAQ
  entry, via `react-router` state, never a URL parameter.

`CateringPageForm`/`CateringFaq` and the admin-hub staff FAQ editor are
explicitly untouched, per the design.

## Gates passed

- **Code review: pass, round 2** — `agents/principal-engineer/reviews/ENG-041.md`.
  Round 1 found and blocked on a real cross-restaurant data leak: the
  FAQ-draft hand-off carried no restaurant id, so an owner managing 2+
  restaurants could carry restaurant A's customer question onto restaurant
  B's FAQ editor after a restaurant switch. Fixed by scoping the draft to
  its originating restaurant and discarding it on mismatch; round 2
  independently re-traced the fix against the original repro and confirmed
  the regression test fails on the pre-fix code, only that test.
- **Quality: pass** — `agents/qa/test-plans/ENG-041.md`. All 4 owned ACs
  (AC1, AC2, AC6, UI-half AC3) covered; one coverage gap (AC1's
  "never another restaurant's" half) closed in-hop, mutation-verified.
- **Security: pass** — `agents/security/reviews/ENG-041.md`. Zero blocking
  findings. `ENG-022`'s ownership-check fix re-confirmed live on
  `aiorders-api`'s current `origin/main`, not taken on any ticket's word.
  PII (`ADR-014`) checked control-by-control against the shipped code.
- **Migration:** n/a — no schema or data-model change in this diff.

## Release readiness

- **Rollback:** no migration, no stored-state change of its own — reverting
  the merge commit fully undoes this diff; `deploy-cf.yml` re-triggers on
  the revert and redeploys the prior build. Not drilled (no CI dashboard
  access from this department's worktree) — reasoned, not tested, same
  posture this repo's prior releases (`ENG-032`, `ENG-039`) already used.
- **Observability:** the one new failure path (`ai_conversations` query)
  logs `error.code` and surfaces a distinct error card with retry. No
  client-side runtime error tracking service exists anywhere in this repo
  (pre-existing gap, same posture already accepted on
  `ENG-002`/`ENG-032`/`ENG-039`).
- **Cost:** $0/month — no new dependency or infrastructure, reuses existing
  Cloudflare Pages capacity and an existing, already-authorized Supabase
  read.
- **Window:** n/a — `restaurant-portal` is registered L1; opening a PR is
  not a release.

## PR

https://github.com/harsimranwalia/restaurant-portal/pull/5

This project is registered **L1** — this department opens the PR, a human
merges. Merging triggers `deploy-cf.yml` (push-triggered) automatically. The
next build-loop pass detects the merge itself (local git ancestry, no reply
needed from you) and advances the ticket.

## Non-blocking findings, named not fixed

None new. The one candidate raised during security review (A04, write-payload
shape/size validation) traces to an already-logged `ENG-040` finding, not a
fresh occurrence on this ticket's own surface.

## Out of scope

- `CateringPageForm.tsx`/`CateringFaq` and the admin-hub staff FAQ editor —
  untouched, per the design.
- Re-deriving AC4/AC5 — satisfied by construction of `ENG-040`'s shared
  `faqs` column, already verified at `ENG-040`'s own acceptance.

This is `ENG-021`'s last sub-ticket. Once this merges and ships, the parent
qualifies for its own `ADR-003`-class exemption (both children settled, at
least one shipped) — not this item's to process, noted so whichever pass
finds the merge isn't surprised the parent is also ready to close out.

## Decision

No reply was written here. `restaurant-portal` PR #5 was merged directly on
GitHub instead, base `main`, no stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-041-customer-questions-and-faq-editor origin/main
MERGED (is ancestor)
$ gh pr view 5 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-041-customer-questions-and-faq-editor",
 "mergeCommit":{"oid":"f64958393eb55b726a3d3c036160dc86c3d0312d"},
 "mergedAt":"2026-09-07T06:18:50Z","state":"MERGED"}
```

Found by this `scheduled` sweep's own step-5 merge detection (2026-09-07,
02:00 PDT pass). All three gate receipts (review/quality/security) re-read
fresh and confirmed `pass`; no migration owed; zero drift (`git diff 01c6ddb
origin/main --stat` empty). A full acceptance-check (AC1, AC2, AC6 in full,
AC3's UI half — the criteria this ticket owns) run against the live,
deployed code — `restaurant-portal`'s push-triggered Cloudflare Pages
workflow confirmed completed 3 seconds after the merge, not just merged to
`main` — see the ticket's own board-file log and
`agents/devops/releases/2026-09-07-restaurant-portal-ENG-041.md`. Carried
`blocked → shipped → verified` this pass. This was `ENG-021`'s last
sub-ticket — both children now settled, the parent's `ADR-003`-class
exemption is satisfied; `continue ENG-021` fired the same pass.
