# Acceptance — ENG-034 (catering menu selector, public form)

## Why this ran in full, not as receipt bookkeeping

Every ticket on this board since `ENG-011` (2026-08-30) has reached
`shipped → verified` via step 5's merge detection as "receipt-confirmation
and bookkeeping only" — re-reading the three gate verdicts, confirming no
migration, and flipping state. `acceptance-check/SKILL.md`'s own trigger is
"a ticket enters state `shipped`," and its stated purpose is exactly the
thing that shortcut skips: confirming the shipped thing does what the PRD
promised, checked against the live result, not against the receipts that
are themselves upstream evidence someone *intended* it to work. Ten tickets
(`ENG-008`, `009`, `010`, `013`, `015`, `022`, `024`, `031`, `032`, `033`)
went `verified` this way with no acceptance-check notebook entry anywhere —
confirmed by listing this directory: the last one before this entry is
`2026-08-30-acceptance.md` (`ENG-007`, `ENG-011`). `exceptions.md` carries
zero rows, so this was never a granted exception — it's drift. Filed as a
proposal (`proposals.md`, this date) rather than corrected retroactively for
the other ten; this entry runs the check properly for `ENG-034`, the ticket
actually in front of this pass.

## Scope

`ENG-034` owns AC-1 (narrowed), AC-2, AC-3, AC-4, AC-5 (client half), AC-6
(client half), AC-9, AC-11 of the parent PRD
(`agents/product-manager/specs/ENG-016-catering-quote-generator.md`).
AC-7/8/12 are `restaurant-portal` (`ENG-032`, verified); AC-5/6's storage
half, AC-10, AC-13 are `aiorders-api` (`ENG-033`, verified) — not re-checked
here, out of this ticket's own scope.

## Check against the live result — not the proxies

**The live result itself is not reachable from this department.** No
Cloudflare Pages dashboard/API access, and `config-site-builder` is a
per-restaurant, config-driven static build (`VITE_RESTAURANT_SLUG`/
`VITE_BRAND_ID`) with no CI/CD auto-deploy on this repo — so there is no
single "the live site" to open even with browser access, and no restaurant
currently has `orderFormEnabled: true` configured regardless (this is a
brand-new opt-in field, default off), so even a reachable live site would
only show gate-closed behaviour today. Same class of access gap `ENG-007`
and `ENG-011` already named for this board (no browser, no throwaway
Postgres) — the substitute that worked there was reading the exact deployed
source at the merged commit rather than the diff or the design's paraphrase
of it. Applied the same way here: `git show origin/main:{path}` for both
changed files, independently, rather than trusting the code review's or
QA's own account of what the diff does.

## Walk every criterion

