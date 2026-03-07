# hedis_gap_ui.py
# ─────────────────────────────────────────────────────────────
# HEDIS Gap Refresh UI — StarGuard Desktop + Mobile
# ─────────────────────────────────────────────────────────────

from shiny import ui

from hedis_gap_trail import HEDIS_MEASURES


def hedis_gap_css() -> ui.tags.style:
    return ui.tags.style("""
        .hedis-panel {
            background: #0f0a2e;
            border: 1px solid #4A3E8F;
            border-radius: 10px;
            padding: 20px;
            margin-top: 16px;
        }
        .hedis-panel-title {
            color: #D4AF37;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-bottom: 16px;
        }
        .kpi-card {
            background: #1a1240;
            border: 1px solid #4A3E8F44;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }
        .kpi-value {
            font-size: 24px;
            font-weight: 800;
            color: #D4AF37;
            line-height: 1;
        }
        .kpi-label {
            font-size: 10px;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 4px;
        }
        .kpi-open  .kpi-value { color: #60a5fa; }
        .kpi-closed .kpi-value { color: #10b981; }
        .kpi-roi   .kpi-value { color: #D4AF37; font-size: 18px; }
        .gap-push-success {
            color: #10b981; font-size: 12px;
            font-weight: 600; margin-top: 8px;
        }
        .gap-push-error {
            color: #f87171; font-size: 12px; margin-top: 8px;
        }
        .hedis-sync-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: #94a3b8;
            margin-bottom: 12px;
        }
        .sync-live { color: #10b981; font-weight: 700; }
    """)


def hedis_gap_panel() -> ui.div:
    """
    Full HEDIS Gap Refresh panel.
    Drop into any StarGuard tab as a nav_panel.
    """
    measure_choices = {
        "": "— Select Measure —",
        **{code: f"{code} — {name}" for code, (name, _) in HEDIS_MEASURES.items()},
    }

    return ui.div(
        hedis_gap_css(),
        # ── Header ──
        ui.div("📊 HEDIS Gap Refresh", class_="hedis-panel-title"),
        ui.div(
            ui.output_text("hedis_sync_status"),
            ui.input_action_button(
                "btn_refresh_gaps", "↻ Refresh Cloud", class_="btn btn-sm btn-outline-secondary"
            ),
            class_="hedis-sync-row",
        ),
        # ── KPI Summary Row ──
        ui.output_ui("hedis_kpi_cards"),
        # ── Push New Gap ──
        ui.card(
            ui.card_header("Push Gap to Cloud"),
            ui.layout_columns(
                ui.input_text("gap_member_id", "Member ID", placeholder="e.g. MBR-00142"),
                ui.input_text("gap_member_name", "Member Name", placeholder="e.g. John Smith"),
                col_widths=[6, 6],
            ),
            ui.layout_columns(
                ui.input_select("gap_measure_code", "HEDIS Measure", choices=measure_choices),
                ui.input_select("gap_status", "Gap Status", choices=["OPEN", "CLOSED", "EXCLUDED"]),
                col_widths=[6, 6],
            ),
            ui.layout_columns(
                ui.input_text("gap_due_date", "Due Date", placeholder="e.g. 2026-12-31"),
                ui.input_text("gap_provider", "Provider Name", placeholder="e.g. Dr. Martinez"),
                col_widths=[6, 6],
            ),
            ui.layout_columns(
                ui.input_select(
                    "gap_intervention",
                    "Intervention Type",
                    choices=["Outreach", "Clinical", "Administrative"],
                ),
                ui.input_numeric("gap_star_impact", "Star Impact (1–5)", value=3, min=1, max=5),
                ui.input_numeric("gap_roi", "ROI Estimate ($)", value=0, min=0, step=100),
                col_widths=[4, 4, 4],
            ),
            ui.div(
                ui.input_action_button(
                    "btn_generate_gap_rec",
                    "🤖 Generate Recommendation",
                    class_="btn btn-outline-primary btn-sm mb-2",
                    style="background:#4A3E8F; color:#fff; border-color:#D4AF37;",
                ),
                class_="gap-generate-row",
            ),
            ui.input_text_area(
                "gap_claude_rec",
                "Claude AI Recommendation",
                placeholder="Fill gap details above, click 🤖 Generate — or paste manually.",
                rows=3,
            ),
            ui.input_action_button(
                "btn_push_gap",
                "☁ Push Gap to Cloud",
                class_="btn btn-primary w-100",
                style="background:#4A3E8F; border-color:#4A3E8F;",
            ),
            ui.output_ui("gap_push_result"),
        ),
        # ── Filter + Table ──
        ui.card(
            ui.card_header("Live Gap Panel"),
            ui.layout_columns(
                ui.input_select(
                    "gap_filter_status",
                    "Filter: Status",
                    choices=["ALL", "OPEN", "CLOSED", "EXCLUDED"],
                ),
                ui.input_select(
                    "gap_filter_measure",
                    "Filter: Measure",
                    choices=["ALL"] + list(HEDIS_MEASURES.keys()),
                ),
                col_widths=[6, 6],
            ),
            ui.output_data_frame("hedis_gap_table"),
        ),
        # ── Close Gap ──
        ui.card(
            ui.card_header("Close a Gap"),
            ui.layout_columns(
                ui.input_text("gap_id_close", "Gap ID", placeholder="e.g. GAP-20260304-104512"),
                ui.input_action_button(
                    "btn_close_gap", "Mark Closed", class_="btn btn-success btn-sm"
                ),
                col_widths=[8, 4],
            ),
            ui.output_ui("gap_close_result"),
        ),
        class_="hedis-panel",
    )
