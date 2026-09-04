---
id: ENG-035
title: "`autopilot`'s system-triggered marketing actions skip authentication entirely — a client-controlled flag reaches a real message-send trigger with no gate"
project: aiorders-api
type: security
size: S
time_estimate: a few hours to half a day
time_spent:
time_remaining:
severity: P0
priority:
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: architect
created: 2026-09-03
updated: 2026-09-04
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-035-autopilot-systemtriggered-auth-bypass.md
  design: agents/architect/designs/ENG-035-autopilot-systemtriggered-auth-bypass.md
  adrs: [ADR-016]
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`supabase/functions/autopilot/index.ts` routes any request carrying
`systemTriggered: true` and a recognized marketing action straight to
`handleMarketing`, **before** the function's own (already-weak) `apikey`
check runs. `systemTriggered` is read directly from the caller's JSON body —
not a header, signature, or secret — so nothing distinguishes a legitimate
system call (a database trigger, per `handlers/welcome.ts`'s own comment)
from an arbitrary HTTP request. Full evidence, file:line citations, and the
repo's own `README.md` naming this exact assumption ("should never be
publicly reachable without another gate") are in the PRD (link above) — not
duplicated here.

Net effect: any caller, with no key or session of any kind, can trigger a
real "welcome offer" email/SMS send to an arbitrary customer/restaurant
pairing (`welcome_offer` is fully implemented; `birthday_offer`/
`winback_offer` are stubs). Real production side effect and cost, not a data
read.

## Outcome

The `systemTriggered` marketing branch denies any caller who cannot present
a real system-level credential — verified by a negative-case test per
marketing action, not just the positive case. The legitimate system caller's
existing `welcome_offer` flow keeps working unchanged.

## Notes

**How this was found.** Not an assigned security sweep — a byproduct of
`ENG-029`'s own tech-design research (restaurant-ownership check on
`autopilot`'s 8 template/log actions), which required reading `index.ts` in
full to design that fix. `ENG-029`'s own evidence was explicitly scoped to
"every one of the 8 actions" and never examined this third routing branch.
Different bug class (authentication bypass via a client-controlled trust
flag, not a missing ownership check) and a non-overlapping code path
(`marketing/`, not `handlers/templates.ts`/`handlers/logs.ts`) — out of scope
for `ENG-029`'s own diff, so filed as its own ticket per
`schedules/eng_build_loop.md` step 3's P0 carve-out.

**Relationship to `ENG-022`/`ENG-029`/`ENG-030`.** Fourth instance this week
of an authorization gap on this codebase, but the **first of a different bug
class** — the other three are all "a real ownership-check primitive exists
(or should) but is missing/defeated/unwired"; this one is "the code trusts a
client-supplied flag as if it were proof of system identity." No existing
`verifyRestaurantAccess`/`requireRestaurantAccess` primitive applies here
directly, since there's no calling *user* to check ownership against — the
legitimate caller is a system component, not a restaurant owner. The fix
shape is different: a system-level credential check, not a restaurant-scope
check. Flagged as a pattern worth the EM's or approver's attention
(`ENG-030`'s own PRD already named three instances of the ownership-check
class as worth a dedicated sweep; this is a second, distinct class on top of
that).

**Not yet located: the real invocation path.** `welcome.ts`'s comment names
"database trigger" as the intended caller, but this PRD did not find the
actual trigger/webhook definition (likely Supabase project config, not
tracked in a migration in this repo). The design step needs to confirm how
the legitimate caller invokes this today before picking a mechanism it can
actually satisfy — named as a risk in the PRD, not resolved here.

## Log

- 2026-09-03 `intake → shaped` (architect, `continue` event pass, context
  `ENG-029` — this finding is a byproduct of that pass's own tech-design
  research, not its assigned subject; see `ENG-029` for the assigned work).
  Mode check clean (repo-root `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean (run before this ticket existed; scoped re-run post-pass below).

  PRD written short-form (auto-skip type, no readback — agent-originated
  finding with its own evidence, `skills/request-readback/SKILL.md`'s "when
  this does NOT run" list). Evidence gathered by reading
  `supabase/functions/autopilot/index.ts`, `marketing/index.ts`,
  `marketing/welcome.ts`, `marketing/birthday.ts`, `marketing/winback.ts`,
  and `marketing/utils.ts` in full against `origin/main` — confirmed the
  routing order (marketing branch checked before the `apikey` check),
  confirmed `welcome_offer` is fully implemented while
  `birthday_offer`/`winback_offer` are stubs, and confirmed
  `supabase/functions/README.md`'s `## autopilot` Notes already name the
  exact assumption being violated ("should never be publicly reachable
  without another gate"). Cross-checked `proposals.md`, `observations.md`,
  `agents/security/reviews/`, `agents/security/notebook/`, and
  `decision-journal.md` for any prior mention of this specific gap before
  filing — none found; closest prior art is `ENG-022`/`ENG-029`/`ENG-030`'s
  own non-goals naming a broader audit as a deferred question, not a
  duplicate finding.

  Incident notice raised: `inbox/2026-09-03-eng035-p0-incident.md`
  (`gate: incident`, `agent: architect`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter and `traces/eng-notify-2026-09-03.log` for the result.

  **State:** `intake → shaped`, `owner: product-manager → architect`.
  **Consequence:** does not consume approver-facing WIP or the approval cap —
  `security`-typed, auto-skip G1, nothing waiting at a gate. Machine WIP
  (1/1, the `ENG-016` family) also unaffected — `shaped` is short of the
  counted range (`ready` through `ready-to-ship`).

  `chained: ENG-035` — `shaped`, owned by `architect`, an agent-owned state;
  firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
  ENG-035` before this pass exits so the design step starts without waiting
  for a scheduled sweep, given the severity — same precedent `ENG-022`'s,
  `ENG-029`'s and `ENG-030`'s own creation entries set. This is the primary
  ticket's (`ENG-029`) own second, separate chain fire in this pass; see that
  ticket's own log for its own chain record. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
  `ENG-029`/`ENG-035`: see pass notes in `agents/eng-manager/board/_index.md`.

- `2026-09-03` no state change — **broken-chain recovery** (eng-manager,
  `scheduled` event pass — whole-board sweep, step 8 dead-end sweep).
  Cross-checked this ticket's own `chained: ENG-035` line against what
  actually happened since, per `eng_build_loop.md` step 8's "a chain that
  was fired is not the same as a chain that ran": no
  `traces/.hops-2026-09-03-ENG-035` file exists (every other ticket touched
  today has one); `traces/.pending` carries no `continue ENG-035` line,
  queued or otherwise; no `*-eng-events-dropped.md` file (today's or
  otherwise) names a dropped `continue ENG-035`; and this log has carried no
  entry since the creation entry above, ~9 hours ago. Conclusion: the fire
  was made but never reached a session — not a drop (no drop notice exists
  to match), not a pass that forgot to chain (the chain line is right
  there) — a lost fire, the same class already named in this instance's own
  incident history as "queued-but-never-drains." This exact gap (board
  ticket exists, no In-flight row, no counter bump) was already noticed
  twice before today and left unfixed, out of scope for the narrow
  `continue ENG-031` events that found it (`observations.md`, rows dated
  2026-09-02 and 2026-09-03) — this sweep is the first pass with the
  whole-board mandate to actually close it.

  **Board index fixed in the same edit:** In-flight row added for
  `ENG-035` (`shaped`, owner `architect`, severity `P0`); `Next ID` counter
  corrected `ENG-035 → ENG-036` (035 has been an allocated ticket since
  2026-09-03T16:56, so 036 is the true next free id — same shape the
  2026-09-02 `ENG-026` counter fix already set). See
  `agents/eng-manager/board/_index.md`'s dated entry for this pass.

  **0 transitions.** `chained: ENG-035` — re-fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-035` before this pass exits: `shaped`, owned by `architect`,
  an agent-owned state, not blocked, not terminal, not held by a cap — the
  same conditions that justified the original (lost) fire still hold.
  Proposal filed (`proposals.md`): the board-index-omission gap is now a
  third occurrence and worth a mechanical check
  (`lib/eng-gate-check.sh`) rather than a fourth pass re-noticing it by
  hand.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` `shaped → designed` (architect, `continue` event pass,
  context `ENG-035` — this ticket's own turn per the recovery sweep's own
  re-fired `chained: ENG-035`). Narrow scope per this event's own contract —
  this ticket only, plus the one byproduct P0 it surfaced (below). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*); not mid-PRD,
  so step 2's checkpoint note doesn't apply. Mode check clean (repo-root
  `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
  (`ENG-035`): both exit 0, clean.

  Read the real code before designing against it, per
  `agents/architect/agent.md` ("match the codebase"). The shared
  `_eng/aiorders-api` worktree was on a stale feature branch
  (`feat/ENG-031-catering-order-capture-migration`, already shipped) with
  one pre-existing stray untracked file
  (`supabase/functions/brand-portal/deno.lock` — third notice, see
  `observations.md`), not on `main` — so read every file this design needed
  via `git show origin/main:` instead of trusting or disturbing that
  worktree, same approach `ENG-029`'s own design pass used for the identical
  reason. `git fetch origin main` first (`3cf5607..78194da`). Read `index.ts`
  and every `marketing/*.ts` file in full against `origin/main`, confirming
  the PRD's own evidence exactly: the `systemTriggered` branch runs before
  the `apikey` check, `welcome_offer` is fully implemented, `birthday_offer`/
  `winback_offer` are stubs.

  **The PRD's own named risk — the real invocation path was not located in
  this repo — investigated, not just carried forward.** `supabase/config.toml`
  confirmed to hold only `project_id`, no per-function `verify_jwt` override;
  a full-repo migration search found no trigger definition naming
  `autopilot` or `welcome_offer`. But two *general* trigger-to-edge-function
  conventions do exist in this project's own migration history:
  `20260807000004_fix_restaurant_website_cache_invalidation_trigger.sql`
  (a row-level Database Webhook via `supabase_functions.http_request(...)`,
  confirmed via the migration's own `RAISE EXCEPTION` guard to carry an
  `Authorization` header copied from a sibling trigger) and
  `20260217000001_platform_analytics_cron.sql` (a `pg_cron` + raw
  `net.http_post` scheduled job with no `Authorization` header at all).
  `welcome_offer`'s own trigger is row-level, matching the first group's
  shape, not the second's — full reasoning in the design and `ADR-016`.

  **Byproduct P0 found and filed separately, not folded into this diff:
  `ENG-036`.** Understanding `marketing/utils.ts`'s own legitimate call
  pattern (required to design this ticket's fix) meant reading
  `outgoing-communications/index.ts`, the function it calls into. That read
  found the identical bug shape — a client-supplied `systemTriggered` flag
  skipping authentication entirely — but wider: it gates the function's
  *entire* auth requirement, for every actor (`influencer`/`brand`/
  `consumer`/`admin`), not one branch. Confirmed live and reachable by
  reading all four `actors/*.ts` handlers in full: `consumers.ts`'s
  `order_feedback_request` (real, fetches a live order by a caller-supplied
  `orderId`) and `welcome_offer`/`every_order`/`first_order`; `brands.ts`'s
  real campaign-notification emails; `admin.ts` and most of
  `influencers.ts` are stubs. Different file, non-overlapping diff from this
  ticket's own — out of scope for this design's own diff, so filed per
  `schedules/eng_build_loop.md` step 3's P0 carve-out, same as this ticket's
  own creation: PRD
  (`agents/product-manager/specs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md`,
  short-form, `security`-type auto-skip G1), board ticket
  (`agents/eng-manager/board/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md`,
  `intake → shaped`, `owner: architect`), incident notice
  (`inbox/2026-09-03-eng036-p0-incident.md`, `lib/eng-notify.sh raise` run,
  exit 0, `notified: 2026-09-04T02:52:24` stamped by hand — script gave no
  delivery confirmation, same as every prior incident notice today). One
  observation filed (`observations.md`): three of this week's four
  authorization gaps were each found as a byproduct of designing the
  previous one, not through an assigned sweep — worth naming as a pattern.

  **Design:** `agents/architect/designs/ENG-035-autopilot-systemtriggered-auth-bypass.md`.
  A new `marketing/auth.ts` exporting `authorizeSystemTrigger(req,
  responseHeaders)`, extracted (not inlined) for the same testability reason
  `ENG-030`'s `analytics/auth.ts` was: `index.ts` calls `serve(...)` at
  module scope, so a test importing it would start a listener. The check:
  `Authorization` must equal `Bearer ${SUPABASE_SERVICE_ROLE_KEY}` — a
  secret this function already reads, never exposed to any client — rather
  than a new secret or the existing `SB_PUBLISHABLE_KEY` (that key is
  designed to be embedded client-side in all four frontends, so gating on it
  alone would not meet AC1's "real system-level credential" bar the PRD
  sets, and would erase the PRD's own stated distinction from
  `ENG-022`/`ENG-029`/`ENG-030`). **One ADR** (`ADR-016`, `decided_by:
  architect`, reversible) records the full reasoning and the two rejected
  alternatives (a new dedicated secret; a signature-verified mechanism).
  `_index.md` there updated (`next_id` → `ADR-017`). **No one-way door** —
  an additive header check ahead of unchanged handler code, no schema
  change, no new datastore or vendor. `touches_data: false`, `touches_models:
  false`. Every acceptance criterion walked individually against the design
  (AC3 covered by gating all three marketing actions in one place; AC4 by
  the extracted, dependency-free check). Full risk table in the design
  itself — **the central, named risk is that the live trigger's actual
  headers cannot be confirmed from this repo** (no DB/CLI/MCP access this
  session); the design cites a real prior incident in this exact codebase
  where an identical class of newly-added header check silently broke a
  sibling trigger for an unknown period
  (`20260807000004`'s own commit message) as the reason this isn't treated
  as a solved problem — mitigated with a distinct denial log line and a
  mandatory manual post-deploy verification step named in Rollout, not left
  as a bare risk statement.

  **State:** `shaped → designed`. **Owner stays `architect`**, not moved to
  `eng-manager` — matches `ENG-029`'s own precedent (state and owner move
  together only when routing actually reaches `ready`).

  **Routing: would be `ready` — held at `designed` instead.** Neither L0 nor
  a one-way door, so the design's own routing reads `ready`, `owner:
  eng-manager`. Machine WIP re-checked fresh from every ticket's own
  frontmatter, not the board header: `ENG-016` (`building`), `ENG-032`
  (`building`), `ENG-033`/`ENG-034` (`ready`) — still `1/1`, none `shipped`.
  Same precedent `ENG-014`/`ENG-017`/`ENG-020`/`ENG-021`/`ENG-023`/`ENG-025`/
  `ENG-026`/`ENG-029`/`ENG-030` already set: held at `designed`, owner
  staying `architect`, rather than writing `ready` while the one slot is
  occupied. `ENG-036` is unaffected by this cap — `shaped` sits outside the
  counted range.

  **Dead-end sweep:** out of scope for a `continue` event (narrower
  contract) — not attempted beyond the `ENG-036` byproduct above, which
  surfaced unsought while reading this ticket's own required evidence. One
  tangential observation filed anyway (cheap, no obligation, step 8b is
  not-negotiable): `20260217000001_platform_analytics_cron.sql`'s cron job
  calls its own edge function (`platform-analytics`) with no `Authorization`
  header and no body-level flag either — noticed only while researching this
  design's own trigger-convention question, not chased (a compute-cost
  question at most, not a clear P0: no message send, no PII in the fire-and
  forget call itself as far as this pass read).

  **Notify sweep:** `ENG-036`'s incident raised and notified above. Swept
  every open `inbox/` item's `notified:`/`nudged:` against the 24h threshold
  (`date -u`: `2026-09-04T02:52`-ish) — nothing newly crosses it since the
  immediately preceding pass's own check (`ENG-015`/`ENG-027`/`ENG-028` all
  still under 24h; `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` already carry
  their one-ever nudge; `ENG-029`/`ENG-030`/`ENG-035` P0 incidents all still
  under 24h regardless of the standing judgment call on whether an
  FYI-only notice should ever be nudged).

  **Board update** — In-flight row for `ENG-035` (`shaped → designed`);
  new row added for `ENG-036`; `Next ID` corrected `ENG-036 → ENG-037`. See
  `agents/eng-manager/board/_index.md` for the full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board and
  scoped `ENG-035`/`ENG-036`: see board index.

  `chained: none` — `designed`, owned by `architect`, not the approver, not
  blocked, not terminal, but held by the machine-WIP cap (`1/1`, the
  `ENG-016` family) — one of the documented no-chain conditions; re-check
  once that family reaches `shipped`. `chained: ENG-036` — `shaped`, owned
  by `architect`, an agent-owned state, not held by any cap (`shaped` sits
  outside the counted WIP range); firing `/bin/zsh
  departments/engineering/lib/eng-trigger.sh continue ENG-036` before this
  pass exits so its own design step starts without waiting for a scheduled
  sweep, given the severity.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` no state change — **decision** event pass, context
  `2026-09-03-eng035-p0-incident.md` (this ticket's own P0 incident notice,
  answered). Reading map for `decision`: steps 4 and 8c, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
  lanes*, *Guards*) — step 5 doesn't apply (not an L1 merge request), step 6
  doesn't apply (the answer doesn't advance the ticket into a machine-owned
  state), step 8's `blocked_from` paragraphs don't apply (ticket isn't
  leaving `blocked`), and neither does *The chain* (this incident is about a
  ticket, not the loop/queue itself). Mode check clean (repo-root `.env` →
  `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-035`) and
  whole-board: both exit 0, clean.

  **The item itself:** `decision: approved`, `decided:
  2026-09-04T14:57:18Z`, no `priority` set, no question asked back — same
  shape as `ENG-022`'s and `ENG-029`'s own P0 incident acknowledgements: a
  bare approval reads as acknowledgement of the interrupt, not an
  instruction to reorder the board.

  **Re-verified current state before concluding "untouched," not assumed
  from the last log entry.** Machine WIP re-checked fresh from every
  ticket's own frontmatter: `ENG-016` `building`, `ENG-031`/`ENG-032`
  `verified`, `ENG-033` `blocked` (`owner: approver`), `ENG-034` `ready` —
  still `1/1`, the family occupies the slot via `ENG-016` (parent, not yet
  `shipped`) and `ENG-034` (the one child still inside the counted
  `ready..ready-to-ship` range). `ENG-035`'s own `priority:` stays empty —
  the one lever the incident notice offered was not exercised. Conclusion
  unchanged from the prior entry: still `designed`, still held, no
  transition available.

  Checked `traces/.pending` while here: `ENG-036`'s own P0 incident item
  already carries `decision: changed` and a `decision
  2026-09-03-eng036-p0-incident.md` event is already queued behind one
  `watch launchd` self-echo — not a lost fire, out of scope for this
  ticket's own narrow event regardless (a different ticket's answered gate).

  Processed note appended to the incident item and moved to
  `inbox/_handled/2026-09-03-eng035-p0-incident.md`, per `eng_build_loop.md`
  step 4's Incident handling (act on the item's own `recommendation:`, then
  archive — no further owner to hand off to). **Journal (step 8c):** row
  added to `decision-journal.md` for this answered gate.

  **Notify sweep (step 7):** swept `inbox/` fresh (`date -u`:
  `2026-09-04T15:13:17Z`) — six open items besides this one. `ENG-009`/
  `ENG-010`/`ENG-027` already carry a `nudged:` timestamp; `ENG-028`'s G1
  (~23h03m since `notified:`), `ENG-030`'s P0 incident (~23h49m), and
  `ENG-033`'s merge request (~13h30m) all still sit under the 24h threshold
  — `ENG-030`'s is close enough that the next pass to touch `inbox/` should
  expect to nudge it. `ENG-036`'s P0 incident already carries a `decision:`
  and is excluded. Nothing crosses this pass; no nudge sent.

  **Step 8b:** nothing new to observe or except beyond the queued-`ENG-036`
  check above (not an anomaly — the queue working as designed). No
  `exception-request:` found in any ticket log.

  business-os itself left uncommitted, same standing default the last
  several passes have each restated — see this session's own final summary
  for the current state of that open question; not re-decided here.

  **Board update (step 10):** In-flight row's `Updated` date bumped
  (2026-09-03 → 2026-09-04), state/owner unaffected. The live file held
  three dated pass entries before this one; rolled the oldest
  (`watch (launchd): all three inboxes swept, no new signal`) to
  `_index-archive.md` first, then appended this pass's own entry, keeping
  three per the keep-three rule. See `_index.md` for the full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-035`) and whole-board: both exit 0, clean.

  `chained: none` — still held by the machine-WIP cap (`1/1`, the `ENG-016`
  family), same condition as the prior entry, re-confirmed fresh rather than
  assumed; re-check once that family reaches `shipped`. Not blocked, not
  terminal, not waiting on the approver — only the cap.
