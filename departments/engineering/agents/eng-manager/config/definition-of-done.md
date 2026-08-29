# Definition of Done

A ticket is done when every box below is checked by the agent that owns it.
Not "done pending review". Not "done except tests". Done.

Read by every agent in the department. The EM refuses to move a ticket to
`verified` with an unchecked box.

## Ticket states

| State | Owner | Exit condition |
|---|---|---|
| `intake` | eng-manager | Shaped: project set, size set, type set, one-line problem statement |
| `shaped` | product-manager | PRD written with acceptance criteria |
| `awaiting-scope` | approver | G1 approved in `inbox/` (auto-skipped for XS / bug / chore / security) |
| `designed` | architect | Tech design written; ADRs logged; one-way doors either decided or escalated |
| `awaiting-decision` | approver | G2 answered (only entered when a one-way door exists) |
| `ready` | eng-manager | Work broken down, sequenced, assigned; WIP slot available |
| `building` | backend / frontend / database | Branch pushed, self-tested, PR body written |
| `in-review` | principal-engineer | Review verdict `pass` |
| `in-qa` | qa | Suite green, acceptance criteria covered, no open P0/P1 |
| `in-security` | security | Security verdict `pass` |
| `ready-to-ship` | devops | Release plan + rollback + observability confirmed |
| `awaiting-release` | approver | G3 approved (auto for L3 projects) |
| `shipped` | devops | Deployed, health checks green, release record written |
| `verified` | product-manager | Acceptance criteria confirmed against the live thing |
| `advised` | eng-manager | **L0 only, terminal.** Design + findings packaged for the approver; nothing built |
| `blocked` | eng-manager | Blocker named, owner named, unblock condition named, `blocked_on` set |
| `dropped` | eng-manager | Reason recorded; no silent abandonment |

