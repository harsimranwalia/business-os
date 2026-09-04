#!/usr/bin/env python3
"""SMS — a marketing channel with two halves, and they are not symmetric.

CAMPAIGNS are bulk sends the operator writes: pick a segment, write the copy,
approve it, send it. They keep the constitution's human gate — a campaign
cannot leave `draft` without someone clicking Approve, and only an approved
campaign can be sent.

SMART REACTIVATION takes no copy and no segment. It reads the lapsed end of
the customer database, runs a headless Claude pass on the partner's own OAuth
token to decide who is worth reaching and what to say to each of them, and
sends. Approved by Harry (2026-09-03) as the one auto-send path in the system:
the whole point is that it is hands-off. The guardrails that replace the human
gate are all in run_reactivation() — quiet mode, a per-run recipient cap, and a
30-day per-customer cooldown read out of the previous runs' records.

WHERE THE CUSTOMERS COME FROM is the partner's own config (see accounts.py):

  crm       Twenty, over the GraphQL API this repo already talks to. Twenty
            carries no order history, so the only honest segments here are
            "everyone" and two based on record dates.
  aiorders  The AIOrders Postgres/Supabase database, direct, scoped to the
            partner's brand id. Needs psycopg — the only non-stdlib import
            anywhere in the control center, imported lazily so a partner on
            the CRM source never pays for it.

THE ASSUMED AIORDERS SCHEMA is named once, in SEGMENT_SQL below. If the real
columns differ, that dict is the single place to correct it and the error a
mismatch produces is shown verbatim in the UI rather than swallowed.

STATE lives with the business, not with this server:
  instances/<id>/marketing/sms/campaigns/<id>.json
  instances/<id>/marketing/sms/reactivation/<id>.json
"""

import base64
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INSTANCES_DIR = ROOT / "instances"
RUN_CLAUDE = ROOT / "departments" / "engineering" / "lib" / "run-claude.sh"

# Reactivation guardrails. These exist because this is the one path that
# reaches a real person's phone with no human in front of it.
REACTIVATION_MAX_RECIPIENTS = 50
REACTIVATION_COOLDOWN_DAYS = 30
REACTIVATION_LAPSED_DAYS = 60
CLAUDE_TIMEOUT_SECONDS = 300

SMS_TIMEOUT_SECONDS = 20
MAX_SMS_CHARS = 320   # two GSM segments; longer is a billing surprise


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slug(text, fallback="campaign"):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (s or fallback)[:48]


def quiet_mode():
    """The constitution's global pause switch. Every component checks it
    itself rather than trusting the scheduler; this is SMS's copy."""
    return (os.environ.get("MODE") or "").strip().lower() in ("sabbath", "retreat", "quiet")


# ── Customer sources ─────────────────────────────────────────────────────────

# Segment id -> (label, why). The two sources expose different segments on
# purpose: inventing a "lapsed 90 days" for a database with no order history
# would be a number that looks real and is not.
CRM_SEGMENTS = [
    {"id": "all", "label": "Everyone", "note": "every CRM person with a phone number"},
    {"id": "new_30d", "label": "Added in the last 30 days",
     "note": "createdAt within 30 days"},
    {"id": "quiet_90d", "label": "No CRM activity in 90 days",
     "note": "updatedAt older than 90 days — a record-touch proxy, not an order signal"},
]

AIORDERS_SEGMENTS = [
    {"id": "all", "label": "Everyone", "note": "every customer of this brand with a phone"},
    {"id": "new_30d", "label": "New in the last 30 days", "note": "created in the last 30 days"},
    {"id": "active_30d", "label": "Ordered in the last 30 days", "note": "last order within 30 days"},
    {"id": "lapsed_60d", "label": "Lapsed 60+ days", "note": "last order 60–90 days ago"},
    {"id": "lapsed_90d", "label": "Lapsed 90+ days", "note": "last order over 90 days ago"},
]

