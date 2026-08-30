# The Engineering Team

Ten agents that build software end-to-end so the approver doesn't have to.
Added 2026-07-27. This is the map — read it before touching any agent in the
department.

## Why it exists

The approver wants to build more than one person can build. The failure mode
isn't lack of ideas, it's that every idea routes through them: they spec it,
they architect it, they write it, they review it, they test it, they ship it.
That serialises everything on one person and ends in burnout.

The team removes the approver from the assembly line. The approver keeps
three jobs — decide what's worth building, break the ties only they can break,
and say yes to production. Everything between those three points is the
team's.

**The measure:** if a change to the department adds a recurring manual step to
the approver's week, it's designed wrong. Automate it or drop it.

## The roster

| Agent | Role | Owns | Can block? |
|---|---|---|---|
| `product-manager` | Approver PM | **The front door.** Intake, problem framing, PRDs, acceptance criteria, verification | Yes — scope |
| `eng-manager` | Engineering Manager | Delivery from the approved PRD on: the board, sequencing, WIP, gates, releases | Yes — sequencing |
| `architect` | Architect + AI Architect | System design, ADRs, AI/LLM architecture, one-way-door calls | Yes — design |
| `principal-engineer` | Principal Engineer | Code standards, every code review, simplicity | **Yes — merge gate** |
| `backend` | Lead Backend Engineer | Server, APIs, jobs, integrations | No |
| `frontend` | Lead Frontend Engineer | UI, client state, accessibility, performance | No |
| `database` | Database Expert | Schema, migrations, indexes, query performance, data integrity | **Yes — migration gate** |
| `qa` | Approver QA Engineer | Test strategy, automated tests, running suites, the bug ledger | **Yes — quality gate** |
| `devops` | AI Ops + CloudOps | Deploy, observability, cost, incidents, model ops | **Yes — release readiness** |
| `security` | Security Expert | OWASP, SOC 2, secrets, dependencies, authz | **Yes — veto to production** |

**Two agents talk to the approver, and only two.** The PM owns the *scope*
conversation — intake, G1, acceptance. The EM owns the *delivery* conversation
— G2, G3, releases, the weekly report, P0. The other eight talk to each other
and write artifacts. This is deliberate: nine agents each pinging the
approver is worse than doing the work themselves.

**The PM is the front door.** Business needs — the approver's requests,
kanban cards, Delivery handoffs — enter at the PM, which is the interface
between business needs and the technical team. Technical work that originates
*inside* the department — a QA bug, a security finding, a devops incident,
tech debt — goes straight to the EM; it's delivery work, not a business need,
and routing it through the PM would be a hop that helps nobody.

(Corrected 2026-07-27 on the approver's instruction. The department was first
built with intake at the EM, which put a delivery manager in the
business-translation seat.)

## The pipeline

```
  business need (the approver, kanban card, Delivery)
     │
     ▼
  [product-manager]  READBACK — input → two blind readings → divergence check
     │ + [architect]    diverge? ONE question, as a choice. Hold until answered.
     │                  (full lane only — a typo fix isn't ambiguous)
     ▼
  [product-manager]  shapes it into a ticket — project, size, type, lane
     │               PRD: readback, problem, criteria (tagged with provenance)
     │                                              ── GATE 1: the approver confirms
     ▼                                                 MEANING first, then scope
  [eng-manager]  picks it up here and owns delivery from this point on
     │           (technical intake — bugs, incidents, findings, debt — does NOT
     │            enter here. It becomes a line in proposals.md and reaches
     │            the approver as one batched G1 in the weekly report. Only
     │            what the approver approves re-enters at this point.
     │            Exception: a P0 on a project not on the internal lane. See
     │            "The department cannot commission itself" below.)
     ▼
  [architect]  tech design + ADRs; AI architecture when the change touches models
     │                                              ── GATE 2: the approver breaks one-way doors only
     ▼                                                 (reversible calls: architect decides, logs ADR)
  [eng-manager]  work breakdown → sub-tickets, sequence, WIP limit
     │
     ├── [database]   schema + migration plan (only when data is touched)
     ├── [backend]    implementation on a branch
     └── [frontend]   implementation on a branch
     │
     ▼
  [principal-engineer]  code review — standards, correctness, simplicity   ◀── BLOCKS
     │
     ▼
  [qa]  test plan → automated tests → run suite → log bugs                 ◀── BLOCKS
     │        └── bugs route back to the owning engineer, tracked to closed
     ▼
  [security]  OWASP + SOC 2 + deps + secrets + authz review                ◀── VETO
     │
     ▼
  [devops]  release readiness: deploy plan, rollback, observability, cost
     │                                              ── GATE 3: the approver approves production
     ▼                                                 (auto for L3 projects, notify only)
  [product-manager]  verifies acceptance criteria against the shipped thing
     │
     ▼
  [eng-manager]  closes the ticket, writes the proof entry, logs the lesson
```

