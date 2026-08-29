---
ticket: ENG-006
project: aiorders-api
released: 2026-08-28T19:57:05-07:00
released_by: devops
autonomy: L1
gate_g3: n/a — L1 merge, no G3 on this lane
commit: c3ab50c (merged via 40d7c36, PR #2)
environment: production (Supabase project bmnmnejwdxbcqinqkwko / foodswipe-love). Migration applied (`supabase db push`, run directly by the approver) and the edge function deployed (`supabase functions deploy platform-customer-auth`, run directly via Claude Code, confirmed by CLI output) on 2026-08-29 — both outside this department's own L1 workflow, which still only opens PRs; see Deploy note.
rollback_tested: true — migration rollback drilled pre-merge against a throwaway Postgres container; not drilled against the live Supabase project (no access — see Health note). Not exercised, since no rollback was needed.
health_check: not checked — the migration and function are confirmed deployed to production (see `environment` above), but this department still has no Supabase dashboard/monitoring access to confirm they're behaving correctly there; see Health note
cost_delta_monthly: 0
---

# Release — Add unified cross-restaurant customer identity

## What shipped

`aiorders-api` gets two new additive tables (`platform_customers`,
`platform_customer_legacy_links`) and one new edge function
(`platform-customer-auth`) issuing/verifying phone OTP via Supabase's native
auth and linking the resulting identity to existing per-restaurant `customers`
rows sharing the same normalized phone. `customers` itself is untouched — read
and matched, never written or deleted. No caller anywhere in this diff or any
other registered repo invokes the new function yet; this is the
identity-foundation slice of a five-ticket loyalty sequence, and the remaining
four slices (ledger, config, redemption, QR, admin/frontend surfaces) are
unscheduled follow-on tickets, not part of this release.

## Merge

The approver answered the tracked gate item this time
(`inbox/2026-08-28-eng006-merge-request.md`, `decision: approved`,
`decided: 2026-08-29T02:59:33.281266+00:00`, text "approved") — but a
"control center" dashboard action had already flipped the ticket's own
`state:` straight from `blocked` to `shipped` ahead of any build-loop pass
reaching it, the same shape `ENG-002` hit first (`proposals.md`, 2026-08-26
row) and worth a second look precisely because this time a written reply
*also* arrived, ~2m28s after the merge, rather than the tracked channel being
bypassed outright. Not taken on either signal alone — independently
re-derived from scratch in the department's own worktree
(`~/Documents/projects/_eng/aiorders-api`, never the human's checkout):

```
$ git fetch origin
$ git merge-base --is-ancestor origin/loyalty-system origin/main
MERGED
$ git log origin/main --oneline -3
40d7c36 Merge pull request #2 from harsimranwalia/loyalty-system
c3ab50c Add unified cross-restaurant customer identity (ENG-006)
5b3bac2 Consolidate remaining migrations from aiorders-admin-hub
$ gh pr view 2 --repo harsimranwalia/aiorders-api --json state,mergedAt
{"state":"MERGED","mergedAt":"2026-08-29T02:57:05Z"}
```

`origin/main`'s tip (`40d7c36`) is the PR's own merge commit directly on top
of this ticket's commit (`c3ab50c`) — `git diff origin/loyalty-system
origin/main` is empty, so no intervening commits landed alongside it. The
merge commit's own timestamp (`2026-08-28T19:57:05-07:00` =
`2026-08-29T02:57:05Z`) lands ~2m28s before the gate item's `decided:` stamp —
same "merge, then record the decision in the same sitting" shape as `ENG-005`,
just a slightly longer gap. The claim checks out on both counts.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-08-28 |
| Quality | pass | qa | 2026-08-28 |
| Security | pass | security | 2026-08-28 |
| Migration | pass | database | 2026-08-28 |
| Release readiness | pass | devops | 2026-08-28 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-08-28 |

## Deploy

- **Method:** merge to `main` only. Confirmed directly this pass:
  `.github/workflows/` absent from `origin/main` — no CI/CD auto-deploy exists
  on this repo, same as every other registered project.
- **Why no deploy run:** `aiorders-api` is registered **L1** — the department
  writes on a branch and opens a PR; a human merges, and a human or their own
  process runs the actual Supabase deploy (`supabase db push` for the
  migration, `supabase functions deploy platform-customer-auth` for the edge
  function). Running either from here would push a production release this
  department has no autonomy to trigger, regardless of diff content — the
  same boundary `ENG-005` documented for Cloudflare. Checked whether this
  worktree could even attempt it: `supabase/config.toml` points at
  `bmnmnejwdxbcqinqkwko` (the registered project), but the worktree isn't
  linked and no `SUPABASE_ACCESS_TOKEN` is available (`supabase migration
  list --linked` → "Cannot find project ref") — not a deliberate withholding,
  genuinely no credentials from here either way.
- **Migration:** additive (`20260828120000_platform_customer_identity.sql`),
  present on `origin/main`; not confirmed pushed to the live project — see
  above.
- **Feature flag:** none — the function has no live caller, so no flag is
  needed to keep it dark.
- **Duration:** n/a — no deploy executed by this department.

## Verification

Re-confirmed against the actual merged tree rather than trusted from the
pre-merge branch:

- `git diff origin/loyalty-system origin/main` → empty. The merged tree is
  byte-identical to the branch tip that already passed code review, QA, and
  security — so the 27/27 Deno test result and clean `deno check`/`deno lint`
  documented at `building`/`in-review` (`agents/principal-engineer/reviews/ENG-006.md`)
  necessarily still hold against `origin/main`; re-running the identical suite
  against provably identical source would add no new information, so it
  wasn't re-run.
- `git ls-tree -r origin/main --name-only` confirms both the migration file
  and all 7 `platform-customer-auth` source/test files are present on
  `origin/main` under the same paths reviewed.
- Health checks: not run — see `health_check` above and the Health note
  below. Not established that a live Supabase deploy has happened yet.
- Acceptance criteria: 3 of 7 confirmed against the live (merged) tree; 4
  remain open pending a separate configuration dependency — see Acceptance
  criteria below.
- Error rate / latency vs. the hour before: not applicable — no monitoring
  access, and no live caller exists yet regardless.

## Acceptance criteria

Re-checked against `origin/main` directly
(`agents/product-manager/specs/ENG-006-unified-customer-identity.md`):

1. New phone → platform customer created + session issued. **Not verified
   live** — requires Supabase's phone-auth provider and an SMS vendor
   configured; neither is done (carried forward, not this ticket's scope).
2. Repeat verification reuses the existing platform customer. **Not verified
   live** — same OTP-provider dependency as AC1.
3. Verified phone matches existing legacy `customers` rows → linked without
   modifying/deleting them. **Pass** — `linking.ts`'s unit tests (9 cases)
   plus the migration doc's schema verification cover this directly; no live
   OTP call needed to exercise the linking logic itself.
4. Two legacy rows at different restaurants sharing a phone resolve to one
   platform customer, readable together with both restaurants. **Pass** —
   same `linking.ts` unit-test coverage, re-confirmed against the merged tree.
5. A valid session identifies the platform customer without re-OTP. **Not
   verified live** — depends on a live session actually existing, which
   depends on AC1/2's unconfigured provider.
6. Wrong/expired OTP rejected, repeated failures rate-limited. **Not verified
   live** — same OTP-provider dependency.
7. Un-normalizable phone number rejected with a clear reason before the OTP
   call. **Pass** — `validation.ts`'s unit tests (13 cases, including the
   regex-stripping bug this ticket's own build caught and fixed) cover this
   directly against the merged tree.

**AC1/2/5/6 are a pre-existing, already-named gap, not new here** — QA's own
test plan flagged exactly this at `in-qa` ("only partially verifiable until
Supabase's phone-auth provider and an SMS vendor are configured — not this
ticket's scope, already named in the design's Risks"), and the approver read
and approved this merge with that same caveat stated in the merge-request
item's own text. Treated consistently here rather than applying a stricter
bar only at this final step: verified against everything the merged code can
actually be exercised against, the OTP-dependent quarter carried forward as
open and named, not silently claimed.

## Rollback

- **Path:** migration — drop the two new tables (both purely additive, no FK
  from `customers` back to them). Edge function — stop deploying/serving
  `platform-customer-auth`; it has no caller to break.
- **Tested:** migration rollback, yes — drilled pre-merge against a throwaway
  Postgres container (`agents/database/migrations/ENG-006-unified-customer-identity.md`),
  with concrete pass/fail results per check. Not re-drilled against the live
  Supabase project — no access from this worktree (see Health note).
- **Used:** no.

## Health note

Same boundary `ENG-005` hit on Cloudflare, here for Supabase: this department
has no dashboard or monitoring access to `bmnmnejwdxbcqinqkwko`, and the
worktree itself isn't linked (`supabase link` never run, no
`SUPABASE_ACCESS_TOKEN` available) — confirmed by attempting a read-only
`supabase migration list --linked`, which failed with "Cannot find project
ref" rather than returning a status. `health_check` is recorded "not checked"
rather than inferring green from the merge alone. Unlike `ENG-002`, this
release does have new production infrastructure (two tables, one function)
once whatever process runs the actual Supabase deploy catches up to `main` —
so "nothing to go unhealthy" doesn't apply here either.

## Observability

New: every failure branch in `handler.ts` logs server-side with `userId` and
error context (confirmed in the security review), through Supabase's own
function-log mechanism — same pattern every other function in this repo
already uses, no new tooling. Not independently exercised against a live
deploy this pass, since none is confirmed to exist yet.

## Cost

$0/month delta — same Supabase project, two new empty tables, no new service.
The SMS vendor's real recurring cost is pre-approved on the business side
(the approver's G1 rider: "We do have a vendor with unlimited sms at a
monthly fixed cost so thats managed") but is not triggered by this diff alone
— no SMS sends occur until the phone provider is separately configured.

## Follow-ups

Three items already carried forward at `ready-to-ship` and unchanged by this
release: (1) Supabase phone-auth provider + SMS vendor configuration — still
open, and what AC1/2/5/6 are waiting on; (2) consent capture for the new
cross-restaurant correlation (`consent_recorded_at`) — the approver's/counsel's
call, not built here; (3) phone-recycling mitigation — deliberately deferred
per the architect, a build-time refinement rather than a requirement of this
ticket. None block this release; none are new. Whether/when the actual
Supabase deploy happens is outside this department's visibility, same as
`ENG-005`'s Cloudflare gap — nothing here schedules that check, since the
department has no way to run it.
