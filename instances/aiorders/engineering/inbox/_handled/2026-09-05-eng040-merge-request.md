---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-040
recommendation: merge — code review, quality, and security all passed, round 1; no migration (pure addition to an existing per-key loop, no schema change); additive-only, zero regression risk to catering/careers (mutation-verified); unblocks ENG-041's FAQ editor, which has nothing to save to without this
time_estimate: under an hour
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/18
raised: 2026-09-05
notified: 2026-09-05T16:51:18
nudged:
decision:
---

# Merge request — Brand-portal FAQ write path (ENG-040)

Sub-ticket of `ENG-021` (chat-bar engagement + FAQ self-service), sequence 1
of 2. Unblocks `ENG-041`'s FAQ editor.

## What this does

`brand-portal`'s `website.ts` handler allow-lists exactly two keys
(`catering`, `careers`) today. This widens it to a third, `faqs`, so an
owner's own JWT — already authorised to call this endpoint — can write
`restaurant_website.faqs`. `updateWebsiteContent`'s existing per-key loop is
generic over `EditablePage`, so the write side needed zero new lines; the
change is `EDITABLE_PAGES` gaining one entry, `getWebsiteContent` returning
the new field, and a matching `WebsiteFaq` export. `catering`/`careers`
behaviour is unaffected.

## Gates passed

- **Code review: pass, round 1** — `agents/principal-engineer/reviews/ENG-040.md`.
  0/10 automatic failures. One non-blocking finding: the stated reason for
  using `??` instead of `||` on the new `faqs` line doesn't actually hold in
  JS (arrays are always truthy, so either operator behaves identically
  here) — the code is correct regardless, only the documented rationale is
  off.
- **Quality: pass, round 1** — `agents/qa/test-plans/ENG-040.md`. Both owned
  acceptance criteria covered (AC4 in full, AC3's write half); AC5 confirmed
  structural. Found a real gap while writing the plan — the write path
  (`.update()`/`.insert()`) had never been mocked for any key, so it had zero
  test evidence despite being claimed — and closed it for this ticket's own
  key: a new test proves `update_website_content` with `{faqs}` persists
  exactly `{restaurant_id, faqs}`. Mutation-checked: removing `'faqs'` from
  `EDITABLE_PAGES` and re-running turned exactly that one test red, the other
  5 held.
- **Security: pass, round 1** — `agents/security/reviews/ENG-040.md`. Full
  OWASP walk. Verified independently, not taken on the ticket's word, that
  `ENG-022`'s ownership-check fix is live on this branch (ancestry, call
  sites, and the matching checked/written `restaurant_id` all confirmed
  directly). No new authz class — a second writer using the same mechanism
  already governing `catering`/`careers`. No secrets, no new dependency, no
  new PII sink.
- **Migration:** n/a — no schema or data-model change in this diff.

## Release readiness

- **Rollback:** no migration, no stored-state change of any kind — reverting
  the merge fully and safely undoes this diff. Simpler than every ticket
  this repo has shipped that carried a migration.
- **Observability:** both handler paths (`getWebsiteContent`,
  `updateWebsiteContent`) already wrap their body in a try/catch that logs
  via `console.error` before returning a failure to the caller, generic over
  every key including the new one — no new logging mechanism needed, and
  confirmed directly in the diff rather than assumed.
- **Cost:** $0/month — no new dependency, no new infrastructure (diff is
  `website.ts` + its test file + a README line; no manifest touched).
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/18

This project is registered **L1** — this department opens the PR, a human
merges. No CI/CD on this repo; deploying the merged function to
`bmnmnejwdxbcqinqkwko` is a separate manual step after merge, same as every
prior `aiorders-api` release on this board. The next build-loop pass detects
the merge itself (local git ancestry, no reply needed from you) and advances
the ticket.

## Non-blocking findings, named not fixed

1. **A04 — no shape/size validation on `EDITABLE_PAGES` payload values.**
   Pre-existing gap for `catering`/`careers`; `faqs` inherits it rather than
   introducing a new one. Tenant-confined — an owner can only malform their
   own restaurant's row. First occurrence of this specific class, not yet a
   three-strike.
2. **A05 — verbose error message in `requireRestaurantAccess`.**
   Pre-existing, unchanged by this diff, already three-struck and tracked in
   an open proposal. Not re-proposed here.

## Out of scope

- `ENG-041`'s FAQ editor UI — the actual frontend consumer of this write
  path, still `ready`, waiting on this ticket.
- The chat-bar bot's own read of `restaurant_website.faqs` (the other half
  of AC4) — a different function, not touched by this diff.
- `catering`/`careers`' own write-path test coverage, closed only for `faqs`
  here — filed separately as a proposal
  (`agents/eng-manager/proposals.md`, 2026-09-05) rather than fixed inside
  this XS ticket.

## Decision

No reply was written here. `aiorders-api` PR #18 was merged directly on
GitHub instead, base `main`, no stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-040-brand-portal-faq-write-path origin/main
MERGED (is ancestor)
$ gh pr view 18 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-040-brand-portal-faq-write-path",
 "mergeCommit":{"oid":"5e36648b08c32443e287ea75fc2d5877124a75e5"},
 "mergedAt":"2026-09-06T16:11:40Z","state":"MERGED"}
```

Found by this `scheduled` sweep's own step-5 merge detection (2026-09-06,
09:30 PDT pass). All three gate receipts (review/quality/security) re-read
fresh and confirmed `pass`; no migration owed. A full acceptance-check (AC4
and AC5 in full, AC3's write half — the criteria this ticket owns) run
against the live, deployed code — `brand-portal` confirmed redeployed
(version 84) ~18 minutes after merge, not just merged to `main` — see the
ticket's own board-file log and
`agents/devops/releases/2026-09-06-aiorders-api-ENG-040.md`. Carried
`blocked → shipped → verified` this pass. Unblocked `ENG-041`; `continue
ENG-041` fired the same pass.
