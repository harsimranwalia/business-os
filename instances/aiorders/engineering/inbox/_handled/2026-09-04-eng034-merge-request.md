---
type: eng-decision
agent: eng-manager
gate: merge
project: config-site-builder
ticket: ENG-034
time_estimate: ~1.5-2 days
recommendation: merge — code review (round 1), quality (round 1), and security (round 1) all passed on the current diff; last of 4 sub-tickets under ENG-016's catering quote generator, depends_on ENG-033 already shipped; four non-blocking code-review findings carried forward, none blocking
pr_url: https://github.com/harsimranwalia/config-site-builder/pull/4
raised: 2026-09-04
notified: 2026-09-04T10:01:49
nudged:
decision:
---

# Merge request — catering menu selector, public form (ENG-034)

Part of `ENG-016`'s catering quote generator. Last of 4 sub-tickets
(031/032/033/034) — this is the final piece.

## What this does

`CateringMenuSelector` — a new category-grouped dish picker (quantity +
per-dish note, controlled, no fetch/config read of its own) — mounts on
`CateringForm` when the gate is open:

```
orderFormEnabled =
     config.catering?.orderFormEnabled === true          // ADR-009
  && effectiveHasMenu === 'page'
  && effectiveMenu.length > 0
```

resolved per selected location, reusing `CateringForm`'s existing
`selectedLocation` derivation.

- **Gate closed** → the form renders exactly what it renders today, byte for
  byte (AC-9, verified directly against `origin/main`'s own pre-diff file).
- **Gate open** → fulfillment option labels/descriptions come from
  `config.catering.fulfillmentCopy[value]` when present (ADR-008 — no new
  fulfillment values, no remap), `requirements` loses its `required`
  attribute and becomes general notes, `email` becomes required (AC-11, a
  deliberate behaviour change on this branch only), and two submit actions
  replace one — "Submit Quote Request" (needs ≥1 selection) and "Skip & Have
  Someone Contact Me" — both validating the same required-field set
  client-side. Changing `restaurant_id` mid-form resets selections
  (visibly), matching the existing `delivery_method` reset behaviour.

`src/types/restaurant.ts` gains the two new `CateringPageContent` keys.

Depends on `ENG-033` (`aiorders-api`, already merged/shipped) — the picker
POSTs `action_type`/`selections`, which only that endpoint understands.

## Gates passed

- **Code review: pass, round 1** — `agents/principal-engineer/reviews/ENG-034.md`.
  0/10 automatic-failure checks. Every acceptance criterion this ticket owns
  traced against the actual diff, not the design's paraphrase;
  `MenuList.tsx`'s menu-read pattern and the selection-identity key
  confirmed matching by direct comparison. Four non-blocking findings — see
  "Named gaps" below.
- **Quality: pass, round 1** (first real run on this ticket) —
  `agents/qa/test-plans/ENG-034.md`. `config-site-builder` has no test
  runner of any kind (no `test` script, no test-framework dependency, zero
  `*.test.*`/`*.spec.*` files) — every acceptance criterion this ticket owns
  is manual verification with a specific reason, accepted under
  `definition-of-done.md`'s allowance.
- **Security: pass, round 1** — `agents/security/reviews/ENG-034.md`. Full
  OWASP walk, zero findings. This diff adds no field, endpoint, or
  capability beyond what `ENG-033`'s already-reviewed `catering-request`
  accepts from any HTTP client, and adds no new fetch/network call of its
  own. Owner-configured `fulfillmentCopy` renders via plain JSX text
  interpolation (zero `dangerouslySetInnerHTML`) — no stored/reflected XSS.
  Selection identity uses a `Map`, not bracket-assignment off an
  attacker-influenced key — no prototype-pollution shape.

## PR

- `config-site-builder`: https://github.com/harsimranwalia/config-site-builder/pull/4

This project is registered **L1** — merge whenever suits you on GitHub
directly; the next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket once it's in.

## Named gaps, carried forward rather than hidden

- **F1 — no fallback when `SubmitEvent.submitter` doesn't populate**
  (`CateringForm.tsx:131`). An unsupported/non-compliant browser on a
  gate-open submit silently drops `action_type`/`selections` rather than
  failing closed with a message — the request still succeeds and the
  customer sees the same "submitted successfully" text, but it lands with
  none of the itemized detail this feature exists to capture. Lower
  reachability than the same-shaped bug this board failed a round over on
  `ENG-033` (any HTTP client there vs. an aged/non-compliant browser here),
  and it degrades to no worse than the gate-closed experience rather than
  crashing or corrupting data. Fix, if picked up: treat `orderFormEnabled &&
  !submitter` as a blocked submission with a message, the same way the
  zero-selections case is handled.
- **F2 — `||` vs `??` on one label fallback** (`CateringForm.tsx:237`). An
  intentionally-emptied `fulfillmentCopy` label would revert to the
  hardcoded default instead of rendering blank. Style preference, very low
  real-world likelihood.
- **F3 — duplicated loading-spinner JSX** across two button variants
  (`CateringForm.tsx:475-520`). Cosmetic; the file doesn't get meaningfully
  harder to read as-is.
- **F4 — `CateringForm.tsx` is now 540 lines**, further past
  `engineering-standards.md`'s ~400-line smell threshold (already ~420
  pre-diff — this ticket's own net addition is ~120 lines). Not asking for a
  split this round; worth watching if the next ticket here adds materially
  more.
- **`config-site-builder` has no test harness at all** — a materially
  different gap than `aiorders-api`'s own (which at least has `deno test`
  built in for free). Filed as its own proposal
  (`agents/eng-manager/proposals.md`, 2026-09-04), correcting the design
  doc's own citation of this as "`ENG-002`'s tracked gap" — `ENG-002` is
  scoped to `restaurant-portal` only.
- Two pre-existing, non-security-relevant conditions named at the security
  gate rather than re-filed as new findings: no upper bound on `quantity` or
  `selections[].name` length (the latter already logged, `ENG-033` Finding
  2), and native-`required`-only enforcement on `email`/`requirements`.

## Decision

Filled in by you. (None given — resolved by direct GitHub action.)
`config-site-builder` PR #4 merged directly to `main` (`40cfc55`, base `main`,
no stacking) — confirmed via `git merge-base --is-ancestor` on this ticket's
own recorded commit (`62b3ca0`) against fresh `origin/main`, cross-checked
with `gh pr view`. All three gate receipts re-read fresh, still `pass`; no
migration owed (frontend-only). Ticket carried `blocked → shipped →
verified`, including a full acceptance-check against the merged tree (not
receipt-bookkeeping — see the proposal filed this date on why that
distinction matters). This was the last of `ENG-016`'s four sub-tickets;
`continue ENG-016` fired this same pass. Full detail: `ENG-034`'s own
board-file log, 2026-09-04 entry;
`agents/devops/releases/2026-09-04-config-site-builder-ENG-034.md`;
`agents/product-manager/notebook/2026-09-04-acceptance.md`.
