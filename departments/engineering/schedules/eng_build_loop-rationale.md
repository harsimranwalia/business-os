# eng_build_loop — rationale

This file holds the evidence behind the rules in `eng_build_loop.md`: the
dated incident reconstructions, the measurements, the postmortems, and the
enforced-vs-instructed breakdown that explain why each rule reads the way it
does. **`eng_build_loop.md` is the operative document** — a pass follows it
and does not need this file to run. Each rule there that has history carries
a pointer to the section here that holds it; each section here names the
rule it supports. The point of keeping the evidence at all is that a rule with
its evidence attached does not get quietly relaxed — so when a rule in the
procedure is changed, the section here that supports it is where the change
must be argued.

## PRD checkpointing

Supports `eng_build_loop.md` step 2, *PRD-writing is not required to finish
in the pass that started it.*

Observed 2026-09-02: a single sequence-continuation filing (`ENG-007`'s
ticket 3, `skills/acceptance-check/SKILL.md` step 6b) ran the full
`skills/prd-writer/SKILL.md` process end to end as one atomic unit of work,
hit the 3600s ceiling in `lib/eng-trigger.sh` twice in a row with nothing
durable written either time, and camped on the single-flight lock for over
five hours across eight launches — starving two other answered decisions
and every routine `watch`/`scheduled` sweep behind it. The rule that came out
of it — checkpoint after each numbered `prd-writer` step and chain
`continue {TICKET-ID}` rather than pushing on toward a kill with nothing to
show for it — is in the procedure.

## Self-generated tickets

Supports `eng_build_loop.md` step 3, *The department may not turn its own
findings into tickets*, and the internal lane's reason for existing under
*The four lanes*.

**Why this rule exists, stated plainly so it is not quietly relaxed.** This
step used to shape agent findings straight onto the board on the grounds that
they were "delivery work, not business needs." That reasoning was sound for a
department building someone else's product and wrong for one that can file
tickets about itself. By 2026-08-13 it had produced a board where **eleven of
fifteen tickets were the department's own machinery**, two real product
tickets were explicitly held behind that machinery, and the two tickets
diagnosing the department's own token burn had been deprioritised behind its
gate tooling. One pass reliably produced more than one pass of work. The
approver's words: *"I run some tasks and it spits out 2 more so it's
never ending."*

The fan-out was structural, not a failure of judgement in any single pass —
every individual ticket was defensible, and that is exactly why a per-ticket
fix would not have worked. What is capped here is the department's ability to
create its own work at all.

The same board state is why the internal lane exists: the department was
spending most of itself on itself (the approver, 2026-08-13 — eleven of
fifteen tickets on the board were its own machinery).

## Incident items re-derived

Supports `eng_build_loop.md` step 4, the **Incident** gate type — *If the
file already carries a finished investigation, don't re-derive it — verify
it's still current and archive.*

Observed 2026-09-02: `2026-08-30-eng-loop-halted.md` was investigated and
answered (`decision: rejected`) on 2026-09-01, and a same-day scheduled
sweep (`f376e9c`) even re-confirmed it stale and wrote that finding back
into the file — but committed it under `inbox/`, not `inbox/_handled/`,
so the file never stopped looking like an open item. It re-surfaced as
a fresh `decision` event and burned two full 3600s timeouts today
before a third pass finally re-derived the same "already stale"
conclusion in minutes — then spent the rest of its hour investigating
unrelated uncommitted board state it noticed along the way, timed out a
third time, and the event was dropped for good with the archive step
still undone.

## Backlog resolved one item at a time

Supports `eng_build_loop.md` step 4, *When more than one item is answered,
resolve and commit one at a time — oldest first.*

Observed 2026-09-01: an overnight vendor rate
limit (see the back-off note under *The chain* in the procedure) let a
six-item backlog build up. The
pass that ran once the limit cleared spent its time gathering context
across the whole backlog — "the gate-check tooling, the caps/config, the
ticket templates, and the relevant skills" for every item at once — before
committing anything, hit the 3600s ceiling in `lib/eng-trigger.sh`
(`PASS_TIMEOUT_BASE_SECONDS`), and was killed with zero commits. The next
fire re-read the same backlog from scratch to work out what, if anything,
had actually happened, and repeated the same pattern twice more —
three consecutive hour-long timeouts, no forward progress. Committing
after each item bounds the loss: a kill mid-backlog then costs at most the
one item in flight, and the next pass's `git log` on the instance repo
tells it exactly where the previous one stopped, instead of it having to
re-derive that from uncommitted, partially-edited files.

