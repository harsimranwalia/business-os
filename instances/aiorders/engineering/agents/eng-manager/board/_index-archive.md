# Engineering Board — pass log archive

Dated pass entries moved out of `_index.md` once the live board holds more than
three, newest first. The live board keeps its table plus enough recent narrative
to resume a ticket; everything older lives here.

Nothing reads this file on a pass — it is the department's history, not its
state. `lib/eng-gate-check.sh` globs `ENG-*.md` and never sees it.

This exists because every pass reads `_index.md` in full, so an append-only log
there is a tax on every future pass.

---

## 2026-08-24 — decision: gate-check-unavailable resolved

Acted on the answered incident gate `2026-08-24-eng-gate-check-unavailable.md`
(`gate: incident`, tied to ENG-001 because it was the ticket in flight when the
pre-pass check found `lib/eng-gate-check.sh` unreadable). Its `project: life-os`
was stale — a leftover of the pre-carve-out hardcoding bug fixed in business-os
`ed8dd56`/`58ae148`/`9366b84`; `ticket: ENG-001` was correct. Approver had
already recorded `decision: approved`. Independently re-ran
`lib/eng-gate-check.sh` against this instance this pass: exit 0, clean — ENG-001
AC3 satisfied. Logged on ENG-001, moved the gate item to `inbox/_handled/`.
Did not shape ENG-001 further — a decision pass is scoped to the gate it
answers, not PM intake work — so `chained: ENG-001` to hand the ticket to a
fresh `continue` pass.
