# Review log — 2026-09-03

## ENG-022 (round 1, aiorders-api) — pass

Findings by category:

- **Duplication (non-blocking, 1st occurrence).** `offers.ts`'s 8
  access-denial call sites repeat an identical two-line block
  (`console.warn(...)` + `return {success:false, error}`) that a small local
  helper could collapse. Not blocking — matches the file's own pre-existing
  level of per-action repetition, and `offers.ts` deliberately stayed off
  `requireRestaurantAccess` per its own return-style convention. Watching for
  a second occurrence of "repeated denial/error-response block in one file"
  anywhere on this board before treating it as a standards candidate.
- **Positive signal.** A mutation check was actually executed this round
  (not hand-traced): disabling the access check at one throw-convention site
  and one return-convention site turned exactly the two matching tests red,
  with every other test in both files — untouched call sites included —
  staying green. That's the shape every negative-authz test on this board
  should have; worth pointing to as an example for future test-authoring.

## ENG-015 (round 1, aiorders-api + aiorders-admin-hub) — FAIL

Findings by category:

- **Automatic-failure #3/#10 (blocking, 3rd occurrence this week).** Zero
  test coverage on `restaurants.ts`'s new brand-scoping logic
  (`isStaff`/`getPartnerBrandIds`, all three modified functions). Direct
  in-directory precedent (`brands.test.ts`, `loyalty-config.test.ts`) and
  today's own `ENG-022` (24 tests, identical class of fix) both establish
  this is expected, not this repo's baseline. Third occurrence of this
  exact shape this week (`ENG-013` round 1, `ENG-008` round 1 — both logged
  here as "not yet a third," waiting for exactly this) — crosses
  `code-review-gate/SKILL.md` step 10's promotion threshold. Flagged to
  `observations.md` rather than edited directly: `engineering-standards.md`
  lives in the read-only department tree, out of reach for an
  instance-scoped pass.
