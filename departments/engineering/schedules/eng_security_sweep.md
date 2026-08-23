# Schedule: eng_security_sweep

**Status:** 📋 DESIGNED — not yet cron-wired

**Description:** Weekly security sweep across every registered project — dependency CVEs, secret scan, control drift, aged findings.

**Agent:** `agents/security/agent.md`

**Schedule (human):** weekly on sunday at 07:00

**Cron expression:** `0 7 * * 0`

**Suppressed on sabbath/retreat/quiet:** yes — except an active incident, which is always P0

---

## What it does

For every project in `agents/eng-manager/config/projects.md`, respecting each
one's autonomy level:

1. **Dependency CVEs** — new advisories against pinned versions since the last
   sweep. Severity from the advisory, not from the reviewer's mood.
2. **Secret scan** — across tracked files and recent history. A hit is a P0 the
   moment it's found: rotate first, then remove from history.
3. **Control drift** — the SOC 2 controls in `security-baseline.md`. Is the
   evidence trail still complete on recent releases? Have any debug flags,
   permissive CORS rules, or public buckets appeared?
4. **Aged findings** — anything past its severity SLA gets escalated into the
   weekly report.

Findings become tickets automatically, filed to `agents/eng-manager/inbox/`.
**The approver is not involved** — the sweep produces work for the team, not
decisions for them.

## Client boundary — absolute

Every **L0** project (e.g. `<project>`) is read-only for this sweep: it reads
the code and nothing else — **no scanning, no probing, no credential testing,
no enumeration, no infrastructure access.** Unauthorised scanning of a
client's estate is an incident regardless of intent. Findings there go to the
approver as advice, never into a client tracker.

## Why Sunday morning

Ahead of the Sunday evening reporting cadence, so anything found lands in that
week's engineering report rather than waiting seven days. Early enough that a P0
has a full day of runway; quiet enough that it never competes with the
approver's weekend.

## Notes

Built 2026-07-27 with the engineering department. Not yet cron-wired.

If a sweep produces the same finding class three times, that's the promotion
trigger: the finding becomes a standard in `engineering-standards.md` and the
principal engineer catches it at code review instead — earlier and cheaper. The
sweep should produce fewer findings over time; a flat or rising count means the
promotion mechanism isn't being used.