# THE ASSUMED SCHEMA, in one place. `customers` scoped by `brand_id`, with a
# `phone`, a `created_at` and a `last_order_at`. Correct these four statements
# if the real table differs; nothing else in this file names a column.
SEGMENT_SQL = {
    "all": """
        SELECT id::text, COALESCE(name,'') AS name, phone, last_order_at
        FROM customers
        WHERE brand_id = %(brand_id)s AND phone IS NOT NULL AND phone <> ''
    """,
    "new_30d": """
        SELECT id::text, COALESCE(name,'') AS name, phone, last_order_at
        FROM customers
        WHERE brand_id = %(brand_id)s AND phone IS NOT NULL AND phone <> ''
          AND created_at >= now() - interval '30 days'
    """,
    "active_30d": """
        SELECT id::text, COALESCE(name,'') AS name, phone, last_order_at
        FROM customers
        WHERE brand_id = %(brand_id)s AND phone IS NOT NULL AND phone <> ''
          AND last_order_at >= now() - interval '30 days'
    """,
    "lapsed_60d": """
        SELECT id::text, COALESCE(name,'') AS name, phone, last_order_at
        FROM customers
        WHERE brand_id = %(brand_id)s AND phone IS NOT NULL AND phone <> ''
          AND last_order_at < now() - interval '60 days'
          AND last_order_at >= now() - interval '90 days'
    """,
    "lapsed_90d": """
        SELECT id::text, COALESCE(name,'') AS name, phone, last_order_at
        FROM customers
        WHERE brand_id = %(brand_id)s AND phone IS NOT NULL AND phone <> ''
          AND last_order_at < now() - interval '90 days'
    """,
}


def segments_for(cfg):
    src = (cfg or {}).get("customer_source") or ""
    if src == "crm":
        return CRM_SEGMENTS
    if src == "aiorders":
        return AIORDERS_SEGMENTS
    return []


def _twenty_people(cfg, limit=500):
    """Twenty's people, straight over GraphQL. A trimmed copy of server.py's
    _twenty_gql rather than an import of it — server.py imports this module,
    and a cycle to save nine lines is a bad trade.

    Connection comes from the partner's own Config-page fields first — a
    partner can point at their own Twenty workspace — and falls back to the
    repo-wide .env pair other, non-SMS CRM reads already use."""
    base = ((cfg or {}).get("crm_url") or os.environ.get("TWENTY_BASE_URL") or "").rstrip("/")
    key = (cfg or {}).get("crm_api_key") or os.environ.get("TWENTY_API_KEY") or ""
    if not base or not key:
        raise RuntimeError("Twenty URL / API key are not set — add them in Config")
    query = """query($l: Int) {
      people(first: $l, orderBy: {createdAt: DescNullsLast}) {
        edges { node { id name { firstName lastName } phones { primaryPhoneNumber
                primaryPhoneCallingCode } createdAt updatedAt } }
      } }"""
    req = urllib.request.Request(
        f"{base}/graphql",
        data=json.dumps({"query": query, "variables": {"l": limit}}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.loads(r.read().decode())
    if payload.get("errors"):
        raise RuntimeError(payload["errors"][0].get("message", "Twenty error"))
    return [e["node"] for e in payload["data"]["people"]["edges"]]


def _crm_customers(cfg, segment):
    now = datetime.now(timezone.utc)
    out = []
    for p in _twenty_people(cfg):
        phones = p.get("phones") or {}
        number = (phones.get("primaryPhoneNumber") or "").strip()
        if not number:
            continue
        code = (phones.get("primaryPhoneCallingCode") or "").strip()
        name = " ".join(x for x in [(p.get("name") or {}).get("firstName"),
                                    (p.get("name") or {}).get("lastName")] if x).strip()

        def age(field):
            raw = (p.get(field) or "").replace("Z", "+00:00")
            try:
                return (now - datetime.fromisoformat(raw)).days
            except ValueError:
                return None

        if segment == "new_30d" and (age("createdAt") is None or age("createdAt") > 30):
            continue
        if segment == "quiet_90d" and (age("updatedAt") is None or age("updatedAt") < 90):
            continue
        out.append({"id": p["id"], "name": name,
                    "phone": (code + number) if code and not number.startswith("+") else number,
                    "last_order_at": None,
                    "days_since_order": age("updatedAt")})
    return out


def _aiorders_customers(cfg, segment):
    try:
        import psycopg
    except ImportError:
        raise RuntimeError(
            "the AIOrders source needs the psycopg driver — `pip install \"psycopg[binary]\"` "
            "on the machine running the control center")
    sql = SEGMENT_SQL.get(segment)
    if not sql:
        raise RuntimeError(f"unknown segment '{segment}'")
    now = datetime.now(timezone.utc)
    rows = []
    with psycopg.connect(cfg["pg_dsn"], connect_timeout=15) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"brand_id": cfg["brand_id"]})
            for cid, name, phone, last_order in cur.fetchall():
                days = None
                if last_order:
                    if last_order.tzinfo is None:
                        last_order = last_order.replace(tzinfo=timezone.utc)
                    days = (now - last_order).days
                rows.append({"id": cid, "name": name or "", "phone": phone,
                             "last_order_at": last_order.isoformat() if last_order else None,
                             "days_since_order": days})
    return rows


