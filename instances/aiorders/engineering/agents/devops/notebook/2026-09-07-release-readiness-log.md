# Release-readiness log — 2026-09-07

## ENG-044 — `ready-to-ship → blocked`, PR opened

`continue ENG-044` event pass. `skills/release-runner/SKILL.md` run step by
step, same L1 reading this board already established on `ENG-039`/`ENG-040`/
`ENG-041`: step 1 is the clock check only; steps 2-3's readiness content
still runs for L1, minus the window bullet.

**Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies.

**Step 2 (upstream gates) — all four re-read fresh from the receipt files,
not from the ticket log's own account, all passing:**

- `agents/principal-engineer/reviews/ENG-044.md` — `pass`. Function port
  verified byte-for-byte against the real 2024 source; `DROP FUNCTION`
  signature confirmed against the true original; the one live caller traced
  and confirmed unaffected.
- `agents/qa/test-plans/ENG-044.md` — `pass`. AC1 and AC5 (this ticket's own
  owned criteria) covered by inspection, live evidence, and call-site
  trace; no suite exists for `aiorders-api` (open proposal, unrelated to
  this ticket).
- `agents/security/reviews/ENG-044.md` — `pass`, zero findings, blocking or
  non-blocking. Independently re-diffed the ported function against
  `restaurant-marketplace`'s real source; confirmed the channel predicate
  only narrows the pre-existing `approved`/`show_in_marketplace` gate,
  never widens it.
- `agents/database/migrations/ENG-044-foodswipe-channel-visibility-schema.md`
  — `pass`. Live-schema check run before writing the backfill; a real
  Postgres overload-resolution defect caught by testing and closed by a
  leading `DROP FUNCTION IF EXISTS`; both migrations verified end-to-end
  against a disposable replica, both rollbacks actually run.

**Step 3 (readiness gate):**

- *Rollback:* tested, not reasoned — both migrations' rollbacks were
  actually run against a disposable local replica
  (`supabase/postgres:15.8.1.073`) during the `building` hop: the function
  reverts to exactly 13 args with the old call shape still working, and all
  three columns confirmed dropped after migration 1's rollback. Stronger
  position than this repo's own prior releases (`ENG-031`'s `rollback_tested:
  false — reasoned, not drilled`, no replica reachable at the time) — this
  ticket is the first `aiorders-api` migration on this board to actually
  drill both directions.
