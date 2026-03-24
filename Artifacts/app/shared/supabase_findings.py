"""Shared helper — insert rows into cross_app_findings.

Schema (live as of sprint verification):
    id              uuid        PK, gen_random_uuid()
    source_app      text        NOT NULL  — "auditshield" | "starguard" | "sovereignshield"
    finding_type    text        NOT NULL  — "audit_flag" | "star_gap" | "policy_violation" | "session_end"
    severity        text        NOT NULL  default 'info'
    status          text        NOT NULL  default 'open'
    title           text        nullable
    description     text        nullable
    metadata        jsonb       nullable  — trigger_type, client_session_id, app detail
    created_at      timestamptz NOT NULL  default now()
    updated_at      timestamptz NOT NULL  default now()

platform_hub_kpis VIEW filters:
    open_audit_flags       finding_type = 'audit_flag'      AND status = 'open'
    open_star_gaps         finding_type = 'star_gap'         AND status = 'open'
    open_policy_violations finding_type = 'policy_violation' AND status = 'open'
    critical_open          severity     = 'critical'          AND status = 'open'
    remediated_total       status       = 'remediated'

Silent-fail design: all errors logged to stderr only.
Never raises — insert failures must never crash the UI.

Connection (read from os.environ on each insert, not at import):
    Uses psycopg2 with a Postgres connection string (``postgresql://`` or ``postgres://``).
    Hugging Face Spaces may block HTTP/HTTPS to ``*.supabase.co`` (REST and supabase-py);
    direct Postgres (port 5432 / pooler) uses the DSN from the Supabase dashboard.

    Resolution order:
        1. PLATFORM_DATABASE_URL
        2. DATABASE_URL
        3. SUPABASE_DB_URL

    Values that start with ``http://`` or ``https://`` are ignored (those are REST API bases,
    not TCP DSNs). Set a dedicated secret, e.g. ``DATABASE_URL``, to the **Session pooler** or
    **Direct connection** string from Supabase → Project Settings → Database.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Any

import psycopg2
from psycopg2.extras import Json

_TABLE = "cross_app_findings"


def _get_postgres_dsn() -> str:
    for name in ("PLATFORM_DATABASE_URL", "DATABASE_URL", "SUPABASE_DB_URL"):
        v = (os.environ.get(name) or "").strip()
        if not v:
            continue
        low = v.lower()
        if low.startswith("http://") or low.startswith("https://"):
            continue
        if low.startswith("postgresql://") or low.startswith("postgres://"):
            return v
    return ""


def insert_finding(
    *,
    source_app: str,
    finding_type: str,
    severity: str = "info",
    status: str = "open",
    title: str | None = None,
    description: str | None = None,
    trigger_type: str,
    session_id: str | None = None,
    extra_metadata: dict[str, Any] | None = None,
    measure_id: str | None = None,
    policy_id: str | None = None,
) -> bool:
    """Insert one row into cross_app_findings. Returns True on success.

    Args:
        source_app:     "auditshield" | "starguard" | "sovereignshield"
        finding_type:   "audit_flag" | "star_gap" | "policy_violation" | "session_end"
        severity:       "info" | "low" | "medium" | "high" | "critical"
        status:         "open" (action triggers) | "remediated" (session-end rows)
        title:          short human-readable label shown in Hub
        description:    optional longer detail
        trigger_type:   "action" | "session_end"
        session_id:     client session uuid
        extra_metadata: any additional key/value pairs stored in metadata jsonb
        measure_id:     folded into metadata if table has no top-level column
        policy_id:      folded into metadata if table has no top-level column
    """
    dsn = _get_postgres_dsn()
    if not dsn:
        print(
            "[findings] No postgres DSN (PLATFORM_DATABASE_URL / DATABASE_URL / SUPABASE_DB_URL) "
            "— skipping insert (http(s):// URLs are ignored)",
            file=sys.stderr,
        )
        return False

    now = datetime.now(timezone.utc)
    meta: dict[str, Any] = {
        "trigger_type": trigger_type,
        "client_session_id": session_id,
        **(extra_metadata or {}),
    }
    if measure_id is not None:
        meta["measure_id"] = str(measure_id)
    if policy_id is not None:
        meta["policy_id"] = str(policy_id)

    sql = (
        f"INSERT INTO {_TABLE} "
        "(source_app, finding_type, severity, status, title, description, metadata, created_at, updated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    args = (
        source_app,
        finding_type,
        severity,
        status,
        title,
        description,
        Json(meta),
        now,
        now,
    )

    try:
        conn = psycopg2.connect(dsn, connect_timeout=10)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args)
            conn.commit()
        finally:
            conn.close()
        return True
    except Exception as exc:
        print(
            f"[findings] insert failed ({exc}) — source_app={source_app} "
            f"finding_type={finding_type} trigger_type={trigger_type}",
            file=sys.stderr,
        )
        return False
