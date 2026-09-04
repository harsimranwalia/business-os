# Coverage gaps — 2026-09-04

## ENG-033 — first quality-gate run on this ticket found the derivation logic untested, not just the validator

Rounds 1 and 2 on this ticket both failed at code review, so per
`code-review-gate/SKILL.md` step 9 QA's result was discarded both times —
this round is the first time the quality gate actually asked "is AC-5/6/7
covered" on this ticket. It wasn't: `catering-request/index.ts`'s own
status-derivation branching (what actually implements "QUOTE_SUBMITTED →
Quote Generated, selections stored" / "MANUAL_CONTACT_REQUESTED → Contact
Requested, selections force-nulled") has no test. Only its downstream
dependency, `isValidSelections`, does.

**Worth naming as a pattern, not just this ticket's own miss.** This is the
second time on this exact diff family that a piece of logic turned out to
be untestable only because it was never extracted from `index.ts`'s inline
`serve()` callback — round 2 hit this for `isValidSelections` (extraction
was the fix), and this round hits it again one level up, for the code that
*calls* `isValidSelections`. `platform-customer-auth` is this repo's own
existing counter-example: it extracted far enough (`handler.ts`, tested via
constructed `Request` objects with no live Supabase needed for the
pre-DB-call branches) that this class of gap doesn't recur there.
`catering-request` only ever extracted the one function two rounds asked
for by name, not the shape of extraction that would have prevented needing
to ask twice.

**Not filed as a proposal — this doesn't need a ticket, an approval, or a
department-wide fix.** It's closing within `ENG-033`'s own next fix hop,
same as round 2's finding closed within this ticket. Naming it here in case
a third instance of "logic added inline in a `serve()` handler turns out
untestable" shows up on a different ticket — that would be the point
`engineering-standards.md`'s three-occurrences rule is for
(`code-review-gate/SKILL.md` step 10 / principal-engineer's own promotion
mechanism), not this one.

Full finding, the specific fix requested, and the acceptance-coverage
table: `agents/qa/test-plans/ENG-033.md`.
