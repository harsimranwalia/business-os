---
id: ADR-002
title: Verification tickets still owe ready-to-ship and G3 — the gate stays, only its content changes
project: aiorders
ticket: ENG-001
status: accepted
decided_by: architect
date: 2026-08-26
supersedes:
superseded_by:
---

# ADR-002: Verification tickets still owe `ready-to-ship` and G3 — the gate stays, only its content changes

## Context

`ENG-001` passed `in-security` on 2026-08-26 (verdict pass,
`agents/security/reviews/ENG-001.md`). `ADR-001` decided that a verification
ticket — one whose acceptance criteria are all satisfied without a diff in any
registered project — still passes through every state in its lane's normal
path and still owes every receipt, but its Decision text names `building`,
`in-review`, `in-qa`, and `in-security` specifically: the states that existed
between the ticket and its next undecided boundary at the time it was written.
The board's own log at every hop since has read that naming literally rather
than improvising past it, exactly as `ADR-001`'s own Alternatives table warned
against ("leave the gap undocumented and let a future pass improvise a state
mapping on arrival").

The remaining full-lane states all assume a deploy target: `ready-to-ship`
(devops — release plan, rollback, observability), `awaiting-release` (the
approver's G3, "ship it to production?", auto-skipped only when the project's
registered autonomy is L3), `shipped` (devops — deployed, health checks
green, release record written), and `verified` (product-manager — acceptance
criteria confirmed against the live thing). `aiorders`, this ticket's
`project:`, names this instance's own engineering substrate. Re-checked fresh
this pass rather than trusted from `ADR-001`'s own citation:
`agents/eng-manager/config/projects.md` lists only the five app repos, all
**L1**; `config/internal-projects` is empty. So neither of the state table's
two existing auto-routes — L1's merge-request shortcut, L3's auto-approve —
applies, and none was invented for this ticket at registration time, because
`aiorders` was never registered at all.

## Decision

A verification ticket owes `ready-to-ship`, `awaiting-release`, `shipped`, and
`verified` exactly as any other full-lane ticket. None is skipped, and none is
auto-routed by treating this ticket, or this instance's own substrate, as
carrying an autonomy level its registry never granted. Continuing `ADR-001`'s
exact pattern, what changes is only what each state records:

- **`ready-to-ship`** — devops confirms directly, and logs it, that no
  release plan, rollback, or observability plan can exist because no
  registered project carries a diff for this ticket. Same shape as security's
  OWASP walk at `in-security` landing on ten `n/a`s: a real, logged
  confirmation, not a skipped step.
- **`awaiting-release` (G3)** — still a real approver decision. Not waived,
  and not quietly downgraded to L3's notify-after treatment: `aiorders` has no
  autonomy level for this or any future architect to extend one to it
  informally. The question put to the approver is honest rather than
  invented: not "approve this production deploy" (none exists) but "confirm
  this ticket's record — the five repos registered and worktreed, the loop's
  own gate-check passing, a second real ticket having reached the board — is
  accurate, and this ticket is done." It is raised, counted against the
  approval cap, and left to wait exactly like any other G3.
- **`shipped`** — devops records the G3 confirmation in place of a deploy. No
  release record is fabricated at `agents/devops/releases/` for a deploy that
  never happened.
- **`verified`** — product-manager re-confirms all four acceptance criteria
  against disk, exactly as at every earlier gate. The one state `ADR-001`'s
  pattern already covers without change: "confirm against the live thing"
  reads the same whether the live thing is a deployed app or this instance's
  own board and registry.

**Why G3 is not skipped, when `ADR-001` already skipped the literal
branch/PR at `building`.** `building`'s exit condition is a work artifact with
no meaning absent a diff — recording its absence honestly costs nothing and
sets no precedent about who decides what. G3 is different in kind:
`docs/engineering-team.md` names "say yes to production" as one of exactly
three things this department reserves for the approver, permanently and
department-wide, not a setting attached to a project or a ticket shape.
Deciding, on this architect's own authority, that a whole class of ticket
never needs that decision would be this department quietly narrowing what
"the approver decides" means, for one ticket's convenience — the exact
failure this ticket's own history exists to keep from recurring (`main`,
recorded `shipped`, owing all three gates, and nothing said a word).
`ADR-001`'s reversibility argument — "changes no project's autonomy and no
registered repo" — does not transfer here: removing a human decision-point is
not reversible in the same cheap sense a logging convention is, because a
second verification ticket built on "G3 never applies to this shape" is a
norm, not a note.

## Alternatives

| Option | Why not |
|---|---|
| Auto-skip G3 for any verification ticket, mirroring L3's auto-approve route | Autonomy belongs to a registered project and only the approver grants it (`docs/engineering-team.md`, `config/projects.md`'s own header, both repeated department-wide). `aiorders` holds no such grant, and inventing an equivalent keyed on ticket *shape* rather than project is the self-expansion the department's own no-auto-send / never-infer-approval-from-silence posture exists to block. |
| Register `aiorders` in `config/internal-projects`, dropping to the internal lane (no G3 at all) | Already rejected in `ADR-001`, for the same reason: that file reserves the addition to the approver, "should be rare," and this remains expected to be a one-time ticket. Nothing has changed since to revisit it. |
| Leave `ready-to-ship`/`awaiting-release`/`shipped` undefined and let a future pass improvise on arrival | The exact failure `ADR-001` closed, one state later. `lib/eng-gate-check.sh`'s receipt table only inspects `shipped`/`verified`, and all three receipt files already exist for this ticket — a bad `state: shipped` write here would sail through the one enforced check unnoticed. Deciding explicitly is the only thing standing between this ticket and repeating its own origin story. |

## Consequences

**Accepted:** this ticket cannot reach `shipped` until a real G3 item is
raised and answered — on an instance whose approval cap is already 3/3, a
genuine wait, not a formality skipped for convenience.

**Gained:** the pattern is on record for the next instance's own seed ticket,
the same way `ADR-001` already is; no gate is quietly worn down to fit one
ticket's shape; the approver's three reserved decisions stay exactly three.

**Reversibility:** the receipt-recording half (`ready-to-ship`, `shipped`) is
as cheap to change as `ADR-001` — a logging convention only. The G3 half is
not offered as a reversible implementation detail in the same sense; it is the
position that this decision does **not** remove a human decision-point, which
is the safer default and costs nothing to keep.

## Review trigger

If a second verification-only ticket's G3 is answered by the approver with
reasoning that reads as "you didn't need to ask," treat that as
approver-supplied evidence (per the decision journal) that a lighter route is
wanted, and bring a concrete proposal — not a third repeat of this same
question.
