# Release-readiness log — 2026-09-06

## ENG-041 — `ready-to-ship → blocked`, PR opened

`continue ENG-041` event pass. `skills/release-runner/SKILL.md` run step by
step, same L1 reading this board already established on `ENG-039`/`ENG-040`:
step 1 is the clock check only; steps 2-3's readiness content still runs for
L1, minus the window bullet.

**Step 1 (window):** `restaurant-portal` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies.

**Step 2 (upstream gates) — all three re-read fresh from the receipt files,
not from the ticket log's own account, all passing:**

- `agents/principal-engineer/reviews/ENG-041.md` — round 2, `verdict: pass`,
  0/10 automatic failures. Round 1 had failed on a real cross-restaurant
  data leak (the FAQ-draft hand-off carried no restaurant id); round 2
  independently re-traced the fix against the original repro and confirmed
  the regression test fails on the pre-fix code, only that test.
- `agents/qa/test-plans/ENG-041.md` — `last_result: pass`, 42/42. All 4
  owned criteria (AC1, AC2, AC6, UI-half AC3) covered; one coverage gap
  (AC1's "never another restaurant's" half had no test of its own) closed
  in-hop, mutation-verified.
- `agents/security/reviews/ENG-041.md` — `verdict: pass`, 0 blocking
  findings. `ENG-022`'s ownership-check fix independently re-derived live
  against `aiorders-api`'s current `origin/main`, not taken on any ticket's
  word. PII (`ADR-014`) checked control-by-control against the shipped code.

No migration owed — confirmed `agents/database/migrations/` has no
`ENG-041-*.md`, correct for a diff with zero `*.sql` files (the ticket's own
work-breakdown note: no schema change, only a read against an existing
RLS-protected table and a write through `ENG-040`'s already-widened action).

**Step 3 (readiness gate):**

- *Rollback:* no migration, no stored-state change of its own — reverting
  the merge commit fully undoes this diff; `deploy-cf.yml`
  (`.github/workflows/deploy-cf.yml`, confirmed present on this repo, same
  as `ENG-032`'s/`ENG-039`'s own releases) re-triggers on the revert and
  redeploys the prior build. Not drilled — no CI dashboard or Cloudflare
  Pages access from this department's worktree, same boundary `ENG-002`'s,
  `ENG-032`'s and `ENG-039`'s own releases on this repo already named.
  Reasoned, not tested: near-fully-additive diff (660 insertions / 3
  deletions across 8 files), zero deletions of existing behaviour per the
  diffstat already confirmed by review and security.
- *Observability:* read the diff directly rather than assuming. The one new
  failure path this ticket adds (the `ai_conversations` query) logs
  `error.code` via `console.error` and surfaces a distinct error card with
  retry — confirmed in `pages/questions/Index.tsx`, already cited by
  security's own A09 walk. No client-side runtime error tracking service
  exists anywhere in this repo — a pre-existing gap across this whole
  instance, not introduced or worsened by this ticket, same posture already
  accepted at this gate on `ENG-002`/`ENG-032`/`ENG-039`.
- *Cost:* $0/month — no new dependency or infrastructure (no
  manifest/lockfile in the diff, confirmed by review's and security's own
  automatic-failure scans), reuses existing Cloudflare Pages capacity and an
  existing, already-authorized Supabase read (RLS-scoped, `LIMIT`-bounded
  100/page).
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/restaurant-portal`)
re-checked fresh, not assumed unchanged since the security hop: `git fetch
origin` current, branch tip `01c6ddb` matching the ticket's own frontmatter
and the security gate's own cited head, `git status` clean (no drift from a
prior pass). `git merge-base --is-ancestor
feat/ENG-041-customer-questions-and-faq-editor origin/main` → not merged.
`git diff origin/main...HEAD --stat`: 8 files, 660 insertions, 3 deletions —
matches the security gate's own account exactly. `gh pr list --head
feat/ENG-041-customer-questions-and-faq-editor --state all` confirmed no PR
already existed for this branch.

Opened `restaurant-portal` PR #5
(https://github.com/harsimranwalia/restaurant-portal/pull/5). Body: what
changed, the three gates passed with receipt paths (round 1's leak and its
fix named explicitly, not glossed over), the self-test numbers
(re-independently-run at review and security, not just build), rollback/
observability/cost, and what's out of scope (`CateringPageForm`/
`CateringFaq`, the admin-hub staff editor, re-deriving AC4/AC5).

Wrote `inbox/2026-09-06-eng041-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: ~1 to 1.5 days` set on the item, mirroring
the ticket's own field. `lib/eng-notify.sh raise` exited 0, confirmed sent
from the log (`traces/eng-notify-2026-09-06.log`: `sent: active
2026-09-06-eng041-merge-request.md`, `11:16:37`); stamped `notified:
2026-09-06T11:16:37` on the item by hand, copied verbatim from the log,
same standing practice this file's own prior entries use.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy (the
`deploy-cf.yml` GitHub Actions run, unattended once merged) and the release
record both wait for merge detection on a future pass, per the skill's own
step 4 L1 row / step 7 split.

**This is `ENG-021`'s last sub-ticket.** Once this PR merges, a future
pass's step-5 merge detection carries `ENG-041` to `shipped`, which — per
the family's own `ADR-003`-class exemption, already used for `ENG-016` and
`ENG-019` — makes the parent `ENG-021` itself eligible to move
`building → shipped` directly, without its own review/QA/security hops.
Not this hop's to process; noted so the next hop that finds `ENG-041`
merged isn't surprised by the parent also being ready to close out.
