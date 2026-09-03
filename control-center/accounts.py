#!/usr/bin/env python3
"""Accounts, roles and per-partner configuration for the Control Center.

Split out of server.py because it is the one part of this dashboard that is
now a real store rather than a view: it is written from the browser, it holds
secrets, and it decides what every other view is allowed to show.

WHY A FILE AND NOT .env
-----------------------
`CONTROL_CENTER_USERS=a@b.com:1234,c@d.com:5678` was the whole user model, and
it cannot carry a role, a phone number, or an instance assignment — but the
deeper problem is that .env is SOURCED by lib/eng-env.sh. A page that adds a
user would have to rewrite a file that a shell parses, where one stray quote
silently kills every variable below it and takes the build loop with it. So
the store moves to JSON next to this file, and .env keeps its one job: seeding
the store the first time this runs.

TWO FILES, DELIBERATELY
-----------------------
  users.json           identity, role, instance assignment. Read constantly,
                       serialised to the browser on the Partners page.
  partner-config.json  Claude OAuth token, SMS gateway password, Postgres DSN.
                       Never serialised whole — read_config_public() redacts.

Keeping them apart means the listing endpoint physically cannot leak a secret
by forgetting a field, which is the failure mode a single file invites.

Both are chmod 0600 and gitignored.

ROLES
-----
  admin    no restrictions. Sees every instance, the Partners page, and Logs.
  partner  sees only the instances assigned to them, and must supply their own
           Claude OAuth token before any agent work runs on their behalf.
"""

import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

USERS_FILE = HERE / "users.json"
CONFIG_FILE = HERE / "partner-config.json"

ROLES = ("admin", "partner")

# Which email becomes the admin when the store is seeded from .env. Overridable
# so a fresh install elsewhere is not stuck with this repo's owner. Read at
# call time, not import time: server.py imports this module before it runs
# load_env(), so anything read here at import would miss .env entirely.
def _default_admin():
    return os.environ.get("CONTROL_CENTER_ADMIN", "h@aiorders.io").strip().lower()

_LOCK = threading.RLock()

