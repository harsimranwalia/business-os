#!/usr/bin/env python3
"""SMS — a marketing channel with two halves, and they are not symmetric.

CAMPAIGNS are bulk sends the operator writes: pick a segment, write the copy,
approve it, send it. They keep the constitution's human gate — a campaign
cannot leave `draft` without someone clicking Approve, and only an approved
campaign can be sent.

SMART REACTIVATION takes no copy and no segment. It reads the lapsed end of
the customer database and runs a headless Claude pass on the partner's own
OAuth token to decide who is worth reaching and what to say to each of them.
What happens next is chosen per run, at the point the operator starts it:

  auto    Send straight away, with nobody reading the messages first.
          Approved by Harry (2026-09-03) as the one auto-send path in the
          system: the whole point is that it is hands-off. The guardrails
          that replace the human gate are all in run_reactivation() — quiet
          mode, a per-run recipient cap, and a 30-day per-customer cooldown
          read out of the previous runs' records.
  review  Stop at `pending` with every drafted message and the number it is
          bound for, and send nothing until a human presses Send — one
          message at a time, or all of them at once (send_reactivation), or
          none of them (discard_reactivation).

`auto` is not deprecated by `review` existing: both remain available every
run, and the guardrails above apply to both — `review` adds a human on top of
them rather than replacing them.

A `review` run is the one record here that holds real phone numbers, because
the operator has to see which number each message is bound for and the send
still needs it. Each number is masked the instant its message reaches a
terminal state (sent, or skipped), so only messages still waiting on a human
carry one. Discarding a run is therefore also how you make it stop holding
numbers.

WHERE THE CUSTOMERS COME FROM is the partner's own config (see accounts.py):

  crm       Twenty, over the GraphQL API this repo already talks to. Twenty
            carries no order history, so the only honest segments here are
            "everyone" and two based on record dates.
  aiorders  The AIOrders Postgres/Supabase database, direct, scoped to the
            partner's brand id. Needs psycopg — the only non-stdlib import
            anywhere in the control center, imported lazily so a partner on
            another source never pays for it.
  ghl       HighLevel (GoHighLevel) contacts, over the marketplace HTTP API,
            scoped to one location. Like the CRM it carries no order history,
            so it gets the same date-based segments and none of the
            order-based ones.

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

# What a run does once the Claude pass has written the messages. Chosen per
# run by the operator who starts it; "auto" is the historical behaviour and
# stays the sanctioned auto-send path, "review" holds everything at `pending`
# for a human. Anything else is a bug in the caller, not a third mode.
REACTIVATION_MODES = ("auto", "review")

SMS_TIMEOUT_SECONDS = 20
MAX_SMS_CHARS = 320   # two GSM segments; longer is a billing surprise


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mask(phone):
    """What a phone number looks like once it is written to a record for
    keeps. The records are an audit trail, not a second copy of the customer
    database."""
    return "…" + (phone or "")[-4:]


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

# HighLevel contacts carry a created and an updated timestamp and no order
# history, so they get the CRM's segments and the same honest caveat — an
# updated-at gap is a record-touch proxy, not a customer going quiet.
GHL_SEGMENTS = [
    {"id": "all", "label": "Everyone", "note": "every HighLevel contact with a phone number"},
    {"id": "new_30d", "label": "Added in the last 30 days",
     "note": "dateAdded within 30 days"},
    {"id": "quiet_90d", "label": "No HighLevel activity in 90 days",
     "note": "dateUpdated older than 90 days — a record-touch proxy, not an order signal"},
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


# What each source is called on screen, and the set of them load_customers()
# knows how to read. accounts.CUSTOMER_SOURCES is the config-side copy.
SOURCE_LABELS = {"aiorders": "AIOrders", "crm": "CRM (Twenty)", "ghl": "HighLevel"}


def segments_for(cfg):
    src = (cfg or {}).get("customer_source") or ""
    if src == "crm":
        return CRM_SEGMENTS
    if src == "ghl":
        return GHL_SEGMENTS
    if src == "aiorders":
        return AIORDERS_SEGMENTS
    return []


def _iso_age_days(value, now):
    """Days since an ISO-8601 timestamp, or None if it is missing or unparseable.
    The one date rule shared by both sources that have no order history."""
    raw = (value or "").replace("Z", "+00:00")
    try:
        return (now - datetime.fromisoformat(raw)).days
    except ValueError:
        return None


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
            return _iso_age_days(p.get(field), now)

        if segment == "new_30d" and (age("createdAt") is None or age("createdAt") > 30):
            continue
        if segment == "quiet_90d" and (age("updatedAt") is None or age("updatedAt") < 90):
            continue
        out.append({"id": p["id"], "name": name,
                    "phone": (code + number) if code and not number.startswith("+") else number,
                    "last_order_at": None,
                    "days_since_order": age("updatedAt")})
    return out


# ── HighLevel (GoHighLevel) ─────────────────────────────────────────────────
# POST {GHL_API_BASE}/contacts/search
#      Authorization: Bearer <token>
#      Version: v3
#      Content-Type: application/json
#      {"locationId": "…", "pageLimit": 500[, "searchAfter": [...]]}
# https://marketplace.gohighlevel.com/docs/ghl/contacts/search-contacts-advanced
#
# 500 is HighLevel's own ceiling on pageLimit, not a setting — asking for more
# just gets 500 back. Every contact carries its own "searchAfter" cursor;
# reading the whole list means feeding the last contact's cursor from one page
# into the next request, and stopping once a page comes back short of 500.
GHL_API_BASE = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "v3"
GHL_PAGE_SIZE = 500


def _ghl_search(cfg, search_after=None):
    body = {"locationId": (cfg.get("ghl_location_id") or "").strip(),
            "pageLimit": GHL_PAGE_SIZE}
    if search_after is not None:
        body["searchAfter"] = search_after
    # services.leadconnectorhq.com sits behind Cloudflare, which 403s urllib's
    # default "Python-urllib/x.y" User-Agent as a bot signature (error code
    # 1010) — same credentials, same body, only the UA differs from a working
    # curl.
    req = urllib.request.Request(
        f"{GHL_API_BASE}/contacts/search", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {(cfg.get('ghl_api_key') or '').strip()}",
                 "Version": GHL_API_VERSION,
                 "Content-Type": "application/json",
                 "User-Agent": "business-os-sms/1.0"})
    # Longer than the Twenty read's 30s: each page can carry up to 500 contacts.
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace").strip()[:300]
        raise RuntimeError(f"HighLevel returned {e.code}: {detail or e.reason}")


def _ghl_all_contacts(cfg):
    """Every contact at this location, walking pages with the searchAfter
    cursor until one comes back short of GHL_PAGE_SIZE — HighLevel's signal
    that there is nothing left to walk."""
    contacts = []
    search_after = None
    while True:
        page = _ghl_search(cfg, search_after).get("contacts") or []
        contacts.extend(page)
        if len(page) < GHL_PAGE_SIZE:
            break
        search_after = page[-1].get("searchAfter")
        if not search_after:
            break
    return contacts


def _ghl_row(contact, now):
    """One HighLevel contact in the shape every source here returns. The search
    endpoint publishes no response schema, so the name and phone are read
    across the field names a contact actually carries rather than one assumed
    spelling."""
    phone = (contact.get("phone") or "").strip()
    if not phone:
        return None
    name = (contact.get("contactName") or "").strip()
    if not name:
        name = " ".join(x for x in [(contact.get("firstName") or "").strip(),
                                    (contact.get("lastName") or "").strip()] if x)
    touched = _iso_age_days(contact.get("dateUpdated") or contact.get("dateAdded"), now)
    return {"id": contact.get("id") or "", "name": name, "phone": phone,
            "last_order_at": None, "days_since_order": touched,
            "added_days": _iso_age_days(contact.get("dateAdded"), now)}


def _ghl_contacts(cfg, segment):
    for key, what in (("ghl_location_id", "location id"),
                      ("ghl_api_key", "API token")):
        if not (cfg.get(key) or "").strip():
            raise RuntimeError(f"HighLevel {what} is not set — add it in Config")

    now = datetime.now(timezone.utc)
    out = []
    for contact in _ghl_all_contacts(cfg):
        row = _ghl_row(contact, now)
        if row is None:
            continue
        if segment == "new_30d" and (row["added_days"] is None or row["added_days"] > 30):
            continue
        if segment == "quiet_90d" and (row["days_since_order"] is None
                                       or row["days_since_order"] < 90):
            continue
        out.append({k: v for k, v in row.items() if k != "added_days"})
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


TEST_SAMPLE_ROWS = 2


def test_customer_source(cfg):
    """A real sample read of whichever source is configured, triggered by a
    human clicking Test. Every source answers the same way, because "does this
    connect" means the same thing for all three: credentials that reach the
    partner's own customers, not a socket that answers.

    Returns (result, error): result is {"ok", "detail", "count", "sample"} for
    anything the attempt itself produced — a refused login is a result, not an
    error — and error is only for never getting to try at all.

    The sample carries names so the operator can recognise their own data, but
    the phone numbers are masked like every other number this file writes out:
    confirming a connection is no reason to paint customers' numbers across a
    dashboard."""
    src = (cfg or {}).get("customer_source") or ""
    if not src:
        return None, "pick a customer database source first"
    if src not in SOURCE_LABELS:
        return None, f"unknown customer database source '{src}'"

    customers, err = load_customers(cfg, "all")
    if err:
        return {"ok": False, "detail": err}, None

    label = SOURCE_LABELS[src]
    if not customers:
        return {"ok": True, "count": 0, "sample": [],
                "detail": f"connected to {label}, but it returned no customer "
                          "with a phone number"}, None
    return {"ok": True, "count": len(customers),
            "sample": [{"name": c["name"] or "(no name)", "phone": _mask(c["phone"])}
                       for c in customers[:TEST_SAMPLE_ROWS]],
            "detail": f"connected to {label}"}, None


def load_customers(cfg, segment):
    """(customers, error). Never raises — every caller here is an HTTP handler
    that wants the reason on screen, not a 500."""
    src = (cfg or {}).get("customer_source") or ""
    try:
        if src == "crm":
            return _crm_customers(cfg, segment), None
        if src == "ghl":
            return _ghl_contacts(cfg, segment), None
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


def _find_reactivation(instance_id, run_id):
    path = INSTANCES_DIR / instance_id / "marketing" / "sms" / "reactivation" / f"{run_id}.json"
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
You are drafting one-to-one reactivation SMS messages. {review_note} Either \
way, write every message as one you would be comfortable sending unreviewed.

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
    """Customer ids a reactivation run has claimed inside the cooldown window.
    Read from the run records themselves rather than a separate ledger — one
    file to be consistent, and the history is the audit trail anyway.

    A message still waiting for a human (a `review` run's `pending`) counts as
    claimed, not as free. It has not reached anyone yet, but it is about to,
    and letting the next run draft a second message to the same person would
    put two in front of the operator and no cooldown between them once both
    are approved."""
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
            if m.get("sent") or m.get("state") == "pending":
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


def _settle(run):
    """Recompute a review run's counters and status from its own messages.

    The run stays `pending` while anything is still waiting, and a send the
    gateway refused leaves that message pending with its number intact — so
    the operator can press Send again once whatever the gateway complained
    about is fixed, instead of the message being stranded in a terminal state
    with nothing left to send it with. `results.failed` is therefore a count
    of messages still waiting that carry an error, not a permanent tally."""
    msgs = run.get("messages") or []
    sent = [m for m in msgs if m.get("state") == "sent"]
    waiting = [m for m in msgs if m.get("state") == "pending"]
    errors = [{"phone": (m.get("phone") or "")[-4:], "error": m.get("detail") or ""}
              for m in waiting if m.get("detail")]
    run["results"] = {"sent": len(sent), "failed": len(errors), "errors": errors[:20]}
    if waiting:
        run["status"] = "pending"
    elif sent:
        run["status"] = "sent"
    else:
        run["status"] = "discarded" if msgs else "no-one"
    return run


def run_reactivation(instance_id, cfg, actor_email, offer, mode="auto"):
    """Pick lapsed customers, have Claude decide who and what, then either
    send (`mode="auto"`) or hold everything for a human (`mode="review"`).

    The guardrails are the same either way, because in auto they are all
    there is: quiet mode stops the run, the cooldown keeps anyone from being
    texted twice in a month, and the cap bounds the blast radius of a bad
    pass. Every decision is written to the run record whether or not anything
    sent. `review` adds a person on top of those; it does not replace them,
    and it does not retire `auto` — the mode is chosen fresh each run.

    `offer` is asked fresh each run — reactivation has no standing campaign
    copy, so without it the model has nothing concrete to write about and
    could only invent one, which the prompt explicitly forbids. The business
    blurb, by contrast, is standing context and comes from cfg."""
    mode = (mode or "auto").strip().lower()
    if mode not in REACTIVATION_MODES:
        return None, f"unknown reactivation mode '{mode}'"
    # Quiet mode stops the drafting pass too, not just the send. A campaign
    # can still be written during a pause because writing one costs nothing;
    # a reactivation run spends the partner's Claude token, which is exactly
    # the kind of activity the switch is there to stop.
    if quiet_mode():
        return None, f"MODE={os.environ.get('MODE')} — everything is paused"
    if not cfg.get("claude_oauth_token"):
        return None, "no Claude OAuth token in your configuration"
    if not cfg.get("sms_url"):
        return None, "no SMS server configured"
    offer = (offer or "").strip()
    if not offer:
        return None, "an offer is required to run reactivation"

    # A source with no order history can only offer the record-touch proxy;
    # asking it for "lapsed" would be a number that looks real and is not.
    segment = ("quiet_90d" if cfg.get("customer_source") in ("crm", "ghl")
               else "lapsed_60d")
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
        "mode": mode,
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
        # Only a review run gets these — they are the same stamp an approved
        # campaign carries, for the same reason.
        "approved_by": "", "approved_at": "", "sent_at": "",
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
    review_note = (
        "A person reviews each one and presses send, so nothing here reaches a "
        "phone without their approval." if mode == "review" else
        "These go out automatically — no human reviews them before they send.")
    prompt = REACTIVATION_PROMPT.format(
        business_blurb=blurb, offer=offer, review_note=review_note,
        customers=json.dumps(payload, indent=2))
    raw, err = _run_claude(prompt, cfg["claude_oauth_token"])
    if err:
        run.update({"status": "failed", "error": err})
        return _write_record(instance_id, "reactivation", run), None

    msgs, err = _parse_messages(raw)
    if err:
        run.update({"status": "failed", "error": err})
        return _write_record(instance_id, "reactivation", run), None

    chosen = []
    used = set()
    for m in msgs:
        ref = (m or {}).get("ref")
        c = refs.get(ref)
        text = ((m or {}).get("message") or "").strip()
        if not c or not text or ref in used:
            # A repeated ref is the model writing to the same person twice.
            # Taking both would text them twice in one run and, in review
            # mode, give two rows one Send button each.
            continue
        used.add(ref)
        if len(text) > MAX_SMS_CHARS:
            text = text[:MAX_SMS_CHARS]
        # The opaque ref the model was given is also the message id: already
        # unique within the run, and already meaningless outside it.
        chosen.append({"id": ref, "customer_id": c["id"], "name": c.get("name", ""),
                       "phone": c["phone"], "message": text, "sent": False,
                       "state": "pending", "detail": ""})

    if mode == "review":
        # Nothing sends. The numbers stay in the record because the operator
        # has to see which phone each message is bound for and the send needs
        # it; each is masked as its message settles (see send/discard below).
        run.update({"messages": chosen, "chosen": len(chosen)})
        return _write_record(instance_id, "reactivation", _settle(run)), None

    for m in chosen:
        ok, detail = send_one(cfg, m["phone"], m["message"])
        m["sent"], m["detail"] = ok, detail
        m["state"] = "sent" if ok else "failed"
        if ok:
            run["results"]["sent"] += 1
        else:
            run["results"]["failed"] += 1
            if len(run["results"]["errors"]) < 20:
                run["results"]["errors"].append({"phone": m["phone"][-4:], "error": detail})

    # Phone numbers are not kept in the record — the run is an audit trail, not
    # a second copy of the customer database.
    for m in chosen:
        m["phone"] = _mask(m["phone"])

    run.update({"messages": chosen, "chosen": len(chosen), "sent_at": _now(),
                "status": "sent" if run["results"]["sent"] else
                          ("no-one" if not chosen else "failed")})
    return _write_record(instance_id, "reactivation", run), None


def _pending_targets(run, message_ids):
    """The messages an action applies to: the named ones, or — with nothing
    named — every one still waiting. That is the whole difference between the
    per-message buttons and the run-wide ones."""
    wanted = set(message_ids or [])
    return [m for m in (run.get("messages") or [])
            if m.get("state") == "pending" and (not wanted or m.get("id") in wanted)]


def send_reactivation(instance_id, run_id, cfg, actor_email, message_ids=None):
    """Send some or all of a review run's pending messages — the human gate.

    `message_ids` names specific messages (the per-row Send); omitted or empty
    means every message still waiting (Send all). Sending is the approval, so
    the record gets the same approved_by/approved_at stamp an approved
    campaign carries."""
    if quiet_mode():
        return None, f"MODE={os.environ.get('MODE')} — everything is paused"
    run = _find_reactivation(instance_id, run_id)
    if not run:
        return None, "no such reactivation run"
    if run.get("status") != "pending":
        return None, f"this run is {run.get('status')} — nothing is waiting to be sent"
    targets = _pending_targets(run, message_ids)
    if not targets:
        return None, "those messages have already been sent or skipped"

    for m in targets:
        ok, detail = send_one(cfg, m["phone"], m["message"])
        m["detail"] = detail
        if ok:
            m.update({"sent": True, "state": "sent", "phone": _mask(m["phone"])})
        # A refused send deliberately stays pending, number intact, so the
        # operator can try it again — see _settle().
    # The stamp goes on the first press regardless of what the gateway said —
    # approval is the human act, not the delivery. `sent_at` is the opposite:
    # it means something actually left, so a run where every attempt was
    # refused keeps it empty.
    if not run.get("approved_at"):
        run.update({"approved_by": actor_email, "approved_at": _now()})
    if any(m.get("state") == "sent" for m in targets):
        run["sent_at"] = _now()
    return _write_record(instance_id, "reactivation", _settle(run)), None


def discard_reactivation(instance_id, run_id, message_ids=None):
    """Drop pending messages without sending them: one the operator does not
    like (the per-row Skip), or the whole run. Discarding masks the numbers it
    was holding, so it is also how a run stops holding any."""
    run = _find_reactivation(instance_id, run_id)
    if not run:
        return None, "no such reactivation run"
    if run.get("status") != "pending":
        return None, f"this run is {run.get('status')} — nothing is waiting to be skipped"
    targets = _pending_targets(run, message_ids)
    if not targets:
        return None, "those messages have already been sent or skipped"
    for m in targets:
        m.update({"state": "discarded", "sent": False, "detail": "",
                  "phone": _mask(m["phone"])})
    return _write_record(instance_id, "reactivation", _settle(run)), None
