# intervention_optimizer.py
# ─────────────────────────────────────────────────────────────
# Phase 2: Intervention Portfolio Optimizer — StarGuard Mobile
# Ranks gaps by ROI × Star Impact; suggests optimal intervention mix
# Brand: Purple #4A3E8F | Gold #D4AF37 | Green #10b981
# ─────────────────────────────────────────────────────────────

from shiny import ui
import pandas as pd
from typing import Optional

try:
    from hedis_gap_trail import HedisGapDB, fetch_hedis_gaps, apply_gap_suppression_filter
except ImportError:
    HedisGapDB = None
    fetch_hedis_gaps = None
    apply_gap_suppression_filter = lambda df: df


def intervention_optimizer_css() -> ui.tags.style:
    return ui.tags.style("""
        .intervention-optimizer { padding: 16px; }
        .optimizer-score { color: #D4AF37; font-weight: 700; }
        .optimizer-priority { color: #10b981; }
    """)


def compute_priority_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute intervention priority: (star_impact/5) * (1 + roi_estimate/1000)
    Higher = prioritize first.
    """
    if df.empty or "star_impact" not in df.columns:
        return df
    df = df.copy()
    star = pd.to_numeric(df["star_impact"], errors="coerce").fillna(3)
    roi = pd.to_numeric(df.get("roi_estimate", 0), errors="coerce").fillna(0)
    df["priority_score"] = (star / 5.0) * (1.0 + roi / 1000.0)
    return df.sort_values("priority_score", ascending=False)


def intervention_optimizer_panel(gap_db: Optional[HedisGapDB] = None) -> ui.div:
    """
    Drop-in panel for StarGuard Mobile: shows top interventions by priority.
    Pass gap_db if connected; otherwise shows placeholder.
    """
    return ui.div(
        intervention_optimizer_css(),
        ui.div("🎯 Intervention Portfolio Optimizer", class_="hedis-panel-title"),
        ui.p("Top gaps by ROI × Star Impact (suppression applied)", class_="text-muted"),
        ui.output_ui("intervention_optimizer_table"),
        ui.output_text("intervention_optimizer_status"),
        class_="intervention-optimizer"
    )
