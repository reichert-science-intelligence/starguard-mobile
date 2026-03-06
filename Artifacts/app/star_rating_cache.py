# star_rating_cache.py
# ─────────────────────────────────────────────────────────────
# Star Rating Forecast Cache — Google Sheets Persistence
# StarGuard Desktop + Mobile | reichert-science-intelligence
# Caches forecast runs with timestamps; signals cloud thinking
# Brand: Purple #4A3E8F | Gold #D4AF37 | Green #10b981
# ─────────────────────────────────────────────────────────────

import os
import json
import gspread
import pandas as pd
from datetime import datetime, timezone, timedelta
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

FORECAST_COLUMNS = [
    "forecast_id", "timestamp", "contract_id", "plan_name",
    "measurement_year", "current_star_rating", "projected_star_rating",
    "star_delta", "top_gap_measure", "gaps_open", "gaps_closed",
    "hedis_completion_rate", "hcc_risk_score", "cahps_score",
    "roi_projection", "confidence_level", "claude_narrative",
    "cache_status", "cached_by", "last_updated"
]

STAR_THRESHOLDS = {
    5.0: ("⭐⭐⭐⭐⭐", "#D4AF37", "Excellent"),
    4.5: ("⭐⭐⭐⭐½",  "#D4AF37", "Superior"),
    4.0: ("⭐⭐⭐⭐",   "#10b981", "Above Average"),
    3.5: ("⭐⭐⭐½",   "#60a5fa", "Average"),
    3.0: ("⭐⭐⭐",    "#f59e0b", "Below Average"),
    0.0: ("⭐⭐",      "#f87171", "Low Performing"),
}


def star_label(rating: float) -> tuple:
    for threshold, info in sorted(STAR_THRESHOLDS.items(), reverse=True):
        if rating >= threshold:
            return info
    return ("⭐", "#f87171", "Low Performing")


class StarRatingCacheDB:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.connected = False
        self.last_error = None
        self.last_cached_at = None
        self.cache_count = 0
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
            sheet_id = os.environ.get("STAR_CACHE_SHEET_ID", "StarGuard_Star_Rating_Cache")
            try:
                wb = self.client.open(sheet_id)
            except gspread.SpreadsheetNotFound:
                wb = self.client.create(sheet_id)
            self.sheet = wb.sheet1
            self._ensure_headers()
            self.connected = True
            rows = self.sheet.get_all_values()
            self.cache_count = max(0, len(rows) - 1)
            if self.cache_count > 0:
                self.last_cached_at = rows[-1][1]
        except Exception as e:
            self.connected = False
            self.last_error = str(e)

    def _ensure_headers(self):
        if not self.sheet.row_values(1):
            self.sheet.insert_row(FORECAST_COLUMNS, index=1)

    def status(self) -> dict:
        return {
            "connected": self.connected, "error": self.last_error,
            "cache_count": self.cache_count,
            "last_cached_at": self.last_cached_at or "No forecasts cached yet",
            "timestamp": datetime.now(timezone(timedelta(hours=-5))).strftime("%I:%M:%S %p EST")
        }


def cache_forecast(db: StarRatingCacheDB, forecast: dict) -> dict:
    if not db.connected:
        return {"success": False, "error": f"Cloud disconnected: {db.last_error}"}
    try:
        _mark_prior_stale(db, forecast.get("contract_id", ""))
        now = datetime.now(timezone(timedelta(hours=-5)))
        forecast_id = f"FCST-{now.strftime('%Y%m%d-%H%M%S')}"
        current = float(forecast.get("current_star_rating", 0))
        projected = float(forecast.get("projected_star_rating", 0))
        row = [
            forecast_id, now.strftime("%Y-%m-%d %H:%M:%S"),
            forecast.get("contract_id", ""), forecast.get("plan_name", ""),
            forecast.get("measurement_year", datetime.now().year),
            current, projected, round(projected - current, 2),
            forecast.get("top_gap_measure", ""), forecast.get("gaps_open", 0),
            forecast.get("gaps_closed", 0), forecast.get("hedis_completion_rate", 0.0),
            forecast.get("hcc_risk_score", 0.0), forecast.get("cahps_score", 0.0),
            forecast.get("roi_projection", 0.0), forecast.get("confidence_level", "MEDIUM"),
            forecast.get("claude_narrative", "")[:500], "FRESH",
            forecast.get("cached_by", "StarGuard AI"), now.strftime("%Y-%m-%d %H:%M:%S")
        ]
        db.sheet.append_row(row)
        db.cache_count += 1
        db.last_cached_at = now.strftime("%Y-%m-%d %H:%M:%S")
        return {"success": True, "forecast_id": forecast_id, "timestamp": now.strftime("%I:%M:%S %p EST"),
                "star_delta": round(projected - current, 2)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _mark_prior_stale(db: StarRatingCacheDB, contract_id: str):
    if not contract_id or not db.connected:
        return
    try:
        records = db.sheet.get_all_records()
        cache_col = FORECAST_COLUMNS.index("cache_status") + 1
        for i, rec in enumerate(records, start=2):
            if rec.get("contract_id") == contract_id and rec.get("cache_status") == "FRESH":
                db.sheet.update_cell(i, cache_col, "STALE")
    except Exception:
        pass


def fetch_latest_forecast(db: StarRatingCacheDB, contract_id: str = ""):
    if not db.connected:
        return None
    try:
        records = db.sheet.get_all_records()
        df = pd.DataFrame(records)
        if df.empty:
            return None
        df = df[df["cache_status"] == "FRESH"]
        if contract_id:
            df = df[df["contract_id"] == contract_id]
        if df.empty:
            return None
        df = df.sort_values("timestamp", ascending=False)
        return df.iloc[0].to_dict()
    except Exception:
        return None


def fetch_forecast_history(db: StarRatingCacheDB, contract_id: str = "", n: int = 12) -> pd.DataFrame:
    if not db.connected:
        return pd.DataFrame()
    try:
        records = db.sheet.get_all_records()
        df = pd.DataFrame(records)
        if df.empty:
            return df
        if contract_id:
            df = df[df["contract_id"] == contract_id]
        df = df.sort_values("timestamp", ascending=True).tail(n)
        cols = ["forecast_id", "timestamp", "contract_id", "plan_name",
                "current_star_rating", "projected_star_rating", "star_delta",
                "confidence_level", "cache_status"]
        available = [c for c in cols if c in df.columns]
        return df[available].reset_index(drop=True)
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


def fetch_cache_summary(db: StarRatingCacheDB) -> dict:
    if not db.connected:
        return {}
    try:
        records = db.sheet.get_all_records()
        df = pd.DataFrame(records)
        if df.empty:
            return {"total": 0, "fresh": 0, "avg_projected": 0.0, "avg_delta": 0.0, "last_run": "Never"}
        fresh = df[df["cache_status"] == "FRESH"]
        return {
            "total": len(df), "fresh": len(fresh),
            "avg_projected": round(pd.to_numeric(fresh["projected_star_rating"], errors="coerce").mean(), 2),
            "avg_delta": round(pd.to_numeric(fresh["star_delta"], errors="coerce").mean(), 2),
            "last_run": df["timestamp"].max()
        }
    except Exception as e:
        return {"error": str(e)}
