# Standards proposal from security — 2026-09-02

**Filed by:** security, at `ENG-009`'s security gate (three-strike rule,
`skills/security-gate/SKILL.md` step 10). Security proposes; this agent owns
`engineering-standards.md` and makes the edit — two agents writing that file
from independent three-strike rules is a concurrent-write risk with no
conflict handling, so this file only records the proposal.

## The finding, three times now

**Category:** A05 Security Misconfiguration — a handler's `catch` block
returns `error instanceof Error ? error.message : 'Unknown error'` directly
in a client-facing 500 response body, rather than a fixed, generic message.

| # | Ticket | File / function |
|---|---|---|
| 1 | `ENG-013` | `admin-portal/handlers/foodswipe.ts` — `setStageOverride`/`resetStageOverride` |
| 2 | `ENG-008` | `admin-portal/handlers/influencers.ts` — `getInfluencer`/`updateInfluencer` |
| 3 | `ENG-009` | `admin-portal/handlers/influencers.ts` — `getInfluencerActivity` |

Full detail on each: `agents/security/notebook/2026-08-31-findings.md` and
`agents/security/notebook/2026-09-02-findings.md`. None were blocking at
their own gate — every instance is role-gated before the handler runs, and
each copies rather than introduces the pattern (a repo-wide grep at
occurrence 2 found it in **8 files total** on `aiorders-api`, six pre-dating
this department's review process; three-strike counts gate-reviewed
occurrences only, not the repo's pre-existing total).

## Proposed addition to `engineering-standards.md`

Under **Errors and failure**, a new bullet:

> **Never return a caught exception's own `message` in a client-facing error
> response.** A `catch` block returns a fixed, generic message (e.g.
> `"Internal server error"`) and logs the real `error` server-side instead.
> An exception's message can carry internal state — a query fragment, a file
> path, a stack frame, a library's own error text — that a client-facing
> body is not the place for, regardless of whether the route is currently
> role-gated. Added 2026-09-02 after three occurrences across two files on
> `aiorders-api` (`ENG-013`, `ENG-008`, `ENG-009`) — each individually
> low-severity (role-gated, copied not introduced), the pattern itself was
> the actual repeat.

Suggested placement: also add this to the **Automatic review failures**
list (currently 10 items) so code review's checklist catches it going
forward, rather than relying on this agent noticing it again by eye. If
added there, the check is: *any `catch` block whose response body includes
`error.message`, `error.toString()`, or string-interpolates the caught
value* — not merely "an error is logged," which every one of these handlers
already does correctly server-side.

## Why now, not at occurrence 1 or 2

The rule is precise about the threshold — three, not two — since a pattern
seen twice could still be coincidence in two unrelated files, but occurrence
3 landing in the *same file* as occurrence 2 (a third function in
`influencers.ts`) is exactly the shape the three-strike rule expects: not
three independent engineers making the same one-off choice, but one
established file-level convention that new code keeps extending, because
nothing earlier in the pipeline told anyone it was a problem. Code review's
automatic-failure scan on both `ENG-008` and `ENG-009` ran its full 10-item
checklist and did not catch this — it isn't on the list yet, which is
exactly the gap this proposal closes.

## Not acted on by this entry

This is a proposal, not an edit. `engineering-standards.md` is unchanged by
this file. No ticket's gate result changes retroactively — all three
occurrences keep their original `pass` disposition at severity Low.
