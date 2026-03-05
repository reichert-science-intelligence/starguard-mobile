# hedis_gap_trail.py
# ─────────────────────────────────────────────────────────────
# HEDIS Gap Refresh — Google Sheets Cloud Persistence
# StarGuard Desktop + Mobile | reichert-science-intelligence
# Mirrors audit_trail.py pattern for HEDIS analytics layer
# Brand: Purple #4A3E8F | Gold #D4AF37 | Green #10b981
# ─────────────────────────────────────────────────────────────

import os
import json
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ── Sheet Column Schema ───────────────────────────────────────
HEDIS_COLUMNS = [
    "gap_id",
    "timestamp",
    "member_id",
    "member_name",
    "measure_code",
    "measure_name",
    "care_domain",          # Effectiveness | Access | Experience
    "gap_status",           # OPEN | CLOSED | EXCLUDED
    "due_date",
    "provider_name",
    "intervention_type",    # Outreach | Clinical | Administrative
    "star_impact",          # 1–5 weighting
    "roi_estimate",
    "claude_recommendation",
    "last_updated"
]

# ── Care Domain Map ───────────────────────────────────────────
HEDIS_MEASURES = {
    "CBP":  ("Controlling Blood Pressure",     "Effectiveness"),
    "CDC":  ("Diabetes Care",                  "Effectiveness"),
    "W34":  ("Well-Child Visits",              "Effectiveness"),
    "AWC":  ("Annual Wellness Check",          "Effectiveness"),
    "FUH":  ("Follow-Up After Hospitalization","Effectiveness"),
    "PCE":  ("Pharmacotherapy for COPD",       "Effectiveness"),
    "MPM":  ("Medication Management",          "Effectiveness"),
    "COA":  ("Care of Older Adults",           "Effectiveness"),
    "GSD":  ("Statin Use — Diabetes",          "Effectiveness"),
    "BCS":  ("Breast Cancer Screening",        "Effectiveness"),
    "COL":  ("Colorectal Cancer Screening",    "Effectiveness"),
}


# ─────────────────────────────────────────────────────────────
# CONNECTION MANAGER
# ─────────────────────────────────────────────────────────────

class HedisGapDB:
    """
    Manages Google Sheets read/write for StarGuard HEDIS Gap Refresh.
    Credentials: GSHEETS_CREDS_JSON (HF Secret) or service_account.json
    Sheet name:  HEDIS_SHEET_ID env var or 'StarGuard_HEDIS_Gap_Tracker'
    """

    def __init__(self):
        self.client = None
        self.sheet = None
        self.connected = False
        self.last_error = None
        self.record_count = 0
        self._connect()

    def _connect(self):
        try:
            creds_json = os.environ.get("GSHEETS_CREDS_JSON")
            if creds_json:
                creds = Credentials.from_service_account_info(
                    json.loads(creds_json), scopes=SCOPES
                )
            elif os.path.exists("service_account.json"):
                creds = Credentials.from_service_account_file(
                    "service_account.json", scopes=SCOPES
                )
            else:
                raise FileNotFoundError(
                    "No credentials. Set GSHEETS_CREDS_JSON as HF Space Secret."
                )

            self.client = gspread.authorize(creds)
            sheet_id = os.environ.get(
                "HEDIS_SHEET_ID", "StarGuard_HEDIS_Gap_Tracker"
            )
            try:
                workbook = self.client.open(sheet_id)
            except gspread.SpreadsheetNotFound:
                workbook = self.client.create(sheet_id)

            self.sheet = workbook.sheet1
            self._ensure_headers()
            self.connected = True
            self.record_count = max(0, len(self.sheet.get_all_values()) - 1)

        except Exception as e:
            self.connected = False
            self.last_error = str(e)

    def _ensure_headers(self):
        if not self.sheet.row_values(1):
            self.sheet.insert_row(HEDIS_COLUMNS, index=1)

    def status(self) -> dict:
        return {
            "connected": self.connected,
            "error": self.last_error,
            "record_count": self.record_count,
            "timestamp": datetime.now().strftime("%H:%M:%S EST")
        }


# ─────────────────────────────────────────────────────────────
# HEDIS GAP OPERATIONS
# ─────────────────────────────────────────────────────────────

