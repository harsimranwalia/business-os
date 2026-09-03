# Schedule: eng_build_loop

**Status:** 📋 DESIGNED — wiring ready, not yet loaded. Run `./lib/eng-setup.sh --apply`.

**Description:** The engineering department's engine. Runs every in-flight ticket forward until it hits a human or new implementation work.

**Rationale:** the evidence behind these rules — incident reconstructions, measurements, and the enforced-vs-instructed breakdown — lives in the sibling file `eng_build_loop-rationale.md`. A pass does not need it to run; every rule below that has history points at the section holding it.

**Agents:** `agents/product-manager/agent.md` (intake) → `agents/eng-manager/agent.md` (delivery)

**Trigger:** **event-driven.** `lib/eng-trigger.sh` fires on five events:

| Event | Fired by | When |
|---|---|---|
| `intake` | `inbox/requests/` | a request lands — from the approver or a filer |
| `decision` | `lib/eng-notify.sh` | the approver answers a gate |
| `finding` | another agent | QA, security, devops, or the architect files something |
| `continue` | **the pass itself** | a pass ended with the ticket in an agent-owned state |
| `watch` | the scheduler's file-watch (macOS) or 5-minute poll (Windows) | an inbox file changed outside the notify channel — see the watch-event handling in `lib/eng-trigger.sh`. Windows Task Scheduler has no file trigger, so there it is a poll; `watch_fingerprint()` makes a poll that finds nothing cost one `find` and one sha1, with no pass and no hop |

**Schedule (human):** daily at 09:30, 15:30, 20:30, and 02:00 — a **safety net, not the engine**

**Scheduler.** A calendar-interval scheduler that catches a missed run on wake
matters for an instance hosted on a machine that sleeps, because plain cron
silently drops anything scheduled while it was asleep. Both supported hosts are
wake-aware: macOS `launchd` `StartCalendarInterval`, and Windows Task Scheduler
`StartWhenAvailable`. **business-os default is cron**, which runs continuously
and has no wake to miss; an instance on a machine that does sleep should still
prefer one of the two above. Wire either with `./lib/eng-setup.sh --apply` —
it dispatches on `$ENG_HOST`.

**Suppressed on sabbath/retreat/quiet:** yes

**Reading map — what each event must read.** Keyed to step numbers and `##`
titles, never line numbers.

- **Every event, not negotiable:** step 1 (Mode check), step 7 (Notify sweep
  — any pass that writes a gate item raises it there), step 8b (Observations
  and exceptions), step 9 (Chain), step 10 (Board update), and the sections
  *Enforced vs instructed*, *The four lanes*, *Guards*.
- `intake` → step 2.
- `finding` → step 3; step 6 only if the P0 carve-out starts a ticket.
- `decision` → steps 4 and 8c; step 5 when the item is an L1 merge request;
  step 6 when the answer advances the ticket into a machine-owned state;
  step 8's `blocked_from` paragraphs when the ticket leaves `blocked`; *The
  chain* when the item is an incident about the queue.
- `continue` → steps 6 and 6b; step 2 when the ticket is mid-PRD (the
  checkpoint note there).
- `watch` → steps 2, 3 and 4 — it sweeps all three inboxes — and step 5 if
  the changed file is a merge-request item.
- `scheduled` → the whole document. It is the safety-net sweep; narrowing it
  is what the sweep exists to prevent, so it is never narrowed.
- *The chain*, *Cadence*, *Notes* → reference. Read when hunting a lost event
  or a stalled queue, not on a normal pass.

**The map is a floor, not a ceiling.** It names the least a pass must read,
not the most. A pass that finds itself somewhere the map did not send it — a
gate item that turns out to be an incident, a ticket whose state does not
match its event, a rule it half-remembers from a section it skipped — reads
the section it actually needs, then acts. It does not force the work to fit
the sections already read, and it never guesses at a rule it did not read:
that guess is the one failure this map must not cause.

---

## What it does

Each pass, in order:

1. **Mode check** — `.env` → `MODE`. On `sabbath`, `retreat`, or `quiet`, log one
   line and exit.

