---
id: ENG-037
title: Broadcast campaigns, steps, and recipients — schema, indexes, and dispatch cron (migration)
project: aiorders-api
type: feature
size: S
time_estimate: ~half a day
time_spent: ~3h15m since ready → ready-to-ship + release-readiness (PR opened)
time_remaining: none from this hop — blocked on approver merge; merge
  detection ships it and writes the release record automatically once
  merged
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-04
updated: 2026-09-04
branch: feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron
depends_on: []
blocks: [ENG-038]
parent: ENG-019
links:
  prd: agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md
  design: agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md
  adrs: [ADR-018, ADR-019]
  review: agents/principal-engineer/reviews/ENG-037.md
  test_plan: agents/qa/test-plans/ENG-037.md
  security_review: agents/security/reviews/ENG-037.md
  release: agents/devops/releases/2026-09-04-aiorders-api-ENG-037.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/15
---

## Problem

Nothing on this codebase can persist a composed broadcast campaign, its drip
steps, or a per-recipient send queue — the three tables `ENG-038`'s API and
dispatcher need don't exist. `ENG-038` also cannot write its ROI-report query
or its `communication_log` insert blind: the design presumes a specific shape
for two tables this ticket does not create (`orders.promos`, `communication_log`)
that no tracked migration on this repo defines.

## Outcome

**Three new tables** (`design`'s `## Data` section has the full column list;
summarized here):

- `broadcast_campaigns` — one row per composed campaign: `restaurant_id`,
  `type` (`one_time`|`drip`), `status` (`draft`|`scheduled`|`active`|
  `paused`|`completed`|`cancelled`), audience mode + parameter, optional
  `offers.id` reference, `scheduled_send_at`, `created_by`, timestamps.
- `broadcast_campaign_steps` — one row per drip step (a one-time campaign
  gets exactly one implicit step): `campaign_id`, step order, delay from
  enrollment, subject/email body/SMS body.
- `broadcast_campaign_recipients` — one row per (campaign, step, customer):
  `campaign_id`, `step_id`, `customer_id`, `restaurant_id` (denormalized
  deliberately — the dispatcher's claim query must never join out to know
  which restaurant a row belongs to), `due_at`, `status` (`pending`|`sent`|
  `failed`|`skipped_opted_out`|`cancelled`), `sent_at`, error detail.

**Constraints:**
- "Send now" and "send later" are the same row shape (`scheduled_send_at =
  now()` for immediate) — no separate immediate-send path.
- Schema supports an atomic claim (`ENG-038` writes the actual claim query —
  `SELECT ... FOR UPDATE SKIP LOCKED` or an equivalent claiming `UPDATE`);
  this ticket's job is the column/index shape that query needs, not the
  query itself.
- Index on `(status, due_at)` on `broadcast_campaign_recipients` — the
  dispatcher's every-5-minute claim query.
- Index on `(campaign_id)` on the same table — the report view's per-campaign
  aggregation.

**`cron.schedule('broadcast-dispatch-tick', ...)`** — every 5 minutes,
structurally identical to the already-live `platform_analytics_cron`. Per
the design's own Rollout order, this is created in the same migration before
`broadcast-dispatch` is deployed — the tick finds empty tables and no-ops
until `ENG-038` ships; this is the documented safe order, not a race to
avoid.

**No changes to any existing table.** No new column on `customers` — opt-out
reuses `consent_email`/`consent_sms`, already there (`ADR-020`; nothing for
this ticket to do here beyond not adding the column). `communication_log` is
unchanged — `ENG-038` writes to it using the existing polymorphic
`reference_type`/`reference_id` columns.

**Verification, not migration** — read against the live project, findings
written down for `ENG-038` to consume rather than re-derived there:
- `orders.promos`' exact internal key (`ADR-019`'s ROI query needs it to
  match a coupon code correctly — fail loud and document the real shape if
  it doesn't match the assumed one, never guess).
- `communication_log`'s exact column set (`ENG-038` writes
  `reference_type: 'broadcast_campaign'`, `reference_id: campaign.id` to it).