## Reading only what the item needs

Supports `eng_build_loop.md` step 4, *Read only what the item in front of you
needs — not the rest of the backlog "for context."*

The 11:15 retry of the same 2026-09-01 incident
(above, §"Backlog resolved one item at a time") obeyed "one at a time" at
the planning level but then, before
resolving the first item, queued a combined read of four large files at
once — `ENG-007` (63KB), `ENG-008` (72KB), `ENG-013` (74KB), and the
decision-journal (39KB), reasoning that the tickets were "entangled." That
single ~250KB combined read, plus everything already in context from the
sweep, is what the pass was still silently chewing on 34 minutes later
with no commit made. Two tickets sharing history is not a license to load
both in full before acting on either: open only the ticket the item you
are resolving right now belongs to.

## Combined review and quality hop

Supports `eng_build_loop.md` step 6, *Code review and the quality gate are
one combined hop.*

Written as "concurrent" originally and sold as
parallel wall-clock savings — that was wrong: the single-flight lock means two
passes never run at once by design. The saving is one session and one hop
instead of two, which is real but smaller.

## Enumerating artifact mentions

Supports `eng_build_loop.md` step 6b, *Why this is a build-hop step and not a
review one.*

A review that runs the
grep can only report what it finds; a build hop that runs it fixes everything
it finds in the round it is already paying for. ENG-007 cost two full review
rounds in one day on the same class of miss — round 1 found
`agents/eng-manager/config.yaml`
claiming a rule three producers did not honour, round 2 found the *required*
standard behind the producer still contradicting the fix — and one grep over
the receipt paths would have surfaced both. The third round ran the
enumeration first, closed all remaining conflicts, and additionally ruled two
files *out* as false alarms that would otherwise have read as round-4
findings.

## Broken and dropped chains

Supports `eng_build_loop.md` step 8, *Also check for broken chains* and *A
chain that was fired is not the same as a chain that ran.*

The broken-chain check exists because chaining is an instruction to a model,
not a
guarantee: a session that gets truncated or simply doesn't reach the
instruction breaks the chain silently, and without a record there is no way
to tell "waiting normally" from "the chain broke".

The dropped-chain cross-check exists because of what happened next. Observed
2026-08-30/09-02: `ENG-009`
correctly chained its own `continue ENG-009` on reaching `building`; that
event was queued, failed twice during a bad stretch of pass timeouts, and
was dropped — and the ticket then sat at `building` for three days because
nothing re-fired it. The ticket's log line read `chained: ENG-009`, so the
broken-chain check passed it as healthy.

## Board index rolling

Supports `eng_build_loop.md` step 10, *Keep three dated entries, no more.*

This is not tidiness. Every pass reads this file in full, so an append-only
log is a tax on every future pass — measured 2026-08-12 at 1,007 lines /
~16K tokens of resident context, on a file whose live part is a six-row
table. Rolling it here costs one edit by the pass that created the entry.
`lib/eng-gate-check.sh` globs `ENG-*.md` and never reads either file.

## Enforced vs instructed

Supports the section of the same title in `eng_build_loop.md`, which keeps
the instructed list, the ADR-003 parent rule, and the prohibition on the
words "structurally impossible", "blocking" and "non-overridable". This is
the full breakdown.

Every rule here is one of two kinds, and confusing them is the bug this loop's
own parent ticket exists to close. ENG-001 reached `main` recorded as shipped
while owing all three gates, and every check the loop ran stayed green: they all
asked whether the ticket *moved*, never whether it arrived by a legal route.

**Enforced** — a script computes it, a non-zero exit follows, and a pass cannot
talk its way past it:

- `lib/eng-gate-check.sh` itself — the receipt table, read from the filesystem.
- The **pre-pass** run: whatever the check reports is injected into this pass's
  prompt — violations on exit 1, and on exit 2 the fail-closed diagnosis instead,
  which arrives on stderr with nothing on stdout.
