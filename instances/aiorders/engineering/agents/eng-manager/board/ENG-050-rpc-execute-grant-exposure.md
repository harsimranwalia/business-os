---
id: ENG-050
title: Two production RPC functions grant `EXECUTE` to `anon`/`authenticated` — unauthenticated platform-analytics and acquisition-breakdown exposure
project: aiorders-api
type: security
size: S
time_estimate: an hour or two — fix statement already proven twice today on this project (ENG-048)
time_spent:
time_remaining:
severity: P0
priority:
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: security
created: 2026-09-07
updated: 2026-09-07
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-050-rpc-execute-grant-exposure.md
  design: agents/architect/designs/ENG-050-rpc-execute-grant-exposure.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`calculate_platform_analytics()` and `get_acquisition_breakdown(uuid,
timestamptz, timestamptz)` (`aiorders-api`,
`supabase/migrations/20260217000001_platform_analytics_cron.sql` and
`20260905190000_add_acquisition_breakdown_rpc.sql`) each grant `EXECUTE`
only to `service_role` in their own migration, but this project's
`pg_default_acl` also grants `anon`/`authenticated` `EXECUTE` on every new
function by default, and neither migration — nor any other in this repo —
ever revokes it. Full evidence, exact mechanism, and confirmation this is
live in production today are in the PRD (link above) — not duplicated here.

Net effect: any caller holding this project's public anon key can call
either function directly via `supabase.rpc(...)`, today, bypassing both
functions' intended callers (an hourly cron job; `brand-portal`'s own
ownership check) entirely.

## Outcome

Both functions deny `anon` and `authenticated` callers with a real
permission error, verified by an actual denied call, not just a catalog
read. Their two legitimate `service_role` callers (`platform-analytics`'s
cron job, `brand-portal/acquisition.ts`'s ownership-checked path) keep
working unchanged.

## Notes

**How this was found.** Not an assigned security sweep —
`agents/eng-manager/proposals.md`'s 2026-09-07 row (principal-engineer,
reviewing `ENG-048` round 1) found the pattern project-wide but explicitly
deferred "is this actually exploitable" to security. Security made that
call during `ENG-048`'s own security gate, confirmed live twice
independently (production catalog query; disposable-replica reproduction),
and filed the P0 finding:
`agents/eng-manager/inbox/2026-09-07-security-p0-rpc-execute-grant-exposure.md`
(now processed, see Log).

**Severity correction.** The originating finding's frontmatter read
`severity: P1`; its title, carve-out citation, and body reasoning were P0
throughout. Resolved to `P0` in this ticket — matches the carve-out being
invoked, security's own notebook entry, and the bar
`ENG-022`/`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036` were all rated at. See
PRD "Impact" section.

**Data-classification correction.** The originating finding called the
exposed data "Internal"; `security-baseline.md`'s own table lists revenue
under **Confidential**. Doesn't change the outcome — the P0 rating and the
carve-out both turn on the live-exploit criterion
(`security-baseline.md`: "active incident (leaked credential, live exploit,
exposed data)"), independent of data tier. See PRD "Impact".

**The exact fix is already proven, twice, today, on this project** —
`ENG-048`'s own `credit_order_if_eligible` carried the identical gap (found
by code review, fixed by database, independently re-verified four times
including this project's own security gate). Adapted fix and verification
method: PRD "Proposed change"/AC5.

**Scope of a project-wide sweep** (the originating proposal's own
suggestion — "likely the same gap on… most of them") is a design-time scope
call, not pre-decided here; see PRD "Proposed change".

**Bookkeeping.** `agents/eng-manager/proposals.md`'s 2026-09-07
principal-engineer row corrected in place, marked superseded by this
ticket, same pass (see Log).

## Log