def test_db_connection(cfg):
    """A one-off connect-and-ping, triggered by a human clicking Test — proof
    the saved DSN actually reaches a database, not a query for customer data.
    Returns (result, error): result is {"ok", "detail"} on any answer from
    the attempt itself; error is only set for something that means we never
    got to try (no DSN, driver missing)."""
    dsn = (cfg.get("pg_dsn") or "").strip()
    if not dsn:
        return None, "a database connection string is required"
    try:
        import psycopg
    except ImportError:
        return None, ("the AIOrders source needs the psycopg driver — "
                      "`pip install \"psycopg[binary]\"` on the machine running the control center")
    try:
        with psycopg.connect(dsn, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"ok": True, "detail": "connected"}, None
    except Exception as e:
        return {"ok": False, "detail": str(e)}, None


def load_customers(cfg, segment):
    """(customers, error). Never raises — every caller here is an HTTP handler
    that wants the reason on screen, not a 500."""
    src = (cfg or {}).get("customer_source") or ""
    try:
        if src == "crm":
            return _crm_customers(cfg, segment), None
        if src == "aiorders":
            return _aiorders_customers(cfg, segment), None
        return [], "no customer database source configured"
    except Exception as e:
        return [], str(e)


# ── The HTTP SMS gateway ─────────────────────────────────────────────────────
# The gateway this repo actually talks to (a local HTTP-to-SMS relay) takes
# HTTP Basic Auth and a JSON body, and one call can carry many numbers at
# once when they all get the same text:
#   POST <sms_url>   Authorization: Basic base64(username:password)
#   {"textMessage": {"text": "..."}, "phoneNumbers": ["+1...", "+1...", ...]}
# The URL itself is always the partner's own, from config — never hardcoded.

def _post_gateway(cfg, phone_numbers, message):
    """Returns (ok, detail)."""
    url = (cfg.get("sms_url") or "").strip()
    if not url:
        return False, "no SMS server URL configured"
    body = json.dumps({"textMessage": {"text": message},
                       "phoneNumbers": phone_numbers}).encode()
    # api.sms-gate.app sits behind Cloudflare, which 403s urllib's default
    # "Python-urllib/x.y" User-Agent as a bot signature (error code 1010) —
    # same credentials, same body, only the UA differs from a working curl.
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "business-os-sms/1.0"})
    token = base64.b64encode(
        f'{cfg.get("sms_username") or ""}:{cfg.get("sms_password") or ""}'.encode()).decode()
    req.add_header("Authorization", f"Basic {token}")
    try:
        with urllib.request.urlopen(req, timeout=SMS_TIMEOUT_SECONDS) as r:
            resp = r.read(2000).decode("utf-8", "replace").strip()
            return (200 <= r.status < 300), f"{r.status} {resp[:200]}"
    except urllib.error.HTTPError as e:
        return False, f"{e.code} {e.read(200).decode('utf-8', 'replace')}"
    except Exception as e:
        return False, str(e)


def send_one(cfg, to, message):
    """Returns (ok, detail)."""
    return _post_gateway(cfg, [to], message)


def send_batch(cfg, recipients):
    """recipients: [{"phone", "message"}]. Recipients that share identical
    message text go out together in one gateway call — the API accepts a
    phoneNumbers array — so a same-body campaign to N customers is one
    request, not N."""
    sent, failed, errors = 0, 0, []
    groups = {}
    for r in recipients:
        groups.setdefault(r["message"], []).append(r["phone"])
    for message, phones in groups.items():
        ok, detail = _post_gateway(cfg, phones, message)
        if ok:
            sent += len(phones)
        else:
            failed += len(phones)
            for p in phones:
                if len(errors) < 20:
                    errors.append({"phone": p[-4:], "error": detail})
    return {"sent": sent, "failed": failed, "errors": errors}


