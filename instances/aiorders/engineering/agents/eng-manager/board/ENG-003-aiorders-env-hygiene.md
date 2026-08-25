---
id: ENG-003
title: Untrack `.env` from config-site-builder and close related env-hygiene gaps
project: config-site-builder
type: chore
size: M
severity: P2
priority:
state: awaiting-scope
owner: approver
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
  prd: agents/product-manager/specs/ENG-003-aiorders-env-hygiene.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
---

## Input

Verbatim, from `inbox/requests/2026-08-23-aiorders-env-hygiene.md` (now
`inbox/_handled/`), filed by the approver, received 2026-08-23 — preserved
here per `skills/request-readback/SKILL.md` step 1, never edited:

> `.env` is tracked in config-site-builder and unignored in aiorders-admin-hub
>
> Found while committing the AIOrders working trees on 2026-08-23. Neither
> repo's `.gitignore` mentions `env` at all.
>
> **`config-site-builder/.env` is tracked in git.** It holds
> `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` and `VITE_GOOGLE_MAPS_API_KEY`
> with live values, and they are in the repo's history, not just its tip.
> [...]
>
> **`aiorders-admin-hub/.env` is untracked but not ignored** [...]
>
> The Google Maps key is the one worth an actual look: it is billable, and if
> it carries no HTTP-referrer restriction in Google Cloud it can be lifted
> from the bundle and spent by anyone.
>
> **What this asks for:** [1] Check/restrict the Maps key referrer
> restriction. [2] Get `.env` out of tracking in config-site-builder,
> `.gitignore` in both repos, plus a committed `.env.example`. [3] Decide
> whether rotation is warranted.
>
> Also minor, same family: `restaurant-marketplace/.claude/projects/` is
> untracked Claude session data with no `.gitignore` entry.

Full text in the handled request file.

## Readback

See `agents/product-manager/specs/ENG-003-aiorders-env-hygiene.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

`config-site-builder/.env` is tracked in git with live Supabase and Google
Maps credentials; neither it nor `aiorders-admin-hub` ignores `.env` at all.
The Maps key is the one with a real cost attached: if it has no
HTTP-referrer restriction in Google Cloud, it's spendable by anyone who pulls
it from the public bundle — but checking or fixing that is a console
operation this department has no configured access to.

## Outcome

`config-site-builder` no longer tracks `.env`; both it and
`aiorders-admin-hub` ignore `.env` and carry a committed `.env.example`;
`restaurant-marketplace` ignores its untracked Claude session directory; and
the Maps-key check plus any rotation decision are back in front of the
approver as explicit actions only they can take.

## Notes

Scoped `project:` to `config-site-builder` — it's where the only
actually-tracked secret lives, the highest-stakes single piece of this
ticket. The `aiorders-admin-hub` and `restaurant-marketplace` pieces are
smaller (`.gitignore`-only) fixes bundled into the same ticket at the
approver's own request ("same family... worth one line in the same pass")
rather than three separate tickets for three one-line changes. This means
execution touches three repos under one ticket id — see the PRD's Risks
section and the observation filed alongside this ticket.

This ticket does not and cannot check, restrict, or rotate any cloud-console
credential (Google Maps key, Supabase keys) — the department's autonomy here
is git-only. See PRD Non-goals.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-25` `intake → shaped → awaiting-scope` (product-manager) — shaped
  from `inbox/requests/2026-08-23-aiorders-env-hygiene.md` (filed by the
  approver, received 2026-08-23, unprocessed for two days — a `scheduled
  manual-unblock` sweep pass's PM work, not a self-originated finding). Ran
  the full request-readback (`skills/request-readback/SKILL.md`): this PM's
  reading plus a blind architect reading (via an independent subagent, given
  only the raw request + business profile + the relevant registry rows — no
  PM interpretation) — no material divergence on scope or problem; the
  architect's reading sharpened the tip-only-vs-history-rewrite distinction
  and confirmed the department's lack of GCP/Supabase console access
  independently. See the PRD's Readback section for both readings. `size: M`,
  so G1 is required regardless of type per
  `agents/eng-manager/config/definition-of-done.md` → Size table. PRD
  written at `agents/product-manager/specs/ENG-003-aiorders-env-hygiene.md`.
  No `## Dissent` — `agents/critic/agent.md` doesn't exist at the department
  or instance level (already filed as a proposal from `ENG-002`'s pass, not
  refiled). G1 item written to `inbox/2026-08-25-eng003-g1-scope.md` and
  notified. This is the one ticket of three shaped this pass whose G1 could
  be raised — `wip.approver_limit: 2` was at 1/2 (only `ENG-002`) going into
  this pass, leaving exactly one free slot; `ENG-004` and `ENG-005` (shaped
  the same pass, from the same batch of previously-unprocessed requests)
  hold at `shaped` for that reason — see their own tickets. `chained: none`
  — sitting at `awaiting-scope`, owned by the approver.
