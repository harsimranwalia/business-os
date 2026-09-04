---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-033
time_estimate: ~half a day
recommendation: merge — code review (round 4), quality (round 2), and security all passed on the current diff; additive-only change (two new optional/validated fields on an existing public endpoint, status derived server-side, no auth/schema/dependency surface touched — the two nullable columns themselves shipped separately under ENG-031)
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/13
raised: 2026-09-04
notified: 2026-09-04T01:43:02
nudged:
decision:
---

# Merge request — catering-request order-capture fields (ENG-033)

Part of `ENG-016`'s catering quote generator (Piece 1). Unblocks `ENG-034`
(the public dish picker), the last sub-ticket in that family.

## What this does

`catering-request` (the public, unauthenticated form-submission endpoint)
now accepts and validates two new optional fields — `action_type`
(`QUOTE_SUBMITTED` | `MANUAL_CONTACT_REQUESTED`) and `selections` (an
itemized array of `{category, item_id, name, quantity, note}`) — and derives
the catering board's `status` server-side from `action_type`, never from the
request body (this endpoint is unauthenticated, so a client-supplied status
would let anyone drop a request straight into a late-pipeline stage). Every
existing caller (GoHighLevel, `restaurant-marketplace`'s own direct insert)
is unaffected by construction — both fields are optional and the function
already ignores undestructured input.

## Gates passed

- **Code review: pass, round 4** — `agents/principal-engineer/reviews/ENG-033.md`.
  0/10 automatic-failure checks. The status-derivation logic was extracted
  into a pure, exported `deriveActionStatus()` per the quality gate's own
  round-1 finding, independently mutation-tested rather than taken on trust.
- **Quality: pass, round 2** — `agents/qa/test-plans/ENG-033.md`. 17/17
  `deno test`. AC-10/AC-13 not automated, with reasons, accepted under
  `definition-of-done.md`'s manual-verification allowance.
- **Security: pass** — `agents/security/reviews/ENG-033.md`. Full OWASP
  walk, no new route/auth/dependency/logging surface; the two new fields'
  only render path (`restaurant-portal/CateringDetailModal`) escapes by
  construction, verified directly. Two non-blocking findings — see below.

## PR

- `aiorders-api`: https://github.com/harsimranwalia/aiorders-api/pull/13

This project is registered **L1** — merge whenever suits you on GitHub
directly; the next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket once it's in.

## Named gaps, carried forward rather than hidden

- **Pre-existing HTML-injection gap in the owner-notification email**, found
  while reading this function in full for this gate — not part of this
  diff. `index.ts:348-378` (unchanged here) builds the notification
  `message_html` from several form fields via raw string interpolation with
  no HTML-escaping, then forwards it to a third-party webhook (Pabbly
  Connect) that emails/SMS/WhatsApps you. Medium severity — bounded to
  HTML-formatting/link injection in that notification (most email clients
  strip script/event handlers), not code execution, but real and reachable
  by anyone, free, today. This ticket's own two new fields aren't included
  in that email at all, so it doesn't create or worsen this. Filed as a
  proposal (`agents/eng-manager/proposals.md`, 2026-09-04) rather than
  fixed here — out of this diff's own scope.
- **One thing worth a ten-second check on your end, not a blocker:**
  whether Row Level Security is actually turned on for the `catering` and
  `restaurants` tables. No tracked migration ever runs `ENABLE ROW LEVEL
  SECURITY` on either — everything else on this repo's side is consistent
  with it already being on (a 2025-07-29 migration's own framing, "Critical
  Database Security Fixes", removing "dangerous policies", only makes sense
  if it was), but nobody on this pipeline has live database access to
  confirm it directly, on this ticket or the two before it that hit the
  same question (`ENG-015`, `ENG-031`). If you've got a minute in the
  Supabase dashboard: confirming `catering` and `restaurants` both show RLS
  enabled would close this permanently.
- **`selections[].name` has no length cap**, unlike the sibling `note`
  field (capped at 500 chars). Low severity, no new capability beyond this
  already-public endpoint's existing spam exposure — logged as an
  observation, not filed as a proposal.

## Update, 2026-09-04 (`watch (launchd)` event pass) — resolved, shipped

PR #13 now shows `MERGED` on GitHub (`2026-09-04T15:25:13Z`, merge commit
`cd40bbf9`), base `main` — confirmed via `git merge-base --is-ancestor` on
this ticket's own recorded commit (`697df79`) against fresh `origin/main`,
cross-checked with `gh pr view`. All three gate receipts re-read fresh,
still `pass`; no migration owed. Ticket carried `blocked → shipped →
verified`. Unblocks `ENG-034` — `continue ENG-034` fired this same pass.
Full detail: `ENG-033`'s own board-file log, 2026-09-04 entry, and
`agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md`.

The two non-blocking findings and the RLS-confirmation ask above were not
addressed by the merge — they weren't gates, so nothing here waits on them.

## Decision

Filled in by you. (None given — resolved by direct GitHub action; see the
update immediately above.)