2. **Business intake → Product Manager.** The PM sweeps
   `agents/product-manager/inbox/` and `inbox/requests/` for cards
   tagged `eng`. Each becomes a ticket at `intake`, shaped in the same pass, then
   carried toward a PRD. The PM is the department's front door: business needs
   enter there, not at the EM.

   **PRD-writing is not required to finish in the pass that started it.**
   Once the ticket exists on the board (as soon as step 1b of `prd-writer`
   runs), it is a normal machine-owned ticket like any other and chains
   exactly like one (step 6/9, `continue {TICKET-ID}`): finish the current
   numbered `prd-writer` step, write what that step produced to disk, and if
   the PRD process isn't complete, log which step it stopped after and fire
   `continue {TICKET-ID}` rather than pushing on toward a kill with nothing to
   show for it. The next hop resumes from that checkpoint. This applies the
   same way whether the ticket came from this step's fresh intake or from
   step 3's sequence continuation below. (The 2026-09-02 `ENG-007` episode
   that produced this rule — eight launches, over five hours camped on the
   lock, nothing durable written: `eng_build_loop-rationale.md` §"PRD
   checkpointing".)

   **Full-lane requests run the readback first** (`skills/request-readback/SKILL.md`):
   the PM's reading of the raw input, the architect's *blind* reading of the same
   input, and a divergence check. Two careful readers disagreeing is the
   ambiguity detector — if they diverge materially, the approver gets one
   question framed as a choice between the two readings, and the ticket holds
   at `intake` until they answer.

   This is the step that stops a badly-framed request becoming a well-built wrong
   thing. Every gate downstream checks code against spec; only this one checks
   spec against intent. Skipped on the fast lane and on agent-originated work —
   a typo fix isn't ambiguous, and ceremony gets skimmed.