def push_hedis_gap(db: HedisGapDB, record: dict) -> dict:
    """
    Push a single HEDIS gap record to Google Sheets.

    record keys:
        member_id, member_name, measure_code, gap_status,
        due_date, provider_name, intervention_type,
        star_impact, roi_estimate, claude_recommendation
    """
    if not db.connected:
        return {"success": False, "error": f"Cloud disconnected: {db.last_error}"}

    try:
        now = datetime.now()
        gap_id = f"GAP-{now.strftime('%Y%m%d-%H%M%S')}"
        measure_code = record.get("measure_code", "")
        measure_name, care_domain = HEDIS_MEASURES.get(
            measure_code, (record.get("measure_name", ""), "Effectiveness")
        )

        row = [
            gap_id,
            now.strftime("%Y-%m-%d %H:%M:%S"),
            record.get("member_id", ""),
            record.get("member_name", ""),
            measure_code,
            measure_name,
            care_domain,
            record.get("gap_status", "OPEN"),
            record.get("due_date", ""),
            record.get("provider_name", ""),
            record.get("intervention_type", "Outreach"),
            record.get("star_impact", 3),
            record.get("roi_estimate", 0.0),
            record.get("claude_recommendation", "")[:500],
            now.strftime("%Y-%m-%d %H:%M:%S")
        ]

        db.sheet.append_row(row)
        db.record_count += 1

        return {
            "success": True,
            "gap_id": gap_id,
            "timestamp": now.strftime("%H:%M:%S EST"),
            "measure_name": measure_name
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_hedis_gaps(
    db: HedisGapDB,
    n: int = 15,
    filter_status: str = "ALL",
    filter_measure: str = "ALL"
) -> pd.DataFrame:
    """
    Pull gap records with optional filters.
    filter_status: ALL | OPEN | CLOSED | EXCLUDED
    filter_measure: ALL | CBP | CDC | W34 | etc.
    """
    if not db.connected:
        return pd.DataFrame(columns=HEDIS_COLUMNS)

    try:
        records = db.sheet.get_all_records()
        df = pd.DataFrame(records)
        if df.empty:
            return df

        if filter_status != "ALL":
            df = df[df["gap_status"] == filter_status]
        if filter_measure != "ALL":
            df = df[df["measure_code"] == filter_measure]

        df = df.sort_values("timestamp", ascending=False).head(n)

        display_cols = [
            "gap_id", "member_id", "measure_code", "measure_name",
            "gap_status", "due_date", "star_impact",
            "roi_estimate", "intervention_type"
        ]
        available = [c for c in display_cols if c in df.columns]
        return df[available].reset_index(drop=True)

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


def fetch_gap_summary(db: HedisGapDB) -> dict:
    """
    Aggregate summary stats for the dashboard KPI row.
    Returns: { total, open, closed, avg_star_impact, total_roi }
    """
    if not db.connected:
        return {"total": 0, "open": 0, "closed": 0,
                "avg_star_impact": 0.0, "total_roi": 0.0}
    try:
        records = db.sheet.get_all_records()
        df = pd.DataFrame(records)
        if df.empty:
            return {"total": 0, "open": 0, "closed": 0,
                    "avg_star_impact": 0.0, "total_roi": 0.0}

        return {
            "total": len(df),
            "open": len(df[df["gap_status"] == "OPEN"]),
            "closed": len(df[df["gap_status"] == "CLOSED"]),
            "avg_star_impact": round(
                pd.to_numeric(df["star_impact"], errors="coerce").mean(), 2
            ),
            "total_roi": round(
                pd.to_numeric(df["roi_estimate"], errors="coerce").sum(), 0
            )
        }
    except Exception as e:
        return {"error": str(e)}


def close_hedis_gap(db: HedisGapDB, gap_id: str) -> dict:
    """Mark a gap as CLOSED by gap_id."""
    if not db.connected:
        return {"success": False, "error": "Cloud disconnected"}
    try:
        cell = db.sheet.find(gap_id)
        if not cell:
            return {"success": False, "error": f"{gap_id} not found"}

        status_col  = HEDIS_COLUMNS.index("gap_status") + 1
        updated_col = HEDIS_COLUMNS.index("last_updated") + 1
        db.sheet.update_cell(cell.row, status_col, "CLOSED")
        db.sheet.update_cell(
            cell.row, updated_col,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return {"success": True, "gap_id": gap_id, "status": "CLOSED"}
    except Exception as e:
        return {"success": False, "error": str(e)}