## Four lanes, not one

The pipeline above is the **full lane**. Three others exist, and they matter more
than they look.

| Lane | When | Path |
|---|---|---|
| **Full** | Default | As diagrammed above |
| **Fast** | `XS` bug or chore touching none of: auth, payments, data deletion, schema, dependencies, model calls, public contracts, PII | `intake → building → in-review → shipped → verified`. No PRD file, no design, no separate test plan or security state. One combined gate from `principal-engineer`: review + suite run + OWASP on the touched surface. |
| **Internal** | Any ticket on a project registered **internal** (instance-configured, empty by default), at any size or type | `intake → shaped → [G1] → building → in-review → shipped → verified`. Code review only — no quality gate, no security gate, no release readiness, no G3. |
| **Advisory** | Any ticket on an **L0** project — a client-governed repo, e.g. `<project>` | `intake → shaped → designed → advised`. Terminal. Nothing built, branched, or scanned; the design and findings are packaged for the approver to carry into the client's own process. |

The fast lane exists because without it a one-line fix costs five documents and
nine state transitions — so the approver fixes it themself, and the
department only ever gets used on the big tickets where its overhead hurts
most. **It cuts ceremony, never rigour:** the regression test still ships, the
suite still runs green, the OWASP check still covers what the diff touched. A
ticket can drop out of the fast lane into the full pipeline at any point; it
can never enter late.

**The internal lane is that same reasoning applied to a repo instead of a
ticket size** (the approver, 2026-08-13). Every machine gate in this
department was designed for software that ships to someone — a deploy target,
a second committer, a user whose data is in it. A project registered as
internal has none of those, and a release there *is* a commit to `main`.
Running five gates over markdown and local shell scripts bought ceremony
rather than safety, and building the tooling to run those gates became the
department's largest single consumer of its own capacity: on 2026-08-13,
**eleven of the fifteen tickets on the board were the department's own
machinery**, and the only product ticket that had ever shipped was two weeks
old.

Code review is **not** waived, and its receipt is still enforced — `lib/*.sh` is
real code that runs unattended on two hosts. The lane's guard is `project:`,
checked in `lib/eng-gate-check.sh` (`INTERNAL_PROJECTS`), so a client-repo
ticket cannot reach the exemption by relabelling itself. `INTERNAL_PROJECTS`
is instance-configured and empty by default — widening the lane is a
deliberate instance-config change, not a code edit.

The advisory lane exists because an L0 ticket that reached `ready` would be
broken down and assigned to engineers contractually forbidden to write code on
that repo — a dead end in the state machine, landing on the one live client
engagement. Found in review, 2026-07-27.

**Each lane owes receipts, and the receipts are files.** A gate writes a
per-ticket file on a `pass` verdict only, and a ticket may not sit at `shipped`
or `verified` without the ones its lane produces — full owes all three
(`agents/principal-engineer/reviews/{ID}.md`, `agents/qa/test-plans/{ID}.md`,
`agents/security/reviews/{ID}.md`), fast and internal owe the first, advisory
owes none because it clears no gates. `lib/eng-gate-check.sh` reads the
**filesystem**, never the frontmatter: a pass cannot satisfy it by writing
`test_plan: done`.

**What that is worth, precisely.** Nothing intercepts a model writing
`state: shipped` into a markdown file — true prevention is not available on this
architecture, and ADR-002 exists to stop anyone claiming it is. What the check
buys is that **a bad write cannot survive one pass unnoticed**: the build loop
runs it before and after every pass, and a pass that creates a violation raises
an inbox item and a notification within seconds. ENG-001 reached `main`
recorded as shipped while owing all three gates and nothing said a word —
that silence is the thing that was fixed, not the write.