- *Observability:* read the actual caller rather than assuming one exists
  or doesn't. `aiorders-api/supabase/functions/restaurant-marketplace/handlers/restaurants.ts`'s
  `handleRestaurantDiscovery` — the one live caller of `get_restaurants_optimized`
  today — already wraps the RPC call in error handling: logs
  `console.error('Restaurant discovery error:', error)` and automatically
  falls back to `handleRestaurantDiscoveryFallback` on Postgres error code
  `42883` (undefined function), which is exactly the failure class a bad
  `DROP FUNCTION`/signature mismatch would raise. Pre-existing, not added by
  this ticket, but directly on point given this migration's own tested
  defect class (the overload trap the migration file names in full). The
  disposable-replica testing already done confirms this migration doesn't
  trigger that fallback path — the old 13-arg call shape still resolves to
  exactly one, correct function post-migration. Net position: no new
  reachable behavior exists yet either way (nothing calls with a non-null
  `p_channel` until `ENG-045` ships, same "inert until the sibling ships"
  shape `ENG-031`'s own release used), and the one existing caller already
  degrades gracefully rather than hard-failing if something is still wrong.
- *Cost:* $0/month — same Supabase project, three boolean columns plus one
  function replacement, no new service, no new dependency, no index.
  Matches the design's own `## One-way doors` table ("Recurring cost:
  None"), not a fresh judgment call.
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
re-checked fresh, not assumed unchanged since the security hop: `git fetch
origin main` current, `HEAD` at `81350d4` matching every gate's cited head
and the ticket's own frontmatter, `git diff origin/main...HEAD --stat`: 2
files, 273 insertions, 0 deletions — exactly the two migration files, no
drift. Only the same long-standing untracked
`supabase/functions/brand-portal/deno.lock` present (`ENG-029`/`ENG-031`/
`ENG-037`/`ENG-044`'s own `building` hop have each already left it alone).
`gh pr list --head feat/ENG-044-foodswipe-channel-visibility-schema` — empty,
confirmed no PR already existed for this branch.

Opened `aiorders-api` PR #19
(https://github.com/harsimranwalia/aiorders-api/pull/19). Body: what
changed, what it deliberately doesn't do, the disposable-replica test
evidence (including the overload-trap defect and its fix), what to review
hardest (the `DROP FUNCTION IF EXISTS` line), and the four gate receipts
with paths.

Wrote `inbox/2026-09-07-eng044-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: a few hours` set on the item, mirroring the
ticket's own field. `lib/eng-notify.sh raise` exited 0, confirmed sent from
the log (`traces/eng-notify-2026-09-07.log`: `sent: active
2026-09-07-eng044-merge-request.md`, `03:48:06`); stamped `notified:
2026-09-07T03:48:06` on the item by hand, copied verbatim from the log,
same standing practice this file's own prior entries use.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy (a
manual migration push/`supabase functions deploy` after merge, same by-hand
pattern every prior `aiorders-api` release on this board has shown, no
tracked CI/CD on this repo) and the release record both wait for merge
detection on a future pass, per the skill's own step 4 L1 row / step 7
split.

**Machine WIP: checked, unaffected.** `ENG-044` is one of four `ENG-026`
sub-tickets, and this board's own established reading (`ENG-016`'s,
`ENG-019`'s, `ENG-021`'s decompositions) holds the `1/1` slot at the
*family* level, not per row. `ENG-026` itself is still `building`, and
`ENG-045`/`ENG-046` (both `depends_on: [ENG-044]` alone) stay `ready` —
that dependency clears on `verified`, not on `blocked_on: approver` (the
bar `ENG-031 → ENG-032` already set, and the one this ticket's own
`blocks:` field inherits). So the slot is still occupied by family members
inside the counted `ready..ready-to-ship` range, and the "never idle"
slot-freed provision (`eng_build_loop.md` Guards, amended 2026-09-06) — which
frees a slot held by a *single* ticket parking on the approver — doesn't
apply to this hop. Nothing new dispatched. `ENG-047` (depends on `ENG-045`)
is two hops further out regardless.

**This is `ENG-026`'s first sub-ticket.** Once this PR merges, a future
pass's step-5 merge detection carries `ENG-044` to `shipped`/`verified`,
which then clears `ENG-045`'s and `ENG-046`'s shared dependency — both are
candidates to dispatch at that point, machine WIP allowing. Not this hop's
to process; noted so the next hop that finds `ENG-044` merged knows to
check both.

## ENG-048 — `ready-to-ship → blocked`, PR opened

`continue ENG-048` event pass. `skills/release-runner/SKILL.md` run step by
step, same L1 reading this file already established: step 1 is the clock
check only; steps 2-3's readiness content still runs for L1, minus the
window bullet.

**Step 1 (window):** `aiorders-api` is L1 — no window check applies.

**Step 2 (upstream gates) — all four re-read fresh from the receipt files:**
`agents/principal-engineer/reviews/ENG-048.md` (pass, round 2),
`agents/qa/test-plans/ENG-048.md` (pass, round 2),
`agents/security/reviews/ENG-048.md` (pass, zero blocking findings),
`agents/database/migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`
(pass).

**Step 3 (readiness gate):**

- *Rollback:* tested twice against a disposable local replica
  (`supabase/postgres:15.8.1.073`), pre- and post-`CONCURRENTLY` fix, both
  confirmed clean.
- *Observability — read the actual cron body rather than the ticket's own
  "no-op-by-construction" framing of it.* `loyalty-auto-complete-tick`
  calls `net.http_post` **unconditionally** on every 15-minute fire — the
  cron body itself does not check for eligible rows first (that's
  `ENG-049`'s own claim-query responsibility, not this migration's). Until
  `ENG-049` deploys the `loyalty-auto-complete` edge function, every tick
  404s at Supabase's edge-routing layer, and this is invisible today:
  `net.http_post` is fire-and-forget (`pg_net` queues it and returns
  immediately; the response lands in `net._http_response`, which nothing
  reads), and `cron.job_run_details` records the *tick* as succeeded
  regardless of what the HTTP call itself returned — the identical
  mechanism named in this file's own `ENG-037` entry above. Unlike
  `ENG-037`'s two-window case, there is exactly **one** window here: the
  `service_role_key` Vault secret this job authenticates with already
  exists live (confirmed this pass), so only the endpoint is missing, not
  the secret.
  **Judged non-blocking, same three-part reasoning this file's own
  `ENG-037`/`ENG-038` entries already established:** (a) `aiorders-api`
  carries no CI/CD auto-deploy (`find .github` in the worktree: no
  `.github/workflows/`) — merging this PR does not push the migration
  live; someone runs `supabase db push` as a separate, deliberate act,
  outside this hop's and this ticket's own scope. (b) Nothing external
  reads or writes `loyalty_ledger_entries` or either new `orders` column
  yet — no user who could be affected or could complain. (c) The gap is
  bounded and already tracked: it closes the moment `ENG-049` ships
  (`ENG-048.blocks: [ENG-049]`, next in this exact sequence). Named
  precisely (one window, not the two `ENG-037` had) in both the PR body and
  the merge-request item, so whoever eventually pushes this live isn't
  confused by resulting 404 log noise, and so `ENG-049`'s own gates inherit
  the accurate picture rather than a copy-pasted two-window one.
- *Cost:* $0/month. No new paid infrastructure — `pg_cron`/`pg_net` and
  Vault already in live use on this project; one new table, two nullable
  columns, and four indexes are storage-negligible at low row counts; a
  404'd `net.http_post` call invokes no billable compute.
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
re-checked fresh: `git fetch origin main` current; `git diff
origin/main...HEAD --stat` confirms the same one-file, 265-line diff, no
drift from any prior gate's own account. Only the same two long-standing
untracked `deno.lock` files present (`brand-portal`,
`restaurant-marketplace` — unrelated pre-existing work, not this branch).
`gh pr list --head feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron
--state all` — empty, confirmed no PR already existed for this branch.

Opened `aiorders-api` PR #21
(https://github.com/harsimranwalia/aiorders-api/pull/21). Body: what the
migration does, the round-1→round-2 fix history (B1 access control via the
project's own `pg_default_acl` mechanism, B2 negative-amount floor), all
four gate receipts with paths, the one uncorroborated-live claim
(`bill.cart`/`discount` unit), what to review hardest, the observability
finding above in full, and cost.

Wrote `inbox/2026-09-07-eng048-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: half a day` set on the item, mirroring the
ticket's own field. `lib/eng-notify.sh raise` run — `traces/eng-notify-2026-09-07.log`
confirms `sent: active 2026-09-07-eng048-merge-request.md` at `16:18:23`,
copied verbatim into the item's own `notified:` field.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy and the
release record both wait for merge detection on a future pass, per the
skill's own step 4 L1 row / step 7 split.

**Slot freed — chained the family's own next child, per the Guards
amendment dated this same day, not the ENG-044/045/046 misreading it
exists to correct.** `ENG-048` leaving the `ready..ready-to-ship` range
frees the `ENG-027` family's machine slot. `ENG-049`
(`parent: ENG-027`, `depends_on: [ENG-048]`) is that family's next and only
remaining child, sitting `ready`. Its dependency is satisfied now that
`ENG-048` has an open PR (`blocked_on: approver`) — it does not wait for
`ENG-048` to reach `verified`. Confirmed startable (no `hold`, no unmet
dependency, no open scope question) and fired `continue ENG-049` before
this pass exited; full reasoning and queue confirmation on `ENG-048`'s own
board-file log, this date. Not this hop's to build — `ENG-049` branches off
`ENG-048`'s own PR branch as a stacked PR in whichever fresh session picks
up that fire.

## ENG-049 — `ready-to-ship → blocked`, PR opened

`continue ENG-049` event pass. `skills/release-runner/SKILL.md` run step by
step, same L1 reading this file already established: step 1 is the clock
check only; steps 2-3's readiness content still runs for L1, minus the
window bullet.

**Step 1 (window):** `aiorders-api` is L1 — no window check applies.

**Step 2 (upstream gates) — all three re-read fresh from the receipt
files, not from the ticket log's own account, all passing:**

- `agents/principal-engineer/reviews/ENG-049.md` — round 2, `verdict: pass`.
  Round 1 passed clean (0/10 automatic failures); round 2 re-reviewed the
  security-fix commit only.
- `agents/qa/test-plans/ENG-049.md` — round 2, `last_result: pass`, 45/45
  across three suites, all six fully-owned ACs and the webhook/sweep/dine-in
  half of seven more covered, 0 open P0/P1.
- `agents/security/reviews/ENG-049.md` — round 2, `verdict: pass`. Round 1
  failed on one critical finding (unauthenticated CloudWaitress webhook);
  the fix passed round 2 clean, independently re-verified against the
  finding's own requirement, not any prior hop's account.

No migration owed — confirmed `agents/database/migrations/` has no
`ENG-049-*.md`, correct for a diff that's Deno/TS only (`git diff
origin/feat/ENG-048-...cron...HEAD --stat`: 12 files, no `*.sql`); the
schema is `ENG-048`'s own.

**Step 3 (readiness gate):**

- *Rollback:* reasoned, not drilled — this ticket's own diff carries no
  migration (schema is `ENG-048`'s), so reverting the merge removes these
  code paths going forward, same shape `ENG-039`'s/`ENG-040`'s own hops on
  this board already used for a pure-code diff. One asymmetry worth naming
  rather than treating as a gap: a loyalty entry already credited before a
  revert is not retroactively undone — the ticket's own Notes already name
  this as an accepted design property (a human correction is a future
  ticket's own surface, `AC16`'s cancellation-never-touches-the-ledger
  design), not something this hop is discovering fresh.
- *Observability — the one that actually matters this time, checked live,
  not reasoned.* `agents/security/reviews/ENG-049.md`'s own round-2 verdict
  named this explicitly as carried forward to this exact hop: whether
  `CLOUDWAITRESS_WEBHOOK_SECRET` is provisioned. Checked directly against
  the live store, not assumed: `supabase secrets list --project-ref
  bmnmnejwdxbcqinqkwko` — 34 entries, none named `CLOUDWAITRESS_WEBHOOK_SECRET`.
  **Read the actual code before characterizing the blast radius**, rather
  than taking the security receipt's own description on trust:
  `supabase/functions/external-integrations/handlers/cloudwaitress.ts:325` —
  `verifyCloudWaitressSecret(webhookData)` runs immediately after
  `request.json()`, strictly before the structural-validation check, the
  terminal-event branch, and the `order_new` branch. This means an unset
  secret doesn't just leave loyalty crediting unauthenticated — it fails
  every single CloudWaitress webhook call closed (`verifyCloudWaitressSecret`
  returns `false` whenever `Deno.env.get(...)` is empty), including plain
  `order_new`. **This is materially more severe than `ENG-039`'s own
  `BROADCAST_UNSUBSCRIBE_SECRET` gap** (that one degraded one channel per
  message, loudly, and logged); this one would stop all CloudWaitress order
  intake cold the moment this code deploys, silently from the caller's
  perspective (CloudWaitress just sees every webhook 401). **Judged
  non-blocking for opening this PR specifically** — same reasoning
  `ENG-039`'s hop established: `aiorders-api` has no CI/CD auto-deploy
  (`find .github` in the worktree: no `.github/workflows/`), so merging
  this PR does not push it live; the actual `supabase functions deploy` is
  a separate, deliberate, manual act that hasn't happened and isn't this
  hop's to perform. But **this is a hard pre-deploy requirement, not a
  "known limitation to live with"** the way the unsubscribe gap was — named
  at maximum prominence in both the PR body and the merge-request item
  (not just here), with the exact value to set named by file reference
  (`cloudwaitress-middleware/handlers/restaurant.ts`'s own
  `AIORDERS_WEBHOOK.secret`, deliberately not reproduced in either the PR
  or the merge-request item — it's a live production credential and the PR
  is a more exposed surface than this internal notebook). This department
  does not provision production secrets unilaterally (same boundary
  `ENG-039`'s own hop already established for `BROADCAST_UNSUBSCRIBE_SECRET`);
  whoever runs the eventual deploy needs to set this first or in the same
  step, not after.
  Separately: this PR is also what closes `ENG-048`'s own already-named
  observability gap (the cron 404ing every 15 minutes, since the endpoint
  it calls didn't exist) — once both PRs are merged and actually deployed,
  not before.
- *Cost:* $0/month — same Supabase project, no new infrastructure; the
  cron itself is `ENG-048`'s own, already scheduled and already counted
  there.
- *Window:* n/a, L1.

No blocking readiness failure for opening the PR. The webhook-secret gap is
a hard blocker for the *deploy*, named accordingly, not for the PR.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
checked fresh: `git fetch origin`, `HEAD` at `0bec87c` matching every gate's
cited head and the ticket's own frontmatter, only the three already-known
untracked `deno.lock` files present (`brand-portal`, `loyalty-auto-complete`,
`restaurant-marketplace`) — no prior pass died mid-work. `ENG-048`'s own PR
#21 re-confirmed live (`gh pr view 21 --json state,baseRefName,headRefName,mergedAt`):
still `OPEN`, base `main`, not merged — this PR correctly stacks on its
branch rather than `main`. `git diff
origin/feat/ENG-048-...cron...HEAD --stat`: 12 files, 1422 insertions, 31
deletions — matches every prior gate's own account. `gh pr list --head
feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api --state
all` confirmed no PR already existed for this branch.

Opened `aiorders-api` PR #22
(https://github.com/harsimranwalia/aiorders-api/pull/22), base set to
`ENG-048`'s own branch (PR #21, still open) — a stacked PR, per this
ticket's own Notes and `eng_build_loop.md` Guards. Body: what changed, the
webhook-secret pre-deploy requirement in full (above), all three gates
passed with receipt paths, the round-1→round-2 security fix history, the
self-test summary, the `readBalance` correctness fix, non-blocking findings,
and what's out of scope.

Wrote `inbox/2026-09-07-eng049-merge-request.md`, plain `pr_url:` string
(single repo), the webhook-secret requirement repeated at the top of the
item (not just buried in the PR). `time_estimate: a day to a couple of
days` set on the item, mirroring the ticket's own field. `lib/eng-notify.sh
raise` exited 0; confirmed sent from the log
(`traces/eng-notify-2026-09-07.log`: `sent: active
2026-09-07-eng049-merge-request.md`, `18:44:54`); stamped `notified:
2026-09-07T18:44:54` on the item by hand, copied verbatim from the log,
same standing practice this file's own prior entries use.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy (a
manual `supabase functions deploy` after merge, same by-hand pattern every
prior `aiorders-api` release on this board has shown) and the release
record both wait for merge detection on a future pass, per the skill's own
step 4 L1 row / step 7 split. **The eventual deploy hop must not skip the
webhook-secret check above** — flagging here too, not only in the PR/merge
item, so whichever future hop actually runs `supabase functions deploy`
finds it in this file's own running account rather than having to
rediscover it from the PR alone.

**Slot freed, and this time nothing filled it.** `ENG-049` was the last of
`ENG-027`'s two sub-tickets (`ENG-048` → `ENG-049`, a strict chain, no third
child) — with both now `blocked_on: approver`, the family holds no child in
the counted `ready..ready-to-ship` range, so per `eng_build_loop.md` Guards
(amended 2026-09-07, part (b)) the slot is free and there is no next
sibling to fill it with. Checked the top of To-do (the only place a new
start is drawn from, step 6): `ENG-018`, `ENG-028`, `ENG-042` (all
`awaiting-scope`) and `ENG-043` (`intake`) are the only occupants, and each
one's own G1/clarification is already sitting in `inbox/` unanswered
(confirmed by grepping each item for a `decision:` field — none present).
Nothing there is startable. Not extended to the `designed`-state backlog
the way `ENG-019`'s/`ENG-020`'s/`ENG-021`'s/`ENG-026`'s own dispatches once
did — that pool is outside `eng_build_loop.md` step 6's own literal
definition of To-do ("intake, shaped or awaiting-scope... the only place a
new start is drawn from"), a discrepancy between that written rule and this
board's own repeated past practice worth a proposal, not a fourth quiet
repetition of it (filed, `proposals.md`, this date). Wrote the one
permitted "Nothing I can start" item, `inbox/IDLE-2026-09-07.md` — no
other such item was already open. `lib/eng-notify.sh raise` exited 0,
confirmed sent (`18:44:54`, same log), stamped by hand.

`chained: none — idle: nothing startable` on `ENG-049`'s own log — not
`chained: none — blocked_on: approver`, which this step may not write per
the Guards amendment. Full reasoning: `ENG-049`'s own board-file log.
