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
Never raises — Supabase insert failures must never crash the UI.

Credential resolution order (read from os.environ on each insert, not at import):
    1. PLATFORM_SUPABASE_URL  / PLATFORM_SUPABASE_ANON_KEY  (Platform Hub project)
    2. SUPABASE_URL           / SUPABASE_ANON_KEY            (Sovereign primary project)

Rationale: Hugging Face and other hosts may expose secrets after the worker imports
this module; import-time caching would leave URL/key permanently empty.

Transport: official ``supabase`` Python client instead of raw httpx REST calls.
Some runtimes fail to resolve ``*.supabase.co`` via httpx even when the client works.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Any

from supabase import create_client

_TABLE = "cross_app_findings"


def _get_supabase_url() -> str:
    return (
        os.environ.get("PLATFORM_SUPABASE_URL")
        or os.environ.get("SUPABASE_URL")
        or ""
    ).strip()


def _get_supabase_key() -> str:
    return (
        os.environ.get("PLATFORM_SUPABASE_ANON_KEY")
        or os.environ.get("SUPABASE_ANON_KEY")
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        or os.environ.get("SUPABASE_KEY")
        or ""
    ).strip()


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
        measure_id:     optional top-level column when present in table
        policy_id:      optional top-level column when present in table
    """
    url = _get_supabase_url()
    key = _get_supabase_key()
    if not url or not key:
        print("[findings] URL or key missing — skipping insert", file=sys.stderr)
        return False

    now = datetime.now(timezone.utc).isoformat()

    payload = {
        "source_app": source_app,
        "finding_type": finding_type,
        "severity": severity,
        "status": status,
        "title": title,
        "description": description,
        "metadata": {
            "trigger_type": trigger_type,
            "client_session_id": session_id,
            **(extra_metadata or {}),
        },
        "created_at": now,
        "updated_at": now,
    }
    if measure_id is not None:
        payload["measure_id"] = str(measure_id)
    if policy_id is not None:
        payload["policy_id"] = str(policy_id)

    try:
        client = create_client(url, key)
        client.table(_TABLE).insert(payload).execute()
        return True
    except Exception as exc:
        print(
            f"[findings] insert failed ({exc}) — source_app={source_app} "
            f"finding_type={finding_type} trigger_type={trigger_type}",
            file=sys.stderr,
        )
        return False