<!-- eng-host-reach: both -->

**Both hosts run it, since `ENG-009` (2026-08-12).** Until then the check was
written in zsh and the VPS container ships none, so on the container it could not
run at all and the receipt invariant was instructed rather than enforced there —
which, since the board lives on the VPS, was the common case rather than the
exception. The check is now POSIX `sh` and the trigger resolves the host's own
shell, so the Mac and the container both produce a real verdict. **If you find a
note anywhere saying "enforced on the Mac only", it predates ENG-009 and is
stale.**

One route to "unenforced" remains and is deliberate: if the check file is missing
or unreadable, the loop logs it, raises one notice, and continues rather than
halting the department. The full breakdown of which rules are enforced and which
are merely instructed lives in `schedules/eng_build_loop.md` under *Enforced vs
instructed*.

## Priority — the one lever the approver has over the queue

Added 2026-08-13 at the approver's request. **`severity` and `priority`
answer different questions and belong to different people.**

| Field | Question | Owner | Values |
|---|---|---|---|
| `severity` | How bad is this problem? | the agent that files it | `P0`–`P3` |
| `priority` | What should be worked first? | **the approver, only** | `now`, `next`, `hold`, or empty |

Before this field existed, the only way for the approver to change what got
built first was to argue with an agent's severity assessment — which
conflates a technical judgement with an instruction and leaves the approver
negotiating with their own department. The two disagree legitimately and
often: a P3 chore the approver wants today outranks a P1 they're content to
leave until next week.

- **`now`** — start ahead of anything not already in flight, *including a
  higher-severity ticket*. The inversion is the point.
- **`next`** — take the first free slot.
- **`hold`** — do not start, do not drop. The "not now" that is not a kill, and
  it holds everything that `depends_on` the held ticket too.
- **empty** — the default: the EM orders it, exactly as before.

**No agent may write this field**, including the EM, and including on a "the
approver would obviously want this" inference. An agent that thinks
something should move argues it through `severity` or the proposal batch.

**Half of it is enforced, and the docs do not overclaim the other half.**
`lib/eng-gate-check.sh` treats an unrecognised value as a **parse error** —
fail-closed, because a priority the department silently ignored would be an
instruction from the approver that never arrived — and reports
`priority: hold` at `ready`/`building`/`in-review`/`in-qa`/`in-security`/
`ready-to-ship` as a **violation**. `now` and `next` are ordering hints with
no filesystem fact behind them; they are instructed prose and nothing
mechanical holds them.

**It ships with its surfaces.** A field the approver could only set by
opening a markdown file and editing frontmatter would be precisely the
recurring manual step this system is not allowed to add — so `lib/eng-notify.sh`
carries a per-ticket priority control on whichever channel the instance has
configured (a UI control, or a chat command like `prioritise ENG-016` /
`next ENG-014` / `hold ENG-015` / `clear priority on ENG-016`). Setting `now`
fires a pass immediately; waiting for the next scheduled one would make it
indistinguishable from `next`.

## The department cannot commission itself

**Agent-originated work is a proposal, never a ticket** (the approver,
2026-08-13). A QA bug, a security finding, a devops incident, an architect's
tech-debt note — each becomes one line in `agents/eng-manager/proposals.md`.
No id, no board row, nothing sequenced, nothing built. The weekly report puts
the list to the approver as a **single batched G1**; only what the approver
approves becomes a ticket.

**The limit above targets the department inventing work about its own
machinery — it says nothing about finishing a product feature the approver
already asked for** (the approver, clarifying against `ENG-006`, 2026-08-28).
A PRD can propose a multi-ticket sequence, and when the G1 answer on that
first ticket affirms the whole shape rather than just the ticket in front of
it, the rest of the sequence isn't a proposal waiting to be re-argued — it's
already-approved work. `ENG-006`'s own G1 said exactly this: *"the proposed
five-ticket sequence stands as shape to file incrementally, not as four
pre-approved tickets."* In practice: ship ticket one, then the PM files
ticket two itself, raises its own G1, ships it, files ticket three, and keeps
going until the sequence is finished or a G1 comes back rejected or held. The
mechanism lives in `skills/acceptance-check/SKILL.md` step 6b — it's what
"file incrementally" was supposed to mean all along, and until this
clarification nothing actually did it, so the department shipped ticket one
and sat waiting to be asked for ticket two. Nothing about this skips a gate:
every ticket in the sequence still earns its own full G1, its own design, its
own review, QA, and security passes. The only thing that stops being a
manual step is drafting and filing the next PRD.

