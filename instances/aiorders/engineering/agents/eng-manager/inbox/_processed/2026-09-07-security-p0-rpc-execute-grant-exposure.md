---
type: eng-finding
agent: security
project: aiorders-api
severity: P1
date: 2026-09-07
carve_out: "step 3, eng_build_loop.md — P0 on a registered, non-internal-lane project: an actively exploitable vulnerability in code with real users. Ticket immediately, no proposal, no G1."
---

# P0 finding — two production functions callable by unauthenticated callers today

**This is a request to open a ticket immediately, not a proposal for the
weekly batch.** `aiorders-api` is registered `L1` (`config/projects.md`),
not internal-lane, so the carve-out in `eng_build_loop.md` step 3 applies:
"an actively exploitable vulnerability in code with real users... becomes a
ticket immediately, no proposal and no G1." Per the ticket template's own
`source:` field rule, this keeps `source: security` rather than routing
through `proposals.md`.

## What's confirmed, and by whom

`agents/eng-manager/proposals.md`, row dated 2026-09-07 (principal-engineer,
found while reviewing `ENG-048` round 1) already confirmed **live, via
direct read-only query against the actual production project
(`bmnmnejwdxbcqinqkwko`)** — not inferred, not assumed from generic Postgres
defaults:

- `calculate_platform_analytics` (`20260217000001_platform_analytics_cron.sql`)
- `get_acquisition_breakdown` (`20260905190000_add_acquisition_breakdown_rpc.sql`)

Both currently grant `EXECUTE` to `anon` and `authenticated` identically to
`service_role`. `anon` means **no authentication at all** — any caller
holding this project's public anon key (which is meant to be public; it
ships in every frontend bundle by Supabase's own design) can call either
function directly via `supabase.rpc(...)`, today, in production, bypassing
whatever application-layer authorization exists around the code that's
*supposed* to be the only caller.

**Root cause (confirmed independently a second time this pass, on
`ENG-048`'s own gate, against a from-scratch disposable replica of the same
project image):** this project's `public` schema carries a `pg_default_acl`
entry naming `anon`/`authenticated`/`service_role` directly with `EXECUTE`
at function-creation time. This is a separate mechanism from the `PUBLIC`
pseudo-role — a bare `GRANT ... TO service_role` (what both functions
currently have) does nothing to restrict the other two roles, and even
`REVOKE ... FROM PUBLIC` alone (round 1's own first attempt on `ENG-048`,
disproven on this exact project) does not close it. Both roles must be
named explicitly.

## Why this is P1 and not left for the weekly batch

- Confirmed live, not theoretical — direct catalog query against production,
  twice independently (the original finder, and this pass's own replica
  reproduction of the mechanism).
- Zero authentication required (`anon`, not just `authenticated`).
- Real production project serving real users — `aiorders-api` is "highest
  blast radius of the set" per its own `config/projects.md` entry.
- The fix is small, mechanical, and already proven twice on this exact
  project this same day (see below) — there is no design work or open
  question standing between "ticket opens" and "ticket ships."

**Not escalated further than this.** Data classification for both
functions' own output is Internal (aggregate business metrics — revenue,
order/customer counts, acquisition/channel figures), not
Confidential/Restricted — no PII, no credentials, no payment data. This is
why it's filed as a P0 **ticket**, built through the normal pipeline at
whatever pace the machine reaches it, rather than an active-incident
interrupt to the approver. Nothing here rises to "leaked credential" or
"exposed [restricted] data" — the two things security's own interrupt rule
reserves for waking a human directly.

## The fix — already proven, twice, today

`ENG-048`'s own `credit_order_if_eligible` carried the identical gap
(found by code review round 1, fixed by database round 2, independently
re-verified by principal-engineer, QA, and security's own gate — four
parties, same result). The working fix, adapted per function:

```sql
revoke execute on function public.{function_name}({arg_types}) from public, anon, authenticated;
grant execute on function public.{function_name}({arg_types}) to service_role;
```

Naming `anon`/`authenticated` explicitly is the operative part — confirmed
this pass (again) that `... from public` alone does not close it on this
project's `pg_default_acl` setup. Verification method (also proven and
reusable, `agents/security/reviews/ENG-048.md`): apply against a disposable
`supabase/postgres:15.8.1.073` replica, then `has_function_privilege` for
all four roles, then an actual `set role anon; select {function}(...)` to
confirm a real `permission denied`, not just a catalog read.

## Scope note for whoever shapes the ticket

The existing proposal's own text: "Likely the same gap on every other
function in this repo lacking an explicit `REVOKE`, i.e. most of them —
worth a project-wide sweep, not a two-function patch." Sizing that sweep
(how many of this repo's ~12 functions are meant to be public vs.
internal-only) is scoping work for whoever picks this up, not pre-decided
here. At minimum, the two confirmed-live functions above need the fix
immediately; whether this ticket also does the full-repo sweep or a
follow-up ticket does is a scope call, not a blocker to opening this one.

## Bookkeeping

Once this becomes a ticket, please correct `agents/eng-manager/proposals.md`'s
2026-09-07 row in place (mark it superseded by the new ticket id, matching
the correction-in-place convention that file already uses) rather than
leaving two parallel records of the same finding. Not done in this card
since the ticket id doesn't exist yet.

`agents/security/notebook/2026-09-07-findings.md` has the fuller writeup,
including a related but separate three-strike note about the security
gate's own A01 checklist (not this finding, and not blocking it).

---

**Processed 2026-09-07**, `finding` event pass (context
`rpc-execute-grant-exposure`), per `schedules/eng_build_loop.md` step 3's
P0 carve-out: `aiorders-api` confirmed registered `L1`, not internal
(`config/projects.md`), so this became a ticket immediately —
`ENG-050`, `agents/eng-manager/board/ENG-050-rpc-execute-grant-exposure.md`
— rather than a `proposals.md` line. `source: security` kept per
`templates/ticket.md`'s carve-out exception. Two corrections made while
shaping (severity `P1` frontmatter vs. P0 body throughout, resolved P0;
data classification "Internal" claimed vs. `security-baseline.md`'s own
table naming revenue Confidential, resolved without changing the outcome)
— both recorded on the ticket, not silently absorbed here. Incident notice
raised to the approver (`inbox/2026-09-07-eng050-p0-incident.md`),
`agents/eng-manager/proposals.md`'s 2026-09-07 row corrected in place per
this card's own Bookkeeping instruction. Moved here to `_processed/` to
match.