`intake` and `shaped` are owned by the **product-manager** — it is the
department's front door, and business needs enter there rather than at the EM
(corrected 2026-07-27 on the approver's instruction). Technical work originating inside
the department — bugs, incidents, security findings, tech debt — enters at the EM
and starts at `ready`.

### Blocked has two kinds, and they are not equivalent

| `blocked_on` | Means | Consequence |
|---|---|---|
| `agent` | Waiting on another agent, a dependency, or a closed release window | Escalates to the weekly report after 5 working days |
| `approver` | Waiting on a human: an L1 PR to be merged, a risk acceptance, a question only the approver can answer | **Counts against the approval cap**, resurfaces after 3 days |

A ticket blocked on the approver holds its WIP slot. Before this rule (fixed
2026-07-27) `blocked` sat outside both caps, so an L1 PR awaiting a merge freed a
slot, counted against nothing, and let the department start another ticket —
accumulating exactly the pile of finished-but-unapproved work the caps exist to
prevent.

### Priority — the approver's ordering lever, and it is not severity

Added 2026-08-13 at the approver's request. **`severity` and `priority`
answer different questions and are owned by different people**, and running
them together is what this field fixes: before it, the only way for the
approver to change what got worked first was to argue with an agent's
severity assessment.

| Field | Question | Owner | Values |
|---|---|---|---|
| `severity` | How bad is this problem? | the agent that files it | `P0`–`P3` |
| `priority` | What should be worked first? | **the approver, only** | `now`, `next`, `hold`, or empty |

- **`now`** — jump the queue. Start it before anything not already in flight.
- **`next`** — take the first free slot.
- **`hold`** — do not start, do not drop. The "not now" that is not a kill.
- **empty** — the default, and the behaviour that existed before this field: the
  EM orders it.

**These disagree often and legitimately.** A P3 chore the approver wants
today outranks a P1 they're content to leave until next week. When they
conflict, priority wins on *ordering* and severity still governs everything
else — SLA, escalation, whether a bug blocks a release. A `hold` on a P1 does
not make it a P3; it makes it a P1 nobody is working yet.

**No agent may set or change `priority`.** Not the EM, not the architect, not
on a "the approver would obviously want this" inference. An agent that
thinks something should move sooner argues it through `severity` and the
proposal batch, which is exactly where that argument belongs. Writing to this
field is how the one lever the approver has over the queue stops being
theirs.

**One half is enforced.** `lib/eng-gate-check.sh` treats an unrecognised value as
a **parse error** — fail-closed, because a priority the department silently
ignored would be an instruction from the approver that never arrived — and
reports `priority: hold` at `ready`, `building`, `in-review`, `in-qa`,
`in-security` or `ready-to-ship` as a **violation**: the approver said don't
start it and the machine is working it. `now` and `next` are ordering hints
with no filesystem fact behind them, so they stay instructed prose. Do not
describe them as enforced.

**How the approver sets it, without opening a file:** `lib/eng-notify.sh` —
a control on each ticket if the instance's channel supports one, or a chat
command such as `prioritise ENG-016`, `next ENG-014`, `hold ENG-015`, routed
back through the notify command, bucket H.

### The four lanes

| Lane | Applies when | Path |
|---|---|---|
| **Full** | Default | The state table above |
| **Fast** | `size: XS` and `type` is `bug` or `chore`, touching none of: auth, payments, data deletion, schema, dependencies, model calls, public contracts, PII | `intake → building → in-review → shipped → verified`, one combined gate from principal-engineer covering review + suite run + OWASP on the touched surface |
| **Internal** | Any ticket on a project registered **internal**, at any size or type | `intake → shaped → building → in-review → shipped → verified`. Code review only — no quality gate, no security gate, no release readiness, no G3. |
| **Advisory** | Any ticket on an **L0** project (a client-governed repo) | `intake → shaped → designed → advised`. Terminal. |

The fast lane exists because without it a one-line fix costs five documents and
nine transitions, the approver does it themself, and the department only
ever gets used where its overhead hurts most. **What the fast lane cuts is
ceremony, never rigour:** the regression test still ships, the suite still
runs green, and the OWASP check still covers the surface the diff touched. A
ticket can drop out of the fast lane into the full pipeline at any moment; it
can never enter late.

**The internal lane (the approver, 2026-08-13) is the fast lane's reasoning
applied to a whole repo rather than to a ticket size.** Every machine gate in
this department was designed for software that ships to someone: a deploy
target, a second committer, a user whose data is in it. A project registered
internal has none of those — no endpoint, no production, one human, and a
release *is* a commit to `main`. So five gates over markdown and local shell
scripts bought ceremony rather than safety, and the tooling to run those gates
became the department's largest single consumer of its own time. On
2026-08-13, eleven of the fifteen tickets on this board were the department's
own machinery.

**Code review is not waived, and its receipt is still enforced.** `lib/*.sh` runs
unattended on two hosts; the gate that reads it stays. What goes is the QA test
plan, the security review, release readiness, and the release gate — none of
which had a real question to answer on this repo.

The lane's guard is `project:`, checked in `lib/eng-gate-check.sh`
(`INTERNAL_PROJECTS`), so a client-repo ticket cannot reach it by relabelling
itself. `INTERNAL_PROJECTS` is instance-configured and empty by default —
widening the lane is a deliberate instance-config change, with a reason
recorded beside it, not something made in passing.

### Parent tickets — whose receipts are whose

An M or L ticket that gets decomposed keeps its id, and each sub-ticket carries
`parent: <the parent's id>`. **A parent owes no receipts of its own** — no gate
ever ran on it, because it never had a diff, and demanding a receipt for a gate
that did not run is a formality rather than a check (ADR-003). Its evidence is
its children's, and every child is checked normally under its own id.

The exemption holds only when all three are true: the parent has at least one
child, **every** child sits at `shipped`, `verified` or `dropped`, and at least
one child reached `shipped` or `verified`. `dropped` settles a child but proves
nothing, so a parent all of whose children were cancelled has shipped nothing and
has no business at `shipped`.

**`parent:` names another ticket and never itself, and a ring of tickets may not
name each other.** That is not style — self-parenting made a ticket its own
settled, shipped child and dropped all three of its receipts silently at exit 0.
`lib/eng-gate-check.sh` prunes any cyclic `parent:` edge and reports the ticket,
so the attempt fails loudly; a `parent:` naming a ticket that is not on the board
is reported the same way.

## Size

| Size | Meaning | Rough build time | G1 required? |
|---|---|---|---|
| `XS` | Under an hour of work, single file, no new behaviour | Under an hour | No |
| `S` | One clear change, one surface, no new interfaces | A few hours to half a day | Yes, unless bug/chore |
| `M` | Multiple files or surfaces, new interface, no new architecture | Half a day to a couple of days | Yes |
| `L` | New subsystem, new dependency, new data model, or cross-project | Several days to a week+ | Yes + likely G2 |
| `XL` | Doesn't fit — must be split before it leaves `intake` | — | Split it |

Rough build time is a band for prioritizing against other queued work, not a
commitment — a ticket's own PRD may narrow it with specifics the letter alone
can't carry (see `templates/prd.md`'s Cost section). The EM sizes on intake and
the architect may resize after design. An `XL` never
proceeds; splitting it is the EM's job, not the approver's.

## Time tracking and scope changes

Every ticket carries a build-time estimate from its PRD's Cost section, set at
G1 from the Size table's band above and narrowed with specifics when the
ticket has them (`templates/prd.md`). That estimate is not written once and
forgotten — it is carried and revised through `templates/ticket.md`'s `## Log`:

- **Time spent.** Each `## Log` entry written while a ticket is at `building`
  (or back in it after a review round) states the elapsed time for that entry,
  not just the state transition — e.g. `~3h since ready → building`, not just
  `ready → building` — and the same figure, as a running total, is written to
  the ticket's `time_spent` frontmatter field in the same edit.
- **Time remaining.** Each such entry also carries a revised remaining-time
  estimate, mirrored into `time_remaining`. "Unchanged since last entry" is a
  legitimate answer — say so — but the field is never silently dropped once a
  ticket has one.
