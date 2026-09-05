---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-037
time_estimate: ~half a day
recommendation: merge — code review (round 1), quality (round 1), security (round 1), and the migration plan all passed; schema-only migration for ENG-019's broadcast feature, inert until ENG-038 ships; one precise observability note named below, non-blocking
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/15
raised: 2026-09-04
notified: 2026-09-04T12:33:03
nudged:
decision:
---

# Merge request — broadcast campaigns schema and dispatch cron (ENG-037)

Sub-ticket 1 of 3 under `ENG-019` (restaurant marketing broadcasts),
sequenced first per the design's own Rollout order (migration → functions →
frontend). `ENG-038` (backend) and `ENG-039` (frontend) both wait on this
one merging.

## What this does

Adds `broadcast_campaigns`, `broadcast_campaign_steps`,
`broadcast_campaign_recipients` (all RLS-enabled, no policies —
service-role only), five supporting indexes, an `updated_at` trigger, and a
`broadcast-dispatch-tick` `pg_cron` job (every 5 minutes, structurally
matching the live `platform_analytics_cron`). No existing table touched.

## Gates passed

- **Code review: pass, round 1** — `agents/principal-engineer/reviews/ENG-037.md`.
  0/10 automatic failures. Two non-blocking findings — see "Named gaps"
  below.
- **Quality: pass, round 1** — `agents/qa/test-plans/ENG-037.md`. No
  application code reaches these tables yet; schema-matches-design verified
  by direct query against both a disposable local replica and the live
  project's schema dump.
- **Security: pass, round 1** — `agents/security/reviews/ENG-037.md`. 0
  blocking findings. Two non-blocking notes — see "Named gaps" below.
- **Migration plan: pass** — `agents/database/migrations/ENG-037-broadcast-campaigns-schema-and-dispatch-cron.md`.
  `orders.promos`'s exact shape confirmed live (resolves `ADR-019`'s named
  open risk); `communication_log` confirmed unchanged; rollback actually
  executed against a disposable container, not just asserted.

## PR

- `aiorders-api`: https://github.com/harsimranwalia/aiorders-api/pull/15

This project is registered **L1** — merge whenever suits you on GitHub
directly; the next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket once it's in.

## Named gaps, carried forward rather than hidden

- **F1 — `broadcast_campaign_recipients.step_id`'s `on delete cascade` FK
  has no dedicated index.** Postgres doesn't auto-index the referencing
  side of a FK, so a cascade through `step_id` would seq-scan this schema's
  highest-fan-out table. Low-reach today — nothing deletes a step while
  recipient rows could exist for it.
- **F2 — `broadcast_campaigns.scheduled_send_at` is nullable with no
  constraint tying it to `status`.** A future `ENG-038` bug inserting
  `status: 'scheduled'` with a null send time would sit silently unsent
  forever, no error, no log line.
- **Security note — RLS-zero-policy is not a repeat of the `ENG-015`/
  `ENG-031`/`ENG-033` "RLS activation unverified" pattern.** Those tables
  predate tracked history; these three are created and verified live by
  this same migration.
- **Security note — no rate/quota/audience-size cap exists anywhere in the
  broadcast-send plan yet.** Routed forward to `ENG-038`'s own gate
  (`agents/security/notebook/2026-09-04-findings.md`); non-blocking since
  nothing reads or writes these tables today.
- **Observability — the cron tick's outgoing call has two distinct silent-
  failure windows, both harmless today.** `broadcast-dispatch-tick` calls
  `net.http_post` unconditionally every 5 minutes; it does not check for
  pending work first (that's `ENG-038`'s dispatcher function's job, not
  this migration's — this ticket's own Outcome section describes the
  ENG-038-shipped-and-idle case, not the gap here). Window 1, from whenever
  this migration is pushed to the live project until `ENG-038` deploys: the
  call target doesn't exist, every tick 404s. Window 2, from `ENG-038`
  deploying until the `service_role_key` Vault secret is provisioned: the
  call 401s. Neither is visible anywhere today (`net.http_post` is
  fire-and-forget; `cron.job_run_details` shows the tick succeeding
  regardless of the HTTP outcome). Non-blocking: `aiorders-api` has no
  CI/CD auto-deploy, so merging this PR doesn't push the migration live;
  nothing external reaches this path yet, so no user is affected; and the
  gap self-closes once `ENG-038` ships (already `blocks: [ENG-038]`) and
  the secret is provisioned. Named precisely so the resulting log noise
  isn't mistaken for a regression later. Full reasoning:
  `agents/devops/notebook/2026-09-04-release-readiness-log.md`.
- Operational prerequisite, not blocking this ticket or `ENG-038`: the
  `service_role_key` Vault secret doesn't exist yet on the live project.
  Someone with the real key runs one `vault.create_secret(...)` call, once,
  before the first real campaign is expected to send.

## Decision

Filled in by you. (None given — resolved by direct GitHub action.)
`aiorders-api` PR #15 merged directly to `main` (`64baabf`, base `main`, no
stacking) at `2026-09-04T21:19:18Z` — confirmed via `git merge-base
--is-ancestor` on this ticket's own recorded branch against fresh
`origin/main`, cross-checked with `gh pr view`. All four gate receipts
re-read fresh, still `pass`; diff confirmed one file, 148/0 lines, matching
exactly. Ticket carried `blocked → shipped → verified` via receipt
bookkeeping (same route `ENG-031` used — 0 of the parent's acceptance
criteria apply to a schema-only diff, so a full acceptance-check would have
nothing live to check against).

**One correction to this item's own "Named gaps" section, worth stating
plainly rather than leaving stand uncorrected:** the observability note
above reasoned "`aiorders-api` has no CI/CD auto-deploy, so merging this PR
doesn't push the migration live" as part of why Window 1 (the pre-`ENG-038`
404) was non-blocking. This host's linked `supabase` CLI — new capability,
first used on this same ticket — checked the live project directly after
the merge and found the migration **is** live: all three tables exist and
`broadcast-dispatch-tick` is registered and `active` on its 5-minute
schedule. However it reached production, it did — so Window 1 is
confirmed actually happening (a 404 every 5 minutes) rather than merely a
named risk. Still judged non-blocking for every other reason already
given (nothing external reaches the path, no data at risk, self-closes
once `ENG-038` ships); named here so the log noise isn't later mistaken for
a regression. Full detail: `ENG-037`'s own board-file log,
`agents/devops/releases/2026-09-04-aiorders-api-ENG-037.md`. Unblocks
`ENG-038` (`depends_on: [ENG-037]`) — `continue ENG-038` fired this same
pass.
