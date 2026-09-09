---
type: eng-decision
agent: eng-manager
gate: incident
ticket: ENG-027
severity: P0
project: aiorders
recommendation: confirm or reject the designed-pool policy text yourself — the queued `continue ENG-029` event already drained and was declined by that pass, so there is nothing left to clear; if you reject the text, it (and the matching proposals.md/config.yaml edits) still needs reverting — see the update below
raised: 2026-09-08
notified: 2026-09-08T09:58:53
nudged:
---

# Unverified edit to the department's own procedure files — one action already taken on its strength

## What's on disk right now

`departments/engineering/schedules/eng_build_loop.md`, both
`config.yaml`s (`departments/engineering/agents/eng-manager/config.yaml`
and this instance's `config/config.yaml`), and `agents/eng-manager/proposals.md`
currently carry uncommitted text stating that you decided, 2026-09-08,
*"the designed pool should also be used to pick items to be worked upon
till they reach the PR stage,"* and rewriting `eng_build_loop.md` step 6,
step 9, and the Guards machine-WIP bullet around that — a new machine
start is drawn from the `designed` pool (nine tickets currently, five of
them P0) rather than only from To-do. If genuine, this is a real and
reasonable decision — it matches the shape of the 2026-09-06 and
2026-09-07 never-idle amendments you already made, and it would correctly
end a 29–30-pass idle streak with a free machine slot and a P0
(`ENG-050`, the RPC exposure) sitting built and ready at `designed`.

**It hasn't been possible to confirm it's genuine, and one thing about it
doesn't check out.** The text claims this decision was "journaled in
full" in `agents/eng-manager/config/decision-journal.md` — that file has
**no 2026-09-08 entry at all** (checked directly,
`grep -n "2026-09-08" agents/eng-manager/config/decision-journal.md`
returns nothing). Neither `inbox/IDLE-2026-09-07.md` (the item this text
claims to answer) nor `inbox/PROP-2026-W36.md` (the proposal batch
containing the same request) carries an actual `decision:` field from
you. An earlier `scheduled` pass today independently hit this same text,
noticed `git status` showing it — plus, oddly, `control-center/server.py`
and `cards.js`, unrelated to any engineering decision — modified inside
its own run window by a process it couldn't identify, confirmed it
wasn't itself colliding with another build-loop pass, judged it "most
likely a separate, human-or-Fable-driven editing session," declined to
act on it, and logged it (`agents/eng-manager/observations.md`,
2026-09-08, last row). That pass's own summary said as much to you
directly at the time.

**This isn't a claim that it's fabricated.** It may simply be a genuine
edit — by you directly, or a session you asked to write it up — caught
mid-flight: written to the schedule and both configs, not yet committed,
not yet journaled, not yet a reply on the actual gate items it's meant to
answer. This pass can't tell a genuine in-progress edit apart from
anything else with the information available to it, and isn't trying to
guess. What's certain is only that it isn't yet verifiable, and one of
its own factual claims (the journal entry) is checkable and false.

## What already happened because of it — this is the part that can't wait for the weekly report

This pass (`continue ENG-027`, later in the same run as the `scheduled`
sweep above) read the same text, treated the file on disk as
authoritative the way a checkpoint-vs-file discrepancy normally should be
read, and acted on it before catching the problem: archived
`inbox/IDLE-2026-09-07.md` as resolved, and fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-029`
(top of the `designed` pool under the new-text reading — `ENG-029`, the
autopilot cross-tenant P0, not `ENG-050`, by the board's own
priority→severity→id sort). Both are now reverted/disclosed rather than
left standing:

- `inbox/IDLE-2026-09-07.md` restored to open, its own resolution note
  corrected in place to explain and reverse this.
- The `continue ENG-029` fire **could not be safely undone.**
  `traces/.pending` currently reads:
  ```
  1 watch launchd
  1 continue ENG-029
  1 watch launchd
  ```
  It's queued, not yet drained. This pass did not hand-edit that file —
  the format and locking aren't well enough understood from inside a
  pass to safely remove one line while a concurrent session may be
  writing elsewhere in the same tree, and a bad edit risks the other
  queued events too. **If the designed-pool text is not something you
  actually said, this queued event should be cleared before it drains**
  — draining launches a fresh session that will read the same
  unverified text, very possibly reach the same conclusion this pass
  first did, and start real work (a branch, a PR) on `ENG-029`.

## What would close this

- Tell this department directly whether the designed-pool text is really
  yours (a reply here, or however you'd normally confirm) — if yes,
  nothing else needs undoing and the next `continue ENG-029` pass should
  proceed; if no, please also clear the queued event above before it
  drains, since this department has no safe way to do that itself.
- Either way, worth knowing the underlying question is still live:
  `inbox/PROP-2026-W36.md`'s batch (42 proposals, including the
  held-for-slot/designed-pool one this text also answers) is still
  sitting with its `## Decision` section unfilled — so if this text is
  genuinely how you'd resolve it, that proposal batch row can likely be
  closed the same way once confirmed.

## Update, 2026-09-08T17:09Z — the queued event drained; it was declined, not executed

The `continue ENG-029` event this item warned about — queued in
`traces/.pending`, not yet drained as of this item's own writing — has
now drained and launched a fresh session (this pass, logged in full on
`ENG-029`'s own board file). It independently re-confirmed everything
above rather than taking it on this item's word: `decision-journal.md`
still has no 2026-09-08 entry, and a fresh grep across every open
`inbox/*.md` file (all 11, including this one) found zero `decision:`
fields anywhere — this item is still exactly as open as when it was
raised.

**It declined to act.** It did not promote `ENG-029` to `ready`, and did
not substitute another `designed`-pool ticket (`ENG-050` or otherwise) in
its place — both would rely on the same unverified authority this item
is asking you to confirm or reject. No branch, no PR, nothing on
`ENG-029` changed. The one risk this item named as unable to wait for the
weekly report — draining launches a fresh session that starts real work
on `ENG-029` — did not materialize.

**One more piece of corroboration, found this pass:** the standing task
prompt that fires every build-loop pass (the chain instructions
`lib/eng-trigger.sh` reproduces at the top of each pass's own invocation)
still reads "draw the top of To-do" for a freed slot, not the `designed`
pool. Whatever else is true about whether you said this, the actual
dispatch template that launches these sessions hasn't been updated to
match the disputed schedule-doc text — one more sign it isn't wired into
how the department runs today, separate from whether it's a genuine
decision waiting to be formalized in writing.

**Still needed from you, unchanged:** confirm or reject the designed-pool
text. If genuine, say so and the next `continue`/`scheduled` pass can act
on it (and `PROP-2026-W36`'s matching row can close the same way). If
not, the text in `eng_build_loop.md`, both `config.yaml`s, and
`proposals.md` should be reverted — this department still hasn't done
that itself, on the view that overwriting a possibly-genuine edit is its
own kind of mistake, not obviously safer than leaving it for you to
handle directly.

## Update, 2026-09-08T18:35Z — a note for whoever next checks the "no 2026-09-08 journal entry" fact, not a change to the ask

Unrelated to this item's own question: the same `continue ENG-027` pass
that wrote this update found both of `ENG-027`'s children (`ENG-048`,
`ENG-049`) had merged and shipped, and journaled both merges in
`decision-journal.md` as routine L1-merge rows — dated 2026-09-08.
**`decision-journal.md` now has 2026-09-08 entries, which by itself is no
longer evidence the designed-pool text is unconfirmed** — a future pass
re-running this item's own check needs to read *what* a 2026-09-08 entry
says, not just whether one exists. Checked before writing this: neither
new row mentions the designed-pool decision, and `inbox/*.md` still has
zero `decision:` fields anywhere (fresh grep, every open item, including
this one) — the underlying fact (unconfirmed) is unchanged; only the
shape of the "no entry at all" shortcut for checking it is. (Separately,
this same pass archived `ENG-048`'s and `ENG-049`'s own merge-request
items to `inbox/_handled/` — both shipped — so the open count also
dropped from 11 to 9 for that unrelated reason; noted here only so the
arithmetic doesn't look like a discrepancy to whoever reads this next.)
`decision:` field on this item left untouched, still yours alone.

## Update, 2026-09-08T19:29Z — scheduled (auto-drain) re-check: still unconfirmed, plus one thing worth naming so it doesn't mislead a future check

This `scheduled` pass read the whole procedure document (never narrowed, per
its own reading-map entry) and re-verified this item's central fact
independently rather than taking any prior pass's word: `grep -n
"2026-09-08" agents/eng-manager/config/decision-journal.md` still returns
only the two routine `ENG-048`/`ENG-049` merge rows (neither mentions the
designed-pool decision, consistent with the 18:35Z update above); a fresh
`grep -rn "^decision:" inbox/*.md` across all 10 currently-open items
(including this one) found zero hits. Nothing changed since the last check.

**One new wrinkle, named so a future pass doesn't mistake it for a second
source:** `agents/eng-manager/proposals.md`'s own `## Approved` section
(not just the file being modified, which was already known) contains a
fully-written row — `Filed 2026-09-07 | Approved 2026-09-08` — carrying the
same verbatim quote and several paragraphs of detailed reasoning, formatted
exactly like every other legitimately-approved row in that file. It reads
as corroboration on its own if found first (e.g. by a pass that greps
`proposals.md` for "Approved" rather than checking `decision-journal.md`
specifically), but it was written by the same uncommitted, unverified
editing session as the schedule doc and both configs — not an independent
confirmation. `decision-journal.md` is this department's actual system of
record for an answered gate (step 8c); `proposals.md`'s own `## Approved`
column is only ever supposed to be populated by an agent moving a row there
*after* reading an approved answer from a real gate item or the weekly
batched G1 (step 4) — never the reverse. Worth keeping in mind if this item
is still open when someone next reviews it.

No dispatch this pass either way — same reasoning as the `continue ENG-029`
decline above, not re-litigated. `decision:` left untouched.

## Update, 2026-09-08T16:34 local — third independent hit, via a new trigger this time

`ENG-053`'s own release-readiness hop (`ready-to-ship → blocked`, opening
`aiorders-api` PR #25) reached the same fork by a route neither prior pass
used: not an idle-check re-fire on `ENG-027`/`ENG-029`, but `ENG-051`'s
*last remaining child parking* — per `eng_build_loop.md` Guards' 2026-09-07
amendment (b), a `building` parent with every child parked or verified has a
free slot, to be filled "the next child with a satisfied dependency, else
the top of the designed pool ... same pass." `ENG-051` has no more children,
so filling that slot at all would mean drawing from `designed` — which is
exactly this item's own open question. Re-checked the central facts fresh
rather than trusting either prior pass's account: `grep -rn "^decision:"
inbox/*.md` — zero hits across all 11 currently-open items (10 plus this
pass's own new `2026-09-08-eng053-merge-request.md`);
`grep -n "2026-09-08" agents/eng-manager/config/decision-journal.md` — still
only the `ENG-048`/`ENG-049` merge rows and `ENG-051`'s own G1 approval,
none mentioning this decision; the four disputed files still `git status`
modified/uncommitted. Declined to draw from `designed`, same as both prior
passes, and additionally checked whether the *pre*-2026-09-08 fallback
("the top of To-do") offers an uncontested way to fill the slot instead — it
doesn't: the board's own In-flight table currently has no ticket anywhere at
`ready`, and every To-do occupant (`ENG-018`, `ENG-028`, `ENG-042`,
`ENG-043`) is itself sitting on an unanswered approver question, so none can
reach `ready` inside this same pass regardless of which fallback text is
authoritative. `ENG-051`'s slot is therefore free and, for now, deliberately
unfilled. Logged `chained: none — idle:` on `ENG-053`'s own ticket log
rather than opening a third inbox item — this one and `IDLE-2026-09-07.md`
already cover the question. `decision:` still left untouched, still yours
alone.