- The **post-pass** run: a pass that *creates* a violation, or corrupts a ticket
  badly enough that the check fails closed, raises an inbox item and a
  notification (`lib/eng-notify.sh`) within seconds of doing it.
- `lane: fast` requires `size: XS` and a `bug`/`chore` type.
- **`blocked` carrying a `blocked_from` at all** — presence only, counted as a
  violation. Enforced since ENG-009; it was a warning until then, because the
  ticket template did not yet carry the field.
- **A parent ticket's sub-tickets are all settled** before the parent may sit at
  `shipped`/`verified` (ADR-003). A parent owes no receipts of its own — its
  evidence is its children's — but the exemption applies only when every child
  is `shipped`, `verified` or `dropped` and at least one actually shipped. A
  planted child *blocks* its parent rather than exempting it.
- **The board is non-empty.** A board directory that exists and holds no tickets
  is exit 2, not a clean sweep. "Checked nothing" must never read as "clean".

**Enforced on which host: both, since ENG-009.** `lib/eng-gate-check.sh` is
POSIX `sh` and `gate_interpreter` resolves the host's own shell, so the Mac and
the VPS container both run it and both get a real verdict. This was not true
until 2026-08-12: the check was zsh, the container ships no zsh, and every pass
that fired there ran with the receipt rule unenforced. If you are reading an
older note that says "enforced on the Mac only", it is stale.

**Instructed** — prose a session is asked to follow, with nothing mechanical
behind it:

- Merge detection refusing `shipped` from a state that owes gates (step 5).
- **Where a ticket goes when it leaves `blocked`** (step 8). The field's
  *presence* is enforced; its *destination* is not, and `blocked_from` records
  where the ticket was rather than where it should go.
- The release step calling the check before writing `shipped`.

**What this actually buys, stated exactly.** Nothing intercepts a model writing
`state: shipped` into a markdown file. True prevention of the bad write is not
available on this architecture, and any sentence here claiming otherwise is
wrong — see ADR-002. What is bought is that **a bad write cannot survive one
pass unnoticed.** ENG-001's failure mode was silence; this turns silence into a
notification and an inbox item inside the same pass that caused it, on either
host.

Do not describe any of this as "structurally impossible", "blocking", or
"non-overridable". Those words are the reason the parent ticket was filed.

**One residual hole, named rather than hidden.** The loop logs it, raises one
notice, and **continues** — halting the whole department because a check cannot
run is a worse failure than the one being fixed. While it is true, the receipt
rule is instructed rather than enforced, and the pass is told so in its own
prompt.

- **The check is missing or unreadable** — the file is gone or its permissions
  changed. Rare, and it is now the only route to the unavailable path: the
  second hole, *no interpreter on this host*, closed with ENG-009 and the
  resolver now falls through to the host's own shell.

**A note on 127.** It is the trigger's sentinel for "could not run at all", and
it is also what a shell returns for "command not found" — so the sentinel is a
flag set before the invocation, never the number alone. A check that exits 127
from *inside* is an ordinary not-clean verdict and raises the ordinary alarm.

## Why the chain is event-driven

Supports `eng_build_loop.md` §*The chain — why this isn't a cron job*.

A real team doesn't check a board twice a day. Someone pushes, the reviewer is
notified. A bug is filed, it lands in a queue. A PR merges, the next thing
starts. This loop works the same way, and `continue` is the event that makes it
so.

A pass stops after `building` on purpose — each heavy step gets its own
session with fresh context. What
was wrong before was not the split — it was chaining those sessions with a
*clock*: an engineer finishing at 10:00 left the work done, correct, and
untouched until 15:30. Now the pass fires the next hop itself before it exits.

## Queue wording corrections

Supports the queue, back-off and drop paragraphs of `eng_build_loop.md`
§*The chain — why this isn't a cron job*. Each of these is a case where the
procedure's wording and `lib/eng-trigger.sh`'s behaviour disagreed, and the
wording was corrected; the corrected wording is in the procedure, and this is
how each correction came about.

**"Every fire" was the wrong word for what reaches the lock, until
2026-08-13.** ENG-005 round 3 found the code and the sentence disagreeing on
all three of the fires that never reach the lock (an unchanged-fingerprint
`watch`, a ticket over its hop budget, the department over its daily
ceiling).

