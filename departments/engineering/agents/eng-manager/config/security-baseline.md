# Security Baseline

The standard the `security` agent enforces at the security gate. Department-wide,
non-negotiable, and not overridable by any other agent. Only the approver can
accept a risk, explicitly, in writing, as an ADR.

## Posture

**Nothing insecure reaches production.** The gate is binary: `pass` or `fail`.
There is no "pass with concerns" — a concern is either a finding that blocks, or
a note in the backlog, and the reviewer must decide which.

**Threat-model the change, not the codebase.** Every review asks the same four
questions about the diff: what new input can an attacker control, what new
capability does this grant, what new data does this expose, and what breaks if
this component is fully compromised.

## OWASP Top 10 — the review checklist

Every change is checked against the ten. Items that don't apply to the diff are
marked `n/a` with a reason, never skipped silently.

| # | Category | What the reviewer checks |
|---|---|---|
| A01 | Broken Access Control | Every new route/endpoint/action has an authz check. The *negative* case is tested — a user of the wrong tenant/role gets denied. No IDOR: object access is scoped by owner, not by ID alone. No client-side-only authorization. |
| A02 | Cryptographic Failures | TLS everywhere. Secrets and PII encrypted at rest per project classification. No home-rolled crypto. Passwords hashed with a modern KDF (bcrypt/argon2/scrypt), never MD5/SHA1. No sensitive data in URLs, logs, or analytics. |
| A03 | Injection | Parameterised queries only — never string-built SQL. No shell interpolation of user input. Output encoded for its sink (HTML/attribute/JS/URL). ORM escape hatches (`raw`, `literal`) reviewed line by line. **Prompt injection is injection** — see the LLM section. |
| A04 | Insecure Design | Does the feature have a rate limit, a quota, an abuse case? Can it be used to enumerate users, spam a third party, or exhaust a budget? Business-logic abuse (negative quantities, replayed webhooks, race on a balance) considered explicitly. |
| A05 | Security Misconfiguration | No debug mode, verbose errors, or stack traces in production. Default credentials removed. CORS not `*` on anything authenticated. Security headers present (CSP, HSTS, X-Content-Type-Options, Referrer-Policy). Cloud storage not public unless deliberately so. |
| A06 | Vulnerable Components | Every new or bumped dependency: known CVEs, maintenance status, licence, transitive weight. Lockfile committed. No dependency added without justification. |
| A07 | Identification & Auth Failures | Session tokens random, rotated on privilege change, invalidated on logout. Cookies `HttpOnly`, `Secure`, `SameSite`. Brute-force protection on auth endpoints. MFA path not weakened. No auth bypass in a "dev" branch of the code. |
| A08 | Software & Data Integrity | CI/CD inputs trusted. No fetching and executing remote code at runtime. Deserialization of untrusted data reviewed. Webhook signatures verified — always, no "we'll add it later". |
| A09 | Logging & Monitoring Failures | Security-relevant events logged (auth success/failure, authz denial, privilege change, data export). Logs contain no secrets, tokens, or PII. A failure on the new path is visible without a user reporting it. |
| A10 | Server-Side Request Forgery | Any server-side fetch of a user-supplied URL is allowlisted, resolves DNS safely, blocks internal ranges and metadata endpoints, and doesn't follow redirects blindly. |

## LLM and AI-specific

Applied to any change involving a model call, an agent, a tool, or an MCP server.

- **Prompt injection.** Untrusted content — user input, web pages, emails, PR
  comments, tool output, retrieved documents — is delimited and explicitly
  labelled as untrusted data in the prompt. Model output derived from untrusted
  input is never executed, never used as a command, and never trusted to name a
  file path, a URL, a recipient, or a permission.
- **Output validation.** Model output crossing into business logic is parsed
  against a schema. A model that returns nothing, malformed JSON, or hostile
  content has a defined, tested behaviour.
- **Tool authority.** A model-driven tool call can never exceed the authority of
  the user on whose behalf it runs. Destructive tools (delete, send, pay,
  deploy) require a confirmation path that a prompt injection cannot forge.
- **Secrets in context.** No API keys, tokens, or credentials in a prompt, a
  system message, or anything a model can echo back.
- **Data egress.** What leaves the boundary when a model call is made? PII in a
  prompt to a third-party model is a data-processing decision, not an
  implementation detail — it needs an ADR.