| AC | Criterion (this ticket's scope) | Checked against | Result |
|---|---|---|---|
| 1 (narrowed) | Guest count stays always-visible/required; only the *selected* option's helper note is conditional | `CateringForm.tsx` (`origin/main`) lines 382–396: `number_of_guests` field always rendered with `required`, unconditionally; `selectedFulfillmentCopy?.guestCountNote` renders only when the selected option's config carries one | **Pass** — read directly, not cited from the review |
| 2 | Per-option instructional copy comes from that restaurant's own config, never hardcoded | Lines 242–244: `selectedFulfillmentCopy = orderFormEnabled && formData.delivery_method ? config.catering?.fulfillmentCopy?.[formData.delivery_method] : undefined`, rendered at 393–395/415–417. No hardcoded restaurant-specific string introduced by this diff | **Pass** |
| 3 | Dishes shown grouped by that restaurant's own menu categories, each selectable with a quantity | `CateringMenuSelector.tsx` lines 66–78: `menu.map(...).categories.map(...)`, category header from `category.name`; quantity stepper at 97–122 | **Pass** |
| 4 | A selected dish accepts a short free-text note, stored with that selection | Lines 124–137: note input shown when `quantity > 0`, `maxLength={500}`; `setNote` (60–62) writes into the selection's own `note` field, carried through to the POST body via `CateringForm.tsx`'s `selections` state | **Pass** |
| 5 (client half) | "Submit Quote Request" sends `action_type=QUOTE_SUBMITTED` + `selections` (category/item_id/name/quantity/note) | `CateringForm.tsx` lines 131–134, 169–170: submitter value read from the native `SubmitEvent`, `action_type`/`selections` set accordingly; zero-selection guard (136–142) blocks this action specifically | **Pass** (client half only — storage is `ENG-033`'s scope, already verified) |
| 6 (client half) | "Skip & Have Someone Contact Me" sends `action_type=MANUAL_CONTACT_REQUESTED`, no dish required | Second submit button, `value="MANUAL_CONTACT_REQUESTED"` (line 497); the zero-selection guard at 136 checks `actionType === 'QUOTE_SUBMITTED'` specifically, so Skip never blocks on dish count | **Pass (client half)** — one nuance, not a failure: if the customer picked dishes and then clicks Skip, the client still sends the non-empty `selections` alongside `MANUAL_CONTACT_REQUESTED` (truthy `actionType`); AC-6's "no selections" property holds only because `aiorders-api`'s already-shipped `deriveActionStatus` force-nulls them server-side regardless of payload — cross-referenced against `ENG-033`'s own verified receipt, not re-derived here, same conclusion the code review already reached independently |
| 9 | Gate-closed: form behaves exactly as it does today | Every new/conditional expression in the file traces back to the single `orderFormEnabled` boolean (lines 215–218) — `selectedFulfillmentCopy` is `undefined` when false (242–244), `deliveryOptions` labels fall back to the original hardcoded value (`(orderFormEnabled && …) || option.label`, line 237 — `false || option.label` when the gate is closed), the selector block doesn't render (423), email/requirements revert to today's required set (281–289, 438–448), the single legacy submit button renders (505–520), and `actionType` is always `undefined` when the gate is closed (132–134) so `action_type`/`selections` are both dropped by `JSON.stringify`, sending today's exact payload | **Pass** — traced end-to-end myself, not cited from the review's account, since this is the one property this ticket must not get wrong |
| 11 | Missing required contact fields blocks both submit actions; email required only when the gate is open | `full_name`/`phone`/`event_date` unconditionally `required` (259, 272, 365); `email` `required={orderFormEnabled}` (289) — native HTML5 constraint validation runs before either submit button's handler fires, so both actions are blocked identically | **Pass** |

## Non-goals

Scanned the merged diff for anything from the PRD's Non-goals list (pricing,
packages/tiers/upcharges, owner-side quote editing/resend, view tracking) —
none present. Every changed line traces to the design's own `## Components`/
`## Interfaces` sections, same conclusion the code review already reached.
No scope creep.

## Cost

$0/month, confirmed at the security and release-readiness gates already
(no new dependency, no new service) — not re-derived here.

## Route

**All eight criteria this ticket owns: pass**, verified independently
against the exact merged source, not against the test suite, the PR
description, or the engineers' own summaries. State → `verified`, owner →
`eng-manager`.

**Step 6b (continue an approved sequence): does not apply at this
sub-ticket's level.** The PRD's own named next items (Piece 2 — pricing;
Piece 3 — owner edit/resend + view tracking) belong to the *parent*
`ENG-016`'s own sequencing, not to this work-breakdown sub-ticket, and
`ENG-016`'s own G1 answer ("Lets start with piece 1") was already read, on
that ticket's own board log, as endorsing build order rather than
pre-authorizing the rest of the sequence — 6b's bar isn't met there either.
Whether to raise Piece 2 is `ENG-016`'s own question to answer once it
reaches its own acceptance-check, not this ticket's.

## What the estimate got right

`time_estimate: ~1.5-2 days` (single build session plus four gate hops) held
— no rework rounds, no gate failures, matching this family's own `ENG-031`/
`ENG-032`'s clean first-round shape more than `ENG-033`'s four-round history.
The design's own `## Interfaces` section specifying the exact prop shape,
menu-read pattern, and selection-identity key up front is very plausibly why:
nothing in code review's four non-blocking findings touches any of those
three load-bearing pieces.

## What it missed

The design's Risks section cited the missing-test-harness gap as
"`ENG-002`'s tracked gap" — wrong (`ENG-002` is `restaurant-portal`-scoped
only) — caught at the quality gate, not here, but worth naming again: a
design's own Risks section asserting a gap is "already tracked" should be
checked against the actual proposal list before being trusted, the same way
this acceptance-check checked the shipped code against the actual merged
tree rather than the diff's own framing.

## Also worth recording

**Production/live-path verification could not be performed, and this entry
says so rather than rounding up** — no Cloudflare dashboard/API access, and
the new capability has no live restaurant to observe regardless (opt-in,
default off). This is the same honest-substitution shape `ENG-011`'s own
entry set precedent for (reading deployed source directly in place of a
browser check) — worth reusing explicitly as the standard substitute for
this project family specifically, since `config-site-builder`'s per-
restaurant, no-CI-CD shape means "wait for the next ticket to get browser
access" isn't a plan that will ever resolve this gap on its own.