3. **Technical intake → a proposal, not a ticket.** The EM sweeps
   `agents/eng-manager/inbox/` for work that originated inside the department —
   QA bugs, security findings, devops incidents, architect tech debt.

   **The department may not turn its own findings into tickets** (the
   approver, 2026-08-13). Each item becomes one line in
   `agents/eng-manager/proposals.md` and the card moves to `_processed/`. No
   id is allocated, no board row is created, nothing is sequenced, nothing is
   built. The proposal list is surfaced to the approver as a **single batched
   G1** in the weekly report; the approver approves any subset, and only an
   approved proposal becomes a ticket.

   **Why this rule exists, stated plainly so it is not quietly relaxed.** The
   fan-out was structural, not a failure of judgement in any single pass —
   every individual ticket was defensible, and that is exactly why a per-ticket
   fix would not have worked. What is capped here is the department's ability to
   create its own work at all. (The board state that produced it — eleven of
   fifteen tickets the department's own machinery, 2026-08-13 — and the
   approver's own words: `eng_build_loop-rationale.md` §"Self-generated
   tickets".)

   **What's capped is the department inventing work about its own machinery —
   finishing a product feature the approver already scoped as a sequence
   isn't that** (the approver, clarifying against `ENG-006`, 2026-08-28). When
   a PRD proposes a multi-ticket sequence and the G1 answer on it affirms
   proceeding with the whole shape, not just the one ticket in front of the
   approver, the rest of that sequence isn't agent-originated — it's the
   approver's own request, already reviewed once. `skills/acceptance-check/SKILL.md`
   step 6b is where this runs: on verifying a ticket in that position, the PM
   shapes and files the next named item itself — as many hops as that takes,
   see the checkpoint note in step 2 above, not required to land in the
   verify hop itself — and raises its own fresh G1, then does it again for
   the item after, until the sequence is done or a G1 comes back rejected or
   held. No gate gets skipped anywhere in this; what stops being manual is
   only drafting and filing the next PRD instead of waiting for the approver
   to notice it's missing.

   **The one carve-out, and the property that makes it safe.** A **P0 on a
   registered project that is not on the internal lane** — production down, or
   an actively exploitable vulnerability in code with real users — becomes a
   ticket immediately, no proposal and no G1. A live security hole must not
   wait for a weekly batch. Internal-lane projects are excluded from the
   carve-out by name and not by judgement: an internal project has no
   production and no users, so it can never legitimately raise a P0, and the
   carve-out therefore cannot become a route back to self-generated tickets.
   **If an internal-lane finding feels urgent enough to bypass this, it is
   not — write the proposal.**

   **Nothing is lost by waiting.** An unapproved proposal is not a rejection and
   not a dead end: it sits in the list, it is re-surfaced in each weekly report,
   and it expires after **30 days** with one line saying so. Expiry is a real
   terminus, deliberately chosen over an unbounded list — a proposal queue that
   only grows is the same backlog with a different filename.

4. **Gate returns** — read `inbox/` for answered items and act on each.
   Every `type: eng-decision` item carries `agent:` — the agent that *raised*
   it — alongside `project:`, which is only what the work is about. The two
   get conflated easily because both look like a label on the same item, but
   `lib/tuner-harvest.py` groups repeated corrections by `agent:` specifically,
   and a gate item with no `agent:` field lands as `unattributed` — nothing to
   tune, and nobody it points back to. A real harvest run hit exactly this on
   2026-08-18. `lib/eng-trigger.sh` already stamps `agent: eng-manager` on the
   four incident items it writes for the same reason.
   - **G1** (PM's) → `agent: product-manager`. The PRD is approved, changed, or
     killed; approved tickets hand over to the EM.
   - **G2 / G3** (EM's) → `agent: eng-manager`. Advance or kill the ticket per
     the approver's answer.
   - **L1 merge request** → see step 5
   - **Batched proposal G1** (from the weekly report's §3b, `agent:
     eng-manager` — the EM raises this digest regardless of which project each
     bundled row is about) → for **each
     approved** proposal only: allocate an id, write the ticket from
     `agents/eng-manager/config/templates/ticket.md` with `source: proposal` and G1 recorded as
     already answered, and move the row from `agents/eng-manager/proposals.md` → Open to
     → Approved with the ticket id. **Proposals the approver did not name
     stay Open and unchanged** — an answer naming three of seven approves
     three, and reading
     the other four as "not rejected, therefore fine to start" is inferring
     approval from silence, which this system does not do. If the answer is
     ambiguous about which ones, ask once rather than guessing generously.
   - **Approved project card** → append it to
     `agents/eng-manager/config/projects.md` at the approved autonomy level; the
     repo is untouchable until this append happens
   - **Risk acceptance** → the architect records it as an ADR, then the ticket
     continues past the security gate
   - **Incident** (`gate: incident` — the four items `lib/eng-trigger.sh`
     raises on itself: loop halted, loop stalled, events dropped,
     gate-violation watch) → act on the item's own `recommendation:`, write
     the finding as prose in the file, then **move the file into
     `inbox/_handled/` and commit, in this same pass.** There is no ticket to
     hand off to and no next owner the way G1/G2/G3 have one, so this move is
     the only thing that closes the item — write the finding but skip the
     move, and the file stays a top-level inbox entry indefinitely, looking
     exactly like an unanswered one to every later sweep.

     **If the file already carries a finished investigation, don't re-derive
     it — verify it's still current and archive.** A file with prose
     analysis and a populated `## Decision` section already present usually
     means an earlier pass did the work; a fresh gate answer from the
     approver looks the same on disk (`lib/eng-notify.sh` writes
     `decision:`/`## Decision` the moment the approver answers), so check
     whether the narrative already on the file answers the
     `recommendation:` before spending time re-investigating from scratch —
     if it does, confirm nothing's changed and archive. **And once you've
     confirmed it's stale, close it — don't let unrelated uncommitted state
     you notice along the way pull you off this item;** that's its own
     backlog item to raise, not a reason to widen this one. (Observed
     2026-09-02 on `2026-08-30-eng-loop-halted.md`: two full 3600s timeouts
     re-deriving a conclusion already written on the file, a third lost to
     unrelated state, the archive step still undone —
     `eng_build_loop-rationale.md` §"Incident items re-derived".)

   **When more than one item is answered, resolve and commit one at a time —
   oldest first — rather than reading every item's full history before
   acting on any of them.** Committing after each item bounds the loss: a
   kill mid-backlog then costs at most the one item in flight, and the next
   pass's `git log` on the instance repo tells it exactly where the previous
   one stopped, instead of it having to re-derive that from uncommitted,
   partially-edited files. (Observed
   2026-09-01: three consecutive hour-long timeouts on a six-item backlog,
   zero commits — `eng_build_loop-rationale.md` §"Backlog resolved one item
   at a time".)

   **Read only what the item in front of you needs — not the rest of the
   backlog "for context."** Two tickets sharing history is not a license to load
   both in full before acting on either: open only the ticket the item you
   are resolving right now belongs to. If resolving it genuinely requires a
   fact from another ticket, `grep` for that fact rather than reading the
   file whole — the same rule step 6b already applies to artifact mentions.
   Move to the next item's ticket only after the current one is committed.
   (The 11:15 retry of the same 2026-09-01 incident, and the ~250KB combined
   read that stalled it: `eng_build_loop-rationale.md` §"Reading only what
   the item needs".)

   Never infer approval from silence. An unanswered item is not a rejection — it
   stays open and appears in the weekly report's "Waiting on you" section,
   oldest first.

5. **Merge detection** — for every ticket `blocked` on an L1 PR (or PRs — a
   ticket may span more than one repo, `ENG-011` being the first): for
   **each** repo the ticket touches, `git fetch`, then check whether that
   repo's branch head is an ancestor of that project's default branch. A
   multi-repo ticket advances to `shipped` only once **every** repo's branch
   has merged — one repo merging does not ship the ticket, since the change
   is only coherent with all of them in. Partially merged → stays `blocked`,
   still holds its WIP slot, resurfaces after 3 days, and the ticket log
   names which repo(s) are still outstanding so the next pass doesn't
   re-derive it. Local git only: no API call, no cost.

   **One gate item per ticket, never one per repo.** A ticket spanning N
   repos still gets exactly one merge-request item in `inbox/`, listing every
   repo's PR as its own distinct line — never N separate items for what is,
   to the approver, one decision ("merge this ticket"). A second item for the
   same ticket would double-count it against the approver-facing WIP limit
   for work that is genuinely one unit, not two.
   See `skills/release-runner/SKILL.md` step 4 for the format.

   **A merge is not a gate.** Do not advance to `shipped` from a state that owes
   gates — a merged PR proves the code landed, never that it was reviewed,
   tested, or scanned. If the ticket's receipts are not on disk, it goes to the
   state of the first gate it still owes, and the ticket log names which. This
   is **instructed**, not enforced: nothing intercepts the write. What catches
   it is the post-pass receipt check, within the same pass — see *Enforced vs
   instructed* below.

6. **Dispatch** — each in-flight ticket runs forward through **consecutive
   machine-owned states** until it reaches one that needs a human, needs new
   implementation work, or fails a gate. Max 4 transitions per ticket per pass.

   **Order is `priority` first, then severity, then the EM's judgement**
   (the approver's lever, added 2026-08-13 — see `agents/eng-manager/config/definition-of-done.md`):

   - **`priority: now`** starts before anything not already in flight, ahead of a
     higher-severity ticket if there is one. That inversion is the entire point
     of the field; do not "correct" it back to severity order.
   - **`priority: next`** takes the first free slot.
   - **`priority: hold`** is **never started**, and a held ticket already in a
     working state is a violation `lib/eng-gate-check.sh` reports. If you find
     one, stop work and put it back — do not finish it because it is nearly done.
   - **empty** is the default and orders exactly as before.

   **Where a new start comes from: the To-do column, in priority order.** Every
   ticket at `intake`, `shaped` or `awaiting-scope` is one place on the board
   (the approver, 2026-08-13), and it is the only place a *new* start is
   drawn from. When a slot frees, take the highest-priority ticket there —
   `now`, then `next`, then unset, then never `hold` — rather than whatever is
   most recently touched or most interesting. That ordering is the board's own
   sort, so what you pick and what the approver sees at the top of To-do are
   the same ticket. Among tickets of equal priority, take the lowest ticket id
   — the order it was added — never the one that looks most interesting.

   **There is exactly one slot** (machine WIP 1, the approver's correction,
   2026-08-29). It does not free until the ticket occupying it reaches
   `shipped`. Do not start a second ticket into `ready` because the first is
   "basically done" at `ready-to-ship` — basically done is not done, and
   starting early is exactly the shallow-parallelism failure the limit exists
   to stop. Shaping and design work (`intake`/`shaped`/`designed`,
   `awaiting-scope`) is not gated by this slot and may continue as backlog
   grooming — it is paperwork, not code in flight.

   **Never write to `priority` yourself.** It is the approver's field, and an
   agent setting it on a "the approver would obviously want this" inference
   is the department taking back the one lever they have over its queue. If
   you think something should move, that argument goes in `severity` or the
   proposal batch.

   **A `hold` does not free the ticket's dependents.** Anything `depends_on` a
   held ticket stays held too, transitively — otherwise holding a ticket silently
   authorises the work stacked behind it, which is the opposite of what the
   approver asked.

   **Code review and the quality gate are one combined hop** — they read the same
   diff and don't depend on each other, so a single pass does both before
   handing on. If review fails, QA's result from that hop is discarded, because
   the code is about to change. (Why this is one session and one hop, not
   wall-clock parallelism: `eng_build_loop-rationale.md` §"Combined review and
   quality hop".)

   **Security stays strictly after quality.** It checks whether the negative
   authz cases are actually tested, so it needs QA's finished test plan. Running
   it earlier would mean passing a test plan that doesn't exist yet — a hollow
   gate, which is worse than a slow one.

6b. **Before editing on a build hop: enumerate the artifact's mentions.** When
   the change writes or relies on a **rule about an artifact** — a receipt path,
   a state name, a config key, a file another agent is told to produce — do not
   start from the file the instruction named. Start from the artifact's path and
   list every file that mentions it:

   ```
   grep -rn "{the artifact path or key}" --include="*.md" --include="*.sh" \
        --include="*.yaml" agents/ skills/ lib/ docs/
   ```

   Classify each hit before touching anything — **instruction** (tells a
   producer when to write; must agree with the rule), **map** (describes the
   call graph; must not contradict it), **location** (names where a thing lives;
   usually fine). Fix every *instruction* in conflict in this hop. A `map` in
   conflict is fixed here too when it is one line; anything larger gets routed.

   **Why this is a build-hop step and not a review one.** A review that runs the
   grep can only report what it finds; a build hop that runs it fixes everything
   it finds in the round it is already paying for. (ENG-007's two review rounds
   in one day on this class of miss, and the third round that ran the grep
   first: `eng_build_loop-rationale.md` §"Enumerating artifact mentions".)

   The failure this prevents is specific: **an instruction fixed in the file
   someone thought of, while the file that outranks it still says the opposite.**
   The artifact's path is the join key between them, and grepping it is cheap.

7. **Notify sweep** — the mechanism that stops a decision sitting there:
   - Any gate item written this pass → `lib/eng-notify.sh raise {file}`
     immediately, and stamp `notified:` in its frontmatter.
   - Any item with `notified:` older than 24h, no `nudged:`, and no `decision:`
     → `lib/eng-notify.sh nudge {file}`, stamp `nudged:`. **Exactly one
     nudge, ever.** After that it rides the daily brief and the weekly report.

8. **Dead-end sweep** — any ticket with no owner, any open bug with no owner, any
   ticket blocked past its threshold. Fix in the same pass or flag for the
   weekly report.

   **Also check for broken chains.** Every pass records `chained: {ticket-id}`
   or `chained: none` plus a reason in the ticket log before it exits. A ticket
   sitting in an agent-owned state whose last log line shows no chain record —
   or `chained: none` with no reason that justifies stopping — means a pass
   forgot to fire the next hop, and the ticket has been waiting on nothing.
   Resume it here. (Why a record is needed at all — chaining is an instruction
   to a model, not a guarantee: `eng_build_loop-rationale.md` §"Broken and
   dropped chains".)

   **A chain that was fired is not the same as a chain that ran.** The check
   above catches a pass that forgot to write `chained:` at all — it does not
   catch a pass that correctly fired the next hop and then had that queued
   event fail twice and get DROPPED downstream (`lib/eng-trigger.sh`'s
   `MAX_EVENT_ATTEMPTS`, logged to the day's `*-eng-events-dropped.md`). To
   the ticket the two look identical — it sits in an agent-owned state with
   nothing coming — but the log line reads `chained: {ticket-id}`, so the
   check above passes it as healthy. Cross-check every ticket's last
   `chained: {id}` against that day's `*-eng-events-dropped.md` files for a
   `continue {id}` (or `decision`/`finding`/`intake` naming that ticket) with
   no later `chained:` line on the ticket since — same remediation as a chain
   that was never fired: re-fire `lib/eng-trigger.sh continue {ticket-id}` in
   this pass. (Observed 2026-08-30/09-02: `ENG-009` sat at `building` for
   three days exactly this way — `eng_build_loop-rationale.md` §"Broken and
   dropped chains".)

   **Leaving `blocked` returns to `blocked_from`** — the state the ticket left
   to enter `blocked`, written on entry and cleared on the way out. Without it
   the destination is a guess, and the guess is *forward*, which is how a ticket
   skips the gate it was sitting at.

   **The two halves of this rule are not the same kind, and the difference is
   load-bearing.** That the field is *present at all* on a `blocked` ticket is
   **enforced** since ENG-009: `lib/eng-gate-check.sh` counts a missing
   `blocked_from` as a violation and exits 1. Where the ticket *goes* when it
   leaves is still **instructed** prose, and nothing mechanical holds it. Do not
   collapse the two — enforcing presence does not make the return rule true, and
   the return rule is in fact wrong for most of the blocks this department
   actually generates (see the exception below).

   **One documented exception, because it has already bitten:** a ticket that
   entered `blocked` from `in-review` on a *failed* third round does not return
   to `in-review` — that would re-review an unchanged diff. A gate that concluded
   against you sends the ticket to `building`. `blocked_from` records where it
   *was*; it does not always name where it *should go*.

8b. **Observations and exceptions** — the two things that keep this department
   from being permanently literal:
   - **Anything you noticed** that isn't a bug, a ticket, or a finding → append
     one line to `agents/eng-manager/observations.md`. No permission, no owner,
     no obligation. Filing must stay cheaper than deciding whether to file, or
     agents stop noticing. Nothing happens to a single observation; the weekly
     report looks for patterns.

     **Observation vs proposal, since both are one-line appends and step 3 now
     routes real findings into the second file.** An observation asks for
     nothing — it is a note that something is so. A proposal asks for a ticket.
     If you would be disappointed that nobody acted on it, it is a proposal:
     write it to `agents/eng-manager/proposals.md` where the approver will actually see it
     batched. Filing a proposal as an observation is how a real finding gets
     lost, and filing an observation as a proposal is how the batch becomes
     unreadable.
   - **Any `exception-request:` in a ticket log** → the EM answers shape
     exceptions (lane, artifact, sequence, WIP-by-one) in this pass and logs it
     in `agents/eng-manager/config/exceptions.md`. Release-window and machine-gate
     exceptions go to the approver — the EM cannot grant those, ever.
   - **Third exception of the same kind** → stop granting. File an intake card to
     change the process instead. Three of the same means the rule doesn't fit
     reality, not that the tickets are unusual.

8c. **Journal any answered gate** — an answered G1/G2/G3 or merge request gets an
   entry in `agents/eng-manager/config/decision-journal.md`, written by whoever
   raised it. Rejections and edits matter more than approvals: the approver's
   words verbatim where they gave any, and the interpretation labelled as
   interpretation.

   This is the only mechanism by which the department learns to read the
   approver rather than applying generic best practice. An item that timed
   out and got auto-anything never enters the journal — silence says nothing
   about what the approver wants.

9. **Chain** — before this pass exits, if the ticket it touched is in a state
   owned by an agent, fire the next hop:
   `lib/eng-trigger.sh continue {TICKET-ID}`, and write `chained:` into the
   ticket log. Do **not** chain when the ticket is waiting on the approver,
   blocked, terminal, or held by a cap — record `chained: none` and the reason
   instead.

10. **Board update** — `agents/eng-manager/board/_index.md`.

    **Keep three dated entries, no more.** Before you exit, if the file holds
    more than three `## {date} —` pass entries, move the oldest down to
    `agents/eng-manager/board/_index-archive.md` (newest first, under the header
    already there) and leave the pointer section in place. The live board is the
    In-flight table plus enough recent narrative to resume a ticket; everything
    older is history, and history belongs in a file nothing reads on a pass.

    This is not tidiness. Every pass reads this file in full, so an append-only
    log is a tax on every future pass. Rolling it here costs one edit by the
    pass that created the entry. `lib/eng-gate-check.sh` globs `ENG-*.md` and
    never reads either file. (What the unrolled file measured on 2026-08-12:
    `eng_build_loop-rationale.md` §"Board index rolling".)

    **Ticket logs are not rolled** — a ticket's own log is what the next hop
    reads to avoid re-deriving the last one, and on this board the rounds that
    re-derive are the expensive ones. Trim a ticket log only when the ticket
    reaches `verified`.

## Enforced vs instructed — which half of this document is which

Every rule here is one of two kinds. **Enforced** — a script computes it, a
non-zero exit follows, and a pass cannot talk its way past it: that is
`lib/eng-gate-check.sh` and its pre-pass and post-pass runs. **Instructed** —
prose a session is asked to follow, with nothing mechanical behind it. The
full list of what is enforced, why the distinction exists (ENG-001), what the
post-pass check actually buys and the one residual hole:
`eng_build_loop-rationale.md` §"Enforced vs instructed".

**Instructed** — held by this document alone, so hold them:

- Merge detection refusing `shipped` from a state that owes gates (step 5).
- **Where a ticket goes when it leaves `blocked`** (step 8). The field's
  *presence* is enforced; its *destination* is not, and `blocked_from` records
  where the ticket was rather than where it should go.
- The release step calling the check before writing `shipped`.

**Enforced, and stated at no step above:**

- **A parent ticket's sub-tickets are all settled** before the parent may sit at
  `shipped`/`verified` (ADR-003). A parent owes no receipts of its own — its
  evidence is its children's — but the exemption applies only when every child
  is `shipped`, `verified` or `dropped` and at least one actually shipped. A
  planted child *blocks* its parent rather than exempting it.

<!-- eng-host-reach: both -->

**Enforced on which host: both, since ENG-009.** If you are reading an older
note that says "enforced on the Mac only", it is stale.

Do not describe any of this as "structurally impossible", "blocking", or
"non-overridable". Those words are the reason the parent ticket was filed.

## The four lanes

| Lane | When | Path |
|---|---|---|
| **Full** | Default | `intake → shaped → [G1] → designed → [G2] → ready → building → in-review → in-qa → in-security → ready-to-ship → [G3] → shipped → verified` |
| **Fast** | XS bug/chore touching no sensitive surface | `intake → building → in-review → shipped → verified`, with one combined gate (review + suite + OWASP on the touched surface) |
| **Internal** | Any ticket on a project registered internal, any size | `intake → shaped → [G1] → building → in-review → shipped → verified`. Code review only. No QA gate, no security gate, no release readiness, no G3. |
| **Advisory (L0)** | Any ticket on an L0 project — a client-governed repo | `intake → shaped → designed → advised`. Terminal. Nothing built, branched, or scanned. |

A ticket can drop **out** of the fast lane into the full pipeline at any point.
It can never enter the fast lane late.

**The internal lane exists because this department was spending most of itself on
itself** (the approver, 2026-08-13 — the board state is in
`eng_build_loop-rationale.md` §"Self-generated tickets"). Every machine gate
here assumes software that ships to someone; a project registered internal
has no deploy target, no second committer and no user data, and its release
is a commit to `main`. Code review still runs and its receipt is still
enforced — `lib/*.sh` runs unattended on two hosts. The guard is `project:`, in
`lib/eng-gate-check.sh`, so a product ticket cannot relabel its way in.

**G1 still applies on this lane, and that is deliberate** — it is now the only
thing standing between a passing thought about the department and a ticket. See
step 3.

## The chain — why this isn't a cron job

`continue` is the event that makes this loop behave like a team rather than a
board checked twice a day. (The analogy, and the clock-driven chaining it
replaced: `eng_build_loop-rationale.md` §"Why the chain is event-driven".)

**A pass stops after `building` on purpose.** One Claude session that designs,
builds, reviews, tests *and* security-reviews runs out of context and does all
of it badly. So each heavy step gets its own session with fresh context.

The pass fires the next hop itself before it exits:

```
lib/eng-trigger.sh continue {TICKET-ID}
```

**It must not chain** when the ticket is waiting on the approver, blocked,
terminal (`verified`, `advised`, `dropped`), or held by a cap. Those waits are the
design. Chaining a ticket that is genuinely waiting just burns usage.

**One queue, oldest first, consumed only when a pass succeeds.** A fire that
reaches the lock — including one that acquires it immediately — appends its own
`<attempt> <event> <context>` line to `traces/.pending` and then drains the
**front**. So the event a fire arrives with is not necessarily the event it
runs: an older outstanding event goes first. Duplicate lines (the whole
`<event> <context>`, not just the event) collapse before each pop, keeping the
oldest copy — two `scheduled` sweeps are one sweep, and the older copy is the one
carrying the attempt count.

**Three fires never reach the lock:** a `watch` whose fingerprint is unchanged
exits above the lock by design — that is the 2026-07-28 de-noising, and it
skips before spending a hop; a ticket already over its hop budget has its
arriving event **dropped, and announced**; and the department over its daily
ceiling **queues** the arriving event without draining it. None of the three
appends-and-drains. Only the first leaves nothing behind, because subfolder
churn is nothing to leave. ("Every fire" was the wording here until
2026-08-13, and how ENG-005 caught it: `eng_build_loop-rationale.md` §"Queue
wording corrections".)

**A fourth suppression happens BELOW the lock, and the difference is not
pedantry.** A fire arriving inside an armed **back-off window** (ENG-016) takes
the lock like any other — queueing behind a live pass if there is one — appends
its own event, drains the oldest, finds the window armed, re-queues that event at
the **same** attempt and exits without launching. So it does append, it does
drain, and it does write the queue's ordinary `collapsed` / `draining queued
event` lines. What it does not do is start a session. Said as one sentence:
**the first three skip the queue, the fourth skips only the launch.** (Why it
is listed apart from the three above, and the 2026-08-17 correction that put
it here: `eng_build_loop-rationale.md` §"Queue wording corrections".)

The back-off window is armed by a pass that never started (below). It writes **no
line of its own** per fire: the line that arms it names the exact minute it ends,
and one line reports how many fires it ate when it clears. That is what AC3 asks
and it is all it asks — the drain lines above still print once per fire, which is
in fact the readable signature of this window in the log (drain lines repeating
with no `pass start` between them). Logging every suppression on top of that
would reproduce the noise the window exists to stop.

**That silence is bounded, and the bound is not optional.** Nothing else on the
never-started path escalates — no hop is charged, so the daily ceiling never
trips; no attempt is spent, so the two-attempt drop never fires. That is right
for a vendor limit, which clears on its own. It is wrong for a host condition
that does not: `claude not on PATH` is in the same signature list and never
clears. So when the back-off reaches its one-hour ceiling — the point at which
it has stopped growing and the loop has stopped treating the stall as
transient — **one** stall notice goes to `inbox/` and out via
`lib/eng-notify.sh`, latched so it is one per stall rather than one per fire.
Nothing is charged and nothing is dropped; the only thing added is that someone
is told. Removing this bound re-creates the failure ENG-005 exists to
end: a broken environment indistinguishable from a quiet night. (What the
unbounded version did — six fires, one log line, a frozen queue:
`eng_build_loop-rationale.md` §"Queue wording corrections".)

**Events *can* be dropped, and the rules below say exactly when.** ("Never
dropped" was the wording here until ENG-005, and what it cost — nineteen
events in eight days: `eng_build_loop-rationale.md` §"Queue wording
corrections".)

- A failed pass puts its event **back at the front** of the queue, one attempt
  older, and **ends that drain** — the retry waits for a later fire rather than
  relaunching in the same second. The failures actually observed (a monthly spend
  limit, a TCC/EPERM denial) do not clear in milliseconds, so spinning would burn
  both hop budgets to learn nothing.
- **A pass that never STARTED is a third outcome, not a failure** (ENG-016). When
  the account is at its ceiling the launch returns in seconds having done nothing,
  so there is no evidence about the event — only about the account. It refunds
  both hop counters, re-queues at the **same** attempt, spends no life, and arms
  the back-off. It is still bounded by the same two-attempt cap; it just does not
  consume one. (This is not a technicality — ENG-016's own build event was
  dropped this way on 2026-08-13: `eng_build_loop-rationale.md` §"Queue
  wording corrections".)

  **Classification needs three things at once** — the vendor's limit signature in
  the output, short output, and a short run (≤60s). Anything else, and any
  ambiguity, is treated as a real pass and charged. The duration condition is not
  redundant with the length one: a session killed at the ceiling *mid-flight*
  prints nothing regardless of how much work it did. Output length
  separates the prose case; only duration separates did-work from never-ran.
  (The 2026-08-15 pass that proved it: `eng_build_loop-rationale.md` §"Queue
  wording corrections".)
- **The next fire of any kind runs that retry**, because it drains the oldest
  event before its own. **The alarm must not depend on a later pass succeeding.**
  (The first fix left the retry reachable only *below* the failure break, and
  what that hid: `eng_build_loop-rationale.md` §"Queue wording corrections".)
- Retry is bounded at **two attempts**. The second failure drops the event.
- A queue line that does not parse into a legal event name is dropped, and so is
  a queued event whose ticket has spent its daily hop budget.
- **The department's daily hop ceiling does not drop anything.** An event already
  popped when the ceiling hits goes back on the queue at the same attempt — it
  was never launched, so it has not spent a life, and the day's counter clears at
  midnight where a ticket's does not.
- **Every drop raises an inbox item and a notification (`lib/eng-notify.sh`)** — one item per day, with
  each drop appended to it as it happens. The entire bug being fixed was that
  losing an event was silent, so a drop that goes quiet after two tries would be
  the same failure with a counter in front of it. One item rather than one per
  drop is deliberate: on a spend-limited day there are seven, and a muted channel
  loses the first one too.

**Runaway guard: two budgets, sized to the plan tier** (`agents/eng-manager/config.yaml`
→ `plan`). Per-ticket first, so one bouncing ticket is stopped on its own rather
than eating the department's whole allowance; then a daily ceiling. At either
limit the loop halts, writes a notice to `inbox/`, and notifies via
`lib/eng-notify.sh` — a stuck loop must never look like a quiet day.

These catch **bugs**, not healthy work. If the department is legitimately
hitting them, raise `plan.tier` rather than working around them: a guard that
fires on normal days teaches everyone to ignore it.

## Cadence, and where the time actually goes

The two scheduled passes are a **safety net**, not the engine. They exist for
what no local event can see: a PR merged on github.com, a machine that was
asleep, an event pass that died mid-run.

The cheapest speed
available is not failing: engineers get the standards and the security
baseline *before* writing, and first-pass rate is tracked
(`agents/eng-manager/config.yaml` → `speed`). Below 70%, the brief is the problem, not the
engineers.

What stays deliberately slow, and shouldn't change: every human stop is a real
stop, and the approver-facing WIP limit is 2.

(Where the time measurably goes on a full-lane ticket, and why more scheduled
passes is the weakest lever: `eng_build_loop-rationale.md` §"Cadence — where
the time actually goes".)

## Guards

- **Approver WIP limit (2)** — tickets whose path still runs through the
  approver, including a ticket `blocked` on `blocked_on: approver` (an L1 PR
  awaiting merge, a risk acceptance, a question only the approver can
  answer) — it holds its slot there too, not just while a gate is open
  (fixed 2026-07-27, after an L1 PR once freed a slot and sat invisible). At
  the limit, nothing new starts that will need them. There is no separate
  cap on how many decisions may be queued at once — one existed
  (`awaiting_approver_cap`), a life-os holdover removed 2026-08-29 at the
  approver's request; this WIP limit is the one lever on their side now.
- **Machine WIP limit (1)** — tickets moving purely between agents, counting
  states `ready` through `ready-to-ship`. **The approver's correction,
  2026-08-29.** At the
  limit, nothing new enters `ready` until the one ticket in flight reaches
  `shipped`. One ticket, completed end to end, then the next — not several,
  each a little bit done. (It used to scale with the plan tier, up to 12, and
  what that produced: `eng_build_loop-rationale.md` §"Machine WIP limit".)
- **Release window** — **L2/L3 only.** No production release Friday after
  15:00, weekends, during `sabbath`/`retreat`, or while `ENG_RELEASE_FREEZE`
  is set. The Friday 15:30 pass therefore never releases an L2/L3 ticket; it
  advances everything else and leaves the release for Monday. **Does not
  apply to L1** — opening a PR is not a release, and every project on this
  instance is registered L1 (`agents/eng-manager/config/projects.md`). The
  approver's correction, 2026-08-29, after an earlier pass held an L1 ticket
  over a weekend by mistake: *"you anyway don't ship anything, just raise a
  PR, so you do that on weekends too, doesn't matter — I can check them on
  weekdays or weekends, my choice."*
- **Repo isolation** — the loop never runs git operations in a directory the
  approver works in interactively. See `agents/eng-manager/config/projects.md`.
- **Interrupts** — P0 only. Everything else waits for `eng_weekly_report`.

## Notes

Built 2026-07-27 with the engineering department, and revised the same day
(`eng_build_loop-rationale.md` §"Origins").

**Wiring: `./lib/eng-setup.sh --apply`.** It installs and loads the scheduled
jobs, creates the department's git worktrees, and checks `inbox/requests/`
and the configured notify channel. Idempotent — re-run it any time.

**Every path into this loop goes through `lib/eng-trigger.sh`, never a bare
`$CLAUDE -p`.** The `ship_content` / `daily_brief` pattern calls the claude
binary straight; copying that here would run the scheduled passes **outside**
the single-flight lock (able to collide with a live event pass and race the
board index) and **outside** the hop budget (neither counted toward the runaway
guard nor stoppable by it). One script owns the lock and the counters. Caught in
review, 2026-07-27.