- **Authorization bug (blocking, found independent of the missing tests).**
  `updateRestaurant` (`restaurants.ts:207-232`) checks only the target
  restaurant's *existing* `brand_id` against the caller's owned brands, then
  writes every other body field unfiltered via the service-role client — no
  RLS backstop. A partner can `PUT` their own restaurant with
  `{approved: true}` and self-approve it (defeats this ticket's own AC5),
  or with `{brand_id: <unowned brand>}` and reassign it. The build hop's own
  PR-body claim that this can't happen is checked against the code and is
  wrong — the check never inspects the incoming body, only the existing
  row. Exactly the class of bug the missing negative test above exists to
  catch.
- **Verified independently:** `deno check` clean (typecheck can't catch
  either finding — both are authorization logic, not types); worktrees
  match the ticket's recorded commits exactly, no drift; error wording,
  `Profile['role']` literals, and `user.profile` shape all confirmed against
  the actual source rather than trusted from the design/build log.

**Verdict:** fail, round 1. No receipt written. QA's hop discarded, no
test-plan file.

## ENG-015 (round 2, aiorders-api + aiorders-admin-hub) — PASS

Findings by category:

- **Both round-1 findings verified fixed, independently re-derived.**
  `stripPartnerRestrictedFields` closes both the self-approve bypass and
  the brand-reassignment bypass. Re-ran the mutation check myself rather
  than trusting the fix hop's own account: reverted the strip, got exactly
  the three tests naming these findings red (19 others green), restored
  byte-identical, re-ran clean. Same result the fix hop reported — now
  confirmed independently, not merely repeated.
- **Automatic-failure scan:** all 10 clear (#3/#10 closed by the 22 new
  tests).
- **Test quality (positive signal):** assertions on recorded `.update()`
  payloads and on which tables get queried at all — proving behaviour at
  the boundary with the datastore, not implementation internals. The
  "empty brand list never queries `restaurants`" test uses a `from()`
  override that throws on any unstubbed table, so it can't pass vacuously.
- **Three non-blocking notes, none asked for a re-round** (full text in
  the receipt): an untested empty-`{}`-payload PostgREST edge case (low
  severity — either behaviour preserves the security property); a
  pre-existing (not this round's) read-then-write ownership check in
  `updateRestaurant`, theoretically non-atomic, no real trigger path in
  this codebase; and a missing log line on the two new 403s — checked
  against this ticket's own cited precedent (`_shared/restaurantAccess.ts`,
  which also logs nothing on denial) and let go as consistent with that
  convention rather than a deviation from it, rather than promoted off one
  data point on each side.
- **The one substantive gap this round surfaces isn't a code defect: it's
  that AC3/AC4/AC5 (the add-location write path) rest entirely on the new
  RLS policy plus a frontend conditional, and neither this repo
  (`aiorders-admin-hub`, zero test infra) nor this pass (no live Postgres)
  can execute either.** Spent real effort de-risking this via a full
  policy-history trace instead of waving it through — see QA's own test
  plan for the trace itself. Recorded here because it's the kind of gap a
  future review on this same handler family should recognise on sight: a
  security-relevant INSERT/UPDATE policy with no live execution anywhere
  in its own ticket's history is a pattern this board has now hit more
  than once (`ENG-007`/`ENG-011`/`ENG-013`'s migrations, this ticket's own
  migration doc, now the policy's actual *logic*) — worth a proposal if a
  live read-only DB connection is ever wired in, so this class of gap
  closes for every future ticket at once rather than being re-traced by
  hand each time.

**Verdict:** pass, round 2. Receipt written
(`agents/principal-engineer/reviews/ENG-015.md`). QA passed concurrently
with one named, non-blocking coverage gap (above). Ticket continues to
`in-security`.

## ENG-024 (round 1, aiorders-api, fast lane) — pass

Findings by category:

- **Process gap, first occurrence.** Fast lane has no trigger that routes a
  migration discovered at *build* time to `database`'s own gate
  (`schema-change/SKILL.md`'s trigger is `touches_data: true` on an
  architect design — fast lane skips design entirely). This ticket's
  backfill migration went straight from build to this review with no
  database sign-off. Assessed it informally against `schema-change`'s own
  7 failure conditions myself (outside my actual scope — migration is
  explicitly not mine to gate) and found it low-risk: one soft miss (no
  stated runtime estimate/batching), matching this repo's own only backfill
  precedent exactly. Not blocking this verdict; filed as a proposal
  (`proposals.md`, 2026-09-03) since the mechanism gap is general, not
  specific to this migration.
- **Process note (self-correction, worth flagging so it isn't repeated).**
  My first attempt to reproduce the pre-edit `deno check` baseline used
  `git stash -u`, which silently no-ops when the diff is already committed
  (nothing uncommitted to stash) — it re-checked the *already-fixed* file
  against itself and would have produced a false "identical" match had I
  not noticed the line numbers weren't shifting the way the diff implied.
  Correct approach for a committed diff: `git show origin/main:{path} >
  {path}`, check, then `git checkout -- {path}` to restore. Worth
  remembering for any future round that needs a true pre-edit baseline on a
  branch where the fix is already committed, not left as an uncommitted
  working-tree change.
- **Positive signal.** Mutation check executed directly (not hand-traced):
  removing the one-line fix turned exactly the test naming it red, the
  unrelated guard-clause test stayed green, restore was byte-identical
  (`git diff --stat` empty). Same shape `ENG-022`'s own round today already
  set as the example to point to.

## ENG-031 (round 1, aiorders-api, schema-only migration) — pass

Findings by category:

- **Receipt found already written, uncommitted, from a pass with no other
  trace.** `agents/principal-engineer/reviews/ENG-031.md` existed at pass
  start — untracked, dated today, verdict `pass` — but the ticket's own
  frontmatter/log still read `in-review` with `links.review` blank, and
  `agents/qa/test-plans/ENG-031.md` didn't exist at all. No crash evidence
  (business-os sits uncommitted by this board's own current default, not a
  signal on its own), but the review's own claim to have logged itself in
  this file was false until this entry. Treated the same way the previous
  hop treated the migration file it found: verified before trusting.
- **Verified independently rather than re-derived from scratch.** Re-checked
  the migration against the design's `## Data` section myself (columns,
  types, nullability, constraint choice, comment shape) and re-ran the
  receipt's own citation (`proposals.md`, 2026-08-29, eng-manager — still
  open, 5 days old, well under the 30-day expiry) rather than taking either
  on trust. Both hold. No divergence found from the receipt's own
  conclusions — accepted as genuine, not rewritten.
- **Automatic-failure scan: 0/10**, re-confirmed. One file, 26 lines, pure
  DDL — no secret, no silent swallow, no unrelated refactor, no
  commented-out code, nothing bypassing a data layer, no auth/payment/
  deletion path touched.
- **Test quality: n/a.** No application code changed; the correct evidence
  class for a schema-only diff is design-conformance by inspection, not a
  test suite — covered under Design conformance in the receipt itself, not
  invented here as a gap.

**Verdict:** pass (unchanged from the existing receipt — completed and
logged, not re-reviewed from zero). QA's gate ran this same pass, also
pass: `agents/qa/test-plans/ENG-031.md`. Ticket continues to `in-security`.

## ENG-032 (round 1, restaurant-portal) — FAIL

Findings by category:

- **Automatic-failure #3 (blocking, first occurrence on this repo).** The
  `...content`-spread-before-normalised-fields fix in
  `CateringPageForm.tsx` (lines 53-66) — which the ticket, the design's own
  Risks section, and the commit message all independently describe as
  closing a real bug (an owner editing catering copy silently wipes
  `orderFormEnabled`/`fulfillmentCopy` on save) — ships with zero test
  coverage. Not an infrastructure gap: `@testing-library/react`, `jsdom`
  and `vitest` are already installed (`ENG-002`'s harness); nobody has
  written the first `restaurant-portal` component test yet, and this round
  needed to be the one that does. Distinct from the `admin-portal/handlers/`
  #3/#10 pattern `ENG-013`/`ENG-008`/`ENG-015` already tracked three times
  this week (different repo, different language, different failure shape —
  a frontend save-path bug vs. a backend authz gap) — not counted toward
  that same occurrence total.
- **Fix verified correct before flagging only the test (positive
  process note).** Traced all three links in the chain myself rather than
  reviewing the diff in isolation: the `useEffect`'s explicit field list
  never re-overwrites the `...content` spread's `orderFormEnabled`/
  `fulfillmentCopy`; `handleSubmit`'s `onSave({...form, ...})` doesn't
  re-narrow either; and the call site (`pages/website/Index.tsx:125`)
  passes the typed object straight through. The fix itself is right — only
  the evidence is missing.
- **Two non-blocking notes.** Trailing-whitespace-only edits on a few
  pre-existing `CateringKanban.tsx` lines beside the new entries — not
  automatic-failure #7, since the file still carries the same whitespace
  untouched elsewhere, reading as incidental re-typing rather than a
  cleanup pass. `CateringDetailModal.tsx:337` keys a rendered list on array
  `index` — low actual risk, the list is a static, read-only,
  submission-time snapshot never reordered after render.
- **Positive signal.** The mechanical part of this ticket — two new status
  strings across 8 files / 12 literals — matched the design's own named
  throw risk (`CateringKanban`'s `columns`/`statusConfig` pairing) 7-for-7,
  with colors applied consistently per each file's own existing shape
  rather than one copy-pasted pattern.

**Verdict:** fail, round 1. No receipt written. QA's hop discarded, no
test-plan file — the missing test made a real quality-gate run
premature anyway.

## ENG-032 (round 2, restaurant-portal) — pass

Round 1's only finding (automatic-failure #3) closed: `CateringPageForm.test.tsx`
added, and — distinct from every prior round on this board that took the
build pass's "confirmed red" claim on trust — verified it myself this round
by swapping the pre-fix file back in and re-running the test, rather than
re-deriving the conclusion from reading the diff alone. Same for the lint
baseline: round 1 and the fix round each logged a different total (63, then
96) for the identical baseline; resolved by lint-checking `origin/main`'s own
copy of the one file with a real error, independently of both prior claims,
rather than trusting either number. Worth normalizing as the default
verification move for any "confirmed red" or "confirmed zero-new" claim this
board carries forward, not just this ticket's.

Also did the quality-gate's own work this round (combined hop) — two new
component test files, mutation-verified. That reasoning lives in
`agents/qa/notebook/2026-09-03-coverage-gaps.md`, not here.

Full detail: `agents/principal-engineer/reviews/ENG-032.md`.

## ENG-033 (round 1, aiorders-api) — FAIL

Combined review+quality hop. Worktree confirmed on
`feat/ENG-033-catering-request-order-capture-endpoint@e3ef26a`, clean tree
aside from the standing unrelated untracked `deno.lock`. Diff: 2 files, 59
insertions/1 deletion (`git diff origin/main...HEAD`, re-fetched first).

**Automatic-failure scan: 0/10** — secret/credential clean; no new
try/catch; not a bug fix (type: feature, so #3 doesn't apply on its own —
see the blocking finding below, which is a correctness miss, not this
item); `isValidSelections(selections: unknown)` uses `unknown`, not `any`,
and isn't exported; no new query; no new dependency; no drive-by refactor
(insert-object edit only adds keys); no commented code/TODO; write still
goes through `supabase.from("catering").insert(...)`, same as before; no
auth/payment/deletion path touched.

**Blocking finding.** `isValidSelections` (new function, top of
`catering-request/index.ts`) validates `note`'s length only when
`typeof note === 'string'` — a present-but-non-string `note` (e.g. an
object) skips the check entirely and passes. Verified downstream rather
than flagged on suspicion: `restaurant-portal/src/components/catering/
CateringDetailModal.tsx:342` renders `{item.note && <span>...{item.note}
</span>}` as a direct JSX child, `restaurant-portal` has zero error
boundaries anywhere in `src/` (grepped), and objects are always truthy in
JS — so a `note: {}` submitted through this **unauthenticated** public
endpoint throws "Objects are not valid as a React child" the moment an
owner opens that request, unguarded. This is exactly the shape
`engineering-standards.md`'s "Failure direction is uniform" rule (added
2026-08-03) already names: `quantity` and `name` both fail closed, `note`
doesn't, and the one open path inherits the trust the other two earned —
"a half-validated record is a pass with extra steps." The build hop's own
log flagged this exact edge case and chose the narrow reading deliberately
(symmetry with `full_name`/`phone`/`requirements` being unvalidated) — but
those fields carry no typed contract to violate, where `note` does: the
design's own `## Data` section types the element shape as `"note": string
| null`, and `restaurant-portal`'s already-shipped `CateringSelection`
interface mirrors that exactly. `category`/`item_id` are also left
unvalidated by the design, but checked separately and confirmed safe:
`category` only ever becomes an `Object.entries` key (auto-coerced to
string, no crash) and `item_id` is never rendered anywhere in
`restaurant-portal` (grepped, only appears in the interface decl and test
fixtures) — so `note` is the one field where the design's silence is
actually load-bearing. Fix: reject any present `note` that isn't a string,
mirroring `name`'s strictness —
`if (note !== null && note !== undefined && (typeof note !== 'string' ||
note.length > MAX_NOTE_LENGTH)) return false;` or equivalent.

**Two non-blocking, low-confidence notes, not the reason this round
fails:** an empty `name: ""` passes (neither "missing" nor "non-string"
per the letter of the design's table) — renders as a blank list item, no
crash, possibly intentional; an empty `selections: []` with
`action_type: 'QUOTE_SUBMITTED'` passes and yields `status: 'Quote
Generated'` with zero items — the design's validation table doesn't name
this as invalid either, and the frontend (`ENG-034`, not yet built) likely
prevents it via UI, but the backend doesn't defend against a direct API
call. Worth a line in QA's eventual test plan, not blocking.

**One style preference, explicitly not blocking:** the new
selections-validation-and-400-return sits inside the status-derivation
block, after "Normalize data," rather than grouped with the other two
early-return boundary checks (`restaurant_id`, `source`) above it. Letting
this go — the validation is genuinely coupled to the `QUOTE_SUBMITTED`
branch, not a universal gate like the other two.

**Good work:** the conditional spread `...(derivedStatus !== undefined ?
{ status: derivedStatus } : {})` keeps "never touch status when
action_type is absent" exactly right with no extra branching; the
`website.ts` interface addition was checked against
`restaurant-portal/src/types/website.ts` directly and mirrors it
field-for-field, not just claimed to; and flagging the `note`-typing call
explicitly in the ticket log (even though this review reaches a different
conclusion on it) is exactly the right instinct — a silently-resolved
version of the same call would have been worse regardless of which way it
went.

**Verdict:** fail, round 1. No receipt written. QA's hop not run this
round (discarded per the combined-hop design — the code identified above
is about to change), no test-plan file.
