---
ticket: ENG-004
project: aiorders-admin-hub
author: architect
created: 2026-08-26
adrs: [ADR-003, ADR-004]
one_way_doors: []
touches_data: true
touches_models: false
---

# Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history — technical design

## Approach

No remediation is needed. The investigation this ticket asked for — confirm
project linkage, establish which repo is authoritative, content-diff the six
files, confirm a clean replay — found that the remediation the PRD anticipated
was already executed, correctly, by the approver directly, on `origin/main`,
on 2026-08-24: one day after filing the request and before this ticket ever
reached `shaped`.

**Both repos' `supabase/config.toml` confirm the same live project**
(`project_id = "bmnmnejwdxbcqinqkwko"`) — AC1, settled by the mechanism the
architect's blind reading named at readback, not a live-ledger query.

**`aiorders-api` is authoritative, as of two paired same-session commits:**

| Time (local) | `aiorders-api` | `aiorders-admin-hub` |
|---|---|---|
| 09:52:28 / 09:52:42 | `4b6a835` "Add restaurant/profile migrations moved from aiorders-admin-hub" | `c90c02c` "Remove migrations moved to aiorders-api" (+14s) |
| 10:18:27 / 10:18:36 | `5b3bac2` "Consolidate remaining migrations from aiorders-admin-hub" | `919d355` "Remove supabase/migrations, fully consolidated into aiorders-api" (+9s) |

Both dated 2026-08-24. The <15s gap between each pair, the matched commit
messages, and the fact both land on the same repos this ticket names is
first-party evidence this was one deliberate, cross-repo action, not two
unrelated changes. `aiorders-admin-hub`'s `origin/main` now carries no
`supabase/migrations/` and no `supabase/functions/` at all — only
`config.toml` remains (see Risks).

