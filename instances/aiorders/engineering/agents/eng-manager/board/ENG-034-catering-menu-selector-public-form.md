---
id: ENG-034
title: Public catering form — category-grouped dish picker, gated by owner opt-in
project: config-site-builder
type: feature
size: M
time_estimate: ~1.5-2 days
time_spent: build (single session) + review round 1 (pass) + quality gate round 1 (pass) + security round 1 (pass) + release-readiness (PR opened) + merge detection + acceptance-check (pass)
time_remaining: none — verified
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-04
branch: feat/ENG-034-catering-menu-selector-public-form (config-site-builder@62b3ca0)
depends_on: [ENG-033]
blocks: []
parent: ENG-016
links:
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design: agents/architect/designs/ENG-016-catering-quote-generator.md
  adrs: [ADR-008, ADR-009]
  review: agents/principal-engineer/reviews/ENG-034.md
  test_plan: agents/qa/test-plans/ENG-034.md
  security_review: agents/security/reviews/ENG-034.md
  release: agents/devops/releases/2026-09-04-config-site-builder-ENG-034.md
  pr: https://github.com/harsimranwalia/config-site-builder/pull/4
---

## Problem

The public catering form has no way for a customer to select menu items —
`Catering.tsx`'s own "How It Works" copy already promises "2. Customize Your
Menu," a step that exists nowhere in the code today.

## Outcome

A new `CateringMenuSelector` component (category-grouped dish picker,
quantity + per-dish note, controlled, no fetch or config read of its own)
mounts on `CateringForm` when the gate is open:

```
orderFormEnabled =
     config.catering?.orderFormEnabled === true          // ADR-009
  && effectiveHasMenu === 'page'
  && effectiveMenu.length > 0
```

resolved per selected location, reusing `CateringForm`'s existing
`selectedLocation` derivation. Gate closed → the form renders exactly what it
renders today, byte for byte (AC-9). Gate open: fulfillment option labels and
descriptions come from `config.catering.fulfillmentCopy[value]` when present
(ADR-008 — no new fulfillment values, no remap), `requirements` loses its
`required` attribute and becomes general notes, `email` becomes required
(AC-11, a deliberate behaviour change on this branch only), and two submit
actions replace one — "Submit Quote Request" (needs ≥1 selection) and "Skip &
Have Someone Contact Me" — both validating the same required-field set
client-side. Changing `restaurant_id` mid-form resets selections (visibly),
matching the existing `delivery_method` reset behaviour.

`src/types/restaurant.ts` gains the two new `CateringPageContent` keys.

## Notes

Design's `## Interfaces` → "`config-site-builder` — the gate, and what it
gates" and "`CateringMenuSelector` — new component" have the exact gate
expression, prop shape (`{ menu, value, onChange }`), the menu-reading
pattern to match (`MenuList.tsx`'s own `(menu.categories||[]).map` over
`(category.items||category.dishes)`, both field names live), and the
selection-identity rule — composite `${menuIndex}-${categoryIndex}-
${itemIndex}` key, never dish name (repeats across categories) or `item.id`
(optional, can be absent). Called out in the design's own `## Risks` as the
largest single piece of new logic in this ticket.

