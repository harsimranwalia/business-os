# Release-readiness log — 2026-09-03

First entry in this notebook (`agents/devops/notebook/` held only `.gitkeep`
before this pass) — `aiorders-api`'s earlier same-day release-readiness hops
(`ENG-022`, `ENG-024`) left their reasoning inline in the ticket log/PR body
rather than in a notebook; this one follows `conventions.yaml`'s
`ticket_log.entry.reasoning_goes_to` instead, going forward.

## ENG-031 — `ready-to-ship → blocked`, PR opened

`skills/release-runner/SKILL.md` run step by step, not reusing a template
blindly.

**Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`) — skip to
step 4, no window check.

**Step 2 (upstream gates):** re-read, not trusted from the ticket log's own
account — opened all three receipts directly.
`agents/principal-engineer/reviews/ENG-031.md` (pass, 0/10 auto-fail),
`agents/qa/test-plans/ENG-031.md` (pass, no suite applies — pure DDL diff),
`agents/security/reviews/ENG-031.md` (pass, 0 blocking), and the migration
plan `agents/database/migrations/ENG-031-catering-order-capture-migration.md`
(pass). All four agree independently, via their own greps, that neither
column is referenced anywhere in `supabase/functions/` yet.

**Step 3 (readiness gate) — the one requiring actual judgment, not just a
re-read:**

- *Rollback:* documented, not live-drilled. This host has no
  Docker/psql/supabase CLI and no Supabase MCP session — the same gap
  `ENG-007`/`ENG-011`/`ENG-013`/`ENG-024` each already recorded (open
  proposal, `proposals.md`, 2026-08-29). Checked the actual precedent rather
  than assuming the bar: `ENG-007`'s own `ready-to-ship → blocked` hop
  (board file, 2026-08-29 entry) held this same gate on "rollback written"
  — not "rollback executed" — given the identical host limitation, and nothing
  since has raised that bar. `ENG-031`'s rollback is materially lower-risk
  than `ENG-007`'s (two nullable `ADD COLUMN`s with no dependent code at all,
  vs. a trigger plus a handler with a live admin caller), so holding it to a
  bar `ENG-007` didn't clear would be inventing a new standard on the
  smaller-risk ticket. Accepted on the same basis.
- *Observability:* no reachable runtime path exists yet at all (not "exists
  but unmonitored") — both columns are unread and unwritten anywhere in the
  function tree until `ENG-033` ships, independently confirmed by three
  separate greps (review, QA, security) plus my own re-run of the same grep
  this pass. Nothing to observe yet is a stronger position than "observed
  via existing logging" (`ENG-007`'s bar), so this clears on the same
  reasoning a fortiori. The observability question that actually matters —
  does the eventual write path log correctly — belongs to `ENG-033`'s own
  release-readiness hop, not this one.
- *Cost:* $0/month — `ADD COLUMN` with no default is metadata-only, no new
  service, no compute. Not a judgment call.
- *Window:* n/a, L1.

**Step 4 (route):** worktree `_eng/aiorders-api` checked clean before
touching it — one untracked file (`supabase/functions/brand-portal/deno.lock`),
same stray file `ENG-029`'s pass and this ticket's own `building` hop both
already flagged and left alone; third independent notice now, see
`observations.md`. `git fetch` + `git merge-base --is-ancestor` confirmed
the branch not yet merged; `gh pr list --head ... --state all` confirmed no
PR already existed (this ticket's branch was renamed mid-flight by an
earlier hop, so re-checking rather than assuming was worth the one call).
Opened PR #12 (`gh pr create`), body drawn from the four gate receipts plus
this ticket's own `building`-hop PR draft, structured to match `ENG-024`'s
same-day PR (What this does / Gates passed / Release readiness / One named
gap) rather than reaching back to `ENG-007`'s older format. Wrote
`inbox/2026-09-03-eng031-merge-request.md`, `agent: eng-manager` per this
board's consistent convention on every merge-request item so far (`ENG-015`,
`ENG-022`, `ENG-024`) despite the skill itself being devops-owned — matched
the established pattern rather than the more literal reading. `lib/eng-notify.sh
raise` exited 0 with no output (no visible failure this time, unlike the
2026-08-29 `SLACK_WEBHOOK_URL unset` incidents — `.env` now has it set) but
did not stamp `notified:` itself; stamped by hand per this instance's
standing practice when the script's own delivery can't be confirmed from its
output.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: approver`, `links.pr` set. No G3 — L1 has none; the PR merge is the
human gate.

**Security's one non-blocking finding (RLS activation on `public.catering`
unverified from the repo)** was not re-litigated here — already reasoned in
full in `agents/security/reviews/ENG-031.md` and routed to `ENG-033`'s own
future gate. Named again in the PR body for visibility, not re-decided.

Not done, and deliberately not: no deploy, no health check, no release
record. L1's actual deploy (whatever that means for a migration-only
change — this repo has no CI/CD, so a human runs `supabase db push` or
equivalent after merge) and the release record both wait for merge
detection on a future pass, per the skill's own step 4 L1 row.