- **Cost as a security property.** An unbounded model loop is a denial-of-wallet
  vector. Token budgets, call caps, and a kill switch on every autonomous loop.

## Secrets

- Never in code, config committed to git, logs, error messages, test fixtures,
  or a model's context.
- Environment variables or a secret manager, referenced by name in
  `connections/` — never written there.
- Every review runs a secret scan over the diff *and* over the branch history.
  A secret found in history is a leak, not a mistake: it gets rotated, not
  just removed.
- A leaked credential is a P0 the moment it's found.

## SOC 2 — controls the team keeps intact

The business and its projects aren't a SOC 2-audited entity today, but client
work increasingly requires the posture, and retrofitting controls is
expensive. The team builds as if the audit is coming.

| Trust criterion | What the team maintains |
|---|---|
| **Security** (CC6) | Least-privilege access; every access path authenticated and authorised; changes reviewed before production; secrets managed, not embedded; dependencies patched. |
| **Availability** (A1) | Every production change has a rollback. Health checks and alerting on the deployed path. Backups exist and restore has been tested, not assumed. |
| **Processing Integrity** (PI1) | Input validation at boundaries; idempotency on money and message paths; a failed job fails visibly rather than silently dropping work. |
| **Confidentiality** (C1) | Data classified per project; PII encrypted at rest and in transit; access to production data logged; test data is synthetic, never a production dump. |
| **Privacy** (P1–P8) | Collect the minimum; delete on request means actually deleted, including backups policy; third-party processors documented in `connections/`. |
| **Change management** (CC8) | Every production change traceable to a ticket, a review, a test run, and a security verdict. This pipeline *is* the control — the artifacts are the evidence. |

The audit trail this department produces (ticket → PRD → design → review verdict
→ test run → security verdict → release record) is deliberately the shape a
SOC 2 change-management control wants. Don't shortcut it, because the evidence
is the point.

## Data classification

| Class | Examples | Rules |
|---|---|---|
| **Public** | Marketing copy, docs, public repos | No restriction |
| **Internal** | Architecture, metrics, non-client business data | No public exposure; not in a third-party model prompt without thought |
| **Confidential** | Client names, contracts, revenue, pipeline | Encrypted at rest; access logged; never in an external-facing output |
| **Restricted** | Credentials, PII, payment data, the approver's private/personal data | Never in logs, prompts, test fixtures, or any external output. The instance's `CLAUDE.md` already forbids the personal category externally — this extends it to code and telemetry. |

## Client-repo boundary

For any project at autonomy **L0** — a client-governed repo — the security
agent **does not**: run scanners against client infrastructure, probe
endpoints, test credentials, enumerate resources, or open findings in the
client's tracker. It reads code, reviews the approver's diffs, and writes
findings to the approver. Unauthorised scanning of a third party's estate is
an incident regardless of intent.

## When the gate fails

1. Write the finding to the **ticket log** and
   `agents/security/notebook/{date}-findings.md` — category, severity, exact
   location, exploit path, and the specific fix. **Write no receipt file.**
   `agents/security/reviews/{ENG-NNN}.md` is written on a **`pass` verdict
   only** — never on a fail, and never on a risk-acceptance escalation, which is
   not a pass either.

   The reason, so this is not quietly reversed: the check that reads that file
   (`lib/eng-gate-check.sh`) tests only that it exists and is non-empty. It
   cannot read the verdict inside. A receipt written on a fail therefore
   satisfies the exact check it exists to prove, and a ticket could reach
   `shipped` holding a security receipt whose body says the gate failed. This
   step told you to write on a fail until 2026-08-12; ENG-007's review round 2
   caught the conflict with `skills/security-gate/SKILL.md`, which had already
   been fixed.
2. Return the ticket to the owning engineer at state `building`.
3. Never propose a workaround that reduces the finding's severity without
   removing it.
4. If the same finding class appears three times, it stops being a finding and
   becomes a standard: propose an addition to `engineering-standards.md`.

## Escalation to the approver

Only two things reach the approver directly:
- An active security incident (leaked credential, live exploit, exposed data) — P0.
- A risk-acceptance decision: the fix is disproportionate and the team wants
  permission to ship with the risk. Presented as: finding, exploit path, blast
  radius, cost to fix, cost to accept. The approver's answer is recorded as an ADR.

Everything else is fixed, not escalated.
