---
id: ADR-004
title: ENG-004 is a verification ticket for its full remaining lane — second occurrence, different root cause than ADR-001
project: aiorders-admin-hub
ticket: ENG-004
status: accepted
decided_by: architect
date: 2026-08-26
supersedes:
superseded_by:
---

# ADR-004: `ENG-004` is a verification ticket for its full remaining lane — second occurrence, different root cause than `ADR-001`

## Context

All five of `ENG-004`'s acceptance criteria are satisfied without a diff in
any registered project (see the ticket's design and `ADR-003`). `building`'s
documented exit condition — "branch pushed, self-tested, PR body written"
(`definition-of-done.md`) — assumes a diff this ticket will produce. None
will: the diff already exists, on `origin/main`, predating this ticket's
design by two days.

This is the same *shape* of gap `ADR-001` diagnosed for `ENG-001`, but not the
same *cause*, and the difference matters enough to state rather than paper
over. `ENG-001`'s project (`aiorders`) was never a registered project at all —
no diff was ever the mechanism, structurally. `ENG-004`'s project
(`aiorders-admin-hub`) **is** registered, at **L1**, with a real deploy
target and real production data — a diff was exactly the right mechanism
here, and one occurred; it simply didn't come from this ticket's own
`building` state, because the approver produced it directly, unprompted by
this ticket, before the department reached `designed`.

This is also the **second** verification-only ticket on this instance.
`ADR-001`'s own Review trigger names this directly: *"If a second
verification-only ticket appears on this instance, revisit whether the
internal-lane registration rejected above... is now worth raising to the
approver as a G2 — two occurrences is the pattern threshold."* That trigger is
engaged below rather than left to lapse silently.

`ADR-001` named only `building`, `in-review`, `in-qa`, and `in-security` —
the states between `ENG-001` and its next undecided boundary *at the time it
was written*; `ADR-002` had to extend it past `in-security` once `ENG-001`
reached there. This ADR covers `ENG-004`'s entire remaining lane in one pass,
since the full path is already known now.

## Decision

`ENG-004` follows `ADR-001`'s mechanism for every remaining state in its
lane. What changes is only what each state records, in place of a diff or a
deploy:

- **`building`** — records exactly which commits, files, and diffs were
  checked and what each showed (see the ticket log and design). `branch:`
  stays empty with a one-line note, per `ADR-001`.
- **`in-review`, `in-qa`** — principal-engineer and QA each independently
  re-derive the acceptance criteria against disk and git, not against a diff
  that doesn't exist — same discipline `ADR-001` set, re-confirmed rather than
  cited from this pass's numbers.
- **`in-security`** — confirms the RLS/`search_path` hardening in the six
  files is present, unmodified, and correctly ordered in `aiorders-api`'s
  history. Unlike `ENG-001`'s security pass (ten `n/a`s across the board),
  this one has real content: five of the six files under review **are** the
  security surface. This gate is not ceremony here and must not be waved
  through as if it were.
- **`ready-to-ship`** — devops confirms directly that no release plan,
  rollback, or observability plan exists, because the change this ticket
  concerns already shipped outside it on 2026-08-24 — a different reason
  than `ADR-002`'s (no registered project carried a diff at all), same
  honest-recording shape.
- **`awaiting-release` (G3)** — **not** auto-skipped. `aiorders-admin-hub` is
  registered at **L1**, and L1's only defined behaviour is "a human merges" —
  `config/projects.md`'s own autonomy table gives L1 no auto-approve route,
  the same absence `ADR-002` found for `aiorders` (unregistered) but reached
  here by a different fact: a real autonomy level that simply doesn't grant
  this shortcut. G3 asks the honest question — not "approve this deploy"
  (none exists; per the original request, the deployed database was
  unaffected before, during, and after this reconciliation), but "confirm
  this ticket's record is accurate and it's done." Raised and counted against
  the approval cap like any other G3, per `docs/engineering-team.md` naming
  "say yes to production" one of exactly three things this department
  reserves for the approver, department-wide, not a setting attached to a
  project's shape.
- **`shipped`** — devops records the G3 confirmation. No release record is
  fabricated at `agents/devops/releases/` for a deploy this ticket didn't
  make.
- **`verified`** — product-manager re-confirms all five acceptance criteria
  against disk, same as every earlier gate.

**`ADR-001`'s Review trigger, engaged:** internal-lane registration for
`aiorders-admin-hub` is not warranted by this occurrence — see Alternatives.
No G2 is raised for that question. Two occurrences establish that `ADR-001`'s
*mechanism* generalizes past its original single-use case; they do not yet
establish a pattern about registered app projects specifically, since the two
occurrences arrived by different, unrelated causes.

## Alternatives

| Option | Why not |
|---|---|
| Cite `ADR-001` directly, no new ADR | The root cause differs (structural impossibility vs. an out-of-band fix pre-empting an in-flight ticket on a real registered project) — a future reader of `ADR-001` asking "why does `ENG-004` skip `building`" would find no explanation for *this* reason there. `ADR-001`'s own Alternatives table already named this exact failure mode ("leave the gap undocumented and let a future pass improvise") and rejected it once; reusing that rejection's logic here, not its silence. |
| Register `aiorders-admin-hub` on the internal lane, dropping QA/security receipts | Off the table on the facts, not just the process: `INTERNAL_PROJECTS` (`config/internal-projects`) is empty, and admin-hub is a Cloudflare-deployed frontend with real production traffic — the opposite of the "no deploy target, no users" test both `ADR-001` and `docs/engineering-team.md` require for that lane. |
| Escalate to G2 now that `ADR-001`'s Review trigger has fired | Considered directly, per the trigger's own instruction, not skipped. Declined: the two occurrences share a *mechanism* (diff-less full-lane states) but not a *cause*, so they don't yet establish a durable pattern about registered projects worth spending a G2 on. The underlying `ADR-001` mechanism keeps working without strain applied a second time — nothing here argues for changing it. |
| Skip or lighten `in-security` since no new code is introduced | Rejected. Five of the six files under this ticket's history **are** RLS/`search_path` hardening — confirming that hardening survived the consolidation intact is a real, substantive check, arguably the most important gate this ticket owes, not a formality to wave through. |

## Consequences

**Accepted:** five more short passes (`in-review`, `in-qa`, `in-security`,
`ready-to-ship`, G3) each independently confirming facts this design already
gathered, rather than skipped — real, small costs, same as `ADR-001` accepted
for `ENG-001`.

**Gained:** `ADR-001`'s pattern is shown to generalize to a second, causally
different situation without modification; the Review trigger is answered on
record rather than left to lapse; a future third occurrence (or a repeat of
`ENG-004`'s specific cause) has this reasoning to build on rather than
starting cold.

**Reversibility:** cheap. Same as `ADR-001`/`ADR-002` — a recording
convention, changing no project's autonomy and no registered repo. The
G3-not-skipped half is, as in `ADR-002`, a decision *not* to remove a human
checkpoint; that needs no escalation and costs nothing to keep.

## Review trigger

A **third** verification-only ticket on this instance should prompt a
concrete internal-lane-or-alternative proposal rather than a third ad-hoc
ADR extending the same pattern again. Separately: a **second occurrence of
`ENG-004`'s specific cause** — the approver resolving a ticket's actual
subject matter directly, outside the department, while the ticket is still
mid-flight — is worth naming to the approver plainly in the weekly report if
it recurs, since it may mean the department's queue is slower than a fix the
approver is willing to make themselves, which is a latency signal worth
having even though it isn't a gate failure.
