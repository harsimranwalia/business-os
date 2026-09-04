---
id: ENG-029
title: Autopilot API has no restaurant-ownership check on any of its 8 actions — cross-tenant customer-data exposure
project: aiorders-api
type: security
size: M
time_estimate: half a day to a day
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
  prd: agents/product-manager/specs/ENG-029-autopilot-restaurant-scoping-broken.md
  design: agents/architect/designs/ENG-029-autopilot-restaurant-scoping-broken.md
  adrs: [ADR-015]
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`supabase/functions/autopilot/index.ts` and its two handler files
(`handlers/templates.ts`, `handlers/logs.ts`) never verify that the caller
owns the `restaurant_id` they pass in — on any of the 8 actions this function
serves, and without even requiring a valid logged-in session (only a public,
non-secret publishable key). Full evidence, file:line citations, and the
confirmed absence of any check are in the PRD (link above) — not duplicated
here.

Net effect: any caller who can reach this endpoint can read and write any
restaurant's automation templates, and read any restaurant's communication
log — including customer email, phone, and message content — by supplying a
different `restaurant_id`. No exploit tooling needed.

## Outcome

Every `autopilot` action that reads `restaurant_id` from its payload denies a
caller who doesn't own that restaurant, and denies a caller with no valid
session at all — verified by a negative-case test per action, not just the
positive case.

## Notes

**How this was found.** Not an assigned security sweep — a byproduct of
`ENG-019`'s own tech-design research, which reads this same send/log system
(`outgoing-communications` + `autopilot`) as reusable prior art for a new
restaurant-broadcast feature. `ENG-019`'s own design does not reuse
`autopilot`'s current pattern regardless of this ticket's timeline — its new
endpoints get their own ownership check, designed properly rather than
copied from a sibling that turned out unsafe.

**Existing correct primitive to reuse.** `brand-portal/utils.ts`'s
`verifyRestaurantAccess` (and `ENG-022`'s promoted, throwing
`requireRestaurantAccess`, once that ticket ships) is already the
department's correct pattern for exactly this check — likely reusable here
directly or via a small shared-utils move; architect's call at the design
step.

**Relationship to `ENG-022`.** Same bug class (missing/defeated
restaurant-ownership check, `brand-portal/utils.ts`'s own
`verifyRestaurantAccess` existing and correct), different function —
`autopilot` is untouched by `ENG-022`'s fix, which is scoped to
`brand-portal/` only. `ENG-022`'s own PRD named "auditing access checks
outside `brand-portal/`" as an explicit non-goal, worth a follow-on if the
pattern recurred — this is that follow-on, upgraded from "worth checking" to
"confirmed broken" once actually read.

## Log