**Why this exists, in the numbers that produced it.** Technical intake used to
shape straight onto the board, on the reasoning that agent findings are delivery
work rather than business needs — sound for a department building someone else's
product, and wrong for one that can file tickets about itself. On 2026-08-13:

| | |
|---|---|
| Tickets on the board | 15 |
| About the department's own machinery | **11** |
| Product tickets ever shipped | **1**, two weeks earlier |
| Product tickets explicitly held behind that machinery | 2 |

The two tickets diagnosing the department's own token burn had themselves been
deprioritised behind its gate tooling. The approver's description of the
experience: *"I run some tasks and it spits out 2 more so it's never
ending."*

**Every one of those tickets was individually defensible, and that is the point.**
The fan-out was structural — a pass sweeps three inboxes, shapes what it finds,
chains the next hop, and a failed gate chains a rework. One run reliably produced
more than one run of work. No amount of per-ticket judgement fixes a loop whose
output is its own input; what had to be capped was the ability to self-commission
at all.

**The one carve-out, and why it isn't a loophole.** A **P0 on a registered
project that is not on the internal lane** — production down, or an actively
exploitable vulnerability in code with real users — becomes a ticket
immediately, with no proposal and no G1. A live security hole must not wait a
week. Internal-lane projects are excluded **by name rather than by
judgement**, and that is what makes the carve-out safe: the lane is
instance-configured and, by definition, points only at projects with no
production and no users — so an internal project cannot raise a legitimate
P0, and the carve-out can never become a route back to self-generated
tickets.

**Silence costs nothing.** An unapproved proposal is not a rejection and not a
queue with the approver's name on it. It is never nudged, pinged, or
escalated. It is re-listed each week and expires after 30 days with one line
saying so — a real terminus, chosen deliberately, because a proposal list
that only grows is the same backlog with a different filename.

## The gates

**Three approver gates. That's the whole ask on their time.**

| Gate | What the approver is deciding | Raised by | Auto-skipped when |
|---|---|---|---|
| G1 Scope | Is this worth building, and is this the right shape? | `product-manager` | fast lane, or ticket is a security finding |
| G2 One-way door | The expensive-to-reverse call the architect deliberately won't make alone | `eng-manager` | the decision is reversible (architect decides, logs an ADR, moves on) |
| G3 Release | Ship it to production | `eng-manager` | project autonomy is L3 (the approver is notified after, not asked before) |

There is a fourth thing that reaches the approver, and it is not a gate: on
an **L1** project the release opens a PR and asks a human to merge it. That's
a **merge request** — the ticket goes `blocked` with `blocked_on: approver`,
keeps its WIP slot, counts against the approval cap, resurfaces after three
days, and the build loop detects the merge itself by local git ancestry.
Three of five registered projects are L1, so this is the common path.

It's called out because it was originally missing: an L1 release just set
`blocked` and stopped, which freed a WIP slot, counted against nothing, and
let the department accumulate an invisible pile of finished work waiting on
the approver — precisely what the caps exist to prevent. Fixed 2026-07-27.

**Five machine gates. The approver is never involved.**

| Gate | Owner | Blocks on |
|---|---|---|
| Code review | `principal-engineer` | Standards violation, correctness risk, unnecessary complexity, missing tests |
| Migration | `database` | Destructive or unreversible migration, missing rollback, unindexed hot path |
| Quality | `qa` | Suite red, acceptance criteria untested, open P0/P1 bug |
| Release readiness | `devops` | No rollback path, no observability on the new path, unbudgeted recurring cost |
| Security | `security` | Any OWASP Top 10 finding at high severity, secret in code, SOC 2 control break, unreviewed new dependency |