- `2026-09-07` `intake → shaped` (eng-manager, `finding` event pass, context
  `rpc-execute-grant-exposure` —
  `agents/eng-manager/inbox/2026-09-07-security-p0-rpc-execute-grant-exposure.md`).
  Reading map for `finding`: step 3, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*); also read
  `agents/eng-manager/config/security-baseline.md` and
  `agents/security/agent.md`'s `interrupt_rule` in full, and
  `agents/eng-manager/config/definition-of-done.md`'s ticket-states table
  for the `security`-type G1 auto-skip — none named directly by the map,
  needed to evaluate the finding's own escalation call rather than
  transcribe it. Mode check clean (repo-root `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  Confirmed `aiorders-api` registered `L1`, not internal
  (`config/projects.md`) — carve-out applies (`schedules/eng_build_loop.md`
  step 3).

  Read both migration files in full against the department worktree
  (`~/Documents/projects/_eng/aiorders-api`), independently of the finding
  card's own account: confirmed both functions' only grant is `...
  TO service_role`, zero `revoke` statements anywhere in
  `supabase/migrations/`. Read both functions' actual callers rather than
  assuming the intended-caller framing: `platform-analytics/index.ts`
  (`SUPABASE_SERVICE_ROLE_KEY` at lines 230/236, `.rpc('calculate_platform_
  analytics')` at line 53) and `brand-portal/index.ts`/`acquisition.ts`
  (`SUPABASE_SERVICE_ROLE_KEY` at lines 31/41, `handleAcquisition` at line
  192, `verifyRestaurantAccess` before the RPC call) — both legitimate
  callers confirmed `service_role`, so the fix cannot break either; AC3/AC4
  written `[stated]`, not inferred.

  **Two corrections made to the finding as filed, not silently absorbed:**
  severity (`P1` frontmatter vs. P0 body/carve-out throughout — resolved
  P0) and data classification (`Internal` claimed vs.
  `security-baseline.md`'s own table naming revenue `Confidential`) —
  neither changes the outcome, both recorded in this ticket's Notes and in
  the PRD's Impact section so neither reads as silently overridden.

  PRD written short-form (auto-skip type, no readback — agent-originated
  finding with its own evidence, `skills/request-readback/SKILL.md`'s "when
  this does NOT run" list):
  `agents/product-manager/specs/ENG-050-rpc-execute-grant-exposure.md`.

  **Escalated to the approver, not filed silently.**
  `security-baseline.md` ("Only two things reach the approver directly: an
  active security incident (leaked credential, live exploit, exposed
  data)…") and `agents/security/agent.md`'s `interrupt_rule` ("P0 only —
  active incident, leaked credential, or exposed data (via the EM)") — this
  is exactly that channel, and the finding is a confirmed, reproducible
  live exploit independent of the data-tier question above. Same precedent
  `ENG-022`/`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036` already set: incident
  notice raised, informational only, `agent: eng-manager` (the agent
  processing this finding — this field names whoever raises the notice, not
  necessarily the original finder). `inbox/2026-09-07-eng050-p0-incident.md`.
  Ran `lib/eng-notify.sh raise` on it — see the item's own frontmatter for
  the result.

  Corrected `agents/eng-manager/proposals.md`'s 2026-09-07
  principal-engineer row in place — marked superseded by `ENG-050`, per the
  finding's own bookkeeping instruction and the file's existing
  correction-in-place convention. Moved the originating finding card to
  `agents/eng-manager/inbox/_processed/`, annotated.

  **State:** `intake → shaped`, `owner: eng-manager → architect`.
  **Consequence:** does not consume approver-facing WIP or the approval cap
  — `security`-typed, auto-skip G1, nothing waiting at a gate (the incident
  notice is informational, not a gate). Machine WIP (`1/1`, the `ENG-026`
  family) unaffected — `shaped` is short of the counted `ready`..
  `ready-to-ship` range.

  **Dead-end sweep:** out of scope for a `finding` event (narrower
  contract) — nothing else surfaced unsought this pass.
  **Notify sweep:** the incident notice above is the only new gate item
  this pass wrote; raised immediately per step 7.
  **8b:** nothing new to observe or except beyond the two corrections
  already logged above (Notes). The security-gate A01 checklist
  three-strike note in `agents/security/notebook/2026-09-07-findings.md` is
  explicitly not this ticket's and explicitly not blocking — left as
  security filed it.
  **8c:** n/a — the incident notice is freshly raised this pass, not
  answered; journaling happens on the pass that processes the approver's
  reply, same as `ENG-030`'s own precedent.

  **Board update:** `_index.md` — Next ID counter bumped to `ENG-051`;
  `ENG-050` added to In-flight table; oldest of the three live dated
  entries rolled to `_index-archive.md` per the keep-three rule before this
  pass's own entry was appended.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-050`) and whole-board: both exit 0, clean.

  `chained: ENG-050` — `shaped`, owned by `architect`, an agent-owned
  state; firing
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-050`
  before this pass exits so the design step starts without waiting for a
  scheduled sweep, given the severity — same precedent
  `ENG-022`'s/`ENG-029`'s/`ENG-030`'s/`ENG-035`'s own creation entries set.

- `2026-09-07` `shaped → designed` (architect, `continue` event pass).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*); ticket
  was not mid-PRD, so step 2's checkpoint note doesn't apply. Also read
  `skills/tech-design/SKILL.md` in full (owning skill for this step, named
  by the architect's own `agent.md` but not by the reading map directly) and
  `agents/architect/agent.md`. Mode check re-verified fresh, not taken from
  the checkpoint: repo-root `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty. Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-050`) and
  whole-board: both exit 0, clean.

  **Design:** `agents/architect/designs/ENG-050-rpc-execute-grant-exposure.md`.
  Applies `ENG-048` round 2's own proven statement
  (`revoke execute on function {name} from public, anon, authenticated;
  grant execute on function {name} to service_role;`) to both functions in
  one new migration — no schema change, no interface change, both functions'
  bodies untouched. **Independently re-verified the PRD's own "no other
  caller" claim rather than taking it on trust:** grepped both function
  names across all five registered repos
  (`aiorders-api`/`aiorders-admin-hub`/`config-site-builder`/
  `restaurant-marketplace`/`restaurant-portal`) — confirmed exactly the two
  already-named `service_role` callers exist, `aiorders-admin-hub` carries
  only generated type definitions (never an actual call), and the other
  three repos have zero references. AC3/AC4 hold. No one-way door — a
  reversible privilege correction, decided here per
  `skills/tech-design/SKILL.md` step 8, not escalated; `awaiting-decision`
  (G2) correctly not entered.

  **Scope decision (the PRD's own "architect sizes it at design time" ask):**
  scoped this ticket to exactly the two functions security confirmed
  live-exploitable — matches AC1–5, the Outcome section, and the S/"an hour
  or two" estimate. The project-wide sweep of the repo's other ~10 functions
  stays **out of this ticket**, sized separately: corrected
  `agents/eng-manager/proposals.md`'s 2026-09-07 principal-engineer row in
  place (same file's own correction-in-place convention) with this sizing
  decision, rather than leaving "for whoever picks this up" unresolved a
  second time. Full reasoning, including the two alternatives rejected for
  this scope (fixing `pg_default_acl` itself; an application-layer check),
  and the second occurrence of this project's `pg_default_acl` pattern (now
  building toward this role's own three-strike bar for promoting it into
  `engineering-standards.md`):
  `agents/architect/notebook/2026-09-07-eng050-design.md`.

  **Routing (`skills/tech-design/SKILL.md` step 11): not L0, no one-way
  door → `ready`, in principle.** Checked the machine-WIP cap before writing
  that, rather than assuming a free slot: `board/_index.md`'s own In-flight
  table shows `ENG-026` still `building` with children `ENG-044`–`047` all
  `shipped`, which reads like a second family alongside `ENG-027`
  (`building`) at a glance. Resolved by reading past the table rather than
  stopping at it —
  `_index-archive.md`'s own entry ("`ENG-047`: release-readiness — ... family
  settled, slot filled by `ENG-027`") and `ENG-048`'s own board-file log
  (`chained: ENG-049 — slot freed by ENG-048`, "the `ENG-027` family still
  holds the one slot, now via `ENG-049`") confirm `ENG-026`'s row is only
  waiting on its own no-diff closing hop, not a live second occupant.
  Confirmed current holder directly: `ENG-049` (`ENG-027`'s child) sits at
  `ready`, its `depends_on: [ENG-048]` satisfied (`ENG-048` parked,
  `blocked_on: approver`, PR open — Guards, "an open PR does satisfy
  `depends_on`") — `ready` counts toward the cap. `traces/.pending` shows
  `1 continue ENG-049` already queued (fired by `ENG-048`'s own pass), so
  this is active, not idle. **No slot free** — `ENG-050` stays at `designed`,
  `owner: architect`, joining the held-for-slot pool alongside
  `ENG-014`/`017`/`023`/`025`/`029`/`030`/`035`/`036`. 1 transition this
  pass, well under the cap of 4.

  **8b:** no new observation or exception beyond the `proposals.md` sizing
  correction already logged above. No `exception-request:` found on this
  ticket. **8c:** n/a — no G1/G2/G3/merge-request answered this pass (G1 was
  already auto-skipped, at intake).

  **Dead-end sweep (scoped to this event):** no other ticket's state
  changed. `ENG-026`/`ENG-027`/`ENG-048`/`ENG-049` read to resolve this
  ticket's own routing question, not touched.

  **Notify sweep:** nothing raised this pass — a design-only hop with no
  free slot to enter isn't a gate event, same as `ENG-027`'s own
  work-breakdown hop.

  **Board update:** `_index.md` — In-flight row updated (`state: designed`,
  `updated`), narrative note added.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-050`) and whole-board: both exit 0, clean.

  `chained: none — held by machine WIP cap` — the one slot is held by the
  `ENG-027` family via `ENG-049` (`ready`, dependency met, already queued —
  not idle, not this ticket's to chain past). Per the Guards on chaining, a
  ticket held by a cap waits, and that wait is the design; this is not one
  of the four `chained: none` reasons that requires an inbox item (not
  idle, not terminal, not a MODE halt, not a hop-budget exhaustion) — nothing
  written to `inbox/`. The next free slot's dispatch is the pass that
  frees `ENG-027`'s (via `ENG-049`'s own closing hop), not this one; no fresh
  `continue` fired for `ENG-050` itself.

  business-os itself left uncommitted through this edit — same standing
  default carried by every pass since the last reconciliation commit; the
  commit-convention question remains open, not re-decided here.
