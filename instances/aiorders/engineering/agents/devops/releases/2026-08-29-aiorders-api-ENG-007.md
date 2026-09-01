---
ticket: ENG-007
project: aiorders-api
released: 2026-08-29 (exact time not recorded — see Merge note)
released_by: devops (release record itself written retroactively by a `watch` build-loop pass; the `shipped` transition was recorded by the control center, not a pass)
autonomy: L1
gate_g3: n/a — L1 merge, no G3 on this lane
commit: 93617c6 (merged via PR #4, branch `loyalty-system`)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). Migration and the `admin-portal` edge function both confirmed live via the Supabase MCP connection, out-of-band — see Deploy note.
rollback_tested: "not live-drilled — no Docker/psql/supabase CLI on this build host (the same gap ENG-011's migration doc named independently). Reasoned pre-merge via hand-traced trigger semantics plus comparison against three already-applied precedents in this repo; not re-drilled against the live project this pass."
health_check: "not checked via a monitoring dashboard (no access — same standing gap as ENG-005/ENG-006/ENG-011) — but the deploy itself is independently confirmed, not assumed: see Verification."
cost_delta_monthly: 0
---

# Release — Per-restaurant loyalty configuration (ENG-007)

## What shipped

Every restaurant can have an online earn %, a dine-in earn %, and a
redemption value on file, effective-dated, with a full history preserved via
a `BEFORE INSERT` trigger enforcing strictly-increasing, future-only
`effective_from` values. New `admin-portal/handlers/loyalty-config.ts`
(`GET`/`POST`, admin/sub-admin only). No ledger, no points, no redemption, and
no frontend caller exists anywhere in this diff — purely additive config for
tickets 3/4 of the approved loyalty sequence to compute against.

## Merge and shipped-state gap, reconciled here

This ticket's own log already records `blocked → shipped (control center,
merge detected) — recorded on Harry's say-so; ancestry not consulted`. Two
things followed from that bypass, both closed by this pass rather than left
standing:

1. **No independent merge confirmation had been run.** Closed:

   ```
   $ cd _eng/aiorders-api && git fetch origin
   $ git merge-base --is-ancestor origin/loyalty-system origin/main
   MERGED
   $ git log --oneline -1 origin/main
   93617c6 Merge pull request #4 from harsimranwalia/loyalty-system
   ```

   `loyalty-system` confirmed merged, independently of the control center's
   own say-so.

2. **No release record existed**, despite `definition-of-done.md`'s `shipped`
   exit condition requiring one ("Deployed, health checks green, release
   record written") — the gap the control-center bypass leaves every time,
   same shape `proposals.md`'s open control-center-bypass row (2026-08-26,
   corroborated 2026-08-28 on `ENG-006`) already names. This file closes it.

`inbox/_handled/2026-08-29-eng007-merge-request.md` itself still carries no
`decision:` field — genuinely never answered through any channel, not just
found late — since the ticket's own state had already moved past it. A footer
noting this reconciliation has been added to that file; see its own text
rather than duplicating it here.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-08-29 |
| Quality | pass, 44/44 tests | qa | 2026-08-29 |
| Security | pass | security | 2026-08-29 |
| Migration | pass, named gap (no live Postgres dry-run on this host) | database | 2026-08-29 |
| Release readiness | pass | devops | 2026-08-29 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-08-29 |

## Deploy

- **Method:** no CI/CD exists on `aiorders-api` (`.github/workflows/` absent
  from `origin/main`) — merging the PR alone deploys nothing. The department's
  L1 autonomy stops at opening the PR.
- **What actually happened, confirmed read-only via Supabase MCP rather than
  assumed:**
  - `list_migrations` on `bmnmnejwdxbcqinqkwko` shows
    `20260829130000_restaurant_loyalty_configs` applied.
  - `restaurant_loyalty_configs` confirmed present in
    `information_schema.tables`.
  - The `admin-portal` edge function shows `version: 115`, `updated_at`
    **2026-08-30T02:47:37Z**, and its deployed bundle contains the
    `loyalty-config` handler code (`grep` on the fetched bundle: multiple
    `loyalty-config`/`loyalty_config` hits, plus `restaurant_loyalty_configs`
    itself). Deployed from
    `file:///Users/hwalia/Documents/projects/aiorders/aiorders-api/...` — the
    approver's own checkout, not this department's `_eng` worktree — same
    out-of-band pattern `ENG-006`'s release record documented for
    `platform-customer-auth`, and the same deploy event that carried
    `ENG-011`'s stage/health code live (one `admin-portal` redeploy covering
    both tickets' handler changes at once).
- **Why this department didn't run it:** `aiorders-api` is L1; a human merges
  and, absent CI/CD, a human also deploys.

## Verification

Re-confirmed against live state via the three Supabase MCP checks under
Deploy above — all read-only, no cost, no write.

**Acceptance criteria — not yet formally walked.** This record establishes
the merged code is deployed and live; `skills/acceptance-check/SKILL.md`
(product-manager, triggered by `shipped`) does the criterion-by-criterion
walk. Note for that pass: this ticket is item 2 of the approved five-ticket
loyalty sequence (`ENG-006`'s PRD) — step 6b applies if the sequence
condition is met.

## Rollback

- **Path:** migration — drop `restaurant_loyalty_configs` and its trigger
  (purely additive, nothing depends on it yet). Route — revert the 2-line
  `index.ts` addition plus the new handler/test files; no live caller exists
  anywhere in this diff.
- **Tested:** not live-drilled (see frontmatter `rollback_tested`).
- **Used:** no.

## Observability

Every unexpected-error branch logs server-side via `console.error` before
responding (confirmed in code review), through Supabase's existing function-log
mechanism. Not independently exercised against the live deploy — no dashboard
access from this department.

## Cost

$0/month delta — same Supabase project, one new empty table, no new service.

## Follow-ups

- No live-app verification of the new route performed by this department (no
  browser access, no admin session from this host) — carried forward to
  acceptance-check.
- The unplanned Walletly discovery from this ticket's own design work was
  resolved at G2 ("Walletly is being retired/replaced") — already journaled;
  not re-litigated here.
- Whoever files ticket 3 (points ledger) next should know both this ticket's
  table and `ENG-011`'s analytics column are now confirmed live, not just
  merged — the sequence's foundation is real, not paper.