A machine gate is not advisory. No agent may override another agent's gate.
Only the approver can override, explicitly, in a session — and the override
is logged as an ADR with the risk accepted in writing.

## Artifacts — every one has a next step

The dead-end rule (`CLAUDE.md` → "Always do") applies to this department
hardest, because it produces the most artifacts. Nothing here is allowed to be
produced with no owner and no mechanism to advance it.

| Artifact | Written by | Lives at | Next step | Advanced by |
|---|---|---|---|---|
| Business need | product-manager | `agents/product-manager/inbox/` | Shaped into a ticket | Build loop, PM pass |
| Technical finding | qa / security / devops / architect | `agents/eng-manager/inbox/` | Shaped into a ticket | Build loop, EM pass |
| Ticket | product-manager, then eng-manager | `agents/eng-manager/board/{ENG-NNN}-{slug}.md` | Moves through states to `verified` (or `advised` on L0) | Build loop |
| PRD | product-manager | `agents/product-manager/specs/` | G1 approval → design | Inbox approval, then build loop |
| Merge request (L1) | devops | `inbox/` | The approver merges the PR | Build loop detects it by git ancestry |
| Tech design | architect | `agents/architect/designs/` | Work breakdown | Build loop |
| ADR | architect | `agents/architect/decisions/` | None — it's a record | — (terminal by design) |
| Migration plan | database | `agents/database/migrations/` | Applied with the ticket's release | devops release runner |
| Branch + PR | backend/frontend | project repo | Code review | principal-engineer |
| Review verdict | principal-engineer | `agents/principal-engineer/reviews/{ID}.md` on a **pass** only, plus the ticket `review:` block | Pass → QA; fail → back to engineer, and **no receipt file** | Build loop + `lib/eng-gate-check.sh` |
| Test plan | qa | `agents/qa/test-plans/{ID}.md` — written first as the working document, filled in with the result | Tests authored and run | qa + `lib/eng-gate-check.sh` |  <!-- eng-receipt-exception: QA's plan is written before the gate runs; the pass-verdict-only rule does not apply to it -->
| Bug | qa | `agents/qa/bugs/{BUG-NNN}-{slug}.md` | Assigned to an engineer, tracked to closed | Build loop, with SLA by severity |
| Security review | security | `agents/security/reviews/` | Pass → release; fail → back to engineer | Build loop |
| Release record | devops | `agents/devops/releases/` | Acceptance verification | product-manager |
| Cost notice | devops | `reports/costs/{YYYY-MM-DD}-{project}-{ENG-NNN}.md` | One line per notice, surfaced in the weekly report | — (terminal for now; rewires to a finance department if business-os grows one) |
| Project card | eng-manager | `inbox/` | Appended to `projects.md` on approval | Build loop, gate-return step |
| Incident | devops | `agents/devops/incidents/` | Postmortem → follow-up ticket | eng-manager |
| Weekly report | eng-manager | `reports/engineering-{YYYY-WXX}.md` | The approver reads it, or doesn't | — (terminal by design) |
| Proof entry | eng-manager | `reports/proof/{slug}.md` (optional) | Written only when the work was genuinely interesting | — (terminal for now; rewires to a marketing department if business-os grows one) |

## Projects and autonomy

The team works on whatever repo it's pointed at. Every project is registered in
`agents/eng-manager/config/projects.md` with an autonomy level:

- **L0 — observe.** Read and propose only. Never writes code. For client-governed
  repos where someone else's standards apply.
- **L1 — branch.** Writes code on a branch, opens a PR, passes all machine gates.
  The approver (or a cofounder) merges.
- **L2 — merge.** Merges to main once all machine gates pass. The approver
  approves releases.
- **L3 — ship.** Deploys to production after gates. The approver is
  notified, not asked.

Autonomy is a property of the project, not the ticket. Raising a project's
level is the approver's call and only the approver's.

## Rhythm

| Routine | When | What |
|---|---|---|
| `eng_build_loop` | **On event**, plus daily 09:30, 15:30, 20:30, and 02:00 as a safety net | Runs every in-flight ticket forward until it hits a human or new implementation work. The engine. |
| `eng_security_sweep` | Sun 07:00 | Dependency, secret, and control-drift scan across all registered projects. |
| `eng_weekly_report` | Sun 18:30 | One report: shipped, in flight, blocked, what needs the approver. Folds into the Sunday cadence. |