def send_test(cfg, phone):
    """A one-off send to prove the gateway config actually works, triggered by
    a human clicking a button — not a campaign, so nothing is stored."""
    if quiet_mode():
        return None, f"MODE={os.environ.get('MODE')} — everything is paused"
    phone = (phone or "").strip()
    if not phone:
        return None, "a phone number is required"
    ok, detail = send_one(cfg, phone,
                          "Test message from Business OS — your SMS configuration works.")
    return {"ok": ok, "detail": detail}, None


# ── Campaign store ───────────────────────────────────────────────────────────

def _sms_dir(instance_id, kind):
    d = INSTANCES_DIR / instance_id / "marketing" / "sms" / kind
    d.mkdir(parents=True, exist_ok=True)
    return d


def _read_records(instance_id, kind):
    out = []
    d = INSTANCES_DIR / instance_id / "marketing" / "sms" / kind
    if not d.is_dir():
        return out
    for f in sorted(d.glob("*.json"), reverse=True):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
    return sorted(out, key=lambda r: r.get("created_at", ""), reverse=True)


def _write_record(instance_id, kind, rec):
    (_sms_dir(instance_id, kind) / f"{rec['id']}.json").write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return rec


def _find_campaign(instance_id, campaign_id):
    path = INSTANCES_DIR / instance_id / "marketing" / "sms" / "campaigns" / f"{campaign_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def list_campaigns(instance_id):
    return _read_records(instance_id, "campaigns")


def list_reactivations(instance_id):
    return _read_records(instance_id, "reactivation")


def create_campaign(instance_id, cfg, fields, actor_email):
    name = (fields.get("name") or "").strip()
    body = (fields.get("body") or "").strip()
    segment = (fields.get("segment") or "").strip()
    if not name:
        return None, "a campaign needs a name"
    if not body:
        return None, "a campaign needs a message"
    if len(body) > MAX_SMS_CHARS:
        return None, f"message is {len(body)} characters — the cap is {MAX_SMS_CHARS}"
    if not any(s["id"] == segment for s in segments_for(cfg)):
        return None, "pick a segment that exists for your customer source"

    # Sized at creation so the operator approves a real number rather than a
    # promise. Recounted at send time, because the database moves.
    customers, err = load_customers(cfg, segment)
    rec = {
        # The timestamp alone is not unique: two campaigns saved inside the
        # same second wrote the same filename and one silently replaced the
        # other. The suffix is what makes the id an id.
        "id": f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4]}-{_slug(name)}",
        "kind": "campaign",
        "instance": instance_id,
        "name": name,
        "segment": segment,
        "body": body,
        "status": "draft",
        "created_by": actor_email,
        "created_at": _now(),
        "approved_by": "", "approved_at": "",
        "sent_at": "", "recipient_count": len(customers),
        "sizing_error": err or "",
        "results": None,
    }
    return _write_record(instance_id, "campaigns", rec), None


def update_campaign(instance_id, campaign_id, fields):
    rec = _find_campaign(instance_id, campaign_id)
    if not rec:
        return None, "no such campaign"
    if rec["status"] not in ("draft", "approved"):
        return None, f"a {rec['status']} campaign cannot be edited"
    body = (fields.get("body") or "").strip()
    if not body:
        return None, "a campaign needs a message"
    if len(body) > MAX_SMS_CHARS:
        return None, f"message is {len(body)} characters — the cap is {MAX_SMS_CHARS}"
    rec["body"] = body
    if "name" in fields and (fields.get("name") or "").strip():
        rec["name"] = fields["name"].strip()
    # Editing after approval un-approves it. The gate is on the words that go
    # out, not on the record — approving one message and sending another is
    # exactly the hole the gate exists to close.
    if rec["status"] == "approved":
        rec.update({"status": "draft", "approved_by": "", "approved_at": ""})
    return _write_record(instance_id, "campaigns", rec), None


def approve_campaign(instance_id, campaign_id, actor_email):
    rec = _find_campaign(instance_id, campaign_id)
    if not rec:
        return None, "no such campaign"
    if rec["status"] != "draft":
        return None, f"campaign is already {rec['status']}"
    rec.update({"status": "approved", "approved_by": actor_email, "approved_at": _now()})
    return _write_record(instance_id, "campaigns", rec), None


def discard_campaign(instance_id, campaign_id):
    rec = _find_campaign(instance_id, campaign_id)
    if not rec:
        return None, "no such campaign"
    if rec["status"] == "sent":
        return None, "a sent campaign cannot be discarded"
    rec["status"] = "discarded"
    return _write_record(instance_id, "campaigns", rec), None


