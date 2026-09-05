# Release-readiness log — 2026-09-04

## ENG-034 — `ready-to-ship → blocked`, PR opened

`skills/release-runner/SKILL.md` run step by step. Reasoning moved here per
`config/conventions.yaml` → `ticket_log.entry.cap_lines: 20` — a `pass`
release-readiness hop isn't in `over_cap_allowed_when`, so the ticket log
gets facts and pointers only; this file gets the rest.

**Step 1 (window):** `config-site-builder` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies. Read step 1's own "skip
this step entirely and go to step 4" instruction against step 3's own
bullet list, which scopes only its *window-closed* bullet to "L2/L3 only" —
pointless scoping if step 3 never ran for L1 at all. Resolved: step 1 (the
clock check) is what's skipped; steps 2–3's readiness content still runs,
minus the window bullet. Matches this board's own practice on every L1
release-readiness hop to date (`ENG-007`, `ENG-008`, `ENG-013`, `ENG-022`,
`ENG-031`, `ENG-033`) — none of them skipped straight to step 4 either, so
this reading was already the department's revealed behavior, just not
previously written down as a deliberate reading of the text.

**Step 2 (upstream gates):** re-read fresh from the receipt files, not the
ticket log's own account — `agents/principal-engineer/reviews/ENG-034.md`
(`verdict: pass`, round 1, 0/10 auto-fail), `agents/qa/test-plans/ENG-034.md`
(`last_result: no suite` — expected, not a red flag: `config-site-builder`
has no test runner of any kind, confirmed fresh — no `test` script, no
test-framework dependency, zero `*.test.*`/`*.spec.*` files; every AC this
ticket owns is manual verification with a reason, under
`definition-of-done.md`'s allowance), `agents/security/reviews/ENG-034.md`
(`verdict: pass`, round 1, zero findings). No migration applies — frontend-
only diff, no schema/data-layer surface touched.

**Step 3 (readiness gate):**

- *Rollback:* single commit (`62b3ca0`), no migration, no stored-state
  change — reverting the commit (or the merge, once merged) fully and
  safely undoes it. `config-site-builder` has no test command, so — same
  position `ENG-005` (`aiorders-admin-hub`, same L1/Cloudflare/no-test-
  runner shape) already established — there's nothing to drill-run a
  rollback against; named as a gap, not assumed clean. First
  release-readiness pass ever run against `config-site-builder`
  specifically (checked: `agents/devops/releases/` has no prior file for
  this project), so this is a fresh application of the `ENG-005` precedent,
  not a copy of an existing same-project record.
- *Observability:* no new fetch/network call of its own (security gate's
  own grep, zero hits, independently not re-run here) — POSTs through
  `ENG-033`'s already-shipped, already-observed `catering-request` endpoint
  unchanged. The one new client-side failure mode (code review's F1 —
  `SubmitEvent.submitter` has no fallback) fails open silently rather than
  loudly; a named gap, not a monitored path, and there's no server-side
  surface on this ticket's own diff to instrument.
- *Cost:* $0/month — no new dependency (`lucide-react` confirmed
  pre-existing at both the code-review and security gates), no new
  infrastructure, no new vendor.
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/config-site-builder`)
re-checked, not assumed unchanged — still only the same 2-line
`package-lock.json` version-metadata diff outside the reviewed commit
range (npm's own install normalization, already traced by two prior gate
hops), left alone again. `git fetch` + `git rev-list --left-right --count
origin/main...HEAD`: 0 behind, 1 ahead (`62b3ca0` only) — no drift.
`git ls-tree -r origin/main --name-only | grep -i workflow`: no hits —
confirmed directly (not assumed from `aiorders-admin-hub`'s own `ENG-005`
precedent, even though the stack shape matches) that `origin/main` carries
no GitHub Actions auto-deploy; `deploy-cf`/`deploy-all` are manual,
explicitly-invoked `npm` scripts, so opening this PR carries no risk of an
unreviewed auto-deploy. `gh pr list --head
feat/ENG-034-catering-menu-selector-public-form --state all` confirmed no
PR already existed for this branch.

Opened `config-site-builder` PR #4
(https://github.com/harsimranwalia/config-site-builder/pull/4). Body: what
the picker does, the gate expression, the AC-9 byte-identical-when-closed
property, the three gates passed, and all four non-blocking code-review
findings (F1: `SubmitEvent.submitter` no fallback; F2: `||` vs `??` on one
label fallback; F3: duplicated loading-spinner JSX; F4: `CateringForm.tsx`
now 540 lines) plus the two named pre-existing conditions (no upper bound
on `quantity`/`selections[].name` length — the latter already `ENG-033`
Finding 2; native-`required`-only enforcement on `email`/`requirements`).

Wrote `inbox/2026-09-04-eng034-merge-request.md`, plain `pr_url:` string
(single repo, no `pr_urls:` list needed) per
`skills/release-runner/SKILL.md` step 4. `time_estimate: ~1.5-2 days` set on
the item, mirroring the ticket's own field. `lib/eng-notify.sh raise` run —
logged `sent: active 2026-09-04-eng034-merge-request.md` in
`traces/eng-notify-2026-09-04.log` at `10:01:49`; stamped `notified:
2026-09-04T10:01:49` on the item by hand (copied verbatim from the log,
matching this board's own already-flagged local-time-labeled-as-UTC
convention — `proposals.md`, 2026-09-02).

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy and the
release record both wait for merge detection on a future pass, per the
skill's own step 4 L1 row / step 7 split.

**Compliance note on this entry itself.** `ENG-034`'s own build hop
(2026-09-04) filed an observation
(`agents/eng-manager/observations.md`, this date) that `ENG-031`/`ENG-032`/
`ENG-033`'s build-hop log entries all violated `cap_lines: 20`, and wrote
its own build-hop entry short as a self-correction. This ticket's own
*next two hops* (code review + quality, then security) both reverted to
long-form ticket-log entries anyway — the self-correction didn't even hold
across hops on the same ticket, let alone propagate to other tickets. This
release-readiness hop follows the convention (short entry, full reasoning
here) and files a proposal — not a fourth observation — recommending
`lib/eng-gate-check.sh` catch this mechanically, since prose-only reminders
have now been named three separate times (2026-09-03 ×2, 2026-09-04 ×1)
without the drift stopping. See `agents/eng-manager/proposals.md`,
2026-09-04, eng-manager row.

## ENG-037 — `ready-to-ship → blocked`, PR opened

`continue ENG-037` event pass. `skills/release-runner/SKILL.md` run step by
step, same reading already established on this project's own file above
(step 1 is the clock check only; steps 2-3's readiness content still runs
for L1, minus the window bullet).

**Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies.

**Step 2 (upstream gates):** re-read fresh from the receipt files, not the
ticket log's own account. `agents/principal-engineer/reviews/ENG-037.md`
(`verdict: pass`, round 1, 0/10 auto-fail). `agents/qa/test-plans/ENG-037.md`
(`Verdict: PASS`, round 1). `agents/security/reviews/ENG-037.md`
(`verdict: pass`, round 1, 0 blocking). This ticket also owes a migration
plan receipt (schema-only diff) —
`agents/database/migrations/ENG-037-broadcast-campaigns-schema-and-dispatch-cron.md`,
own `## Gate verdict: pass.` section, re-read fresh. All four present and
passing.

**Step 3 (readiness gate):**

- *Rollback:* tested, not just documented — the build hop actually executed
  `cron.unschedule` + three `drop table` statements against a disposable
  local Postgres replica and confirmed a clean post-drop state (migration
  plan doc, "Rollback" section). Stronger evidence than `ENG-034`'s own
  precedent on this exact log (no test runner to drill against there); this
  project at least has a real replica this session could run the rollback
  against.
- *Observability — the one point worth a full write-up.* Read the actual
  migration SQL directly rather than trusting this ticket's own Outcome
  section, which frames the cron tick as "finds empty tables and no-ops."
  That framing is imprecise: `broadcast-dispatch-tick` calls `net.http_post`
  unconditionally on every 5-minute fire — nothing in the cron body queries
  `broadcast_campaign_recipients` first. The empty-queue no-op is
  `ENG-038`'s own dispatcher function's responsibility, not something this
  migration's cron body does itself. Consequence: two distinct silent-
  failure windows exist, not one —
  (1) from whenever this migration is actually pushed to the live project
  until `ENG-038` deploys `broadcast-dispatch`, the call target doesn't
  exist at all and every tick 404s at Supabase's edge-routing layer;
  (2) from when `ENG-038` deploys until someone provisions the
  `service_role_key` Vault secret, the call reaches a real function that
  401s (the scenario the ticket's own drafted PR-body notes already named —
  accurate, but only for window 2, not window 1). Neither window is
  observable anywhere today: `net.http_post` is fire-and-forget (Postgres
  queues it via `pg_net` and returns immediately; the response lands in
  `net._http_response`, which nothing reads), and `cron.job_run_details`
  records the *tick* as succeeded regardless of what the HTTP call itself
  returned.
  **Judged non-blocking, not a readiness-gate failure, for three reasons
  specific to this ticket:** (a) `aiorders-api` carries no CI/CD auto-deploy
  — `git ls-tree -r origin/main --name-only | grep -i workflow` and a direct
  `find .github` in the worktree both confirm no `.github/workflows/`
  exists at all — so merging this PR does not itself push the migration
  live; someone runs `supabase db push` (or equivalent) against the linked
  project as a separate, deliberate act, outside this hop's and this
  ticket's own scope entirely. (b) Nothing external reaches this path yet —
  no UI, no API consumer of these tables exists before `ENG-038`/`ENG-039`
  — so there is no user who could be affected or could complain, which is
  the literal test `skills/release-runner/SKILL.md` step 3 states for this
  criterion. (c) The gap is bounded and already tracked: it closes the
  moment `ENG-038` ships (`ENG-037.blocks: [ENG-038]`, next in this exact
  sequence) and the secret is provisioned. Named precisely — both windows,
  not just the already-documented one — in the PR body's own "Uncertainties"
  section, so whoever eventually pushes this live isn't confused by
  resulting 404/401 log noise, and so `ENG-038`'s own gates inherit the
  accurate picture rather than the ticket's own slightly-imprecise framing.
  One observation filed (`observations.md`, this date) on the general
  pattern — a poller-shaped cron that always fires and leaves the "is there
  work" check to the callee is exactly right, but this repo's *documentation
  style* of describing that as the tick itself "finding nothing and no-oping"
  is loose enough to mislead the next reader; worth tightening the prose
  convention for the next ticket in this exact shape (the security gate's
  own finding already flagged this precedent will recur).
- *Cost:* $0/month. No new paid infrastructure — `pg_cron`/`pg_net` already
  in live use (`platform_analytics_cron`) and Vault already live
  (`resend_api_key`); three new tables and five new indexes are
  storage-negligible at zero rows; `net.http_post` calls that 404/401 at the
  routing/auth layer invoke no billable compute.
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
re-checked fresh, not assumed unchanged since the security hop: `git status`
clean but for the same long-standing untracked `deno.lock`; `git fetch
origin main` current; `git diff origin/main...HEAD --stat` confirms the
same one-file, 148-line diff (`59e9670`). `gh pr list --head
feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron --state all`
confirmed no PR already existed for this branch.

Opened `aiorders-api` PR #15
(https://github.com/harsimranwalia/aiorders-api/pull/15). Body: what the
migration does, the three gates plus the migration-plan receipt, the two
non-blocking code-review findings (F1: `step_id` FK has no dedicated index;
F2: `scheduled_send_at` nullable with no tie to `status`), the two
non-blocking security notes (RLS-zero-policy not a repeat of the
`ENG-015`/`ENG-031`/`ENG-033` pattern; no rate/audience cap, routed to
`ENG-038`), and the observability finding above in full, precise form (both
failure windows, not just the previously-drafted one).

Wrote `inbox/2026-09-04-eng037-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: ~half a day` set on the item, mirroring the
ticket's own field. `lib/eng-notify.sh raise` run — see the ticket log's own
`notified:` stamp and `traces/eng-notify-2026-09-04.log` for the exact time.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy and the
release record both wait for merge detection on a future pass, per the
skill's own step 4 L1 row / step 7 split.

## ENG-038 — `ready-to-ship → building`, returned for a missing migration gate

`continue ENG-038` event pass. `skills/release-runner/SKILL.md` run step by
step, same reading already established on this project's own file above
(step 1 is the clock check only; steps 2-3's readiness content still runs
for L1, minus the window bullet).

**Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies.

**Step 2 (upstream gates) — the check that failed.** Re-read fresh from the
receipt files, not the ticket log's own account.
`agents/principal-engineer/reviews/ENG-038.md` (round 6, `Verdict: PASS`).
`agents/qa/test-plans/ENG-038.md` (round 6, `Verdict: PASS`, 85/85).
`agents/security/reviews/ENG-038.md` (round 2, `Verdict: PASS`, both
round-1 findings closed). All three genuine and independently re-verified
against the underlying receipts, not assumed from the ticket log's own
summary of them.

**But this ticket also owes a migration verdict, and none exists.** The
ticket's own `building` hop (`owner: backend`, per its board-file log)
wrote `supabase/migrations/20260904150000_broadcast_recipients_claimed_status.sql`
directly — read in full this pass at
`~/Documents/projects/_eng/aiorders-api/supabase/migrations/`, not taken on
the review/security receipts' word for its contents. It: (1) drops and
recreates `broadcast_campaign_recipients_status_check` to add `'claimed'`;
(2) adds `broadcast_campaign_recipients_step_id_idx`, a new btree index;
(3) adds a new check constraint, `broadcast_campaigns_scheduled_requires_time`,
on a *different* table. Real schema surface, not a cosmetic rename.

No `agents/database/migrations/ENG-038-*.md` exists (confirmed:
`ls agents/database/migrations/` lists `ENG-006` through `ENG-037`, no
`ENG-038`). No board-file log entry anywhere on this ticket attributes any
hop to `database`. Compare `ENG-037`/`ENG-031` — this board's two other
migration-carrying tickets — both of which show `building → in-review
(database/principal-engineer-adjacent...)` in their own logs and both of
which have their own `agents/database/migrations/{id}-*.md` plan doc,
written *before* review, with the rollback actually executed against a
disposable Postgres replica/container and confirmed clean. `ENG-038`'s own
migration's rollback exists only as a trailing SQL comment — never run.
(Checked whether `links.migration` is even a tracked frontmatter key on
this board before treating its absence as evidence: it isn't — `ENG-037`'s
own frontmatter, the ticket that *is* the migration, has no `links.migration`
key either. Dropped that thread; the real evidence is the missing receipt
file and log entry, not a frontmatter key this template never carries.)

This is not a paperwork gap. `agents/backend/agent.md`'s own `never_touches`
list names exactly this: "schema design or migrations (database owns those
— you request, they design)" — backend wrote this migration itself rather
than requesting it, and the ticket's own build-hop log entry says so
plainly ("a new migration... ENG-037's schema deliberately left this to
this ticket"), without ever routing it to `database`. `config/conventions.yaml`
(department root) names "code review, migration, quality, release
readiness, security" as five separate blocking machine gates — migration is
not a sub-item of code review — and `agents/database/agent.md` names "the
migration gate" as `database`'s own exclusive scope, distinct from what
principal-engineer or security checked incidentally while reading the same
file for their own purposes (constraint legality; whether `'claimed'`
closes their own authz finding). Neither of those is "forward-only and
reversible, rollback tested not assumed, indexes justified, backfill plan"
(`definition-of-done.md`'s Data checklist, `database`'s own stated
criteria), and neither agent claims to have checked those.

`skills/release-runner/SKILL.md` step 2, verbatim: "A missing verdict is a
fail, not an assumption — return the ticket to the gate that never ran."
That is what this hop does.

**Step 3 (readiness gate) — checked anyway, for what it's worth while step
2 already fails.** Read `broadcast-dispatch/dispatch.ts` in full to assess
observability on the one gap the migration's own comment names (a
recipient row stuck at `status = 'claimed'` if the process is killed
between the atomic claim and the try block that resolves it — no automatic
recovery sweep exists). Every *reachable* failure path already logs
(`console.error`) and marks a terminal status via `markRecipient` —
`resolveRecipient`'s own catch-all included. The only truly unmonitored
edge is a hard process kill mid-claim, which no application code can catch
by definition; it's self-diagnosable via the exact query the migration's
own comment already gives (`select * from broadcast_campaign_recipients
where status = 'claimed' and created_at < now() - interval '1 hour'`), and
it's bounded (a missed send, not data loss or a security exposure). Judged
non-blocking on its own, consistent with how `ENG-037`'s own
release-readiness hop treated a similar dispatcher-side gap. **Not the
reason this ticket is returned** — named for completeness, since step 2
already fails independently and a future re-run of this hop shouldn't have
to re-derive it.
*Cost:* $0/month, unaffected by the migration-gate question either way — no
new infrastructure regardless of what `database`'s own gate concludes.
*Window:* n/a, L1.

**Step 4 not reached.** No PR opened, no merge request raised —
release-readiness does not pass while step 2 owes a verdict.

**Disposition:** `ready-to-ship → building`, `owner: devops → database`.
Not `blocked`: no ticket on this board has ever used `blocked` for an
unmet gate verdict (only for an external wait — an L1 PR, a question only
the approver can answer), and `building` is where `ENG-037`'s and
`ENG-031`'s own `database` work already happened, before their own
`in-review` hop — the precedented home for exactly this kind of work, not
a new state invented for this ticket. Whether `database`'s own gate pass,
once it runs, requires anything beyond writing the missing receipt
(re-testing the existing SQL against a disposable replica, confirming the
rollback executes clean, confirming the new index/constraint are
justified) — or turns up something that changes the migration file itself,
which would put the ticket back through `in-review` for that diff alone —
is for that hop to determine, not assumed here either way.

Proposal filed (`proposals.md`, this date): no mechanical check anywhere in
`lib/eng-gate-check.sh` catches a migration file with no matching
`agents/database/migrations/` receipt before `ready-to-ship`/`shipped` —
confirmed directly, both the scoped (`ENG-038`) and whole-board pre-pass
`eng-gate-check.sh` runs this hop made exited 0 clean despite the gap
already existing at that point. Related to, but a distinct mechanism from,
the existing 2026-09-03 principal-engineer proposal on the same file
(fast-lane design never triggering `schema-change/SKILL.md`) — that one is
about the lane never firing the trigger; this one is about the trigger
being available on a full-lane ticket and nothing enforcing that `backend`
use it instead of writing the schema itself.

## ENG-038 (round 2) — `ready-to-ship → blocked`, PR opened

`continue ENG-038` event pass, fired by the migration-gate hop's own
`chained: ENG-038`. `skills/release-runner/SKILL.md` run step by step, same
L1 reading established on this project's own file above.

**Step 1 (window):** `aiorders-api` is L1 — no window check applies.

**Step 2 (upstream gates) — all four re-read fresh from the receipt files,
not from the ticket log's own account, and all still passing:**

- `agents/principal-engineer/reviews/ENG-038.md` — round 6, `verdict: pass`,
  0/10 automatic failures.
- `agents/qa/test-plans/ENG-038.md` — round 6 (security-fix follow-up),
  `Verdict: PASS`, 85/85, all seven ACs.
- `agents/security/reviews/ENG-038.md` — round 2, `verdict: pass`, both
  round-1 blocking findings (unauthenticated arbitrary-content send; no
  audience/interval cap) verified closed against the code and schema
  directly.
- `agents/database/migrations/ENG-038-broadcast-recipients-claimed-status.md`
  — `Gate verdict: pass`, written by the immediately-prior hop this pass
  chains from. Additive-only, rollback actually executed against a
  disposable replica and behaviourally re-verified (not just "ran clean").

No gap this round — the one that returned round 1 is closed.

**Step 3 (readiness gate):**

- *Rollback:* the migration's own rollback is the real risk surface here
  (code changes ship as a PR, not a deploy, for L1) — already tested per
  the migration receipt above. Nothing else to drill: no deploy happens in
  this hop.
- *Observability — two points, one carried forward, one newly confirmed
  live.*
  1. **Carried forward, re-confirmed unchanged since round 1's own check**
     (no code touched this ticket's dispatcher since then): a recipient row
     stuck at `status = 'claimed'` if the process is killed between the
     atomic claim and the send resolving. No automatic recovery sweep;
     self-diagnosable via the query the migration file's own comment gives;
     bounded to a missed send, not data loss or exposure. Judged
     non-blocking, same reasoning as round 1's return hop.
  2. **New this round, checked directly against the live project rather
     than left as a named risk:** `supabase functions list
     --project-ref bmnmnejwdxbcqinqkwko` — no `broadcast-dispatch` or
     `broadcast-unsubscribe` function deployed. `supabase db query "select
     jobname, schedule, active from cron.job where jobname =
     'broadcast-dispatch-tick'" --linked` — `active: true`,
     `*/5 * * * *`. This confirms `ENG-037`'s own release-readiness hop's
     after-the-fact correction (board index, `ENG-037`'s closing
     paragraph): Window 1 (the pre-`ENG-038` 404) isn't just a named risk,
     it has been actually happening, every 5 minutes, since `ENG-037`
     merged (~14:19 PDT today) and is still happening as of this hop
     (~21:03 PDT). Did not chase the exact status code per tick —
     `cron.job_run_details` shows the tick's own SQL statement succeeding
     regardless of the outbound HTTP result (already-documented gap,
     `net.http_post` is fire-and-forget), and `net._http_response` mixes
     in responses from this project's other cron jobs with no reliable way
     to attribute a given row to this call specifically without deeper
     forensics than this hop's own question needs. **Judged non-blocking,
     same three reasons `ENG-037`'s hop already gave, still true today:**
     no CI/CD auto-deploy means merging *this* PR doesn't add new
     production traffic; nothing external reaches this path before
     `ENG-039` ships; and — checked fresh this round — all three broadcast
     tables are still empty (0 rows), so the live window, while real, is
     presently inert: no campaign exists to be silently missed. Named
     prominently in this PR's own body and the merge-request item (not
     just here) so whoever merges understands this isn't a purely
     theoretical gap and deploying promptly closes it, and so the
     resulting log noise isn't later mistaken for a regression.
- *Cost:* $0/month — no new dependency (confirmed at security's own A06
  check, this round's diff), no new infrastructure. The Vault-secret
  provisioning step (`ENG-037`'s own Window 2) is a $0 configuration action,
  not a cost.
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
checked fresh: `git status` clean but for three untracked `deno.lock`
files (one per new function directory this ticket adds — same established,
already-traced "auto-generated lockfile" pattern this project's prior gates
have already accepted, just multiplied by the new directories). `git fetch
origin` current. `git diff origin/main...HEAD --stat`: 18 files,
3235/7 lines, all 11 commits attributable to this ticket alone (`git log
--oneline origin/main..HEAD`) — confirmed `origin/main` already carries
`ENG-037`'s own migration (`20260904140000`, merged as PR #15, `64baabf`),
so this diff is exactly the incremental `ENG-038` surface, nothing more.
`gh pr list --head
feat/ENG-038-broadcast-composer-dispatcher-unsubscribe --state all`
confirmed no PR already existed for this branch. No `.github/workflows/`
on this repo (re-confirmed) — opening this PR carries no auto-deploy risk.

Opened `aiorders-api` PR #16
(https://github.com/harsimranwalia/aiorders-api/pull/16). Body: what each
of the four surfaces does, all four gates passed with receipt paths, five
non-blocking findings (the new TOCTOU race; the claimed-row-stuck edge
case; `cancel_broadcast` not flipping claimed rows; `enrollAudience`'s
untested cross-tenant scoping; `ENG-036`'s still-open shared bypass), and
the deploy-time note on the live cron window in full, precise form (both
what's confirmed live and both remaining steps for whoever deploys).

Wrote `inbox/2026-09-04-eng038-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: ~2-3 days` set on the item, mirroring the
ticket's own field. `lib/eng-notify.sh raise` run — `sent: active
2026-09-04-eng038-merge-request.md` at `21:06:41`,
`traces/eng-notify-2026-09-04.log`; stamped `notified: 2026-09-04T21:06:41`
on the item by hand, copied verbatim from the log.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy and the
release record both wait for merge detection on a future pass, per the
skill's own step 4 L1 row / step 7 split.

**Aside, not part of this ticket's own gate: `ENG-037`'s current board
state was checked while confirming this diff's base, since the two are
adjacent.** It reads `state: verified` — already carried `blocked →
shipped → verified` by an earlier `scheduled` pass's own step-5 merge
detection (board index, `ENG-037`'s closing paragraph). No stale state
found, nothing to fix; recorded here only because the release-readiness
round 1 log above (same file, written before that scheduled pass ran)
could otherwise mislead a future reader into thinking `ENG-037` was still
sitting on an open merge request.