`depends_on: [ENG-033]` — last in the design's Rollout order; the picker
POSTs `action_type`/`selections`, which only `ENG-033` makes the endpoint
understand. Full sequencing rationale:
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`.

## Log

- `2026-09-03` `(created) → ready` (eng-manager, `work-breakdown`,
  `continue ENG-016` event pass) — sub-ticket of `ENG-016`, sequence 4 of 4,
  last in the chain. Held at `ready`: `depends_on: [ENG-033]` not yet
  `shipped`. `time_estimate` ~1.5-2 days. `chained: none` — waiting on a
  sibling, not agent-actionable yet.

- `2026-09-04` `ready → building` (frontend, `continue ENG-034` event pass,
  per the prior `watch (launchd)` pass's own `chained: ENG-034` — `ENG-033`
  shipped, satisfying this ticket's sole dependency). Mode clean
  (`MODE=active`). Pre-pass `eng-gate-check.sh`, scoped + whole-board: both
  exit 0.

  Built all three files the design's `## Components` table names for this
  surface (`src/types/restaurant.ts`, new `CateringMenuSelector.tsx`,
  `CateringForm.tsx`). No gate this hop, no receipt written. Self-tested:
  `npm install` (first ever in this worktree), `npm run lint` (both
  touched/new files clean; `restaurant.ts`'s 4 hits confirmed pre-existing
  via `git stash`), `npm run build` clean, `npx tsc --noEmit` clean (beyond
  this project's own defined check surface, run for extra rigor). Committed
  `config-site-builder@62b3ca0`
  (`feat/ENG-034-catering-menu-selector-public-form`, branched fresh off
  `origin/main` — the worktree's prior branch was `ENG-016`'s own, never
  diverged), pushed. Full reasoning and every interpretation call:
  `agents/eng-manager/notebook/2026-09-04-eng034-build.md`.

  **1 transition**, under the cap of 4. Machine WIP unaffected — still 1/1,
  `ENG-016` family, its last sibling now dispatched. Dead-end sweep (scoped
  to this event): no other ticket touched. Notify sweep (current
  `2026-09-04T16:13:26Z`): `ENG-028`'s G1 crossed 24h with no `nudged:`/
  `decision:` (`notified: 2026-09-03T16:10:27`) — nudged
  (`lib/eng-notify.sh nudge`), stamped `nudged: 2026-09-04T09:13:37`
  (copied verbatim from the trace log, same standing local-time-labeled-as-
  UTC convention this board already uses). `ENG-027`/`ENG-030` already
  carry their one-time nudge. One observation filed (`observations.md` —
  ticket-log length convention). Step 6b: not run — product code internal
  to one repo, no receipt path/state name/config key/cross-agent artifact
  involved. Journal: n/a — no gate answered this hop.

  `chained: ENG-034` — `building` is agent-owned (next hop: code review,
  principal-engineer); not the approver, not blocked, not terminal, not held
  by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-034` before this pass exits. Post-pass `eng-gate-check.sh`,
  scoped + whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass has
  used; the commit-convention question remains open, not re-decided here.

- `2026-09-04` **`building → in-review → in-qa`: code review + quality gate,
  round 1, both PASS** (principal-engineer + qa, combined review+quality
  hop, `continue ENG-034` event pass, per prior hop's own `chained:
  ENG-034`). Reading map for `continue`: steps 6 and 6b (design already
  complete, not mid-PRD), plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped
  (`ENG-034`) and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matched verbatim (`building`/`frontend`, prior hop's build
  self-tested and committed, next hop code review). WIP re-checked fresh
  off every ticket's own frontmatter (`ENG-016` `building`; `ENG-031`/
  `ENG-032`/`ENG-033` all `verified`), not trusted from the checkpoint:
  still 1/1, held by the `ENG-016` family, `ENG-034` its only active
  member.

  **Worktree not clean — investigated before proceeding, not assumed
  harmless.** `~/Documents/projects/_eng/config-site-builder` carried an
  uncommitted 2-line `package-lock.json` diff. Traced rather than guessed:
  content is exactly `package.json`'s own `version` field (`1.0.0` →
  `2.2.0`) mirrored into the lockfile's two metadata copies — npm's own
  normalization on `install`, zero dependency change — and matches the
  prior `building` hop's own logged `npm install` (its first ever in this
  worktree). Distinct from `config/projects.md`'s "uncommitted changes mean
  a previous pass died mid-work" warning, which is about stranded *code*;
  no uncommitted code existed here, and this diff sits outside the reviewed
  commit range (`origin/main...HEAD`) either way. Left alone rather than
  discarded or stashed, noted on the review receipt rather than silently
  worked around.

  **Code review: PASS, round 1.** 0/10 automatic failures. Read
  `MenuList.tsx` and `isDishHidden` directly to confirm
  `CateringMenuSelector`'s menu-read shape, selection-identity key, and
  no-stock-stays-selectable rule all match the design's own stated
  requirement to mirror them, rather than trusting the design's paraphrase.
  Traced AC-9 (the property this ticket must not violate) end-to-end
  against `origin/main`'s own pre-diff file: gate-closed labels, required
  set, submit markup and wire payload all identical. Every AC this ticket
  owns (1, 2, 3, 4, 5/6-client, 9, 11) traced against the actual diff.
  **Four non-blocking findings**, all specific and actionable: (F1)
  `handleSubmit`'s `SubmitEvent.submitter` read has no fallback — an
  unsupported/non-compliant browser on a gate-open submit silently drops
  `action_type`/`selections` rather than failing closed with a message,
  the one place this diff's failure direction isn't uniform with the rest
  of it; judged non-blocking given materially lower reachability than the
  same-shaped bug this board failed a round over on `ENG-033` (that one:
  any HTTP client, no special conditions; this one: an aged/non-compliant
  browser, and the fallback degrades to no worse than gate-closed rather
  than crashing or corrupting data). (F2) `||` vs `??` on one label
  fallback — an intentionally-emptied label would revert to the hardcoded
  default. (F3) the loading-spinner JSX is duplicated across two button
  variants. (F4) `CateringForm.tsx` is now 540 lines, further past the
  400-line smell threshold (already ~420 pre-diff). Full detail on all
  four: `agents/principal-engineer/reviews/ENG-034.md`, `links.review` set.

  **Quality gate: PASS, round 1 — first real run on this ticket.**
  `config-site-builder` has zero test runner of any kind, confirmed fresh
  (no `test` script, no `vitest`/`jest`/`@testing-library` dependency, zero
  `*.test.*`/`*.spec.*` files) — a materially different gap than
  `aiorders-api`'s own (which at least has `deno test` built in for free),
  so every acceptance criterion this ticket owns is manual verification
  with a specific reason and specific evidence, under
  `definition-of-done.md`'s allowance, same shape this family's own
  `ENG-033` already used for its AC-10/AC-13 rows. The design's own Risks
  section names this exact gap but cites it as "`ENG-002`'s tracked gap" —
  **checked, not assumed: that citation is wrong.** `ENG-002` is scoped to
  `restaurant-portal` only (its own `project:` field), and no open
  `proposals.md` row named `config-site-builder` specifically before this
  pass. Fresh proposal filed below rather than silently inheriting the
  wrong citation as if the gap were already tracked. Full AC-by-AC
  evidence, failure-path table, and regression-risk trace:
  `agents/qa/test-plans/ENG-034.md`, `links.test_plan` set.

  **Independent verification, this session, shared by both gates rather
  than re-run twice for identical output.** `npm run lint` (whole project):
  191 pre-existing problems, `CateringForm.tsx`/`CateringMenuSelector.tsx`
  both **0 hits**; `restaurant.ts`'s 4 `no-explicit-any` hits confirmed
  byte-identical against `origin/main`'s own copy of the same lines
  (shifted by this diff's own insertions), not introduced here. `npm run
  build`: clean. `npx tsc --noEmit` (beyond this project's own defined
  check surface): clean, 0 errors.

  **2 transitions** (`building → in-review → in-qa`), under the cap of 4.
  Machine WIP unaffected — still 1/1, `ENG-016` family. No approver-facing
  WIP or approval-cap change — no gate answered this hop.
  `time_spent`/`time_remaining` updated in frontmatter; owner
  `frontend → eng-manager`, matching this family's own established
  precedent for a same-round double-pass (`ENG-031`/`ENG-032`/`ENG-033`:
  owner rests at `eng-manager` once both gates clear in one hop, not at
  either gate's own nominal owner).

  Dead-end sweep (scoped to this event): no other ticket touched. Notify
  sweep: current `2026-09-04T16:34:18Z` — all three open `inbox/` items
  (`ENG-027` rescope, `ENG-028` G1, `ENG-030` P0 incident) already carry
  their one-time `nudged:` timestamp; nothing crossed 24h fresh, nothing
  raised this pass (a review/quality pass isn't approver-facing on its
  own). **One proposal filed** (`proposals.md`): `config-site-builder`'s
  own missing test harness, correcting the design's imprecise `ENG-002`
  citation, same shape the already-open `aiorders-api`/`aiorders-admin-hub`
  rows already take. No observations filed separately — the four review
  findings and the `package-lock.json` sighting are fully recorded on this
  ticket's own log and the review receipt, the same precedent this board's
  other review rounds already set (non-blocking notes live in the receipt,
  not a duplicate `observations.md` line). Step 6b: not run — this hop
  wrote review/test-plan receipts and ticket frontmatter/log only; no
  receipt path, state name, config key, or cross-agent artifact rule was
  touched or relied on. Journal: n/a — no G1/G2/G3 or merge request
  answered this pass.

  `chained: ENG-034` — `in-qa` is agent-owned (security next); not the
  approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-034` before this pass exits. Post-pass `eng-gate-check.sh`,
  scoped + whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **`in-qa → in-security → ready-to-ship`: security gate,
  round 1, PASS** (security, `continue ENG-034` event pass, per prior hop's
  own `chained: ENG-034`). Reading map for `continue`: steps 6 and 6b
  (design already complete, not mid-PRD), plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode
  check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `eng-gate-check.sh`, scoped (`ENG-034`) and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matched verbatim (`in-qa`/`eng-manager`, both prior gates
  pass, next hop security). WIP re-checked fresh off every `ENG-016`
  sibling's own frontmatter (`ENG-016` `building`; `ENG-031`/`ENG-032`/
  `ENG-033` all `verified`), not trusted from the checkpoint: still 1/1,
  held by the family, `ENG-034` its only active member. Worktree
  re-checked, not assumed unchanged since the last hop: still only the
  same 2-line `package-lock.json` version-metadata diff outside the
  reviewed commit range, already traced to `npm`'s own install
  normalization by the prior hop — re-confirmed rather than re-derived,
  left alone again.

  **Security gate: PASS, round 1.** Read the design's own `## Interfaces`
  (the gate expression, `CateringMenuSelector`'s props/menu-read/selection-
  identity, the `catering-request` validation table) and `## Risks` first,
  for trust-boundary context, rather than starting from the diff cold.
  Threat-modelled the four standard questions: this diff adds no field,
  endpoint, or capability beyond what `ENG-033`'s already-reviewed,
  already-shipped `catering-request` accepts from any HTTP client — it is
  the client-side construction of a payload shape that gate already passed
  — and adds no new fetch/network call of its own (grepped the diff:
  zero), so no new data reaches a new audience either. Walked all ten
  OWASP categories explicitly, each marked applicable or `n/a` with a
  reason (full table: `agents/security/reviews/ENG-034.md`). Two worth
  naming here: **A03 Injection** — the one genuinely new rendered-data
  source this ticket introduces, owner-configured
  `config.catering.fulfillmentCopy` (label/description/guestCountNote),
  confirmed rendering via plain JSX text interpolation with zero
  `dangerouslySetInnerHTML` in either changed file (grepped directly, not
  assumed) — React's default escaping holds, no stored/reflected XSS.
  Selection identity uses a `Map`, not bracket-assignment off an
  attacker-influenced key, so this diff carries none of the prototype-
  pollution shape `ENG-032`'s own gate had to check for its own `reduce`
  pattern. **A04 Insecure Design** — quantity can't go negative through the
  UI (decrement disables at 0, any `quantity <= 0` call removes the
  selection rather than storing it); a caller bypassing the UI entirely is
  bounded by `ENG-033`'s own already-reviewed server validation. Named,
  not re-filed, two pre-existing conditions out of this diff's own repo:
  no upper bound on `quantity` or `selections[].name`'s length (the latter
  already logged, `ENG-033` Finding 2) and the native-`required`-only
  enforcement on `email`/`requirements`, both explicitly non-security-
  relevant and both already on record. Independently confirmed
  `lucide-react` pre-existing (`package.json:58`, grepped directly rather
  than taken from the code review's own account) — A06 clean, no new
  dependency. Secrets: `git diff`/`git log -p` over the diff and the
  branch's single commit (`62b3ca0`), no match. LLM checklist: n/a in
  full, no model/agent/tool/MCP/RAG anywhere in this diff. Negative-case
  authz coverage: n/a, same conclusion `ENG-032`/`ENG-033` already reached
  for this feature — no auth/tenant/role surface exists in this diff to
  test against, independently re-confirmed rather than assumed. SOC 2
  evidence trail (ticket → PRD → design → review → QA → this verdict →
  release record) checked complete, no gap.

  **Zero findings** — the two adjacent pre-existing conditions named under
  A04 were checked and disclosed in the receipt rather than manufactured
  into fresh findings; neither is newly introduced or newly worsened by
  this diff, and one is already on record. Per the security-gate skill's
  own step 9 (write the receipt on `pass`, and only on `pass`): receipt
  written, `agents/security/reviews/ENG-034.md`, `links.security_review`
  set on this ticket in the same edit.

  **2 transitions** (`in-qa → in-security → ready-to-ship`), under the cap
  of 4. Machine WIP unaffected — `ready-to-ship` is still inside the
  counted `ready..ready-to-ship` range, still 1/1, still the `ENG-016`
  family. No approver-facing WIP change — a security pass isn't a gate
  item for the approver. `time_spent`/`time_remaining` updated in
  frontmatter; owner `eng-manager → devops`, matching this family's own
  established shape for a gate that clears and routes on to the next
  agent in the same hop.

  Dead-end sweep (scoped to this event): no other ticket touched. Notify
  sweep: current `2026-09-04T16:45:39Z` — all three open `inbox/` items
  (`ENG-027`, `ENG-028`, `ENG-030`) already carry their one-time `nudged:`
  timestamp (checked fresh, not carried from the checkpoint); nothing to
  nudge again, nothing raised this pass (a security pass that clears isn't
  approver-facing on its own). No observations or proposals filed this
  hop — both conditions surfaced during the review are already tracked
  (one is `ENG-033` Finding 2's own record; the other is a named, accepted,
  non-security-relevant design choice, not a gap). Step 6b: not run — this
  hop wrote a security receipt and ticket frontmatter/log only, using
  conventions the skill already defines; no receipt path, state name,
  config key, or cross-agent artifact *rule* was itself touched or relied
  on. Journal: n/a — no G1/G2/G3 or merge request answered this pass.

  `chained: ENG-034` — `ready-to-ship` is agent-owned (release-readiness
  next, devops); not the approver, not blocked, not terminal, not held by
  a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-034` before this pass exits. Post-pass `eng-gate-check.sh`,
  scoped + whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` `ready-to-ship → blocked` (devops, `continue ENG-034` event
  pass). `skills/release-runner/SKILL.md`: L1 (`config/projects.md`) skips
  the window check; all three upstream gates re-confirmed **pass** (review,
  quality — `no suite`, expected, no test runner on this project — and
  security; receipts already linked). Readiness gate held: rollback
  documented not live-drilled (no test command, same bar `ENG-005` already
  set for this stack shape), no new server-side failure path (POSTs through
  `ENG-033`'s already-observed endpoint), $0/month cost, no auto-deploy
  workflow on `origin/main`. Opened `config-site-builder` PR #4
  (https://github.com/harsimranwalia/config-site-builder/pull/4), wrote
  `inbox/2026-09-04-eng034-merge-request.md`, notified (stamped
  `2026-09-04T10:01:49` from the trace log). Full reasoning, including the
  step-1/step-3 L1-scope interpretation call:
  `agents/devops/notebook/2026-09-04-release-readiness-log.md`.
  `blocked_on: approver`, `blocked_from: ready-to-ship`, `owner: approver`,
  `links.pr` set. Approver-facing WIP uncapped; machine WIP unaffected —
  `blocked` leaves the counted range, and this is the `ENG-016` family's
  last ticket. One proposal filed (`proposals.md`) recommending
  `eng-gate-check.sh` mechanically enforce `cap_lines: 20`, given this
  ticket's own prior two hops (review+quality, security) both drifted back
  to long-form entries right after the build hop's own self-correction —
  detail in the notebook entry above.
  `chained: none` — blocked on the approver; merge detection (step 5)
  resumes it on a future pass.

- `2026-09-04` **`blocked → shipped → verified`** (eng-manager +
  product-manager, `watch (launchd)` event pass — step 5, merge-request item
  changed). `git fetch` + `git merge-base --is-ancestor 62b3ca0 origin/main`:
  YES; `gh pr view 4`: `MERGED`, base `main` directly, no stacking. All three
  receipts re-read fresh: review/quality/security all `pass`; no migration
  (frontend-only). Release record written:
  `agents/devops/releases/2026-09-04-config-site-builder-ENG-034.md` — this
  department does not run `config-site-builder`'s own manual deploy scripts
  at L1 (same posture `ENG-033`'s and `ENG-032`'s own records already set);
  full reasoning there. **Acceptance-check run in full**, not as
  receipt-bookkeeping (the shortcut the last ten tickets used with no
  notebook entry — see why, and every AC walked against the merged tree
  directly): `agents/product-manager/notebook/2026-09-04-acceptance.md`. All
  8 owned criteria pass. Proposal filed (`proposals.md`) on the ten-ticket
  acceptance-check gap.

  **2 transitions**, under the cap of 4. Machine WIP unaffected — still 1/1,
  held by the `ENG-016` family; the parent itself still occupies the slot
  until it reaches `shipped`. Merge-request item moved to `inbox/_handled/`;
  decision-journal entry written.

  `chained: ENG-016` — not this ticket (`verified` is terminal), but the
  parent this ticket's own shipping now makes eligible for its own
  ADR-003-class exemption (all four children `shipped`/`verified`). Fired
  `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-016` before this pass exits.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.