# The user acting on the current request. ThreadingHTTPServer gives each
# request its own thread, so thread-local is exactly the right scope: every
# instance-listing function in server.py reads this instead of taking an
# `actor` argument through six call layers it does not otherwise need.
_CURRENT = threading.local()


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _write_json(path, data):
    """Write, then tighten the mode. Written to a temp file and replaced so a
    crash mid-write cannot leave a half-parsed user store — which would lock
    every account out at once."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass  # Windows; the ACL is whatever the profile gives it
    os.replace(tmp, path)


# ── The user store ───────────────────────────────────────────────────────────

def _seed_from_env():
    """First run only: turn CONTROL_CENTER_USERS into a real store.

    The seed rule preserves the access people already had. Everyone in that
    line could see every business, so every seeded partner is assigned every
    instance that exists right now — nobody loses access on upgrade, and the
    admin narrows it from the Partners page. _default_admin() becomes the admin;
    if it is not in the line, the first entry is, because a store with no
    admin has no way to grow one.
    """
    raw = os.environ.get("CONTROL_CENTER_USERS", "")
    pairs = []
    for pair in raw.split(","):
        pair = pair.strip()
        if not pair or ":" not in pair:
            continue
        email, _, pin = pair.partition(":")
        email, pin = email.strip().lower(), pin.strip()
        if email and pin:
            pairs.append((email, pin))

    existing = [i.name for i in sorted((ROOT / "instances").glob("*"))
                if i.is_dir()] if (ROOT / "instances").is_dir() else []

    preferred = _default_admin()
    admin_email = preferred if any(e == preferred for e, _ in pairs) else (
        pairs[0][0] if pairs else None)

    users = []
    for email, pin in pairs:
        is_admin = email == admin_email
        users.append({
            "email": email,
            "name": "",
            "phone": "",
            "pin": pin,
            "role": "admin" if is_admin else "partner",
            "instances": [] if is_admin else list(existing),
            "created_at": _now(),
            "last_login": "",
        })
    return {"version": 1, "seeded_from_env": bool(users), "users": users}


def _load():
    with _LOCK:
        if not USERS_FILE.exists():
            store = _seed_from_env()
            _write_json(USERS_FILE, store)
            return store
        store = _read_json(USERS_FILE, None)
        if not isinstance(store, dict) or not isinstance(store.get("users"), list):
            # Unparseable store. Refuse to silently reseed over it — that would
            # quietly reset roles and instance assignments.
            raise RuntimeError(f"{USERS_FILE} is unreadable; fix or move it aside")
        return store


def _save(store):
    with _LOCK:
        _write_json(USERS_FILE, store)


def all_users():
    return list(_load()["users"])


def get_user(email):
    if not email:
        return None
    email = email.strip().lower()
    for u in _load()["users"]:
        if u["email"] == email:
            return u
    return None


def any_users():
    """False means nobody can log in — the startup warning still wants to say so."""
    return bool(_load()["users"])


def touch_login(email):
    with _LOCK:
        store = _load()
        for u in store["users"]:
            if u["email"] == (email or "").strip().lower():
                u["last_login"] = _now()
                _save(store)
                return


# ── Validation ───────────────────────────────────────────────────────────────

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _clean_instances(value):
    if not isinstance(value, list):
        return []
    seen, out = set(), []
    for v in value:
        v = str(v).strip()
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _validate(email, pin, role, instances, *, require_pin):
    if not email or not EMAIL_RE.match(email):
        return "a valid email is required"
    if require_pin or pin:
        if not re.match(r"^\d{4,12}$", pin or ""):
            return "PIN must be 4–12 digits"
    if role not in ROLES:
        return f"role must be one of {', '.join(ROLES)}"
    if role == "partner" and not instances:
        return "a partner needs at least one instance assigned"
    known = {i.name for i in (ROOT / "instances").glob("*") if i.is_dir()}
    unknown = [i for i in instances if i not in known]
    if unknown:
        return f"unknown instance(s): {', '.join(unknown)}"
    return None


def create_user(fields):
    email = (fields.get("email") or "").strip().lower()
    pin = (fields.get("pin") or "").strip()
    role = (fields.get("role") or "partner").strip().lower()
    instances = _clean_instances(fields.get("instances"))
    if role == "admin":
        instances = []
    err = _validate(email, pin, role, instances, require_pin=True)
    if err:
        return None, err
    with _LOCK:
        store = _load()
        if any(u["email"] == email for u in store["users"]):
            return None, f"{email} already exists"
        user = {"email": email, "name": (fields.get("name") or "").strip(),
                "phone": (fields.get("phone") or "").strip(), "pin": pin,
                "role": role, "instances": instances,
                "created_at": _now(), "last_login": ""}
        store["users"].append(user)
        _save(store)
    return public_user(user), None


def update_user(email, fields):
    """Patch semantics: only the keys present are touched. A blank `pin` means
    'leave the PIN alone', so the edit form does not have to re-ask for it
    every time a phone number changes."""
    email = (email or "").strip().lower()
    with _LOCK:
        store = _load()
        user = next((u for u in store["users"] if u["email"] == email), None)
        if not user:
            return None, "no such user"

        role = (fields.get("role") or user["role"]).strip().lower()
        instances = (_clean_instances(fields["instances"])
                     if "instances" in fields else user.get("instances", []))
        if role == "admin":
            instances = []
        pin = (fields.get("pin") or "").strip()

        err = _validate(email, pin, role, instances, require_pin=False)
        if err:
            return None, err

        # The last admin must stay an admin. Demoting them leaves a store
        # nobody can administer and no page that can fix it.
        if user["role"] == "admin" and role != "admin":
            if sum(1 for u in store["users"] if u["role"] == "admin") <= 1:
                return None, "this is the only admin — promote someone else first"

        if "name" in fields:
            user["name"] = (fields.get("name") or "").strip()
        if "phone" in fields:
            user["phone"] = (fields.get("phone") or "").strip()
        if pin:
            user["pin"] = pin
        user["role"] = role
        user["instances"] = instances
        _save(store)
    return public_user(user), None


def delete_user(email, *, acting_email):
    email = (email or "").strip().lower()
    if email == (acting_email or "").strip().lower():
        return None, "you cannot delete your own account"
    with _LOCK:
        store = _load()
        user = next((u for u in store["users"] if u["email"] == email), None)
        if not user:
            return None, "no such user"
        if user["role"] == "admin" and sum(
                1 for u in store["users"] if u["role"] == "admin") <= 1:
            return None, "this is the only admin"
        store["users"] = [u for u in store["users"] if u["email"] != email]
        _save(store)
    delete_config(email)
    return {"deleted": email}, None


def public_user(u):
    """A user as the Partners page sees them — everything except the PIN.
    `pin_set` rather than the PIN itself: the page needs to show that one
    exists and offer a reset, never to display it."""
    return {"email": u["email"], "name": u.get("name", ""),
            "phone": u.get("phone", ""), "role": u.get("role", "partner"),
            "instances": list(u.get("instances", [])),
            "created_at": u.get("created_at", ""),
            "last_login": u.get("last_login", ""),
            "pin_set": bool(u.get("pin")),
            "config_ready": config_ready(u["email"])}


# ── Who is acting, and what they can see ─────────────────────────────────────

def set_current(user):
    _CURRENT.user = user


def current():
    return getattr(_CURRENT, "user", None)


def is_admin(user=None):
    u = user if user is not None else current()
    return bool(u) and u.get("role") == "admin"


def visible_instances(user=None):
    """The instance ids this user may see. None means 'no restriction' — a
    distinct value from the empty list, which means 'assigned nothing'."""
    u = user if user is not None else current()
    if u is None or is_admin(u):
        return None
    return set(u.get("instances") or [])


def can_see_instance(instance_id, user=None):
    allowed = visible_instances(user)
    return allowed is None or instance_id in allowed


def filter_instance_dirs(dirs, user=None):
    """Filter an iterable of instance directories by what the actor may see.
    The single choke point every roster function in server.py goes through."""
    allowed = visible_instances(user)
    if allowed is None:
        return list(dirs)
    return [d for d in dirs if d.name in allowed]


# ── Per-partner configuration ────────────────────────────────────────────────
# Claude OAuth token, the HTTP SMS gateway, and where this partner's customers
# come from. Keyed by email, so it follows the account rather than the instance
# — the token is the person's, not the business's.

SECRET_FIELDS = ("claude_oauth_token", "sms_password", "pg_dsn")

DEFAULT_CONFIG = {
    "claude_oauth_token": "",
    "sms_url": "",
    "sms_username": "",
    "sms_password": "",
    "customer_source": "",     # "aiorders" | "crm"
    "brand_id": "",            # aiorders only
    "pg_dsn": "",              # aiorders only
    "updated_at": "",
}


def _load_configs():
    with _LOCK:
        data = _read_json(CONFIG_FILE, {"version": 1, "configs": {}})
        if not isinstance(data.get("configs"), dict):
            data = {"version": 1, "configs": {}}
        return data


def read_config(email):
    """The real config, secrets included. Server-side callers only."""
    email = (email or "").strip().lower()
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(_load_configs()["configs"].get(email) or {})
    return cfg


def _mask(value):
    if not value:
        return ""
    return "•" * 8 + (value[-4:] if len(value) > 4 else "")


def read_config_public(email):
    """What the browser is allowed to see: every non-secret value verbatim,
    every secret reduced to 'set' plus its last four characters. The Config
    page never receives a token it could accidentally log or paste."""
    cfg = read_config(email)
    out = {k: v for k, v in cfg.items() if k not in SECRET_FIELDS}
    for k in SECRET_FIELDS:
        out[k + "_set"] = bool(cfg.get(k))
        out[k + "_hint"] = _mask(cfg.get(k))
    out["ready"] = config_ready(email)
    out["missing"] = config_missing(email)
    return out


def write_config(email, fields):
    """Patch semantics, and secrets have their own rule: a blank secret means
    'unchanged', because the browser was never given the current value to send
    back. Clearing one is an explicit `{"clear": ["claude_oauth_token"]}`."""
    email = (email or "").strip().lower()
    if not email:
        return None, "no user"

    source = (fields.get("customer_source") or "").strip().lower()
    if source and source not in ("aiorders", "crm"):
        return None, "customer source must be 'aiorders' or 'crm'"

    url = (fields.get("sms_url") or "").strip()
    if url and not url.startswith(("http://", "https://")):
        return None, "SMS server URL must start with http:// or https://"

    with _LOCK:
        data = _load_configs()
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(data["configs"].get(email) or {})

        for key in ("sms_url", "sms_username", "customer_source", "brand_id"):
            if key in fields:
                cfg[key] = (fields.get(key) or "").strip()
        for key in SECRET_FIELDS:
            val = (fields.get(key) or "").strip()
            if val:
                cfg[key] = val
        for key in fields.get("clear") or []:
            if key in SECRET_FIELDS:
                cfg[key] = ""

        if cfg["customer_source"] == "aiorders" and not cfg["brand_id"]:
            return None, "the AIOrders source needs a brand id"

        cfg["updated_at"] = _now()
        data["configs"][email] = cfg
        _write_json(CONFIG_FILE, data)
    return read_config_public(email), None


def delete_config(email):
    email = (email or "").strip().lower()
    with _LOCK:
        data = _load_configs()
        if data["configs"].pop(email, None) is not None:
            _write_json(CONFIG_FILE, data)


def config_missing(email):
    """What is still missing before this partner's SMS work can run. Returned
    as a list rather than a boolean so the UI can name the gap instead of
    saying 'not configured' and leaving someone hunting."""
    cfg = read_config(email)
    missing = []
    if not cfg["claude_oauth_token"]:
        missing.append("Claude OAuth token")
    if not cfg["sms_url"]:
        missing.append("SMS server URL")
    if not cfg["customer_source"]:
        missing.append("customer database source")
    elif cfg["customer_source"] == "aiorders":
        if not cfg["brand_id"]:
            missing.append("AIOrders brand id")
        if not cfg["pg_dsn"]:
            missing.append("AIOrders database connection string")
    return missing


def config_ready(email):
    return not config_missing(email)
