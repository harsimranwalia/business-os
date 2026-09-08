# Coverage gaps — 2026-09-06

## ENG-041 — a client-side tenant-scoping filter had no test pinning it, on the same ticket that just proved the pattern leaks

First quality-gate run on this ticket (round 1 never reached QA — review
failed first, discarded per `code-review-gate/SKILL.md` step 9). The read
query behind AC1 (`questions/Index.tsx`, "never another restaurant's")
filters with `.eq('restaurant_id', currentRestaurant.id)`, but nothing in
the diff asserted that filter stays in place. Only live RLS backed it, and
RLS authorises a user for *every* restaurant they manage, not just the one
selected in the portal — for the explicitly-supported 2+-restaurant owner,
RLS does not stand in for the client-side scope the way it would for a
single-restaurant user.

**Worth naming because this exact ticket already produced the sibling bug.**
Review round 1 on this same ticket failed on the FAQ-*write* side leaking a
draft across restaurants for precisely this reason — a scoping check that
existed nowhere durable enough to survive a refactor. The read-side query
had the filter and it was correct, but "correct today" and "pinned by a
test" are different claims, and this board just watched the gap between
them cost a full review round on the write side of the same feature. Closed
directly rather than filed as a bug: added
`pages/questions/Index.test.tsx :: "scopes the query to the currently
selected restaurant (AC1)"`, mutation-verified (removed the `.eq(...)`
call, confirmed only this test went red, restored clean) per this role's
"extend where coverage is thin."

**Not filed as a proposal.** One occurrence closed within its own gate run,
same disposition as every other first-quality-gate-run finding on this
board. Naming it here in case a second instance of "a multi-tenant scoping
filter shipped correct but untested, on a project with real per-restaurant
data" shows up on a different ticket — that would be the point to consider
a sharper rule (e.g., the quality gate treating any new query against a
table with a `restaurant_id`/tenant column as needing an explicit scoping
test, the same way pagination already gets one), not this single occurrence.

Full finding, the fix, and the acceptance-coverage table:
`agents/qa/test-plans/ENG-041.md`.
