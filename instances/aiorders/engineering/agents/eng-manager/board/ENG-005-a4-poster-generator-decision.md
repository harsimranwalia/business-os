---
id: ENG-005
title: Decide and act on the orphaned A4PosterGenerator component
project: aiorders-admin-hub
type: chore
size: S
severity: P3
priority:
state: shaped
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-25
updated: 2026-08-25
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
---

## Input

Verbatim, from `inbox/requests/2026-08-23-a4-poster-generator-unwired.md`
(now `inbox/_handled/`), filed by the approver, received 2026-08-23 —
preserved here per `skills/request-readback/SKILL.md` step 1, never edited:

> A4PosterGenerator is committed but not reachable
>
> `src/components/A4PosterGenerator.tsx` was committed to `aiorders-admin-hub`
> on 2026-08-23 (`bfddffe`) so the work would be tracked rather than sitting
> loose in the working tree. Nothing imports it — a grep across `src/` finds
> no reference outside the file itself. It is in the repo and unreachable
> from the running app.
>
> **What this asks for:** First decide whether it is wanted, then act on the
> answer. If it is, wire it into a route or a surface in the admin hub and
> say which. If it is not, delete it — `bfddffe` is a single-file commit
> specifically so reverting it is clean.
>
> Small, and genuinely low stakes. Worth capturing only so a
> committed-but-dead component does not quietly become permanent.

Full text in the handled request file.

## Readback

See `agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

`A4PosterGenerator.tsx` is fully committed to `aiorders-admin-hub` but
unreachable from the running app — nothing imports it. Whether it's wanted
at all is the open question the request itself leads with.

## Outcome

Either the component is wired into a named, reachable surface in the admin
hub, or `bfddffe` is cleanly reverted — whichever the approver decides at
G1.

## Notes

**Not yet gated, and for a different reason than `ENG-004`.** This ticket's
`size: S` + `type: chore` would ordinarily auto-skip G1 per
`config/definition-of-done.md`'s Size table — but the ticket's entire scope
depends on an unresolved fork (wire in vs. delete) that only the approver
can settle, so G1 is being required anyway as a deliberate judgement call,
not because the size/type mechanics demand it. See the PRD's Readback
section for the reasoning. Separately, and on top of that: even if G1 were
being raised this pass, `wip.approver_limit` (2) had exactly one free slot
and it went to `ENG-003` — see that ticket's log.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-25` `intake → shaped` (product-manager) — shaped from
  `inbox/requests/2026-08-23-a4-poster-generator-unwired.md` (filed by the
  approver, received 2026-08-23, unprocessed for two days — a `scheduled
  manual-unblock` sweep pass's PM work, not a self-originated finding). Ran
  the full request-readback (`skills/request-readback/SKILL.md`): this PM's
  reading plus a blind architect reading (independent subagent, raw request
  + business profile + the admin-hub registry row only) — no material
  divergence; the architect's reading added a plausible print/QR-poster
  hypothesis (not treated as fact) and flagged a real risk this PM's first
  pass missed: the component may depend on code that exists only in
  `admin-hub`'s 64 uncommitted human-checkout files, which could make
  "wire it in" fail for reasons invisible to this department. See the PRD.
  PRD written at
  `agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`,
  deliberately without committed acceptance criteria for either branch of
  the fork (see PRD step 5 note) — writing criteria for an unmade decision
  would be inventing scope, which `skills/prd-writer/SKILL.md`'s own
  failure-modes list warns against.

  **G1 required despite auto-skip eligibility — logged explicitly since this
  deviates from the mechanical rule.** `size: S` + `type: chore` ordinarily
  skips G1 per the Size table ("S: Yes, unless bug/chore"). Requiring it
  anyway is a judgement call: the skip exists for routine work whose shape
  is already understood, and this ticket's shape — wire in vs. delete — is
  exactly the thing G1 exists to settle, not a scope this PM can responsibly
  guess at just because the ticket is small. Treated as a shaping judgement
  call in the same spirit as the doc-inconsistency calls `ENG-002`'s pass
  made (logged, not hidden), not as a formal process exception under
  `agents/eng-manager/config/exceptions.md` — no established rule is being
  broken, since neither `config.yaml` nor `definition-of-done.md` addresses
  what to do when a ticket's own scope is the open question.

  **G1 not raised this pass regardless** — `wip.approver_limit` (2) had one
  free slot, which went to `ENG-003` (see that ticket's log for the
  ordering). Holding at `shaped`, owner `product-manager`. `chained: none`
  — held by the WIP cap; the next dispatch's To-do-column pick-up
  (`schedules/eng_build_loop.md` step 6) advances this, not a chain fired
  from here.
