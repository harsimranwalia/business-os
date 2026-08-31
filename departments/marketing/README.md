# Marketing department

Three agents that take a business from "we should be publishing something" to
published, measured content — without the business's approver writing a post.

Ported out of `life-os` on 2026-08-29 to become reusable across businesses,
the same way `departments/engineering` was on 2026-08-22. Where that port made
a decision — two roots, role vocabulary, MODE, the notify seam — this one
makes the same decision rather than a slightly better one. Two departments
with two sets of conventions cost more than either saves.

**Read `docs/marketing-team.md`** for the roster, the pipeline, the eight gates
and the channel autonomy model. That document is the department. This one only
explains how to run it for a business.

## The two roots

| | |
|---|---|
| `$MKT_DEPT` | `departments/marketing/` — the shared template. **Read-only at runtime.** |
| `$MKT_INSTANCE` | `instances/{business}/marketing/` — one business's state. The only thing ever written to. |

A pass that writes under `$MKT_DEPT` is a bug. Changing the template is a
deliberate commit against business-os, not something a run does.

Agent **definitions** are shared. Agent **memory** is per-instance. So is the
voice corpus, and that one matters more here than anywhere else: a business's
voice is the least transferable thing it owns, and a template that shipped one
would be actively harmful.

## Install

```sh
./install.sh <business> --approver <name>            # dry run, writes nothing
./install.sh <business> --approver <name> --apply    # create the instance
```

It creates the instance root, the content stage folders, an empty voice corpus
with a guide stub, and a topic bank seeded with the questions a first planning
run needs answered.

## Run

```sh
export MKT_DEPT=/path/to/departments/marketing
export MKT_INSTANCE=/path/to/instances/<business>/marketing
```

`MKT_INSTANCE` is never guessed. Guessing wrong means publishing one business's
content under another business's account, which is the failure the split exists
to prevent and the one nobody can take back.

## Roles

**The approver** — the single human with gate authority: M1 strategy, M2 the
piece, M3 channel autonomy. The five machine gates (brief completeness, voice,
format limits, cadence, asset readiness) stay machine-owned and blocking; only
the approver overrides one, explicitly and recorded.

**A filer** — may file a topic, holds no gate authority. Topics land in
`inbox/requests/` with `source: filer` and are drained by the CMO at planning.
A filer never approves a piece.

Bound per instance in `config/config.yaml`. No file in the template names a
person.

## What you must do before the first publish

The installer creates a working instance. It cannot create a business, and
four things are genuinely yours:

1. **`../knowledge/business-profile.md`** — what the business is, who it
   serves, what it sells. Shared with the engineering department; if that
   department is already installed for this business, it exists already.
2. **`voice/guide.md`** — the words to use, the words never to use, and the
   fingerprint. The stub asks the right questions.
3. **`voice/samples/{register}.md`** — real published material in the
   business's own voice, one file per register. This is the part people skip
   and it is the part that decides whether the drafts are usable. Ten per
   register is the floor; below it the department still drafts, it just leans
   harder on review and on your approval.
4. **`config/config.yaml` → `channels`** — which channels are live, at which
   autonomy tier, publishing by which method, with which credential env var.

An instance with none of these will still run. It will produce competent,
generic content that sounds like nobody, which is the specific failure this
department exists to avoid.

## Pause

`.env` → `MODE` set to `sabbath`, `retreat` or `quiet` halts every component.
Checked inside each component at start of run, never by the scheduler — cron
keeps firing and the run exits silently. Same convention the rest of
business-os uses.

`.env` → `MKT_PUBLISH_FREEZE` is different and narrower: planning, drafting,
review and approval all continue, and nothing publishes. Approved pieces queue
and drain oldest-first when it lifts. Use it when the approver is around enough
to work but not around enough to respond if something lands badly.

## Contract

`config/conventions.yaml` is the seam between the template and a business: the
two roots, the instance layout, the role vocabulary, the gates, the channel
autonomy tiers, the voice and proof seams, the publishing methods, and the
naming conventions. Read it before changing anything structural.

## Relationship to the engineering department

They share `instances/{business}/knowledge/business-profile.md` — one
description of the business, not two that drift.

They also share one directional seam. `departments/engineering/config/conventions.yaml`
declares `reports/proof/` with the note that it "rewires to a marketing
department if one exists". One now does: marketing **reads**
`../engineering/reports/proof/` and never writes to it. Engineering owns what
it built; marketing owns what gets said about it.