- **Frontmatter is what the control-center dashboard reads.** `time_estimate`,
  `time_spent`, and `time_remaining` in the ticket's frontmatter are not
  decoration alongside the Log — they're the structured mirror of it that the
  dashboard actually renders. An agent that updates the Log prose without
  updating these three fields has left the dashboard showing stale numbers;
  update both in the same edit, always.
- **Scope discovered outside G1 is never silently absorbed.** A requirement,
  integration conflict, or piece of work that was not in the ticket's PRD is
  new scope, full stop — whether an architect finds it at design time (a
  one-way door, G2), an engineer finds it mid-build
  (`agents/backend/agent.md`, `agents/frontend/agent.md` — "that's a new
  ticket"), or the approver asks for it while this ticket is already queued or
  building. Each is raised — as a G2 item if it's a one-way door, as a new
  ticket via the PM otherwise — and the raise states, plainly:
    1. what the new piece is,
    2. how much time it adds on top of the current ticket's remaining
       estimate (a number or band, never "some more time"), and
    3. the two options this leaves: absorb it now (the remaining estimate
       moves and is logged), or hold it as a new ticket behind what's already
       queued.
  The added figure from (2) is also set in the gate item's own `time_impact`
  frontmatter field — the control-center dashboard reads that field to flag a
  gate as scope-affecting, not the prose. A gate with nothing to add on top of
  the current estimate leaves `time_impact` empty. Every `type: eng-decision`
  inbox item — not only scope-change ones — also carries `time_estimate` in
  its own frontmatter (mirroring the ticket's own field), so the dashboard
  shows the current estimate on the card itself, before it's opened.
  The approver decides which. Nobody upstream of that decision picks for them
  by quietly doing the extra work anyway.

## Severity — the only urgency vocabulary

Nothing in this department is "urgent", "critical", "ASAP", or "high priority".
It has a severity, and severity has a definition.

| Severity | Definition | Response | May interrupt the approver? |
|---|---|---|---|
| **P0** | Production down, data loss in progress, or an active security incident | Immediate, drops everything | **Yes** |
| **P1** | Core function broken for real users, no workaround | Next build-loop pass | No |
| **P2** | Broken with a workaround, or degraded experience | Within the week | No |
| **P3** | Cosmetic, minor, or a nice-to-have | Backlog, no commitment | No |

If a thing does not meet the P0 definition, it waits for the report. An agent
that escalates a P1 as a P0 gets that logged as a correction in its notebook.

## Done checklist — every ticket

**Product**
- [ ] Acceptance criteria written before code, testable, and each one verified against the shipped result
- [ ] Non-goals recorded, so scope creep is visible
- [ ] Any user-visible copy reviewed for the right voice (project's voice, not the approver's personal voice, unless it's the approver speaking directly)

**Engineering**
- [ ] Meets `engineering-standards.md`, including the project's own conventions
- [ ] No automatic-review-failure items present
- [ ] Lint and typecheck clean
- [ ] Build succeeds
- [ ] Branch named per convention, commits clean, no secrets in history

**Data** (when the change touches data)
- [ ] Migration is forward-only and reversible, or the irreversibility is an approved ADR
- [ ] Rollback path tested, not assumed
- [ ] Indexes exist for every new query pattern on a table over ~10k rows
- [ ] No unbounded scan on a hot path
- [ ] Backfill plan for existing rows, with runtime estimated

**Quality**
- [ ] Automated test for every acceptance criterion
- [ ] Regression test for every bug fixed
- [ ] Failure paths tested, not just the happy path
- [ ] Full suite green — not "green except the flaky one". A flaky test is a P2 bug with a ticket.
- [ ] Manual verification note where automation genuinely can't reach (with a reason)

**Security**
- [ ] OWASP Top 10 pass against the changed surface
- [ ] Authn/authz checked on every new endpoint or route — including the negative case
- [ ] All external input validated at the boundary
- [ ] No secret, key, or credential in code, logs, or error messages
- [ ] New dependencies reviewed: licence, maintenance, CVEs
- [ ] PII handling matches the project's data classification
- [ ] SOC 2 relevant controls unbroken (see `security-baseline.md`)

**Operations**
- [ ] Deploy plan written, rollback path defined and tested
- [ ] Observability on the new path — a failure is visible without a user reporting it
- [ ] Recurring cost delta calculated; anything above $0/mo goes to CFO before release
- [ ] Feature flag or safe default where the change is risky
- [ ] Release record written after deploy

**Closing**
- [ ] Ticket state `verified`
- [ ] Bugs found during the ticket either fixed or filed with an owner
- [ ] Anything learned written to the owning agent's notebook
- [ ] Proof entry written (optional) if genuinely interesting (`reports/proof/{slug}.md`)

## Release windows

- No production release Friday after 15:00 local, or on a weekend.
- No production release during `sabbath` or `retreat` mode, or while
  `ENG_RELEASE_FREEZE` is set.
- P0 hotfixes are the only exception, and they still pass the security gate.

## What "done" is not

- Merged is not done.
- Deployed is not done.
- "Works on my machine" is not done.
- "Tests pass locally but CI is flaky" is not done.
- Done is `verified` — the acceptance criteria confirmed against the running thing.