def send_campaign(instance_id, campaign_id, cfg):
    """The only path from an approved campaign to the gateway."""
    if quiet_mode():
        return None, f"MODE={os.environ.get('MODE')} — everything is paused"
    rec = _find_campaign(instance_id, campaign_id)
    if not rec:
        return None, "no such campaign"
    if rec["status"] != "approved":
        return None, "only an approved campaign can be sent — approve it first"

    customers, err = load_customers(cfg, rec["segment"])
    if err:
        return None, f"could not read the customer database: {err}"
    if not customers:
        return None, "that segment is empty right now"

    results = send_batch(cfg, [{"phone": c["phone"], "message": rec["body"]}
                               for c in customers])
    rec.update({"status": "sent" if results["sent"] else "failed",
                "sent_at": _now(), "recipient_count": len(customers),
                "results": results})
    return _write_record(instance_id, "campaigns", rec), None


# ── Smart reactivation ───────────────────────────────────────────────────────

REACTIVATION_PROMPT = """\
You are drafting one-to-one reactivation SMS messages. These go out \
automatically — no human reviews them before they send — so every message \
must be one you would be comfortable sending unreviewed.

About the business:
{business_blurb}

The offer to use for this run — mention it only where it genuinely fits, \
never invent a different one:
{offer}

Below is a JSON array of lapsed customers. Each has an opaque `ref`, a first \
name (possibly empty), and `days_since_order`. Phone numbers are deliberately \
withheld; you never need one.

{customers}

Decide which of these are actually worth reaching right now, and write one \
message for each you choose. Leave out anyone a message would not genuinely \
serve — reaching fewer people well is the correct answer, and an empty list \
is a valid answer.

Rules for every message:
- Under 160 characters, including any sign-off.
- Plain text. No links, no emoji, no ALL CAPS, no fake urgency. The offer \
above is the only discount, price, or menu item you may mention — never \
invent another.
- Use the person's first name only if it is present and looks like a real name.
- One clear, honest reason to come back, in the business's own voice: warm, \
short, not salesy.
- Never claim anything about their past orders beyond how long it has been.

Reply with JSON and nothing else — no prose, no code fence:
{{"messages": [{{"ref": "<ref>", "message": "<text>"}}]}}
"""


