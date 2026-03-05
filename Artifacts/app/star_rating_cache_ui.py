# star_rating_cache_ui.py
# ─────────────────────────────────────────────────────────────
# Star Rating Forecast Cache UI — StarGuard Desktop + Mobile
# ─────────────────────────────────────────────────────────────

from shiny import ui


def star_cache_css() -> ui.tags.style:
    return ui.tags.style("""
        .star-cache-panel {
            background: #0f0a2e;
            border: 1px solid #4A3E8F;
            border-radius: 10px;
            padding: 20px;
            margin-top: 16px;
        }
        .star-cache-title {
            color: #D4AF37;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }
        .forecast-hero {
            background: linear-gradient(135deg, #1a1240 0%, #2d1f6e 100%);
            border: 1px solid #4A3E8F;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 16px;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 16px;
            align-items: center;
        }
        .forecast-hero-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
        .forecast-hero-value { font-size: 36px; font-weight: 900; color: #D4AF37; line-height: 1; }
        .forecast-hero-sub { font-size: 11px; color: #64748b; margin-top: 4px; }
        .forecast-delta-pos { color: #10b981; font-size: 22px; font-weight: 800; }
        .forecast-delta-neg { color: #f87171; font-size: 22px; font-weight: 800; }
        .forecast-delta-neu { color: #94a3b8; font-size: 22px; font-weight: 800; }
        .cache-banner-fresh { background: #0d2a1a; border: 1px solid #10b981; border-radius: 8px; padding: 10px 16px; font-size: 12px; color: #10b981; font-weight: 600; margin-bottom: 12px; }
        .cache-banner-stale { background: #2a1a0d; border: 1px solid #f59e0b; border-radius: 8px; padding: 10px 16px; font-size: 12px; color: #f59e0b; font-weight: 600; margin-bottom: 12px; }
        .cache-banner-empty { background: #1a1a2e; border: 1px solid #4A3E8F44; border-radius: 8px; padding: 10px 16px; font-size: 12px; color: #94a3b8; margin-bottom: 12px; }
        .star-kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-bottom: 16px; }
        .star-kpi-card { background: #1a1240; border: 1px solid #4A3E8F44; border-radius: 8px; padding: 12px; text-align: center; }
        .star-kpi-value { font-size: 22px; font-weight: 800; color: #D4AF37; line-height: 1; }
        .star-kpi-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
        .star-kpi-delta-pos .star-kpi-value { color: #10b981; }
        .star-kpi-delta-neg .star-kpi-value { color: #f87171; }
        .conf-high { background:#1a3a2a; color:#10b981; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700; }
        .conf-medium { background:#1e3a5f; color:#60a5fa; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700; }
        .conf-low { background:#2a1a1a; color:#f87171; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700; }
        .cache-push-success { color:#10b981; font-size:12px; font-weight:600; margin-top:8px; }
        .cache-push-error { color:#f87171; font-size:12px; margin-top:8px; }
        .cache-sync-row { display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#94a3b8; margin-bottom:12px; }
        @media (max-width: 600px) {
            .forecast-hero { grid-template-columns: 1fr 1fr; }
            .forecast-hero-value { font-size: 28px; }
            .star-kpi-row { grid-template-columns: repeat(2, 1fr); }
        }
    """)


def star_rating_cache_panel() -> ui.div:
    return ui.div(
        star_cache_css(),
        ui.div("⭐ Star Rating Forecast Cache", class_="star-cache-title"),
        ui.div(
            ui.output_text("star_cache_sync_status"),
            ui.input_action_button("btn_refresh_cache", "↻ Refresh", class_="btn btn-sm btn-outline-secondary"),
            class_="cache-sync-row"
        ),
        ui.output_ui("cache_freshness_banner"),
        ui.output_ui("forecast_hero_card"),
        ui.output_ui("star_cache_kpi_row"),
        ui.card(
            ui.card_header("Run & Cache New Forecast"),
            ui.layout_columns(
                ui.input_text("fcst_contract_id", "Contract ID", placeholder="e.g. H1234"),
                ui.input_text("fcst_plan_name", "Plan Name", placeholder="e.g. BlueCare Medicare Advantage"),
                col_widths=[4, 8]
            ),
            ui.layout_columns(
                ui.input_numeric("fcst_year", "Measurement Year", value=2026, min=2020, max=2030),
                ui.input_numeric("fcst_current", "Current Stars", value=3.5, min=1.0, max=5.0, step=0.5),
                ui.input_numeric("fcst_projected", "Projected Stars", value=4.0, min=1.0, max=5.0, step=0.5),
                col_widths=[4, 4, 4]
            ),
            ui.layout_columns(
                ui.input_text("fcst_top_gap", "Top Gap Measure", placeholder="e.g. CBP"),
                ui.input_numeric("fcst_gaps_open", "Gaps Open", value=0, min=0),
                ui.input_numeric("fcst_gaps_closed", "Gaps Closed", value=0, min=0),
                col_widths=[4, 4, 4]
            ),
            ui.layout_columns(
                ui.input_numeric("fcst_hedis_rate", "HEDIS Completion Rate", value=0.75, min=0.0, max=1.0, step=0.01),
                ui.input_numeric("fcst_hcc", "HCC Risk Score", value=1.0, min=0.0, max=5.0, step=0.01),
                ui.input_numeric("fcst_cahps", "CAHPS Score", value=80.0, min=0.0, max=100.0, step=0.1),
                col_widths=[4, 4, 4]
            ),
            ui.layout_columns(
                ui.input_numeric("fcst_roi", "ROI Projection ($)", value=0, min=0, step=1000),
                ui.input_select("fcst_confidence", "Confidence Level", choices=["HIGH", "MEDIUM", "LOW"]),
                col_widths=[6, 6]
            ),
            ui.input_text_area("fcst_narrative", "Claude AI Forecast Narrative",
                placeholder="Paste Claude-generated forecast summary here...", rows=3),
            ui.input_action_button("btn_cache_forecast", "⭐ Cache Forecast to Cloud",
                class_="btn btn-primary w-100", style="background:#4A3E8F; border-color:#4A3E8F;"),
            ui.output_ui("cache_push_result"),
        ),
        ui.card(
            ui.card_header("Forecast History"),
            ui.layout_columns(
                ui.input_text("fcst_filter_contract", "Filter by Contract ID", placeholder="Leave blank for all"),
                ui.input_action_button("btn_load_history", "Load History", class_="btn btn-sm btn-secondary"),
                col_widths=[8, 4]
            ),
            ui.output_data_frame("forecast_history_table"),
        ),
        class_="star-cache-panel"
    )