**The loop is event-driven, not scheduled.** A real team doesn't check a board
twice a day: someone pushes, the reviewer is notified. Work moves when something
happens — a request arrives, a gate is answered, a finding is filed, or a pass
ends with the ticket still in an agent-owned state and fires the next hop itself.
The two scheduled passes are a safety net for what no local event can see: a PR
merged on github.com, a machine that was asleep, an event pass that died.

Within a pass a ticket moves as far as it can, through consecutive machine-owned
states, stopping only at a human, at new implementation work, or at a failed
gate. It stops after `building` because one session that designs, builds,
reviews, tests and security-reviews runs out of context and does all of it badly
— so the next hop gets a fresh session, chained by an event rather than a clock.
Details and the runaway guard: `schedules/eng_build_loop.md` and the event queue,
hop accounting and single-flight lock in `lib/eng-trigger.sh`. (This pointed at
`connections/eng-event-loop.md`, which came from life-os and was never ported —
business-os has no `connections/`.)

The first version advanced one state per scheduled pass, which made a
review → QA → security run take a day and a half of pure waiting. That was a
mistake about what the calm is for. **The calm protects the approver's
attention, not machine latency** — machine gates cost the approver nothing,
so making them wait on it buys nothing. What stays deliberately slow: the
approver-facing WIP limit of 2, and every human stop being a real stop.

## Speed — where the time actually goes

The department will never be optimised for raw speed; it's optimised for the
approver not being in the loop. But slow-for-no-reason is just waste, and
most of the original slowness was exactly that. Ranked by how much elapsed
time each actually costs:

| # | Where time goes | Typical cost | The lever |
|---|---|---|---|
| 1 | **Waiting on the approver** | Hours to days. Usually the majority. | Answer through `lib/eng-notify.sh` — it fires a pass immediately. Or raise the project's autonomy so the gate stops existing. Or use the fast lane, where it never applies. |
| 2 | **Pass boundaries** | Up to ~6h, or overnight, or a weekend | Event triggers: intake and answered gates run a pass now, not at 15:30. |
| 3 | **Rework rounds** | A full gate cycle each | Shift left — engineers get the standards and the security baseline *before* writing. First-pass rate is tracked; below 70% the brief is the problem, not the engineers. |
| 4 | **Serial gates** | One model run each | Review and quality now run concurrently. Security stays after quality — it checks QA's test plan, so running it early would pass a plan that doesn't exist. |
| 5 | **WIP** | Blocks a second ticket starting | Split into two limits: 2 for tickets that will need the approver, 1 for tickets moving purely between agents — one ticket shipped before the next starts (the approver's correction, 2026-08-29; this was 6–12 and produced many shallow, unfinished tickets instead of throughput). |

**More scheduled passes is still the weakest lever** — not because sessions are
expensive, but because polling for work that isn't there is waste at any price.
Events beat polling on merit. Add a pass only when the metrics show tickets
genuinely sitting idle between them.

**The biggest single lever is autonomy.** Every gate removed is an unbounded
wait removed. Any project raised to L3 would ship without G3 entirely — the
approver notified after, not asked before. That's the approver's call and
only theirs; the EM cannot raise a level.

**What should stay slow.** Every human stop is a real stop. The
approver-facing WIP limit of 2 stays. Machine gates never get skipped to
save time — a hollow gate is worse than a slow one, and a department that
ships fast by not checking is just the approver doing it themself with extra
steps.

**Honest expectation, after all of this:** a full-lane M ticket is still a
multi-day thing, and throughput is a handful of tickets a week. What it buys is
correctness, an audit trail, and the approver's absence from the assembly
line. When speed genuinely matters more than those, doing it by hand is still
faster — and that's a legitimate call to make ticket by ticket, not a failure
of the system.

## The plan tier is a setting, not a constraint

Set 2026-07-27 on the approver's instruction: *"don't design so that we hold
back on the $20 pro plan, I can upgrade to $100 if these agents are better
than a real team."*

Until then, several real decisions had been shaped by an assumed budget — hop
ceilings, how many tickets could move at once, how thorough a review could
afford to be. That was the wrong axis to optimise. **Build what the work needs,
say what it costs, let the approver decide.**

One value controls it: `agents/eng-manager/config.yaml` → `plan.tier`.

| Tier | Hops/day | Hops/ticket | Machine WIP | Review depth |
|---|---|---|---|---|
| `pro` — $20 | 40 | 8 | 1 | standard |
| `max_5x` — $100 | 200 | 20 | 1 | thorough |
| `max_20x` — $200 | 600 | 40 | 1 | thorough |

Changing it moves every budget except machine WIP, which is fixed at 1 across
every tier (the approver's correction, 2026-08-29): a bigger plan buys more
hops per day and a deeper review, never more tickets moving at once. See
`agents/eng-manager/config.yaml` → `wip.machine_limit` for why.

**Two things do not move with the tier:**

- **No Anthropic API billing. No deployed endpoints.** These were never really
  about money — metered API spend has no natural ceiling where a subscription
  does, and a deployed endpoint is an ops burden and an attack surface the
  approver has to keep alive. Overruling either is a deliberate decision of
  the approver's, not a side effect of upgrading a plan.
- **`approver_limit: 2`.** The approver's attention is the one thing no
  subscription buys more of. Every other limit here exists to protect machine
  sanity; that one exists to protect the approver, and it stays.

And the guards stay guards. Hop ceilings catch *bugs* — a ticket bouncing
between two states — not healthy work. If the department is legitimately
hitting them, raise the tier; don't work around them. A limit that fires on
normal days teaches everyone to ignore it.

## "Better than a real team" — how you'd actually know

That was the condition attached to the upgrade, so it deserves numbers rather
than a feeling. A real senior team, on a good week, gets you:

| | A real team | What this department has to beat it |
|---|---|---|
| **Throughput** | 5–15 tickets/week, but you're in every standup | A handful/week, and you're in it three times per ticket |
| **First-pass gate rate** | ~60–70% | Tracked. Target 70%. Below that, the brief is wrong, not the engineers. |
| **Escaped defects** | The honest measure of any team | `agents/qa/bugs/_index.md` → "Escaped to production". Should stay near zero and be reviewed every time it isn't. |
| **Consistency** | Varies by who picked up the ticket | Every ticket gets the same OWASP walk, the same standards, the same test discipline. This is where agents genuinely win. |
| **Audit trail** | Usually reconstructed after the fact | Produced as a by-product: ticket → PRD → design → review → tests → security verdict → release record |
| **Your time** | Standups, 1:1s, reviews, unblocking | Three decisions per ticket |

### The four things a real team does that a checklist doesn't

Named as limitations first, then built. Three now have mechanisms; the fourth
partly does. None of them make an agent wise — they make the department
*accumulate* the thing rather than never having it.

**Pushing back on a bad idea → the Critic has a standing seat at G1.**
`agents/critic/` already existed as the one voice whose job is arguing the other
side; it was simply never invoked. Now every PRD goes to it before it reaches
the approver, and it writes a `## Dissent` into the G1 item — **only when it
has one.**

The PM is structurally the wrong agent to kill work: its job is turning requests
into buildable tickets, and an agent whose output is PRDs will tend to produce
PRDs. The approver gets both voices, each argued properly, in the item they're
already reading. It doesn't block and it doesn't create a second decision.

*Deviation, deliberate:* the Critic is documented as invoke-only, never
scheduled, never interrupting. Both still hold — this isn't scheduled, and it
adds a paragraph to an existing decision rather than a new one. The rule exists
to stop the Critic generating unsolicited output *at* the approver, and it
does.

**Taste → the decision journal.**
`agents/eng-manager/config/decision-journal.md`. Every answered gate is
recorded with the approver's reasoning in their own words, and the PM and
architect read it before writing. Rejections and edits are weighted above
approvals.

This is how a senior person actually develops taste for a specific approver:
not from the brief, but from watching what they kill, what they halve, and
what they wave through. Three consistent decisions promote to a pattern; one
is an anecdote, and the file says so.

**Noticing the unasked thing → the observations ledger.**
`agents/eng-manager/observations.md`. Any agent, any pass, one line, no
permission and no owner: *"while I was in there, I noticed…"*.

Nothing happens to a single observation, deliberately. Only a **pattern** —
three related, or one recurring across projects — reaches the weekly report. The
value of noticing is in the repetition, and a system that escalated every
observation would be worse than one that never noticed. Filing has to stay
cheaper than deciding whether to file, or agents stop noticing at all.

**Knowing when to break the process → the exception log, partly.**
`agents/eng-manager/config/exceptions.md`. An agent can request an exception with
a reason and an honest account of what it costs if it's wrong. The EM grants
*shape* exceptions — lane, artifact, sequence, WIP by one. The approver
grants the two that matter: release window, and any machine-gate verdict,
recorded as an ADR.

**The five machine gates are never excepted by an agent.** They aren't process,
they're the guarantee, and that distinction is the whole point.

The part that makes this more than paperwork: **three exceptions of the same kind
means the process is wrong.** At the third, the EM stops granting and files a
ticket to change the rule instead. That's most of what "knowing when to break the
process" looks like in a good team — not heroic rule-breaking, but noticing where
your own rules keep failing and fixing them.

### What still genuinely isn't there

Honest, because a department that can't say this isn't trustworthy:

- **Judgement under genuine novelty.** All four mechanisms above learn from
  repetition. The first time something is truly new, the department has nothing
  to pattern-match against and will be literal about it.
- ~~**Knowing what you actually meant.**~~ **Now has a mechanism** — the readback
  (`skills/request-readback/SKILL.md`). Two agents read the raw request
  independently, the architect blind to the PM's reading, and **divergence
  between them is the ambiguity detector.** Asking one agent "is this ambiguous?"
  gets a confident answer with nothing behind it; two careful readers of the same
  sentence disagreeing is an actual test. On divergence the approver gets one
  question, framed as a choice between the two readings — answerable in three
  seconds from a phone.

  Every gate downstream checks code against spec. This is the only one that
  checks spec against intent, and it runs first because "you misunderstood me" is
  cheaper and far more common than "that's a bad idea". The readback leads the G1
  item, so meaning and scope are confirmed in the same tap — no extra gate, no
  extra step.

  Still can't catch: a request where both readers are confidently wrong in the
  same direction. Rarer than a plain misread, but real.
- **The intuition that comes from having been burned.** A senior engineer's
  "I don't like this and I can't tell you why yet" is real signal. The Critic can
  argue a case; it cannot have a bad feeling.
- **Caring about the outcome.** It will execute a doomed plan impeccably. Nothing
  here substitutes for you deciding the plan is wrong.

**The number that decides it:** hours *the approver* spends per shipped
ticket, tracked in the weekly report. If that's falling while escaped defects
stay near zero, the department is earning its keep and a tier upgrade buys
more of a good thing. If it's flat, more plan won't fix it — the design is
wrong somewhere, and the weekly report's health paragraph should say so
plainly.

## What the team will not do

- Interrupt the approver for anything short of P0 — production down, data
  loss, or an active security incident. Everything else waits for the report.
- Batch up a queue of PRs for the approver to review. WIP is capped (default
  2). The team finishes before it starts.
- Ship an L2/L3 change to production on a Friday after 15:00, on a weekend,
  during `sabbath` or `retreat` mode, or while `ENG_RELEASE_FREEZE` is set.
  Hotfixes for P0 only. **Does not apply to L1** — opening a PR is not a
  production release, so it happens any day. Every project on the AIOrders
  instance is L1.
- Work on client repos above their registered autonomy level.
- Manufacture urgency. Severity has a definition (`config/definition-of-done.md`);
  "important" is not a severity.

## Relationship to the rest of the business

- **Delivery agent** owns *client engagements* — scope, sprints, retainers,
  client comms. The engineering team owns *building software*. When Delivery's
  engagements need code written, Delivery files an intake card with the EM; it
  does not direct engineers.
- **CFO** gets recurring-cost lines from `devops` whenever a release adds spend.
- **Marketing** gets proof entries when the team ships something interesting.
- **The weekly report is terminal** — the approver reads it or doesn't. An
  aggregator may surface the EM's digest in a daily brief later, if the
  instance grows one; the department does not route engineering work itself.