**The fourth suppression is listed apart from those three on purpose.** A fire
arriving inside an armed back-off window (ENG-016) takes the lock, appends,
drains, and re-queues at the same attempt — it skips only the launch. Counting
it with the three
above would put it in the part of the procedure a pass reads when it is
hunting a
lost event during an outage, and send that pass looking above the lock where
there is nothing to find. Corrected 2026-08-17 (ENG-016 code review
round 2) after the fix for a comment-vs-code contradiction reproduced the same
contradiction in the procedure.

**The stall notice bound.** Nothing else on the never-started path escalates,
which is right for a vendor limit and wrong for a host condition that does not
clear: `claude not on PATH` is in the same signature list and never
clears, and before this bound six consecutive fires produced one log line and
then indefinite silence with the queue frozen. Removing the bound re-creates
the failure ENG-005 exists to end: a broken environment indistinguishable from
a quiet night.

**"Never dropped" was the wording until ENG-005, and it was never true.**
The queue was popped *before* the pass ran and the exit status was never
inspected, so a pass that died had already consumed its event: nineteen were lost
that way in eight days, each needing the twice-daily safety net to notice. It now
reads correctly, which means saying plainly that events *can* be dropped.

**A pass that never started is a third outcome, and this is not a
technicality:** it is exactly how ENG-016's own build
event was dropped on 2026-08-13, after two launches that between them did
nothing at all.

**Why classification needs duration as well as output length.** A session
killed at the ceiling *mid-flight*
prints nothing regardless of how much work it did, and on 2026-08-15 a
793-second pass wrote three files and then emitted two lines. Output length
separates the prose case; only duration separates did-work from never-ran.

**The first fix left the retry unreachable on a bad day.** "The next fire of
any kind runs that retry" is the part the first fix got wrong: it left the
retry reachable only *below* the failure break, so on a day when nothing
succeeded no retry ever ran, no event ever reached the attempt cap, and the
loud drop never fired at all. A broken environment was again
indistinguishable from a quiet night — this section's own bug, one layer up.
The alarm must not depend on a later pass succeeding.

## Cadence — where the time actually goes

Supports `eng_build_loop.md` §*Cadence, and where the time actually goes*.

Measured against a full-lane ticket, the time goes, in order:

1. **Waiting on the approver** — unbounded, and usually the majority of
   elapsed time. No loop change touches this. The fixes are: answer through
   `lib/eng-notify.sh` (which now fires a pass immediately), raise a project's
   autonomy so a gate stops existing, or use the fast lane where the gate never
   applies.
2. **Pass boundaries** — this was up to ~6 hours, or overnight, or a weekend.
   The event chain removes it for everything that happens locally; what's left
   is only what a scheduled pass exists to catch.
3. **Rework rounds** — each failed gate costs a full cycle. The cheapest speed
   available is not failing: engineers get the standards and the security
   baseline *before* writing, and first-pass rate is tracked
   (`agents/eng-manager/config.yaml` → `speed`). Below 70%, the brief is the problem, not the
   engineers.
4. **Serial gates** — now partly parallel (review ∥ quality).

**More scheduled passes is still the weakest lever** — not because sessions are
expensive, but because polling for work that isn't there is waste at any tier.
Events beat polling on merit. Add events before adding passes.

## Machine WIP limit

Supports `eng_build_loop.md` §*Guards*, *Machine WIP limit (1)*, and step 6,
*There is exactly one slot.*

The approver's correction,
2026-08-29. This used to scale with the plan tier (up to 12), reasoned as
"these cost the approver nothing, so throttling them bought only latency."
True about cost, wrong about the outcome: at 6–12 in flight, a pass advanced
every ticket by one shallow step and moved to the next, so the board carried
many tickets simultaneously mid-pipeline and none of them ever reached
`shipped` — a department that looked busy and shipped nothing.

## Origins

Supports `eng_build_loop.md` §*Notes*.

Built 2026-07-27 with the engineering department. Revised the same day after
a Sonnet review found two structural faults: `blocked`
sat outside both caps, and L0 tickets had no terminating path and would have been
dispatched to engineers forbidden to write on that repo. Both fixed in the
procedure.