- Whether `orders(restaurant_id, created_at)` already has an index —
  presumed present (`ENG-020`'s design makes the same presumption for the
  same table). If missing, raise a separate ticket rather than adding an
  index inside this one.

## Notes

`ADR-018` (poller over per-recipient QStash — proven at aggregate-tick scale,
not single-event scale) is why this is a cron schedule against a claim table
rather than one scheduled message per recipient. `ADR-019` is why the
verification bullet above exists at all: the PRD's own Assumed section reads
AC4 as reusing an existing redemption-tracking mechanic, and none exists —
`orders.promos` (already captured by `external-integrations/handlers/
cloudwaitress.ts`, unrelated to this ticket) is what `ENG-038`'s report query
reads instead, so its shape has to be confirmed, not assumed, before that
query is written.

No acceptance criterion is directly verifiable from this diff alone —
schema-only, matches `ENG-031`'s own precedent on `ENG-016`'s board file.
Inert until `ENG-038` starts writing to these tables. Full surface-split and
sequencing reasoning:
`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`.

## Log

- `2026-09-04` `(created) → building` (eng-manager, `work-breakdown`,
  `continue ENG-019` event pass) — sub-ticket of `ENG-019`, sequence 1 of 3,
  no dependency, so dispatched straight to `building`. `time_estimate` ~half
  a day, 0h spent. Machine WIP: this ticket is part of `ENG-019`'s own
  family, not a second occupant of the `1/1` slot — same reading
  `ENG-016`/`ENG-031` already established, applied fresh in the notebook
  above. `chained: ENG-037` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-037`
  before this pass exits.

- `2026-09-04` `building → in-review` (database/principal-engineer-adjacent,
  `continue` event pass, context `ENG-037`). Narrow scope per this event's
  own contract (resume this ticket from its current state only). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check
  clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-037`: exit 0, clean.

  **This host has docker + an authenticated, linked `supabase` CLI** —
  unlike every host `ENG-031`/`ENG-007`/`ENG-011`/`ENG-013`'s own passes ran
  on. Recorded in `agents/database/notebook/` so future tickets check this
  before defaulting to repo-grep-only verification.

  **Worktree found mid-use on an unrelated ticket's branch, not started
  fresh.** `~/Documents/projects/_eng/aiorders-api` was on
  `feat/ENG-033-catering-request-order-capture-endpoint` — a different
  ticket in `ENG-016`'s family, already fully committed and pushed
  (`git status`: up to date with origin, nothing uncommitted except the
  same long-standing untracked `deno.lock` three prior passes have already
  independently noticed). Not a dead pass: verified via `git log
  origin/main..HEAD` on that branch showing real, already-pushed commits,
  not orphaned work. Safe to switch away from — switching branches doesn't
  touch existing commits — so `git fetch origin main` (`5415ef0`, confirmed
  current) then `git checkout -B
  feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron origin/main`,
  leaving `ENG-033`'s branch and worktree state untouched.

  **Verification against the live project** (this ticket's own explicit
  "Verification, not migration" job): schema-only dump
  (`supabase db dump --linked --schema public`) plus two narrowly-scoped
  read-only queries (schema names only from `vault.secrets`; one non-empty
  `orders.promos` sample, one column, one row, no customer/order identity
  pulled) against the linked live project (`bmnmnejwdxbcqinqkwko`). Full
  findings in `agents/database/migrations/ENG-037-*.md`, summarized: (1)
  `orders.promos` is `jsonb[]` (Postgres array-of-jsonb, not a jsonb-array
  column), each element a full CloudWaitress promo object keyed by `code`
  — resolves `ADR-019`'s named open risk with a real sample rather than a
  guess; (2) `communication_log`'s live columns match the design's
  "unchanged" claim exactly; (3) `orders(restaurant_id, created_at)` is not
  missing — `idx_orders_analytics_optimized` already covers it as its
  leading two columns, so no proposal needed. Both query outputs carried
  the CLI's own untrusted-data envelope; treated as inert data throughout,
  nothing in either resembled an instruction.

  **A path mistake, caught and fixed before it reached git.** First write
  of the migration file went to
  `~/Documents/projects/aiorders/_eng/aiorders-api/...` — one directory
  level wrong (`_eng` nested under the human's own `aiorders/` tree instead
  of being its sibling, per `config/projects.md`'s own two-path layout).
  Caught immediately on the next `git add` (path didn't match any tracked
  worktree file); confirmed via `find` that the stray tree held exactly the
  one file just written and nothing pre-existing, removed it
  (`rm -rf .../aiorders/_eng`), confirmed zero `_eng` entries remained under
  the human's tree, then rewrote the file at the correct path
  (`~/Documents/projects/_eng/aiorders-api/...`). No git operation ever ran
  in the wrong location — the mistake was a plain-file write, caught before
  any commit — but flagged here plainly rather than quietly, since a second
  pass hitting the same one-letter-off path deserves to find this note
  first.

  **Schema built and self-tested against a disposable local replica** — new
  this pass, not available to `ENG-031`/`ENG-007`/`ENG-011`/`ENG-013`: a
  fresh `supabase/postgres:15.8.1.073` container seeded with a minimal
  stand-in for the live tables this migration references, migration applied
  unmodified, then verified by direct query (not by re-reading the SQL):
  all three tables present with `relrowsecurity = t`, all five indexes
  present with the intended columns, the cron job registered with the
  correct schedule, the audience-mode check constraint actually rejecting a
  bad combination, a real insert succeeding with the `updated_at` trigger
  actually firing on update, the step-order unique constraint actually
  rejecting a duplicate, and the rollback actually executed (not just
  asserted) with a clean post-drop check. Full detail, every design
  decision, and the one open question routed to `ENG-038` rather than
  guessed (a `channel` column was **not** added to
  `broadcast_campaign_recipients` despite one ambiguous line in the
  design's Interfaces section, because the same design states twice,
  unambiguously, "one row per (campaign, step, customer)"):
  `agents/database/migrations/ENG-037-broadcast-campaigns-schema-and-dispatch-cron.md`.

  **One operational prerequisite named, not silently assumed or silently
  skipped.** The cron job authenticates to `broadcast-dispatch` via a Vault
  secret (`service_role_key`, referenced by name — never a raw value in the
  migration file); confirmed via `SELECT name FROM vault.secrets` (names
  only) that Vault is already live on this project (`resend_api_key`
  exists) but this specific secret does not yet. This session has no
  business holding the real service-role key value, so provisioning it is a
  named, one-line, out-of-band manual step — harmless to leave undone until
  `ENG-038` has a real campaign to send (design's own "empty tables, no-op"
  safety already covers it), not a blocker for this ticket or `ENG-038`'s
  own build/ship.

  **Artifact enumeration (step 6b):**
  `grep -rn "broadcast_campaign" --include="*.md" --include="*.sh" --include="*.yaml" departments/ instances/aiorders/engineering/`
  plus separate greps for `broadcast-dispatch-tick` and
  `service_role_key`/`SUPABASE_SERVICE_ROLE_KEY`. Every hit for the three
  table names (`ENG-019`'s own ticket file, `ENG-038`'s ticket file,
  `ADR-018`, the board archive) agrees on names and shape — no instruction
  or map in conflict. Every existing `SUPABASE_SERVICE_ROLE_KEY` mention
  elsewhere in the repo is an edge function reading it from `Deno.env`, a
  different mechanism for a different runtime — confirms rather than
  contradicts this migration's own claim that no prior convention exists
  for a `pg_cron`-side reference to this key.

  **PR body written** (`building`'s own exit condition; no PR opened yet —
  L1 opens the PR at release-readiness):
  - *What it does:* Adds `broadcast_campaigns`, `broadcast_campaign_steps`,
    `broadcast_campaign_recipients` (all RLS-enabled, no policies —
    service-role only), five supporting indexes, an `updated_at` trigger
    reusing the existing `update_updated_at_column()`, and a
    `broadcast-dispatch-tick` `pg_cron` job (every 5 minutes, structurally
    matching the live `platform_analytics_cron`).
  - *What it deliberately does not do:* No existing table touched. No
    `channel` column on `broadcast_campaign_recipients` (see the open
    question above — routed to `ENG-038`, not guessed). No cross-column
    check requiring an email/SMS channel on a step, matching
    `communication_templates`' own precedent rather than inventing a
    stricter rule.
  - *Uncertainties:* the cron job's outgoing call needs a Vault secret that
    doesn't exist yet (named above, non-blocking). `orders.promos`'
    internal key is now confirmed live, not merely assumed — low residual
    risk.
  - *What to review hardest:* the `broadcast_campaigns_audience_param_check`
    constraint logic and the RLS/no-policy choice on all three tables —
    both added beyond the design's own literal Data section text, reasoned
    from established precedent elsewhere in this repo rather than
    requested verbatim.

  Branch `feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron`
  created fresh from `origin/main` (`5415ef0`), committed (`59e9670`, 1
  file) and pushed to `origin`.

  **1 transition this pass** (`building → in-review`), under the cap of 4 —
  `in-review`/`in-qa` (combined hop, principal-engineer + qa) is a fresh
  session's work per `eng_build_loop.md`'s "a pass stops after `building` on
  purpose."  No WIP-cap change: already inside the counted
  `ready`..`ready-to-ship` range at `building`; `in-review` is still inside
  it.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-review` needs no approver gate.
  Nothing to nudge.

  **Observations filed:** (1) this host's docker/supabase-CLI capability,
  cross-referenced into `agents/database/notebook/` as the durable copy
  since it changes how every future database ticket should approach
  verification. (2) the stray
  `supabase/functions/brand-portal/deno.lock`, still untracked in the
  `aiorders-api` worktree, now independently noticed by three passes
  (`ENG-029`, `ENG-031`, this one) without being cleaned up or explained.

  Post-pass `departments/engineering/lib/eng-gate-check.sh ENG-037` and
  whole-board: both exit 0, clean.

  `chained: ENG-037` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-037`
  before this pass exits.

- `2026-09-04` `in-review → in-qa`: code review + quality gate, round 1,
  both **PASS** (principal-engineer + qa, combined review+quality hop,
  `continue ENG-037` event pass, context `ENG-037`, per prior hop's own
  `chained: ENG-037`). Reading map for `continue`: steps 6 and 6b (design
  already complete, not mid-PRD), plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-037`: exit 0, clean.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint. Worktree (`~/Documents/projects/_eng/aiorders-api`) re-checked
  fresh: on the correct branch, up to date with `origin`, `git diff
  origin/main...HEAD --stat` confirms the one-file, 148-line diff; clean
  except the same long-standing untracked `deno.lock` prior passes already
  noted. `supabase projects list` double-checked before running any live
  query — the unfiltered output's first few rows are *other* projects on
  this account, and a truncated view of it briefly looked unlinked; the full
  list confirms `bmnmnejwdxbcqinqkwko` (`foodswipe-love`) is the one marked
  linked, matching the worktree's own `supabase/.temp/project-ref` and
  `config.toml`. Recorded here because a second pass skimming the same
  command's output could draw the wrong conclusion from a short capture.

  **Code review: PASS, round 1.** 0/10 automatic failures. Read the design's
  `## Data`/`## Interfaces` sections and both ADRs directly, not the
  ticket's paraphrase; checked every column/constraint/index against the
  committed SQL. Independently re-verified every FK target and the one
  claim uncheckable against this repo's tracked history
  (`communication_templates`' column types, copied by this migration but
  defined in no migration anywhere in this repo) against the **live**
  schema directly (`supabase db dump --linked --schema public`, schema-only,
  this session) — matches exactly. **Two non-blocking findings**, both
  specific and actionable: (F1) `broadcast_campaign_recipients.step_id`
  carries an `on delete cascade` FK with no dedicated index — Postgres
  doesn't auto-index the referencing side, so a cascade through `step_id`
  would seq-scan the schema's own highest-fan-out table; judged low-reach
  today since no interface deletes a step while any recipient rows could
  exist for it. (F2) `broadcast_campaigns.scheduled_send_at` is nullable
  with no constraint tying it to `status` — a future `ENG-038` bug inserting
  `status: 'scheduled'` with a null send time would sit silently
  unsent forever, no error, no log line; flagged because this same
  migration already sets a higher bar elsewhere in the same file
  (`broadcast_campaigns_audience_param_check`,
  `broadcast_campaign_steps_order_unique`, both added beyond the design's
  literal text) and this gap is the identical shape, just not extended this
  far. Full detail, both fixes specified: `agents/principal-engineer/
  reviews/ENG-037.md`, `links.review` set.

  **Quality gate: PASS, round 1.** `aiorders-api` has no suite/lint/
  typecheck/build command of any kind (`config/projects.md`'s Commands
  table, confirmed empty across the board) and no application code exists
  yet to exercise these tables (`grep -rln "broadcast_campaign"
  supabase/functions/`: zero hits, re-run fresh this hop) — 0 of parent
  `ENG-019`'s 7 acceptance criteria apply to this diff, all requiring
  `ENG-038`. This ticket's own criterion (schema matches design exactly) is
  covered by two independent direct-query checks: the disposable-container
  run from the build hop (re-read, not re-derived) and a fresh live-schema
  dump run in this hop — a materially stronger evidence class than this
  board's own prior precedent on the same shape of gap
  (`ENG-031`/`ENG-007`/`ENG-011`/`ENG-013`, none of which had local Postgres
  access). Migration timestamp ordering re-confirmed
  (`20260904140000` sorts last). Zero bugs filed; no open P0/P1 on the
  board. Full detail: `agents/qa/test-plans/ENG-037.md`, `links.test_plan`
  set.

  **2 transitions this pass** (`in-review → in-qa` is recorded as one
  transition, matching `ENG-031`'s own precedent for a same-round
  double-pass — see that ticket's log), under the cap of 4. Owner
  `principal-engineer → eng-manager`, matching this board's own established
  precedent for a same-round double-pass (`ENG-031`/`ENG-032`/`ENG-033`/
  `ENG-034`: owner rests at `eng-manager` once both gates clear in one hop,
  not at either gate's own nominal owner). No WIP-cap change — still inside
  the counted `ready..ready-to-ship` range. `time_spent`/`time_remaining`
  updated in frontmatter.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-qa` needs no approver gate.
  Nothing to nudge.

  **Observation filed** (`observations.md`): the design's own Data section
  names `customers`/`offers`/`orders`/`communication_log` as tables defined
  in no tracked migration in this repo, but not `communication_templates` —
  which this same review found is *also* untracked (confirmed by grep for
  its own column names across every migration in the repo). Worth knowing
  for any future ticket that reads that table's shape the way this one did.

  Post-pass `departments/engineering/lib/eng-gate-check.sh ENG-037` and
  whole-board: see below.

  `chained: ENG-037` — `in-qa` is agent-owned (security gate next), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-037`
  before this pass exits.

- `2026-09-04` `in-qa → ready-to-ship`: security gate, round 1, **PASS**
  (security, `continue ENG-037` event pass, context `ENG-037`, per prior
  hop's own `chained: ENG-037`). Reading map for `continue`: steps 6 and
  6b (design already complete, not mid-PRD), plus the not-negotiable set
  (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*).
  Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-037`: exit 0, clean.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint. Worktree (`~/Documents/projects/_eng/aiorders-api`)
  re-checked fresh: on the correct branch, `git fetch origin main` current,
  `git diff origin/main...HEAD --stat` confirms the same one-file, 148-line
  diff (`59e9670`); clean except the same long-standing untracked
  `deno.lock` prior passes already noted.

  **`skills/security-gate/SKILL.md` run in full.** Threat-modeled the
  diff against all four questions before the checklist (no reachable
  input, no live new capability — RLS-zero-policy on all three tables
  confirmed by the build hop's own disposable-container query, cron tick
  double-inert until both `ENG-038` deploys and a Vault secret exists — no
  new data exposed, no change to blast radius under full compromise).
  Read `agents/architect/decisions/ADR-016.md`/`ADR-017.md`/`ADR-018.md`
  directly (not the ticket's paraphrase) to confirm this migration's
  service-role-bearer cron auth is the correct side of the
  `systemTriggered`-bypass fix those ADRs made for `ENG-035`/`ENG-036`
  earlier the same evening, not a fresh instance of that bug class.
  Independently re-ran the reachability grep
  (`grep -rln "broadcast_campaign" supabase/functions/`: zero hits) and a
  secrets scan over the diff and full commit history (`git diff`/`git log
  -p` for key/secret/password/token/bearer/PEM patterns: every hit is the
  literal name `service_role_key`, never a resolved value).

  **Verdict: PASS**, 0 blocking findings. Every OWASP category marked
  applicable or n/a with a reason; two non-blocking notes: (1) explicitly
  confirmed this ticket's RLS-enabled-with-zero-policies is **not** a 4th
  occurrence of the `ENG-015`/`ENG-031`/`ENG-033` "RLS activation
  unverified" pattern — those tables predate tracked history, these three
  are created and verified live by this same migration; (2) no rate
  limit/quota/audience-size cap exists anywhere in the plan for broadcast
  sends (confirmed by grep against the PRD, design, and
  `outgoing-communications/README.md`) — non-blocking since nothing reads
  or writes these tables yet, routed forward to `ENG-038`'s own gate via
  `agents/security/notebook/2026-09-04-findings.md` rather than filed as a
  proposal, same mechanism `ENG-031`'s RLS finding used to reach `ENG-033`.
  Full detail: `agents/security/reviews/ENG-037.md`, `links.security_review`
  set in the same edit.

  **1 transition this pass** (`in-qa → ready-to-ship`), under the cap of
  4. Owner `eng-manager → devops`, per `skills/security-gate/SKILL.md`
  step 9's routing on a `pass` verdict. No WIP-cap change — still inside
  the counted `ready..ready-to-ship` range. `time_spent`/`time_remaining`
  updated in frontmatter.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `ready-to-ship` needs no approver
  gate yet (that's devops's own L1 merge-request step next). Nothing to
  nudge.

  **Observation filed** (`observations.md`): the cron job's Vault-secret
  dereference is a live subquery inside the stored `cron.schedule` body,
  never a precomputed value — so the job's own stored definition never
  holds the resolved credential. Worth a future `pg_cron`-authenticated
  job on this project copying this exact shape.

  Post-pass `departments/engineering/lib/eng-gate-check.sh ENG-037` and
  whole-board: see below.

  `chained: ENG-037` — `ready-to-ship` is agent-owned (devops's
  release-readiness hop next), not the approver, not blocked, not
  terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-037`
  before this pass exits.

- `2026-09-04` `ready-to-ship → blocked`: release-readiness, **PASS**
  (devops, `continue ENG-037` event pass). `skills/release-runner/SKILL.md`
  in full — L1, window skipped. Four upstream gates re-confirmed fresh from
  their receipts (review/quality/security/migration): all `pass`. Readiness
  gate held: rollback tested (disposable container), $0/month, no window.
  One non-blocking observability finding — the cron tick calls out
  unconditionally, not gated on pending work, so a pre-`ENG-038` 404 window
  exists distinct from the documented post-`ENG-038` 401 one; named in the
  PR body, not a gate failure (no auto-deploy here, nothing external
  reaches the path yet). Full reasoning:
  `agents/devops/notebook/2026-09-04-release-readiness-log.md`.

  Opened `aiorders-api` PR #15
  (https://github.com/harsimranwalia/aiorders-api/pull/15), wrote
  `inbox/2026-09-04-eng037-merge-request.md`, notified (`12:33:03`).
  `blocked_on: approver`, `blocked_from: ready-to-ship`,
  `owner: approver`, `links.pr` set. One observation filed
  (`observations.md`).

  `chained: none` — blocked on the approver; merge detection (step 5)
  resumes it on a future pass.

- `2026-09-04` `blocked → shipped → verified` (eng-manager, `scheduled`
  event pass — whole-board sweep, step 5 merge detection). Reading map for
  `scheduled`: the whole document, never narrowed. Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  `ENG-037` was the only ticket anywhere on the board at `state: blocked`.
  Worktree (`~/Documents/projects/_eng/aiorders-api`) fetched fresh:
  `git merge-base --is-ancestor origin/feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron
  origin/main` → ancestor (merged). Cross-checked `gh pr view 15`: `state:
  MERGED`, base `main`, no stacking, `mergedAt: 2026-09-04T21:19:18Z` —
  about 1h40m after the prior `watch` pass's own check (~19:39 UTC) found it
  still open. One file, 148 additions/0 deletions (`gh pr view --json
  files`), matching this ticket's own recorded diff exactly — no drift.

  **Not advanced on the merge alone** (step 5's "a merge is not a gate"):
  re-read all four upstream receipts directly —
  `agents/principal-engineer/reviews/ENG-037.md`,
  `agents/qa/test-plans/ENG-037.md`, `agents/security/reviews/ENG-037.md`,
  `agents/database/migrations/ENG-037-broadcast-campaigns-schema-and-dispatch-cron.md`
  — all four still `pass`. No acceptance criterion of the parent PRD applies
  to this diff (0 of 7, all require `ENG-038`, already established at the
  `in-qa` hop) — matches `ENG-031`'s own precedent (schema-only sub-ticket,
  inert), so receipt-bookkeeping to `verified` is the correct route, not a
  hollow full acceptance-check run against criteria that cannot yet be
  checked against a live result (`acceptance-check/SKILL.md` step 2 asks for
  the live result, and there is none — 0 readers/writers exist before
  `ENG-038`).

  **New this pass — the deploy question prior releases on this board left
  open was actually answered.** This host's linked `supabase` CLI
  (`agents/database/notebook/2026-09-04-host-tooling-capability.md`)
  confirmed live, read-only: all three tables exist in `bmnmnejwdxbcqinqkwko`
  and `broadcast-dispatch-tick` is registered and `active` on its 5-minute
  schedule. Both queries carried the CLI's own untrusted-data envelope;
  treated as inert data, nothing in either resembled an instruction. This
  also means the pre-`ENG-038` observability gap named non-blocking at
  release-readiness (every tick 404s until `ENG-038` deploys the callee) is
  now confirmed actually happening in production, not merely a named risk —
  still non-blocking (nothing external reaches the path, no data at risk,
  self-closes once `ENG-038` ships), named plainly in the release record so
  the resulting log noise isn't later read as a fresh regression.

  Release record written: `agents/devops/releases/2026-09-04-aiorders-api-ENG-037.md`,
  `links.release` set in the same edit. `state: blocked → verified`,
  `owner: approver → eng-manager`, `blocked_on`/`blocked_from` cleared.

  Merge-request item moved to `inbox/_handled/`, amended in place with a
  plain-language merge note. Journal entry added (`decision-journal.md`) —
  silent GitHub merge, no written reply, same shape as every prior L1 merge
  on this board.

  **Consequence for the family:** this ticket's `blocks: [ENG-038]` —
  `ENG-038`'s sole dependency (`depends_on: [ENG-037]`) is now satisfied.
  `ENG-039` still depends on `ENG-038` in turn, unaffected by this merge
  alone. Machine WIP unaffected — this ticket already left the counted
  `ready..ready-to-ship` range at its prior `ready-to-ship → blocked` hop;
  the family's slot is held by `ENG-019`/`ENG-038`/`ENG-039` regardless.
  `ENG-019` (parent) still cannot reach `shipped`/`verified` until every
  child is settled (`ADR-003`) — two siblings remain unbuilt.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — pure receipt-confirmation and bookkeeping plus a live
  verification query, no new implementation work, same precedent
  `ENG-031`'s own ship carried.

  **Dead-end sweep (scoped to this event):** see the board index's own
  whole-board sweep notes for this pass.

  **Notify sweep:** nothing new to raise (no gate opened this pass).
  `ENG-027`/`ENG-028` already past their one-time `nudged:`, nothing to
  nudge again; `ENG-016`'s Piece-2 question still under the 24h threshold.

  **Step 8b:** one observation filed (`observations.md`) — the
  pre-`ENG-038` 404 window is now confirmed live and firing every 5 minutes,
  not just a named pre-merge risk. No `exception-request:` found on this
  ticket's log.

  **Step 8c:** decision-journal entry added (see above).

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board:
  see the board index's own closing note for this pass.

  `chained: none` — `verified` is terminal; the chaining guard never fires
  on a terminal ticket. `chained: ENG-038` fired instead, recorded on
  `ENG-038`'s own log — see that ticket's file.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.