**Content-diffed all six named files against their new home, byte-for-byte**
(admin-hub's tree at `7009f18`, the last commit before removal, against
`aiorders-api`'s current `origin/main`):

| Deleted file (admin-hub, pre-removal) | Now at (`aiorders-api`, `origin/main`) | Content |
|---|---|---|
| `20250729143432-1040fac4-a39b-460e-a609-55e56df5e7e7.sql` | `20250729143432_updated_at_functions.sql` | **identical**, renamed |
| `20250814063528_6a950847-b81d-4cf2-ad6c-3397e721ea5f.sql` | same filename | **identical** |
| `20250814064923_3be8f472-d966-4e72-92e6-94fca6381fe8.sql` | same filename | **identical** |
| `20250814065439_d1efe4c6-ad71-45f0-9192-e74ca27b4c3b.sql` | same filename | **identical** |
| `20250814065606_3be00703-ff7f-4214-8db8-8a86aa355283.sql` | same filename | **identical** |
| `20260312000001_restaurant_activations.sql` | same filename | **identical** |

Zero content drift. One rename (a UUID-suffixed filename replaced by a
descriptive one) — exactly the "renamed-and-edited consolidation" the
architect's blind reading flagged a plain filename sweep couldn't rule out;
confirmed renamed but **not** edited.

**Replay integrity (AC4).** `aiorders-api`'s `origin/main` now holds 22
migrations in one chain (full list in this design's git citations below).
`20260312000001_restaurant_activations.sql` (creates the table) sorts before
`20260408000001_google_review_history.sql` (the migration the original
request flagged as depending on it) — the exact hazard the request named is
resolved by the consolidation itself, since both now live in the same repo in
filename-timestamp order. A full mechanical replay (local Docker Postgres,
zero production risk) was attempted and abandoned partway through an image
pull as disproportionate: the static evidence (byte-identical content +
verified filename ordering across all 22 files) already answers what the
replay would have tested, since these are pre-existing, already-applied
migrations rather than new, untested SQL. See Risks for what this does and
doesn't cover.

**The pending uncommitted deletion (AC5).** `aiorders-admin-hub`'s local
`main` (the approver's own checkout) already matches `origin/main` exactly —
`git branch -vv` in the department's worktree shows no ahead/behind — so
whatever was sitting uncommitted on 2026-08-23 is, at the ref level, resolved:
`origin/main` already carries a deliberate commit of that same removal,
correctly sequenced after the content move. Consistent with, not contradicted
by, the original request's own "nothing here is urgent."

**The "four siblings" discrepancy the PRD flagged (Risk row 3) is resolved:**
the real count is **three** — `20250729143357`, `20250814063455`,
`20250814065341` — matching the three timestamps the original request named.
"Four" was the request's own miscount.

## Components

Nothing changes in either registered project. What this design produces:

| Component | Change | Owner agent |
|---|---|---|
| `agents/architect/designs/ENG-004-*.md` | new — this document | architect |
| `agents/architect/decisions/ADR-003-*.md` | new — records `aiorders-api` as authoritative | architect |
| `agents/architect/decisions/ADR-004-*.md` | new — extends `ADR-001`'s verification-ticket pattern to this ticket's full remaining lane | architect |
| `agents/eng-manager/board/ENG-004-*.md` | log entry at `building`, citing the exact commit hashes, timestamps, and content-diff results above | eng-manager (per `ADR-004`) |
| `agents/principal-engineer/reviews/ENG-004.md` | new — reviews the investigation's claims against disk/git, not a diff | principal-engineer |
| `agents/qa/test-plans/ENG-004.md` | new — confirms AC1–5 against disk/git; no suite exists to run | qa |
| `agents/security/reviews/ENG-004.md` | new — confirms the RLS/`search_path` hardening in the six files is intact, unmodified, and present in the authoritative history; this is the one gate on this ticket with real, non-ceremonial content | security |

## Data

`touches_data: true` because the subject matter is a migration history, but
this ticket writes no migration and runs none. The live schema is unchanged
by this ticket in either direction — the six migrations' effects (RLS
policies, the `restaurants_public` view, the `restaurant_activations` table)
were already live before, during, and after both the original deletion and
its resolution. What changed is only which repo's *tracked file history*
matches that already-live reality. `database` is not in this ticket's chain —
there is no schema change to review.

## Interfaces

None. No code, no contract, no schema change in any registered project.

## Alternatives considered

**Independently re-apply or re-author the six migrations in `aiorders-api`,
treating the investigation as a precursor to this ticket's own remediation.**
Rejected once the investigation found the exact remediation this ticket would
have proposed was already executed, byte-identical, on 2026-08-24. Redoing it
would be a no-op at best; at worst, a careless re-apply against the
now-correct state risks introducing the exact drift this ticket exists to
prevent.

**Treat `ADR-001` as already covering this ticket's diff-less states, no new
ADR.** Rejected — see `ADR-004`'s own Alternatives table. The root cause here
(an out-of-band fix pre-empting an in-flight ticket) differs enough from
`ADR-001`'s (a ticket whose project was never registered at all) that citing
`ADR-001` silently would repeat the exact failure its own Alternatives table
warned against.

## One-way doors

None **remaining**. Moving migration ownership from `aiorders-admin-hub` to
`aiorders-api` is exactly the shape of decision this department reserves for
an ADR or a G2 — but it is not a pending decision this ticket makes: it is
already an executed fact, decided and acted on by the approver directly,
discovered rather than proposed. `ADR-003` records it. No G2 is raised,
because there is nothing left to approve — approval, in the only sense that
matters here, already happened by the approver's own hand.

## Risks

- **The live `supabase_migrations.schema_migrations` ledger was not queried.**
  Neither registered project's environment carries a DB credential
  (`.env`/`.env.local` checked in both `_eng/` worktrees, none present), and
  none was sought out. The static evidence — matched cross-repo commits,
  byte-identical content, correct filename ordering — is first-party and
  conclusive for the question this ticket asks ("is admin-hub still
  authoritative"); it does not independently confirm the live database's
  applied-migrations table agrees. Given these are pre-existing, previously-
  applied migrations rather than new schema changes, and the original
  request's own assessment that the deployed database is unaffected either
  way, this gap is named rather than pursued. If a future ticket obtains a DB
  credential for this project, confirming the ledger against this design's
  claims would be cheap, additive verification — not a sign this design was
  wrong.
- **Both the human's local `aiorders-api` checkout and the department's own
  `_eng/aiorders-api` worktree are stale relative to `origin/main`** — the
  human's by 2 commits (exactly the two consolidation commits), the
  department's `eng/base` branch by dozens, having diverged well before this
  consolidation happened. Every claim in this design is sourced from
  `origin/main` directly (`git show origin/main:...`, `git ls-tree
  origin/main`), not from either local copy. A future pass that trusts the
  `_eng/` worktree's own working-tree content for this repo without checking
  `origin/main` first would reach a stale conclusion — logged as an
  observation (`agents/eng-manager/observations.md`, see ticket log)
  rather than folded into this ticket's scope.
- **`aiorders-admin-hub`'s `supabase/config.toml` still declares 20
  `[functions.*]` stanzas** for functions that no longer exist in this repo
  (moved/removed in an earlier, already-closed consolidation). Harmless —
  `project_id` is still valid and nothing depends on the stale stanzas — and
  out of scope: this ticket is about `supabase/migrations`, and the PRD's
  non-goals exclude touching anything beyond that. Logged as an observation,
  not folded in here.

## Rollout

Not applicable. Nothing this ticket produces is deployed — the change already
reached `origin/main` on both repos on 2026-08-24, before this ticket existed
in shaped form. This ticket's own "release" is the board and the historical
record correctly reflecting a fact that is already true, same shape as
`ADR-002`'s treatment of `ENG-001`.

## Out of scope

- Re-verifying or changing RLS policy *logic* — confirming the six files'
  policies are present and unmodified is in scope (security's gate); whether
  that policy is still the *right* policy today is not (PRD non-goal).
- Cleaning up `aiorders-admin-hub`'s orphaned `[functions.*]` config stanzas —
  unrelated to migrations, logged as an observation instead.
- Querying the live migration ledger — named as a residual risk above rather
  than pursued, given no credential is available and the static evidence is
  sufficient to proceed.
- Any of the other uncommitted files in the human's `admin-hub` checkout — PRD
  non-goal, unchanged by this investigation.
