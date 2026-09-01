# Acceptance — ENG-011 (client stage & health visibility)

## What the estimate got right

Cost held at $0/month exactly as scoped — reusing `onboarding_step`/
`is_active` and extending the existing hourly analytics aggregate rather than
adding new infrastructure meant there was genuinely nothing new to price. The
G1 readback's three evidence-grounded proposed defaults (stage taxonomy,
health signal, splitting "tickets" out as a standing question) all survived
unchanged to shipped code. Checking the live repos before proposing defaults,
rather than guessing, keeps paying off — worth continuing on every PRD that
has the option.

## What it missed

The PRD and design both treated "reuse an existing pipeline" as a pure cost
saving, and it was — but reusing infra also means inheriting that infra's own
operational risk, on a timeline this ticket doesn't control. The reused
pipeline (`calculate_platform_analytics()`'s hourly cron) started failing
(401, gateway-level, unrelated to this ticket's own diff) a few hours after
this ticket's own PRs merged — found only because this acceptance-check
verified against live production data instead of trusting the migration/QA
gates' static checks. Neither the design's Risks section nor the QA test
plan's gap list named "the reused pipeline stops running for reasons outside
this ticket" as a category. Worth a line in a future PRD's Risks section
whenever a design's cost saving comes from reusing something already live:
reused infra can go stale or break independently of the new code sitting on
top of it, and that's a real, distinct risk from "will the new code work."

## Also worth recording

This is the first ticket on this board to reach acceptance-check with no
browser access available to this host — the same standing gap the release
record already named for monitoring dashboards. What substituted, and
worked:

- Reading the exact deployed source at the merged commit
  (`git show origin/main:<path>`, never touching the shared worktrees'
  checked-out branches, so no risk to other tickets' in-progress work).
- Sampling real production rows via the read-only Supabase MCP connection to
  catch data-shape issues synthetic unit-test inputs can't (e.g. confirming
  `calculate_platform_analytics()` actually emits brand-level rollup rows in
  production, not just in the function's declared shape).
- One live, unauthenticated `curl` against the actual production endpoint to
  independently close a negative-auth criterion QA had explicitly left
  unverified ("pass by construction — not independently re-verified").

None of this is a full click-through, and this entry says so rather than
rounding up — but it's a real, repeatable substitute worth reusing on the
next ticket that hits the same no-browser gap, rather than re-deriving it
from scratch. Worth naming again if the next acceptance-check hits the same
wall a second time — two data points would make it a proposal, per this
board's own convention.

# Acceptance — ENG-007 (per-restaurant loyalty configuration)

## What the estimate got right

Sized `S`, and it held — no auth, no session, no identity mapping meant this
really was materially smaller than `ENG-006`, and cost landed at the
predicted $0/month. The PRD's own inferred/proposed requirements (insert-only
effective-dating, "not enrolled" as the unconfigured default, basic
non-negative validation) all survived unchanged through design, build, and
into the deployed code — confirmed directly against the live bundle, not
assumed from the receipts.

## What it missed

Nothing in the PRD's Risks section, the design's Risks section, or the QA
test plan flagged what turned out to be the actual practical bottleneck for
*verifying* this ticket: an `S`-sized ticket whose entire acceptance surface
is insert-time DB-trigger behavior (AC1/2/3/6 all depend on it) is a poor fit
for a host with no throwaway Postgres. Three separate gates — migration, QA,
release-readiness — each independently named "no live Postgres dry run" as a
gap and each carried it forward rather than closing it, because closing it
requires infrastructure none of them have. Acceptance-check inherited the
same gap a fourth time and closed most of it by hand-tracing the *deployed*
trigger source (stronger than hand-tracing git source, since it confirms what
actually shipped) rather than by exercising a live insert — deliberately, to
avoid writing a fake rate into a real restaurant's config ahead of ticket 3
giving this table a real reader. Worth a line in future PRDs for
trigger/constraint-heavy tickets: name the verification path (throwaway
container, a designated test fixture, or explicit sign-off that hand-tracing
the deployed source is the accepted bar) at design time, not discovered as a
recurring gap at four separate gates.

## Also worth recording

`skills/acceptance-check/SKILL.md` step 6b (continue an approved sequence)
did not fire for this ticket, and the reason is worth a proposal rather than
just this note if it recurs at ticket 3: 6b requires *this ticket's own* G1 to
have explicitly re-affirmed the sequence, and a G1 recommendation that merely
*mentions* the sequence for context (as this ticket's did) isn't the same as
the G1 *answer* touching it — the approver's bare "approved" here didn't. If
every subsequent ticket in a five-item sequence gets a G1 written the same
way (context mentioned, not asked as its own question), 6b may never fire
again for the rest of this sequence, which would mean the mechanism built to
automate `ENG-006 → ENG-007`'s hand-off only ever fires once. Worth watching
whether ticket 3's own G1 (if filed) is written to ask the continuation
question explicitly — that's the fix, not loosening 6b's bar.
