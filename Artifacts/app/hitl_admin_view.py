# hitl_admin_view.py
# ─────────────────────────────────────────────────────────────
# Phase 2: HITL Admin View — StarGuard Mobile (gap suppressions)
# Human-in-the-loop: manage gap suppression rules
# Brand: Purple #4A3E8F | Gold #D4AF37
# ─────────────────────────────────────────────────────────────

from htmltools import Tag
from shiny import ui
from hedis_gap_trail import (
    get_gap_suppressions,
    add_gap_suppression,
    remove_gap_suppression,
)


def hitl_admin_css() -> Tag:
    return ui.tags.style("""
        .hitl-admin { padding: 20px; }
        .hitl-rule-row { margin-bottom: 10px; padding: 10px; background: #1a1240; border-radius: 6px; }
    """)


def hitl_admin_panel(app_type: str = "gap") -> Tag:
    """HITL Admin View panel for StarGuard Mobile (gap suppressions only)."""
    return ui.div(
        hitl_admin_css(),
        ui.h4("[Admin] HITL Admin View - Gap Suppressions"),
        ui.p("Manage suppression rules for HEDIS gap records.", class_="text-muted"),
        ui.card(
            ui.card_header("Add Suppression"),
            ui.layout_columns(
                ui.input_text("hitl_gap_id", "Gap ID", placeholder="e.g. GAP-20260304-104512"),
                ui.input_text("hitl_gap_reason", "Reason", placeholder="e.g. Member deceased"),
                col_widths=[6, 6]
            ),
            ui.input_action_button("btn_add_gap_suppression", "Add Suppression", class_="btn-warning btn-sm"),
            ui.output_ui("hitl_gap_add_result"),
        ),
        ui.card(
            ui.card_header("Active Suppression Rules"),
            ui.output_ui("hitl_gap_rules_list"),
            ui.input_action_button("btn_refresh_hitl_gap", "Refresh", class_="btn-sm mt-2"),
        ),
        ui.card(
            ui.card_header("Remove Suppression"),
            ui.layout_columns(
                ui.input_text("hitl_gap_remove_id", "Gap ID to Un-suppress", placeholder="e.g. GAP-20260304-104512"),
                ui.input_action_button("btn_remove_gap_suppression", "Remove", class_="btn-success btn-sm"),
                col_widths=[8, 4]
            ),
            ui.output_ui("hitl_gap_remove_result"),
        ),
        class_="hitl-admin"
    )