def _recent_reactivation_refs(instance_id):
    """Customer ids texted by a reactivation run inside the cooldown window.
    Read from the run records themselves rather than a separate ledger — one
    file to be consistent, and the history is the audit trail anyway."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=REACTIVATION_COOLDOWN_DAYS)
    recent = set()
    for run in list_reactivations(instance_id):
        try:
            when = datetime.fromisoformat((run.get("created_at") or "").replace("Z", "+00:00"))
        except ValueError:
            continue
        if when < cutoff:
            continue
        for m in run.get("messages") or []:
            if m.get("sent"):
                recent.add(m.get("customer_id"))
    return recent


def _run_claude(prompt, oauth_token):
    """A headless pass on the partner's own token, through the same launcher
    every engineering pass goes through — same binary resolution, same
    permission flag, same host quirks already solved there."""
    if not RUN_CLAUDE.exists():
        return None, f"missing {RUN_CLAUDE}"
    shell = "/bin/sh"
    env = {**os.environ, "CLAUDE_CODE_OAUTH_TOKEN": oauth_token}
    env.pop("CLAUDECODE", None)
    try:
        proc = subprocess.run([shell, str(RUN_CLAUDE), "-p", prompt],
                              cwd=str(ROOT), env=env, capture_output=True,
                              text=True, timeout=CLAUDE_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        return None, f"the Claude pass did not finish in {CLAUDE_TIMEOUT_SECONDS}s"
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()[:400]
        return None, f"claude exited {proc.returncode}: {detail}"
    return proc.stdout, None


def _parse_messages(raw):
    """Pull the JSON object out of whatever came back. A model that wrapped it
    in a fence or a sentence should not cost a run."""
    text = (raw or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None, "the pass returned no JSON"
    try:
        data = json.loads(text[start:end + 1])
    except ValueError as e:
        return None, f"the pass returned unparseable JSON: {e}"
    msgs = data.get("messages")
    if not isinstance(msgs, list):
        return None, "the pass returned no `messages` array"
    return msgs, None


def run_reactivation(instance_id, cfg, actor_email, offer):
    """Pick lapsed customers, have Claude decide who and what, and send.

    Auto-send, so the guardrails are here rather than in a human: quiet mode
    stops it, the cooldown keeps anyone from being texted twice in a month, and
    the cap bounds the blast radius of a bad pass. Every decision is written to
    the run record whether or not anything sent.

    `offer` is asked fresh each run — reactivation has no standing campaign
    copy, so without it the model has nothing concrete to write about and
    could only invent one, which the prompt explicitly forbids. The business
    blurb, by contrast, is standing context and comes from cfg."""
    if quiet_mode():
        return None, f"MODE={os.environ.get('MODE')} — everything is paused"
    if not cfg.get("claude_oauth_token"):
        return None, "no Claude OAuth token in your configuration"
    if not cfg.get("sms_url"):
        return None, "no SMS server configured"
    offer = (offer or "").strip()
    if not offer:
        return None, "an offer is required to run reactivation"

    segment = "quiet_90d" if cfg.get("customer_source") == "crm" else "lapsed_60d"
    customers, err = load_customers(cfg, segment)
    if err:
        return None, f"could not read the customer database: {err}"

    skipped_cooldown = _recent_reactivation_refs(instance_id)
    pool = [c for c in customers if c["id"] not in skipped_cooldown]
    pool.sort(key=lambda c: c.get("days_since_order") or 0, reverse=True)
    pool = pool[:REACTIVATION_MAX_RECIPIENTS]

    run = {
        "id": f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4]}-reactivation",
        "kind": "reactivation",
        "instance": instance_id,
        "created_by": actor_email,
        "created_at": _now(),
        "offer": offer,
        "segment": segment,
        "candidates": len(customers),
        "skipped_cooldown": len(customers) - len([c for c in customers
                                                  if c["id"] not in skipped_cooldown]),
        "considered": len(pool),
        "status": "running",
        "messages": [],
        "results": {"sent": 0, "failed": 0, "errors": []},
        "error": "",
    }
    if not pool:
        run.update({"status": "no-one", "error": ""})
        return _write_record(instance_id, "reactivation", run), None

    # Opaque refs, not customer ids and never phone numbers: the model gets
    # what it needs to choose and nothing that identifies anyone.
    refs = {}
    payload = []
    for c in pool:
        ref = uuid.uuid4().hex[:8]
        refs[ref] = c
        payload.append({"ref": ref,
                        "first_name": (c.get("name") or "").split(" ")[0],
                        "days_since_order": c.get("days_since_order")})

    blurb = (cfg.get("business_blurb") or "").strip() or f"({instance_id} — no business description on file)"
    prompt = REACTIVATION_PROMPT.format(
        business_blurb=blurb, offer=offer, customers=json.dumps(payload, indent=2))
    raw, err = _run_claude(prompt, cfg["claude_oauth_token"])
    if err:
        run.update({"status": "failed", "error": err})
        return _write_record(instance_id, "reactivation", run), None

    msgs, err = _parse_messages(raw)
    if err:
        run.update({"status": "failed", "error": err})
        return _write_record(instance_id, "reactivation", run), None

    chosen = []
    for m in msgs:
        c = refs.get((m or {}).get("ref"))
        text = ((m or {}).get("message") or "").strip()
        if not c or not text:
            continue
        if len(text) > MAX_SMS_CHARS:
            text = text[:MAX_SMS_CHARS]
        chosen.append({"customer_id": c["id"], "name": c.get("name", ""),
                       "phone": c["phone"], "message": text, "sent": False,
                       "detail": ""})

    for m in chosen:
        ok, detail = send_one(cfg, m["phone"], m["message"])
        m["sent"], m["detail"] = ok, detail
        if ok:
            run["results"]["sent"] += 1
        else:
            run["results"]["failed"] += 1
            if len(run["results"]["errors"]) < 20:
                run["results"]["errors"].append({"phone": m["phone"][-4:], "error": detail})

    # Phone numbers are not kept in the record — the run is an audit trail, not
    # a second copy of the customer database.
    for m in chosen:
        m["phone"] = "…" + m["phone"][-4:]

    run.update({"messages": chosen, "chosen": len(chosen),
                "status": "sent" if run["results"]["sent"] else
                          ("no-one" if not chosen else "failed")})
    return _write_record(instance_id, "reactivation", run), None
