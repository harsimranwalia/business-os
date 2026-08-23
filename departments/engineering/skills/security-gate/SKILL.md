# Skill: security-gate

**Owner:** security
**Model:** opus (threat reasoning over a whole change)
**Trigger:** a ticket enters state `in-security`; also the Sunday sweep
**Suppressed when:** sabbath, retreat — except an active incident, always P0

---

## Purpose

The production veto. Binary verdict, OWASP plus LLM coverage, and findings
specific enough that the engineer knows exactly what to change.

---

## Inputs

- `agents/eng-manager/config/security-baseline.md` — the standard (required)
- `agents/architect/designs/{ENG-NNN}-{slug}.md` — the trust boundaries
- The full diff, and the branch history for secrets
- `agents/qa/test-plans/{ENG-NNN}.md` — are the negative authz cases tested?
- `agents/eng-manager/config/projects.md` — autonomy level and client boundaries
- `agents/security/notebook/` — where findings cluster on this project

---

## Steps

### 1. Mode and boundary check

`sabbath` or `retreat`: exit, unless this is an active incident. Then check the
project's autonomy level. **For an L0 project (`<project>`): no scanning, no
probing, no credential testing, no enumeration.** Read the code, write findings
to the approver, stop. Unauthorised scanning of a third party's estate is an
incident regardless of intent.

### 2. Threat-model the change

Four questions about this diff, answered before the checklist:

1. What new input can an attacker control?
2. What new capability does this grant, and to whom?
3. What new data does this expose, and to whom?
4. What breaks if this component is fully compromised?

The checklist without this step is theatre.

### 3. Walk OWASP A01–A10

Per the baseline's table. Every category is marked applicable or `n/a` **with a
reason** — silence is indistinguishable from an oversight three months later.

The two that catch the most in practice:
- **A01 Broken Access Control** — every new route has an authz check, object
  access scoped by owner rather than ID alone, no client-side-only authorization
- **A03 Injection** — parameterised queries, no shell interpolation, output
  encoded for its sink, ORM raw escape hatches read line by line

### 4. Walk the LLM checklist — when the change touches a model, agent, tool, MCP, or RAG

- **Prompt injection:** is untrusted content delimited and labelled as data?
  Untrusted means user text, web pages, emails, PR comments, tool output,
  retrieved documents, file contents.
- **Trust boundary:** does model output become a command, path, URL, recipient,
  query, or permission decision without validation? That's a finding.
- **Tool authority:** can a model-driven action exceed the authority of the user
  it runs for? Do destructive tools have a confirmation path injection cannot
  forge?
- **Data egress:** what leaves the boundary in a prompt, and was that a decision
  someone consciously made? PII to a third-party model needs an ADR.
- **Denial of wallet:** token budget, call cap, kill switch — verified present,
  not assumed.

### 5. Scan

- **Secrets:** the diff *and* the branch history. A secret in history is a leak —
  rotate, don't just remove. **A leaked credential is a P0 the moment it's found.**
- **Dependencies:** every new or bumped one — known CVEs, maintenance status,
  licence compatibility, transitive weight. Regardless of ticket size.
- **Config:** debug mode, verbose errors, permissive CORS, missing security
  headers, public storage.

### 6. Check the negative cases in the tests

An authz test that only proves the authorised user gets in proves nothing. If
wrong-tenant, wrong-role, and no-token aren't tested, that's a finding — filed
against this ticket, not deferred to QA's backlog.

### 7. Check the SOC 2 evidence trail

Ticket → PRD → design → review verdict → test run → this verdict → release
record. Complete? The artifacts *are* the change-management control; an
incomplete trail is a control gap, not a paperwork issue.

### 8. Decide the verdict

Every finding: **category, severity, exact location, exploit path, specific
fix.** Decide blocking or backlog before you write anything — there is no "pass
with concerns."

Never propose a workaround that lowers a finding's severity without removing it.

**Nothing is written to `agents/security/reviews/` at this step.** The verdict
decides where it goes, and that is step 9.

### 9. Route — and on `pass`, and only on `pass`, write the receipt

- **pass** → write `agents/security/reviews/{ENG-NNN}.md` with the verdict, the
  OWASP walk, every finding and its disposition, and what was scanned; set
  `links.security_review` on the ticket to that path in the same write. Then
  state `ready-to-ship`, owner `devops`.
- **fail** → state `building`, owner the implementing engineer, with the fix
  specified, **and no receipt file.** The verdict goes in the ticket log and
  `agents/security/notebook/{date}-findings.md`, which is where it already goes.
- **risk acceptance wanted** → state `blocked`, owner `eng-manager`, and record
  `blocked_from: in-security` in the same write. Escalate through the EM as:
  finding, exploit path, blast radius, cost to fix, cost to accept. The
  approver decides; their answer is recorded as an ADR, never as a passing
  verdict. **No receipt** — an accepted risk is an ADR plus a later `pass`, not
  a gate that cleared.

**Why the write moved out of step 8.** `lib/eng-gate-check.sh` tests that the
receipt file exists and is non-empty; it cannot read the verdict inside. A gate
that writes its receipt on the way through regardless of outcome satisfies the
exact check it exists to prove, and a ticket could reach `shipped` holding three
receipts that all say "failed" — which is ENG-004's bug arriving back through the
fix for it. This gate wrote in step 8 and routed in step 9 until 2026-08-11, so a
failed security gate left a receipt behind; ENG-007's review round 1 caught it.

### 10. Three-strike check

Third occurrence of a finding class → **propose** it to the principal engineer,
who owns `engineering-standards.md` and makes the edit. You don't write that file
— two agents editing it from two independent three-strike rules is a
concurrent-write risk with no conflict handling. Once it's a standard, code
review catches it earlier and cheaper than this gate does. Fewer findings over
time is the goal.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/security/reviews/{ENG-NNN}.md` | **The receipt — written on a `pass` verdict ONLY, never on a fail and never on a risk-acceptance escalation.** The check that reads it (`lib/eng-gate-check.sh`) tests that the file exists and is non-empty; it cannot read the verdict inside. So a receipt written on a fail satisfies the exact check it is meant to prove. Carries the verdict, the OWASP walk, every finding and its disposition, and what was scanned. Set `links.security_review` on the ticket in the same write. |
| ticket log | One line: verdict. On a fail this and the notebook are the whole record — there is no receipt. |
| `agents/security/notebook/{date}-findings.md` | Category and project patterns |
| `agents/principal-engineer/notebook/` | Standards proposal on a third occurrence |

---

## Trace

`traces/security-{run-id}.json` — ticket, verdict, findings by category and
severity, OWASP categories marked n/a, dependencies reviewed.

---

## Failure modes to avoid

- **Passing because a release is waiting.** The release waits.
- **"Pass with concerns."**
- **Accepting risk yourself.** Only the approver accepts risk, in writing, as an ADR.
- **Skipping a category silently** instead of marking it `n/a` with a reason.
- **Security theatre** — findings that impress rather than protect.
- **Touching a client estate.** L0 is absolute.
