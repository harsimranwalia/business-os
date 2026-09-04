---
id: ENG-036
title: "`outgoing-communications` skips authentication entirely for any system-triggered send — cross-actor unauthenticated message dispatch"
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
  prd: agents/product-manager/specs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md
  design: agents/architect/designs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md
  adrs: [ADR-017]
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`supabase/functions/outgoing-communications/index.ts` skips its entire
authentication block whenever the caller's JSON body sets `systemTriggered:
true` — no header, signature, or secret involved, just a plain boolean the
caller supplies themselves. Unlike `ENG-035`'s narrower `autopilot` bug, this
gates the function's *whole* auth requirement, for every `actor`/`action`
pair it serves (`influencer`, `brand`, `consumer`, `admin`), not one branch.
Full evidence and file:line citations are in the PRD (link above) — not
duplicated here.

Confirmed real, not stub, by reading all four `actors/*.ts` handlers in
full: `consumers.ts`'s `order_feedback_request` (fetches a live order by a
caller-supplied `orderId`, sends to a caller-supplied `customerEmail` if
given) and `welcome_offer`/`every_order`/`first_order`; `brands.ts`'s
campaign-notification emails to real restaurant owners/managers. `admin.ts`
and most of `influencers.ts` are stubs.

## Outcome

The `systemTriggered` branch denies any caller who cannot present a real
system-level credential, checked once ahead of the `actor` switch so it
covers every current and future actor/action pair. Every legitimate internal
caller (`autopilot/marketing/utils.ts`'s `scheduleWithQStash` and
`sendViaOutgoingComms`, confirmed; any others the design step finds) keeps
working unchanged.

## Notes

**How this was found.** Not an assigned security sweep — a byproduct of
`ENG-035`'s own tech-design research: designing `autopilot`'s fix required
reading `outgoing-communications/index.ts` in full, since
`marketing/utils.ts` calls it directly and its receiving-side trust model
was necessary context. `ENG-035`'s own PRD had explicitly named this
function's "identical-shaped check" as *not read in depth* and out of its
scope — this ticket is that follow-up, now confirmed rather than
speculative.

**Relationship to `ENG-035`.** Same bug class (a client-supplied
`systemTriggered` flag trusted as proof of system identity) in a sibling
function, not a new class — the fourth authorization gap this codebase has
surfaced this week, and the second in this exact shape (the first being
`ENG-035` itself). `ENG-035`'s own design (`ADR-016`, once written) is the
direct starting point for this ticket's own design: same mechanism, if this
function's actual callers support it — to be confirmed at design time, not
assumed here.

**Second-order finding, not first-order.** `ENG-029`'s design pass found
`ENG-035` while reading `autopilot/index.ts` for its own, unrelated fix;
this ticket was found the same way one level further out, while reading
`ENG-035`'s own dependency. Flagged as a pattern worth the EM's or
approver's attention in `observations.md`: three of this week's four
authorization gaps were each found as a byproduct of designing the previous
one, not through an assigned sweep — a dedicated pass across every edge
function for this same `systemTriggered`-style client-trusted-flag shape
might surface the rest at once rather than one hop at a time.

## Log

- 2026-09-03 `intake → shaped` (architect, `continue` event pass, context
  `ENG-035` — this finding is a byproduct of that pass's own tech-design
  research, not its assigned subject; see `ENG-035` for the assigned work).
  Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
  (`ENG-035`): both exit 0, clean (run before this ticket existed; scoped
  re-run post-pass below).

  PRD written short-form (auto-skip type, no readback — agent-originated
  finding with its own evidence, `skills/request-readback/SKILL.md`'s "when
  this does NOT run" list). Evidence gathered by reading
  `supabase/functions/outgoing-communications/index.ts` and all four
  `actors/*.ts` handlers (`consumers.ts`, `brands.ts`, `admin.ts`,
  `influencers.ts`) in full against `origin/main` — confirmed the
  `systemTriggered` branch skips the entire auth block (not just one
  routing arm, unlike `ENG-035`), and confirmed `consumers.ts`'s
  `order_feedback_request` and `welcome_offer`/`every_order`/`first_order`
  plus `brands.ts`'s campaign notifications are real, non-stub sends.
  Cross-checked `proposals.md`, `observations.md`,
  `agents/security/reviews/`, `agents/security/notebook/`, and
  `decision-journal.md` for any prior mention before filing — none found;
  closest prior art is `ENG-035`'s own Non-goals, which named this function's
  check as unaudited, not a duplicate finding.

  Incident notice raised: `inbox/2026-09-03-eng036-p0-incident.md`
  (`gate: incident`, `agent: architect`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter and `traces/eng-notify-2026-09-03.log` for the result.

  **State:** `intake → shaped`, `owner: product-manager → architect`.
  **Consequence:** does not consume approver-facing WIP or the approval cap —
  `security`-typed, auto-skip G1, nothing waiting at a gate. Machine WIP
  (1/1, the `ENG-016` family) also unaffected — `shaped` is short of the
  counted range (`ready` through `ready-to-ship`).

  `chained: ENG-036` — `shaped`, owned by `architect`, an agent-owned state;
  firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
  ENG-036` before this pass exits so the design step starts without waiting
  for a scheduled sweep, given the severity — same precedent `ENG-022`'s,
  `ENG-029`'s, `ENG-030`'s and `ENG-035`'s own creation entries set. This is
  the primary ticket's (`ENG-035`) own second, separate chain fire in this
  pass; see that ticket's own log for its own chain record. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
  `ENG-035`/`ENG-036`: see pass notes in `agents/eng-manager/board/_index.md`.

- 2026-09-03 `shaped → designed` (architect, `continue` event pass, context
  `ENG-036`, its own turn per the prior pass's own `chained: ENG-036`).
  Narrow scope per the event's own contract — this ticket only. Reading map
  for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*, *The four lanes*, *Guards*); not mid-PRD, so
  step 2's checkpoint note doesn't apply. Mode check clean (repo-root `.env`
  → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board and scoped
  (`ENG-036`): both exit 0, clean.

  **Design work — full reasoning in
  `agents/architect/designs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md`
  and `ADR-017`.** Read `index.ts` via `git show origin/main:` (the shared
  `_eng/aiorders-api` worktree was still on `feat/ENG-031-...`, not `main` —
  same read-only-against-remote approach `ENG-035`'s own design pass used).
  Confirmed the bug as filed: the entire auth block sits behind one
  `if (!systemTriggered)` with no `else`.

  **Caller enumeration (the PRD's own named risk) done fresh rather than
  trusted from the PRD's one example:** grepped `outgoing-communications`
  against all five registered repos at each one's own remote default
  branch, not `aiorders-api` alone. Found two more callers beyond the PRD's
  one — `aiorders-admin-hub`'s `cloudflare-workers/queue-consumer/index.ts`
  (a third legitimate `systemTriggered: true` caller, confirmed sending
  `Authorization: Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`) and three
  non-`systemTriggered` callers (`Activation.tsx`'s `bag_insert_shared`,
  `restaurant-portal`'s `campaigns/CreateEdit.tsx`'s `campaign_created`,
  and this repo's own `influencer-invitations.ts`'s `visit_scheduled`) that
  forward or use an ambient user session and are unaffected by the fix
  either way. `restaurant-marketplace` and `config-site-builder`: no
  reference to this function in either. All three `systemTriggered: true`
  callers confirmed sending `ADR-016`'s exact header already — stronger
  evidence than `ENG-035` had, since every caller here is an HTTP call site
  read in full, not an untracked DB trigger.

  Designed `outgoing-communications/auth.ts` (new file,
  `authorizeSystemTrigger(req, responseHeaders)`, same signature `ADR-016`
  used) called from a new `else` branch completing the existing
  `if (!systemTriggered)` block — one call site, ahead of the `actor`
  switch, per AC3. `ADR-017` records two decisions: reusing `ADR-016`'s
  mechanism rather than a new secret (three live callers across two repos
  would need coordinated reconfiguration this session can't make or
  verify), and keeping this as its own file rather than extracting to
  `_shared/` now, since `ADR-016`'s own file doesn't exist in the tree yet
  (`ENG-035` is still `designed`, not `building`) and forcing a shared
  extraction now would couple this ticket's build to `ENG-035`'s branch for
  a ~20-line, zero-behavior-cost duplicate. Filed as an observation
  (`observations.md`), not a proposal.

  One-way doors: none — additive header check, no schema/data change,
  decided here rather than escalated (`touches_data`/`touches_models` both
  `false`). Residual risk is lower than `ADR-016`'s (no unverifiable DB
  trigger here) but not zero: whether `SUPABASE_SERVICE_ROLE_KEY`'s
  *deployed* value actually matches between the Cloudflare Worker
  environment and the Supabase project's own secret can't be confirmed from
  source. Mitigated the same way `ADR-016` mitigated its own larger version
  of this gap — a distinct denial log line, plus a mandatory (lighter-weight)
  manual post-deploy log check named in the design's own Rollout section.

  **State:** `shaped → designed`, `owner: architect` (unchanged — `designed`
  is architect-owned per `definition-of-done.md`). `links.design` and
  `links.adrs` set on this ticket's own frontmatter.

  **Routing: would be `ready` — held at `designed`.** Machine WIP re-checked
  fresh off `ENG-016`/`032`/`033`/`034`'s own frontmatter (not board-header
  prose): `ENG-016`/`ENG-032` `building`, `ENG-033`/`ENG-034` `ready` — still
  `1/1`, none `shipped`. Same precedent `ENG-035` and this board's other
  `designed`-and-waiting tickets already sit under.

  **1 transition** (`shaped → designed`), under the cap of 4. Machine WIP
  unaffected (`designed` sits outside the counted range). No approver-facing
  or approval-cap change — `security`-typed, G1 already auto-skipped at
  intake, and `designed` here carries no one-way door so no G2 is raised
  either (`definition-of-done.md`: `awaiting-decision` "only entered when a
  one-way door exists").

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** every open `inbox/` item checked fresh against the 24h
  threshold — nothing newly crosses it this pass. **Step 6b:** not run — a
  design hop, not a build hop; no product code written this pass, so no
  artifact-mention grep applies. One observation filed
  (`observations.md`): the `_shared/` consolidation of `ADR-016`'s and this
  ticket's near-identical `authorizeSystemTrigger` copies, worth doing once
  both ship, per `ADR-017`'s own Review trigger. **Journal:** not applicable
  — no G1/G2/G3 answered this pass.

  **Board update:** In-flight row for `ENG-036` (`shaped → designed`).

  Post-pass `lib/eng-gate-check.sh`, whole-board and scoped `ENG-036`: see
  pass notes in `agents/eng-manager/board/_index.md`.

  `chained: none` — `ENG-036` sits at `designed`, owned by `architect`, not
  the approver, not blocked, not terminal, but held by the machine-WIP cap
  (`1/1`, the `ENG-016` family); re-check once that family reaches
  `shipped`.

- 2026-09-04 `designed` (no transition) (eng-manager, `decision` event pass,
  context `inbox/2026-09-03-eng036-p0-incident.md` — this ticket's own P0
  incident notice, answered). Reading map for `decision`: steps 4 and 8c,
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*,
  *The four lanes*, *Guards*). Step 5 doesn't apply (not an L1 merge
  request); step 8's `blocked_from` paragraphs don't apply (ticket isn't
  leaving `blocked`); *The chain* doesn't apply (this incident is about a
  ticket, not the loop/queue itself). Mode check clean (repo-root `.env` →
  `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  whole-board and scoped (`ENG-036`): both exit 0, clean.

  **The item itself, unlike its two siblings.** `ENG-029`'s and `ENG-035`'s
  own P0 incidents were both answered with a bare `approved` — nothing to
  act on beyond acknowledgement. This one was answered `changed` at
  `2026-09-04T14:58:46.245104+00:00`, with a substantive claim attached,
  verbatim: "When you add auth to this edge function any code using it will
  break, that needs a ticket to update all the code that used it." Read as
  an instruction, not a bare acknowledgement — so step 6's "does the answer
  advance the ticket into a machine-owned state" question doesn't fit this
  cleanly either; what it actually calls for is checking the claim against
  what design already knows, not a state transition.

  **Checked, not assumed either way.** Re-read this ticket's own design
  (`agents/architect/designs/ENG-036-outgoing-communications-systemtriggered-auth-bypass.md`)
  and `ADR-017` rather than taking the approver's premise at face value or
  dismissing it unread. The design's own caller-enumeration table already
  answers exactly this question, done at design time precisely because the
  PRD named "every legitimate caller must be enumerated" as a named risk:
  grepped `outgoing-communications` against all five of this instance's
  registered repos, not `aiorders-api` alone, and found three call sites
  that set `systemTriggered: true` — `autopilot/marketing/utils.ts`'s
  `scheduleWithQStash` and `sendViaOutgoingComms` (`aiorders-api`), and
  `aiorders-admin-hub`'s `cloudflare-workers/queue-consumer/index.ts` — the
  only ones this fix's new `else` branch puts a credential check in front
  of. All three already send exactly the credential the check will require
  (`Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY`), confirmed by reading
  each call site's own source directly. The other three known callers
  (`visit_scheduled`, `bag_insert_shared`, `campaign_created`) don't set
  `systemTriggered` and stay on the function's existing, untouched
  user-session path — this diff adds no `else` there, so they're unaffected
  either way. **No caller this codebase's own source shows requires a code
  change as a result of this fix.**

  **Action taken: no ticket filed.** A ticket to "update all the code that
  used it" would have no actual content — there is no caller left to
  update. Named plainly rather than quietly declined, the same shape this
  board already used for `ENG-027`'s "if not cancelled or deleted" condition
  (vacuous as the code stood, named rather than built as decorative) — a
  mismatch between the approver's reasonable general expectation and this
  specific diff's already-verified effect, stated openly so it's visible and
  reversible rather than silently overridden. The one residual risk in this
  area (whether the deployed `SUPABASE_SERVICE_ROLE_KEY` value actually
  matches between the Cloudflare Worker and Supabase's own secret store — a
  configuration fact, not something a source read can confirm) is already
  covered by the design's own Rollout section as a mandatory manual
  post-deploy log check, not left uncovered by this decision. If a caller
  this enumeration missed turns up later — in that check, or in any future
  code — that is a new finding at that time, same as any other gap this
  board catches, not something foreclosed by closing this item now.

  Processed note (full reasoning, same as above) appended to the incident
  item and moved to `inbox/_handled/2026-09-03-eng036-p0-incident.md`, per
  `eng_build_loop.md` step 4's Incident handling. **Journal (step 8c):** row
  added to `decision-journal.md` for this answered gate, approver's words
  verbatim plus this interpretation labelled as interpretation. **Step 8b:**
  one observation filed (`observations.md`) — the incident notice itself is
  written before design happens, so it can't carry the design's own
  caller-safety evidence yet, which makes a "won't this break things"
  reaction to the notice alone expected rather than a sign of anything
  rushed; worth knowing if this recurs on a future P0 incident answer.

  **Machine WIP re-checked fresh, not assumed unchanged:** `ENG-016`
  `building`, `ENG-031`/`ENG-032` `verified`, `ENG-033` `blocked` (`owner:
  approver`), `ENG-034` `ready` — still `1/1`, the family still holds the
  slot. `ENG-036` stays `designed`, `owner: architect`, no design change.

  **Notify sweep (step 7):** swept `inbox/` fresh (`date -u`:
  `2026-09-04T15:25:51Z`). `ENG-009`/`ENG-010`/`ENG-027` already carry a
  `nudged:` timestamp. `ENG-028`'s G1 (~23h15m since `notified:`) and
  `ENG-033`'s merge request (~13h43m) both still sit under the 24h
  threshold. **`ENG-030`'s P0 incident crossed 24h this pass** (notified
  2026-09-03T15:24:21, ~24h01m elapsed, no `nudged:`, no `decision:`) —
  nudged (`lib/eng-notify.sh nudge`), stamped `nudged: 2026-09-04T15:26:20`.
  Nudge call logged `sent: active`, not `sent: nudge`
  (`traces/eng-notify-2026-09-04.log`) — the same standing `MODE`-clobber
  bug `proposals.md`'s 2026-08-25 row already carries, reconfirmed live for
  a third time today; not re-amended for a same-day recurrence with no new
  signal beyond what that row and today's `scheduled` pass already recorded.

  business-os itself left uncommitted, same standing default the last
  several passes have each restated; not re-decided here.

  **Board update (step 10):** In-flight row's `Updated` date bumped
  (2026-09-03 → 2026-09-04), state/owner unaffected. The live file held
  three dated pass entries before this one; rolled the oldest (`scheduled`
  sweep entry) to `_index-archive.md` first, then appended this pass's own
  entry, keeping three per the keep-three rule. See `_index.md` for the
  full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board and
  scoped `ENG-036`: both exit 0, clean.

  `chained: none` — `ENG-036` stays held by the machine-WIP cap (`1/1`, the
  `ENG-016` family), re-confirmed fresh, not assumed. Not blocked, not
  terminal, not waiting on the approver — only the cap.