- 2026-09-03 `intake → shaped` (architect, `continue` event pass, context
  `ENG-019` — this finding is a byproduct of that pass's own tech-design
  research, not its assigned subject; see `ENG-019` for the assigned work).
  Mode check clean (repo-root `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  PRD written short-form (auto-skip type, no readback — agent-originated
  finding with its own evidence, `skills/request-readback/SKILL.md`'s "when
  this does NOT run" list). Evidence gathered by reading
  `supabase/functions/autopilot/index.ts` in full against both its handler
  files (`handlers/templates.ts`, `handlers/logs.ts`) — every one of the 8
  actions traced from route to query, not pattern-matched — plus confirming
  the Supabase client here uses the service-role key (RLS bypassed
  regardless) and that `user`, though fetched, is never threaded into any
  handler's signature. Cross-checked `proposals.md`, `observations.md`,
  `agents/security/reviews/`, `agents/security/notebook/`, and
  `decision-journal.md` for any prior mention of this specific gap before
  filing — none found; the closest prior art is `ENG-022`'s own "outside
  `brand-portal/`" non-goal, not a duplicate finding.

  Incident notice raised: `inbox/2026-09-03-eng029-p0-incident.md`
  (`gate: incident`, `agent: architect`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter and `traces/eng-notify-2026-09-03.log` for the result.

  **State:** `intake → shaped`, `owner: product-manager → architect`.
  **Consequence:** does not consume approver-facing WIP or the approval cap —
  `security`-typed, auto-skip G1, nothing waiting at a gate. Machine WIP
  (1/1, `ENG-016`) also unaffected — `shaped` is short of the counted range
  (`ready` through `ready-to-ship`).

  `chained: ENG-029` — `shaped`, owned by `architect`, an agent-owned state;
  firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
  ENG-029` before this pass exits so the design step starts without waiting
  for a scheduled sweep, given the severity — same precedent `ENG-022`'s own
  creation entry set. This is a second chain fire in a pass whose primary
  subject is `ENG-019`; see that ticket's own log for its own, separate
  chain record. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: see pass
  notes in `agents/eng-manager/board/_index.md`.

- 2026-09-03 `shaped → designed` (architect, `continue` event pass, context
  `ENG-029` — this ticket's own turn at the front of `traces/.pending`).
  Narrow scope per this event's own contract — this ticket only, plus the
  one byproduct P0 it surfaced (below). Reading map for `continue`: steps 6
  and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*, *The four lanes*, *Guards*). Mode check clean (repo-root
  `.env` → `MODE=active`; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-029`) and whole-board: both exit 0, clean.

  Read the real code before designing against it, per
  `agents/architect/agent.md` ("match the codebase"): `~/Documents/projects/_eng/aiorders-api`
  was mid-build on `ENG-016`'s own family (branch
  `feat/ENG-016-catering-quote-generator`, two files uncommitted —
  `ENG-031`'s own migration and a pre-existing untracked `deno.lock`, neither
  touched) — so read every file this design needed via `git show origin/main:`
  instead of trusting or disturbing that worktree, same approach `ENG-021`'s
  own pass used for the identical reason. Read `index.ts` and both handler
  files in full against `origin/main`, confirming the PRD's own table exactly:
  6 template actions with no ownership check, `get_logs`/`get_stats` the same,
  `user` fetched but declared-and-unused in both handler signatures (the
  board's own creation-entry log said "never threaded into any handler's
  signature" — technically imprecise, since it *is* in both signatures, just
  never read from; the substance — no check happens — is correct, not
  reopened here, out of this event's own narrow contract). Confirmed
  `ENG-022`'s branch (`fix/ENG-022-brand-portal-tenant-isolation`) is not
  merged (`git merge-base --is-ancestor` against `origin/main`: false) before
  deciding whether this design could depend on it.

  **Byproduct P0 found and filed separately, not folded into this diff:
  `ENG-035`.** Reading `index.ts` in full (required to design this ticket's
  own fix) surfaced a third routing branch — `systemTriggered`-gated
  marketing actions (`welcome_offer`, fully implemented;
  `birthday_offer`/`winback_offer`, stubs) — checked *before* even the weak
  `apikey` gate, trusting a plain client-supplied boolean as proof of system
  identity. Confirmed live and reachable with zero credentials by reading
  `marketing/index.ts`, all three `marketing/*.ts` handlers, and
  `marketing/utils.ts`'s send/queue functions directly; cross-checked against
  `supabase/functions/README.md`'s own `## autopilot` Notes, which already
  name the exact assumption being violated ("should never be publicly
  reachable without another gate"). Different bug class from this ticket
  (authentication bypass via a trusted client flag, not a missing ownership
  check) and a non-overlapping code path — out of scope for this design's own
  diff, so filed per `schedules/eng_build_loop.md` step 3's P0 carve-out, same
  as this ticket's own creation: PRD
  (`agents/product-manager/specs/ENG-035-autopilot-systemtriggered-auth-bypass.md`,
  short-form, `security`-type auto-skip G1), board ticket
  (`agents/eng-manager/board/ENG-035-autopilot-systemtriggered-auth-bypass.md`,
  `intake → shaped`, `owner: architect`), incident notice
  (`inbox/2026-09-03-eng035-p0-incident.md`, `lib/eng-notify.sh raise` run,
  exit 0, `notified: 2026-09-03T16:57:26` stamped). One observation filed
  (`observations.md`) naming the cross-ticket pattern — two independent
  authorization-bug classes surfacing this week, not just a fourth instance
  of the same one.

  **Design:** `agents/architect/designs/ENG-029-autopilot-restaurant-scoping-broken.md`.
  A session check (`index.ts`, one new location, closes AC2 for all 8 actions
  at once) plus a per-action ownership check (`templates.ts`/`logs.ts`,
  threading the already-fetched-but-unused `user` down into each action
  function), reusing `_shared/restaurantAccess.ts`'s `verifyRestaurantAccess`
  — already on `main`, already return-based (matching both handler files' own
  no-throw convention with no wrapper needed), already proven as a
  cross-function-directory primitive by `api-key-auth`. **One ADR**
  (`ADR-015`, `decided_by: architect`, reversible): why `_shared/
  restaurantAccess.ts` was used instead of `brand-portal/utils.ts`'s version
  the PRD's own Notes speculated about — the latter's throwing variant exists
  only on `ENG-022`'s own unmerged branch, and using it would have forced an
  artificial `depends_on: [ENG-022]` this design avoids entirely. `_index.md`
  there updated (`next_id` → `ADR-016`). **No one-way door** — an additive
  authorization check importing an existing shared primitive, no schema
  change, no new datastore or vendor; decided here rather than escalated, no
  G2. `touches_data: false` (no migration; the two handler files' Supabase
  client uses the service-role key, so RLS is not a factor either way — the
  application-code check *is* the only access control layer, same load-bearing
  fact `ENG-022`'s own security review already established for `brand-portal`
  and confirmed here still holds for `autopilot`), `touches_models: false`
  (no model/agent/tool touched anywhere in the diff). Every acceptance
  criterion walked individually against the design, full risk table
  (including the four `template_id`-only actions' new lookup-then-check
  shape, and the same-file-non-overlapping-region note against `ENG-035`):
  the design itself.

  **State:** `shaped → designed`. **Owner stays `architect`**, not moved to
  `eng-manager` — see Routing below; matches the corrected 2026-09-03
  convention (`state` and `owner` move together per `templates/ticket.md`'s
  own rule; an earlier owner-moves-ahead-of-state pattern from `ENG-022`'s
  2026-08-29 creation is exactly the violation `observations.md` row 210
  later caught live on `ENG-014` — not repeated here).

  **Routing (step 11): would be `ready` — held at `designed` instead.**
  Neither L0 nor a one-way door, so the skill's own routing reads `ready`,
  `owner: eng-manager`. Machine WIP re-checked fresh from every ticket's own
  frontmatter, not the board header: `ENG-016` (`building`), `ENG-031`
  (`building`), `ENG-032`/`ENG-033`/`ENG-034` (`ready`) — still `1/1`, the
  family reading `ENG-016`'s own work-breakdown pass established earlier
  today. Same precedent `ENG-014`/`ENG-017`/`ENG-023`/`ENG-025`/`ENG-026`/
  `ENG-020`/`ENG-021` already set: held at `designed`, owner staying
  `architect`, rather than writing `ready` while the one slot is occupied.
  `ENG-035` is unaffected by this cap — `shaped` sits outside the counted
  range.

  **Dead-end sweep:** out of scope for a `continue` event (narrower
  contract) — not attempted beyond the `ENG-035` byproduct above, which
  surfaced unsought while reading this ticket's own required evidence.
  **Notify sweep:** no new gate item for `ENG-029` itself (no one-way door).
  `ENG-035`'s incident raised and notified separately, above. Swept `inbox/`
  for the 24h-no-nudge-no-decision check: nothing new crosses it this pass.

  **Board update** — header's ADR/observation pointers unaffected (tracked in
  their own files); In-flight table: `ENG-029`'s own row (`shaped → designed`,
  updated date) and a new `ENG-035` row. See
  `agents/eng-manager/board/_index.md` for the full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-029`, `ENG-035`) and whole-board: see board index.

  `chained: ENG-029` — `designed`, owned by `architect`, an agent-owned
  state; not the approver, not blocked, not terminal, but nothing further for
  the architect to do until a machine-WIP slot frees (re-check then, same as
  `ENG-020`/`ENG-021`'s own identical position) — recorded as `chained: none`
  below is wrong for this exact reason on those two tickets' own precedent,
  so this line instead notes the correct read: **`chained: none`** — held by
  the machine-WIP cap (`1/1`, the `ENG-016` family), one of the documented
  no-chain conditions; re-check once that family reaches `shipped`.
  `chained: ENG-035` — `shaped`, owned by `architect`, an agent-owned state;
  firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
  ENG-035` before this pass exits so its own design step starts without
  waiting for a scheduled sweep, given the severity — same precedent
  `ENG-022`'s, `ENG-029`'s and `ENG-030`'s own creation entries set.

- 2026-09-03 `designed` (no transition — re-checked, still held) (architect,
  `continue` event pass, context `ENG-029` — this ticket's own turn at the
  front of `traces/.pending`). Reading map for `continue`: steps 6 and 6b,
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*,
  *The four lanes*, *Guards*) — not mid-PRD, so step 2's checkpoint note
  doesn't apply. Mode check clean (repo-root `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-029`) and
  whole-board: both exit 0, clean.

  **Dispatch (step 6): machine WIP re-checked fresh from every ticket's own
  frontmatter, not the board index table** (the table's own staleness on
  this exact ticket is why — see below): `ENG-016` `building`, `ENG-031`
  `building`, `ENG-032`/`ENG-033`/`ENG-034` `ready` — still `1/1`, none
  `shipped`. `ENG-029`'s own `depends_on: []` and `priority:` (empty, so the
  one approver lever the incident notice offered was not exercised) confirm
  the WIP cap is the only thing holding it. No transition available; stays
  `designed`. Same conclusion as the prior pass, reconfirmed against live
  state rather than assumed from the log.

  **Found and fixed: the board index's In-flight row for this ticket was
  stale**, still reading `shaped` where this ticket's own frontmatter and
  the log entry directly above have read `designed` since the prior pass.
  Cross-checked both `_index.md` and `_index-archive.md` for a dated section
  entry from that prior (`shaped → designed`) pass: **none exists in
  either file** — its own step 10 (Board update) appears to have never run,
  and `ENG-035` (filed in that same pass) has no In-flight row at all.
  **This is now a second instance of the identical gap**: `ENG-020`'s own
  pass already logged the same failure shape on `ENG-019`'s continue pass
  (ended after filing a P0 byproduct — `ENG-029` itself — without writing
  its own board update). Both instances share a shape: a design pass that
  discovers and fully files a P0 byproduct ticket, then never completes its
  own board-index entry. Filed as an observation below rather than fixed for
  `ENG-035` — a different ticket, out of this event's own narrow contract,
  same precedent `ENG-020`'s pass set for the `ENG-014` gap it found and
  left. This ticket's own row **is** fixed here, since it's the ticket this
  event is about.

  **Notify sweep:** swept `inbox/` for the 24h-no-nudge-no-decision check
  (`date -u`: `2026-09-04T00:17:18`) — `inbox/2026-09-02-eng008-merge-request.md`
  (notified `2026-09-02T23:24:37`, no `nudged:`, no `decision:`) has crossed
  24h (~24h53m). Ran `departments/engineering/lib/eng-notify.sh nudge` on
  it (confirmed via `traces/eng-notify-2026-09-03.log`: `sent`) and stamped
  `nudged: 2026-09-04T00:18:02` myself — the script posts and logs only, it
  does not write the item's own frontmatter. Every other open item is either
  still under 24h (`ENG-015`, `ENG-022`, `ENG-024`, `ENG-027` rescope,
  `ENG-028`, and the `ENG-029`/`ENG-030`/`ENG-035` P0 incidents, all
  informational-only with nothing owed) or already carries its one-ever
  nudge (`ENG-009`, `ENG-010`).

  **One observation filed** (`observations.md`): the recurring
  design-pass-ends-without-its-own-board-update pattern named above, now
  two instances (`ENG-019`→found `ENG-029`; `ENG-029`→found `ENG-035`) —
  worth the next occurrence triggering a proposal per the "third exception
  of the same kind" logic in `eng_build_loop.md` step 8b, even though this
  isn't literally an exception grant. Not a ticket — no code is broken,
  a process step was skipped twice by sessions under load from an
  unplanned P0 detour, which is a judgement-conformance question, not a bug.

  **Dead-end sweep:** out of scope for a `continue` event (narrower
  contract) — not attempted beyond the observation above, which surfaced
  unsought while re-verifying this ticket's own dispatch state.
  **Journal:** no gate answered this pass (no G1/G2/G3, no merge request) —
  not applicable.

  **Board update** — `_index.md`'s In-flight row for `ENG-029` corrected
  (`shaped → designed`); its "Waiting on the approver" `ENG-008` prose
  updated to drop the now-stale "not yet due for a nudge" line. Rolled the
  oldest of the four now-live dated entries (`continue ENG-020`) to
  `_index-archive.md` per the keep-three rule, and appended this pass's own
  entry. See `_index.md` for the full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-029`) and whole-board: see board index.

  `chained: none` — held by the machine-WIP cap (`1/1`, the `ENG-016`
  family: `ENG-016`/`ENG-031` `building`, `ENG-032`–`034` `ready`, none
  `shipped`), one of the documented no-chain conditions; re-check once that
  family reaches `shipped`. Not blocked, not terminal, not waiting on the
  approver — only the cap.

- 2026-09-04 `designed` (no transition) (eng-manager, `decision` event pass,
  context `inbox/2026-09-03-eng029-p0-incident.md` — this ticket's own P0
  incident notice, answered by the approver). Reading map for `decision`:
  steps 4 and 8c, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*, *The four lanes*, *Guards*). Step 5 doesn't apply (not an L1
  merge request); step 6 doesn't apply per the map's own qualifier — the
  answer doesn't advance the ticket into a machine-owned state; step 8's
  `blocked_from` paragraphs don't apply (ticket isn't leaving `blocked`);
  *The chain* doesn't apply (this incident is about a ticket, not the
  loop/queue itself). Mode check clean (repo-root `.env` → `MODE=active`;
  no instance-level override). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh` not run separately this
  time — run once, scoped and whole-board, after this pass's edits (below);
  both exit 0, clean.

  **The item itself:** `decision: approved`, `decided:
  2026-09-04T14:57:09Z`, no `priority` set, no question asked back — the
  item's own text framed it as "nothing to decide... filled in only if you
  want to set priority or have a question," so a bare approval reads as
  acknowledgement of the interrupt, not an instruction to reorder the
  board. Same shape as `ENG-022`'s own P0 incident acknowledgement
  (`inbox/_handled/2026-08-29-eng022-p0-incident.md`), same read.

  **Re-verified current state before concluding "untouched," not assumed
  from the last log entry.** Machine WIP re-checked fresh from every
  ticket's own frontmatter: `ENG-016` `building`, `ENG-031`/`ENG-032`
  `verified`, `ENG-033` `blocked` (`owner: approver`), `ENG-034` `ready` —
  still `1/1`, the family occupies the slot via `ENG-016` (parent, not yet
  `shipped`) and `ENG-034` (the one child still inside the counted
  `ready..ready-to-ship` range); `ENG-031`/`ENG-032` reaching `verified`
  since the prior entry didn't free it. `ENG-029`'s own `priority:` stays
  empty — the one lever the incident notice offered was not exercised.
  Conclusion unchanged from the prior pass: still `designed`, still held,
  no transition available.

  Processed note appended to the incident item and moved to
  `inbox/_handled/2026-09-03-eng029-p0-incident.md`, per `eng_build_loop.md`
  step 4's Incident handling (act on the item's own `recommendation:`, then
  archive — no further owner to hand off to). **Journal (step 8c):** row
  added to `decision-journal.md` for this answered gate.

  **Notify sweep (step 7):** swept `inbox/` fresh (`date -u`:
  `2026-09-04T15:02:16`) — nine open items besides this one. All either
  already carry a `nudged:` timestamp (`ENG-009`/`ENG-010`/`ENG-027` merge
  requests and rescope G1) or sit under 24h since `notified:`
  (`ENG-028`'s G1 ~22h51m, `ENG-030`'s P0 incident ~23h38m, `ENG-033`'s
  merge request ~13h19m) — `ENG-035`/`ENG-036`'s P0 incidents already carry
  a `decision:` and are excluded. Nothing crosses this pass; no nudge sent.

  business-os itself left uncommitted, same standing default the last
  several passes have each restated — see this session's own final summary
  for the current state of that open question; not re-decided here.

  **Board update (step 10):** In-flight table unaffected (no state change).
  The live file held three dated pass entries before this one; rolled the
  oldest (`scheduled (context ENG-028): ENG-008 found fully merged...`) to
  `_index-archive.md` first, then appended this pass's own entry, keeping
  three per the keep-three rule. See `_index.md` for the full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-029`) and whole-board: both exit 0, clean.

  `chained: none` — still held by the machine-WIP cap (`1/1`, the `ENG-016`
  family), same condition as the prior entry, re-confirmed fresh rather than
  assumed; re-check once that family reaches `shipped`. Not blocked, not
  terminal, not waiting on the approver — only the cap.
