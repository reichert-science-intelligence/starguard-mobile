"""
StarGuard AI Mobile - Medicare Advantage Intelligence Platform
Main application entry point with hamburger menu sidebar navigation
"""

from pathlib import Path
import pandas as pd
from shiny import App, ui, render, reactive
from utils.theme_config import get_theme, get_mobile_css, get_mobile_meta
from cloud_status_badge import cloud_status_css, cloud_status_badge, provenance_footer
from hedis_gap_trail import HedisGapDB, push_hedis_gap, fetch_hedis_gaps, fetch_gap_summary, close_hedis_gap
from hedis_gap_ui import hedis_gap_panel
from star_rating_cache import (
    StarRatingCacheDB, cache_forecast,
    fetch_latest_forecast, fetch_forecast_history,
    fetch_cache_summary, star_label
)
from star_rating_cache_ui import star_rating_cache_panel
from pages.star_predictor import star_predictor_ui, star_predictor_server
from pages.hedis_analyzer import hedis_analyzer_ui, hedis_analyzer_server
from pages.ai_validation import ai_validation_ui, ai_validation_server
from pages.risk_stratification import risk_stratification_ui, risk_stratification_server
from pages.roi_portfolio_optimizer import roi_portfolio_optimizer_ui, roi_portfolio_optimizer_server
from pages.care_gap_workflow import care_gap_workflow_ui, care_gap_workflow_server
from pages.executive_dashboard import executive_dashboard_ui, executive_dashboard_server
from pages.provider_scorecard import provider_scorecard_ui, provider_scorecard_server
from pages.model_monitor import model_monitor_ui, model_monitor_server
from pages.member_profile import member_profile_ui, member_profile_server


def navigation_bar():
    """
    Create mobile-optimized navigation header with hamburger menu sidebar.

    Returns:
        Navigation UI component with header and sidebar
    """
    return ui.div(
        # Top header bar with branding
        ui.div(
            ui.div(
                ui.h1(
                    "StarGuard AI",
                    style="color: white; font-size: 1.5rem; margin: 0; font-weight: 700; letter-spacing: -0.5px;"
                ),
                ui.p(
                    "Medicare Advantage Intelligence",
                    style="color: rgba(255,255,255,0.85); font-size: 0.875rem; margin: 0.25rem 0 0 0; font-weight: 400;"
                ),
            ),
            class_="navbar"
        ),
        # Hamburger menu button (mobile only)
        ui.div(
            ui.div(
                ui.tags.span(),
                ui.tags.span(),
                ui.tags.span(),
                class_="hamburger-icon"
            ),
            id="menu-toggle",
            class_="menu-toggle",
            onclick="toggleSidebar()"
        ),
        # Sidebar overlay (darkens background when open)
        ui.div(
            id="sidebar-overlay",
            class_="sidebar-overlay",
            onclick="toggleSidebar()"
        ),
        # Sidebar navigation
        ui.div(
            ui.div(
                ui.tags.h2("Navigation"),
                ui.tags.p("Select a page"),
                class_="sidebar-header"
            ),
            ui.div(
                ui.div(
                    "📊 Executive Dashboard",
                    class_="sidebar-nav-item active",
                    id="nav-dashboard",
                    onclick="navigateTo('dashboard')"
                ),
                ui.div(
                    "⭐ Star Rating Predictor",
                    class_="sidebar-nav-item",
                    id="nav-star",
                    onclick="navigateTo('star')"
                ),
                ui.div(
                    "⭐ Star Forecast Cache",
                    class_="sidebar-nav-item",
                    id="nav-starcache",
                    onclick="navigateTo('starcache')"
                ),
                ui.div(
                    "📊 HEDIS Gap Analyzer",
                    class_="sidebar-nav-item",
                    id="nav-hedis",
                    onclick="navigateTo('hedis')"
                ),
                ui.div(
                    "📊 HEDIS Gaps (Cloud)",
                    class_="sidebar-nav-item",
                    id="nav-hedisgaps",
                    onclick="navigateTo('hedisgaps')"
                ),
                ui.div(
                    "📊 Member Risk Stratification",
                    class_="sidebar-nav-item",
                    id="nav-risk",
                    onclick="navigateTo('risk')"
                ),
                ui.div(
                    "💰 ROI Portfolio Optimizer",
                    class_="sidebar-nav-item",
                    id="nav-roi",
                    onclick="navigateTo('roi')"
                ),
                ui.div(
                    "📋 Care Gap Closure Workflow",
                    class_="sidebar-nav-item",
                    id="nav-workflow",
                    onclick="navigateTo('workflow')"
                ),
                ui.div(
                    "👨‍⚕️ Provider Scorecard",
                    class_="sidebar-nav-item",
                    id="nav-providers",
                    onclick="navigateTo('providers')"
                ),
                ui.div(
                    "👤 Member 360° Profile",
                    class_="sidebar-nav-item",
                    id="nav-profile",
                    onclick="navigateTo('profile')"
                ),
                ui.div(
                    "🤖 AI Validation Dashboard",
                    class_="sidebar-nav-item",
                    id="nav-ai",
                    onclick="navigateTo('ai')"
                ),
                ui.div(
                    "🤖 Model Monitor",
                    class_="sidebar-nav-item",
                    id="nav-monitor",
                    onclick="navigateTo('monitor')"
                ),
                ui.div(
                    "ℹ️ About",
                    class_="sidebar-nav-item",
                    id="nav-about",
                    onclick="navigateTo('about')"
                ),
                ui.div(
                    "📋 Services & Pricing",
                    class_="sidebar-nav-item",
                    id="nav-services",
                    onclick="navigateTo('services')"
                ),
                class_="sidebar-nav"
            ),
            ui.div(
                ui.tags.hr(style="margin: 1rem 1.5rem; border-color: #e0e0e0;"),
                ui.div(
                    ui.tags.small(
                        "StarGuard AI v1.0",
                        style="display: block; text-align: center; color: #999; font-size: 0.75rem;"
                    ),
                    style="padding: 0 1.5rem 1rem 1.5rem;"
                )
            ),
            id="nav-sidebar",
            class_="nav-sidebar"
        ),
        # Navigation tabs (desktop only - hidden on mobile)
        ui.div(
            ui.input_radio_buttons(
                "page_nav",
                "",
                choices={
                    "dashboard": "📊 Executive",
                    "star": "⭐ Star Ratings",
                    "starcache": "⭐ Star Cache",
                    "hedis": "📊 HEDIS Gap Analyzer",
                    "hedisgaps": "📊 HEDIS Gaps (Cloud)",
                    "risk": "📊 Risk Strat",
                    "roi": "💰 ROI Portfolio",
                    "workflow": "📋 Workflow",
                    "providers": "👨‍⚕️ Providers",
                    "profile": "👤 Member 360°",
                    "ai": "🤖 AI Validation",
                    "monitor": "🤖 ML Monitor",
                    "about": "ℹ️ About",
                    "services": "📋 Services"
                },
                selected="dashboard",
                inline=True
            ),
            class_="nav-tabs-container"
        ),
        # JavaScript for sidebar functionality
        ui.tags.script("""
            function toggleSidebar() {
                const sidebar = document.getElementById('nav-sidebar');
                const overlay = document.getElementById('sidebar-overlay');
                const toggle = document.getElementById('menu-toggle');

                sidebar.classList.toggle('active');
                overlay.classList.toggle('active');
                toggle.classList.toggle('active');
            }

            function navigateTo(page) {
                if (typeof Shiny !== 'undefined') {
                    Shiny.setInputValue('page_nav', page);
                }
                document.querySelectorAll('.sidebar-nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                const navEl = document.getElementById('nav-' + page);
                if (navEl) navEl.classList.add('active');
                toggleSidebar();
            }
        """)
    )


# HEDIS Gap cloud persistence — Google Sheets
hedis_db = HedisGapDB()

# Star Rating Forecast cache — Google Sheets
star_cache_db = StarRatingCacheDB()


def footer():
    """Footer with contact info."""
    return ui.div(
        ui.tags.hr(style="margin: 2rem 0 1rem 0; border-color: #e0e0e0;"),
        ui.div(
            ui.markdown("""
            **StarGuard AI** | Built by Robert Reichert  
            [LinkedIn](https://www.linkedin.com/in/robertreichert-healthcareai/) | [Portfolio](https://tinyurl.com/bdevpdz5)
            """),
            style="text-align: center; padding: 1rem; color: #666; font-size: 0.875rem;"
        )
    )


# Placeholder page content until real pages are added
def placeholder_page(title, emoji):
    return ui.div(
        ui.div(title, class_="card-header"),
        ui.div(
            ui.p(f"{emoji} {title} - Page content will go here when implemented."),
            class_="card-body"
        ),
        class_="card"
    )


app_ui = ui.page_fluid(
    ui.tags.head(
        ui.HTML(get_mobile_meta()),
        ui.HTML(get_mobile_css())
    ),
    ui.head_content(
        cloud_status_css(),
        ui.tags.script("""
            (function(){
                if (typeof Shiny !== 'undefined') {
                    Shiny.addCustomMessageHandler('gap_show_loading', function(msg) {
                        var ta = document.getElementById('gap_claude_rec') || document.querySelector('textarea[id$="gap_claude_rec"]');
                        if (ta) ta.value = '⏳ Claude is generating...';
                    });
                    Shiny.addCustomMessageHandler('gap_set_rec', function(msg) {
                        var v = (msg && msg.value) || msg || '';
                        var ta = document.getElementById('gap_claude_rec') || document.querySelector('textarea[id$="gap_claude_rec"]');
                        if (ta) ta.value = v;
                        try { Shiny.setInputValue('gap_claude_rec', v); } catch(e) {}
                    });
                }
            })();
        """),
        ui.tags.style("""
            /* Mobile badge compaction — fits smaller screens */
            .cloud-badge-panel {
                padding: 8px 12px !important;
                margin-bottom: 10px !important;
            }
            .cloud-badge-row {
                font-size: 11px !important;
            }
            .cloud-badge-title {
                font-size: 10px !important;
            }
            .provenance-footer {
                flex-direction: column !important;
                gap: 2px !important;
                font-size: 10px !important;
                padding: 4px 12px !important;
                text-align: center !important;
            }
        """)
    ),
    navigation_bar(),
    cloud_status_badge(app_variant="starguard", layout="strip"),
    ui.output_ui("page_content"),
    footer(),
    provenance_footer(app_variant="starguard"),
    theme=get_theme(),
    title="StarGuard AI - Medicare Advantage Intelligence"
)


def server(input, output, session):
    get_page = lambda: input.page_nav()
    star_predictor_server(input, output, session, get_current_page=get_page)

    # ── HEDIS Gap Refresh (Google Sheets cloud) ───
    _gap_push_result = reactive.Value(None)
    _gap_close_result = reactive.Value(None)

    @output
    @render.text
    def hedis_sync_status():
        if input.page_nav() != "hedisgaps":
            return ""
        s = hedis_db.status()
        if s["connected"]:
            return f"☁ Cloud Live — {s['record_count']} gaps — {s['timestamp']}"
        return f"⚠ Disconnected — {s.get('error', 'No credentials')}"

    @output
    @render.ui
    def hedis_kpi_cards():
        if input.page_nav() != "hedisgaps":
            return ui.div()
        input.btn_refresh_gaps()
        input.btn_push_gap()
        s = fetch_gap_summary(hedis_db)
        if "error" in s:
            return ui.div(f"⚠ {s['error']}", style="color:#f87171;font-size:12px;")
        return ui.div(
            ui.div(ui.div(str(s["total"]), class_="kpi-value"), ui.div("Total Gaps", class_="kpi-label"), class_="kpi-card"),
            ui.div(ui.div(str(s["open"]), class_="kpi-value"), ui.div("Open", class_="kpi-label"), class_="kpi-card kpi-open"),
            ui.div(ui.div(str(s["closed"]), class_="kpi-value"), ui.div("Closed", class_="kpi-label"), class_="kpi-card kpi-closed"),
            ui.div(ui.div(str(s["avg_star_impact"]), class_="kpi-value"), ui.div("Avg Star Impact", class_="kpi-label"), class_="kpi-card"),
            ui.div(ui.div(f"${s['total_roi']:,.0f}", class_="kpi-value"), ui.div("Est. ROI", class_="kpi-label"), class_="kpi-card kpi-roi"),
            class_="kpi-row"
        )


    @reactive.effect
    @reactive.event(input.btn_generate_gap_rec)
    def _generate_gap_rec():
        if input.page_nav() != "hedisgaps":
            return
        session.send_custom_message("gap_show_loading", {})
        try:
            import anthropic
            client = anthropic.Anthropic()
            member_id = input.gap_member_id() or "N/A"
            member_name = input.gap_member_name() or "N/A"
            measure_code = input.gap_measure_code() or "N/A"
            intervention = input.gap_intervention() or "Outreach"
            star_impact = input.gap_star_impact() or 3
            prompt = f"""Generate a concise care gap recommendation (2-4 sentences) for:
Member: {member_id} — {member_name}
HEDIS Measure: {measure_code}
Intervention: {intervention}
Star Impact: {star_impact}

Write a practical, actionable recommendation for closing this gap. Return only the text, no preamble."""
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            rec = resp.content[0].text.strip() if resp.content else ""
            ui.update_text_area("gap_claude_rec", value=rec)
        except Exception as e:
            err_msg = str(e)
            if "ANTHROPIC" in err_msg.upper() or "api_key" in err_msg.lower():
                err_msg = "ANTHROPIC_API_KEY not set. Add to .env or Space secrets."
            ui.update_text_area("gap_claude_rec", value=f"Error: {err_msg}")

    @reactive.effect
    @reactive.event(input.btn_push_gap)
    def _push_gap():
        if input.page_nav() != "hedisgaps":
            return
        record = {
            "member_id": input.gap_member_id() or "",
            "member_name": input.gap_member_name() or "",
            "measure_code": input.gap_measure_code() or "",
            "gap_status": input.gap_status() or "OPEN",
            "due_date": input.gap_due_date() or "",
            "provider_name": input.gap_provider() or "",
            "intervention_type": input.gap_intervention() or "Outreach",
            "star_impact": input.gap_star_impact() or 3,
            "roi_estimate": input.gap_roi() or 0,
            "claude_recommendation": input.gap_claude_rec() or "",
        }
        _gap_push_result.set(push_hedis_gap(hedis_db, record))

    @output
    @render.ui
    def gap_push_result():
        if input.page_nav() != "hedisgaps":
            return ui.div()
        r = _gap_push_result()
        if r is None:
            return ui.div()
        if r.get("success"):
            return ui.div(f"✅ {r.get('gap_id', '')} pushed — {r.get('measure_name', '')} — {r.get('timestamp', '')}", class_="gap-push-success")
        return ui.div(f"❌ {r.get('error', '')}", class_="gap-push-error")

    @output
    @render.data_frame
    def hedis_gap_table():
        input.btn_refresh_gaps()
        input.btn_push_gap()
        input.btn_close_gap()
        return render.DataGrid(
            fetch_hedis_gaps(hedis_db, n=15,
                filter_status=input.gap_filter_status() or "ALL",
                filter_measure=input.gap_filter_measure() or "ALL"),
            width="100%", height="320px"
        )

    @reactive.effect
    @reactive.event(input.btn_close_gap)
    def _close_gap():
        r = close_hedis_gap(hedis_db, input.gap_id_close() or "")
        _gap_close_result.set(r)

    @output
    @render.ui
    def gap_close_result():
        if input.page_nav() != "hedisgaps":
            return ui.div()
        r = _gap_close_result()
        if r is None:
            return ui.div()
        if r.get("success"):
            return ui.div(f"✅ {r.get('gap_id', '')} → CLOSED", class_="gap-push-success")
        return ui.div(f"❌ {r.get('error', '')}", class_="gap-push-error")

    # ── Star Rating Forecast Cache (Google Sheets) ───
    _cache_push_val = reactive.Value(None)

    @output
    @render.text
    def star_cache_sync_status():
        if input.page_nav() != "starcache":
            return ""
        s = star_cache_db.status()
        if s["connected"]:
            return f"☁ Cache Live — {s['cache_count']} forecasts — Last run: {s['last_cached_at']} — {s['timestamp']}"
        return f"⚠ Disconnected — {s.get('error', 'No credentials')}"

    @output
    @render.ui
    def cache_freshness_banner():
        if input.page_nav() != "starcache":
            return ui.div()
        input.btn_refresh_cache()
        input.btn_cache_forecast()
        latest = fetch_latest_forecast(star_cache_db)
        if latest is None:
            return ui.div("📭 No forecasts cached yet — run your first forecast below.", class_="cache-banner-empty")
        return ui.div(f"✅ FRESH — {latest.get('plan_name', '')} ({latest.get('contract_id', '')}) — {latest.get('timestamp', '')}", class_="cache-banner-fresh")

    @output
    @render.ui
    def forecast_hero_card():
        if input.page_nav() != "starcache":
            return ui.div()
        input.btn_refresh_cache()
        input.btn_cache_forecast()
        latest = fetch_latest_forecast(star_cache_db)
        if latest is None:
            return ui.div()
        current = float(latest.get("current_star_rating", 0))
        projected = float(latest.get("projected_star_rating", 0))
        delta = float(latest.get("star_delta", 0))
        conf = latest.get("confidence_level", "MEDIUM").lower()
        _, proj_color, proj_label = star_label(projected)
        if delta > 0:
            delta_html = ui.span(f"+{delta:.1f} ▲", class_="forecast-delta-pos")
        elif delta < 0:
            delta_html = ui.span(f"{delta:.1f} ▼", class_="forecast-delta-neg")
        else:
            delta_html = ui.span("→ No Change", class_="forecast-delta-neu")
        return ui.div(
            ui.div(ui.div("Current Rating", class_="forecast-hero-label"),
                  ui.div(f"{current:.1f}★", class_="forecast-hero-value", style="color:#94a3b8;"),
                  ui.div(star_label(current)[2], class_="forecast-hero-sub")),
            ui.div(ui.div("Projected Rating", class_="forecast-hero-label"),
                  ui.div(f"{projected:.1f}★", class_="forecast-hero-value", style=f"color:{proj_color};"),
                  ui.div(proj_label, class_="forecast-hero-sub")),
            ui.div(ui.div("Star Delta", class_="forecast-hero-label"), delta_html,
                  ui.div(ui.span(latest.get("confidence_level", ""), class_=f"conf-{conf}"),
                        class_="forecast-hero-sub", style="margin-top:6px;")),
            class_="forecast-hero"
        )

    @output
    @render.ui
    def star_cache_kpi_row():
        if input.page_nav() != "starcache":
            return ui.div()
        input.btn_refresh_cache()
        input.btn_cache_forecast()
        s = fetch_cache_summary(star_cache_db)
        if not s or "error" in s:
            return ui.div()
        delta_class = "star-kpi-delta-pos" if s.get("avg_delta", 0) >= 0 else "star-kpi-delta-neg"
        delta_prefix = "+" if s.get("avg_delta", 0) >= 0 else ""
        return ui.div(
            ui.div(ui.div(str(s.get("total", 0)), class_="star-kpi-value"), ui.div("Total Cached", class_="star-kpi-label"), class_="star-kpi-card"),
            ui.div(ui.div(str(s.get("fresh", 0)), class_="star-kpi-value"), ui.div("Fresh", class_="star-kpi-label"), class_="star-kpi-card"),
            ui.div(ui.div(f"{s.get('avg_projected', 0):.2f}★", class_="star-kpi-value"), ui.div("Avg Projected", class_="star-kpi-label"), class_="star-kpi-card"),
            ui.div(ui.div(f"{delta_prefix}{s.get('avg_delta', 0):.2f}", class_="star-kpi-value"), ui.div("Avg Star Δ", class_="star-kpi-label"), class_=f"star-kpi-card {delta_class}"),
            ui.div(ui.div(str(s.get("last_run", "—"))[:10], class_="star-kpi-value", style="font-size:14px;"), ui.div("Last Run", class_="star-kpi-label"), class_="star-kpi-card"),
            class_="star-kpi-row"
        )

    @reactive.effect
    @reactive.event(input.btn_cache_forecast)
    def _cache_forecast():
        if input.page_nav() != "starcache":
            return
        forecast = {
            "contract_id": input.fcst_contract_id() or "",
            "plan_name": input.fcst_plan_name() or "",
            "measurement_year": input.fcst_year() or 2026,
            "current_star_rating": input.fcst_current() or 3.5,
            "projected_star_rating": input.fcst_projected() or 4.0,
            "top_gap_measure": input.fcst_top_gap() or "",
            "gaps_open": input.fcst_gaps_open() or 0,
            "gaps_closed": input.fcst_gaps_closed() or 0,
            "hedis_completion_rate": input.fcst_hedis_rate() or 0.75,
            "hcc_risk_score": input.fcst_hcc() or 1.0,
            "cahps_score": input.fcst_cahps() or 80.0,
            "roi_projection": input.fcst_roi() or 0,
            "confidence_level": input.fcst_confidence() or "MEDIUM",
            "claude_narrative": input.fcst_narrative() or "",
            "cached_by": "StarGuard AI — Robert Reichert"
        }
        _cache_push_val.set(cache_forecast(star_cache_db, forecast))

    @output
    @render.ui
    def cache_push_result():
        if input.page_nav() != "starcache":
            return ui.div()
        r = _cache_push_val()
        if r is None:
            return ui.div()
        if r.get("success"):
            delta_str = f"+{r['star_delta']}" if r['star_delta'] >= 0 else str(r['star_delta'])
            return ui.div(f"✅ {r.get('forecast_id', '')} cached — Star Δ {delta_str} — {r.get('timestamp', '')}", class_="cache-push-success")
        return ui.div(f"❌ {r.get('error', '')}", class_="cache-push-error")

    @output
    @render.data_frame
    def forecast_history_table():
        if input.page_nav() != "starcache":
            return render.DataGrid(pd.DataFrame(), width="100%", height="300px")
        input.btn_load_history()
        input.btn_cache_forecast()
        return render.DataGrid(
            fetch_forecast_history(star_cache_db, contract_id=input.fcst_filter_contract() or "", n=12),
            width="100%", height="300px"
        )

    hedis_analyzer_server(input, output, session, get_current_page=get_page)
    ai_validation_server(input, output, session, get_current_page=get_page)
    risk_stratification_server(input, output, session, get_current_page=get_page)
    roi_portfolio_optimizer_server(input, output, session, get_current_page=get_page)
    care_gap_workflow_server(input, output, session, get_current_page=get_page)
    executive_dashboard_server(input, output, session, get_current_page=get_page)
    provider_scorecard_server(input, output, session, get_current_page=get_page)
    model_monitor_server(input, output, session, get_current_page=get_page)
    member_profile_server(input, output, session, get_current_page=get_page)

    @output
    @render.ui
    def page_content():
        page = input.page_nav()
        if page == "star":
            return ui.div(star_predictor_ui(), id="star-predictor-page")
        elif page == "hedis":
            return ui.div(hedis_analyzer_ui(), id="hedis-analyzer-page")
        elif page == "hedisgaps":
            return ui.div(hedis_gap_panel(), id="hedis-gaps-cloud-page")
        elif page == "starcache":
            return ui.div(star_rating_cache_panel(), id="star-cache-page")
        elif page == "ai":
            return ui.div(ai_validation_ui(), id="ai-validation-page")
        elif page == "risk":
            return ui.div(risk_stratification_ui(), id="risk-stratification-page")
        elif page == "roi":
            return ui.div(roi_portfolio_optimizer_ui(), id="roi-portfolio-page")
        elif page == "workflow":
            return ui.div(care_gap_workflow_ui(), id="workflow-page")
        elif page == "dashboard":
            return ui.div(executive_dashboard_ui(), id="dashboard-page")
        elif page == "providers":
            return ui.div(provider_scorecard_ui(), id="providers-page")
        elif page == "monitor":
            return ui.div(model_monitor_ui(), id="monitor-page")
        elif page == "profile":
            return ui.div(member_profile_ui(), id="profile-page")
        elif page == "about":
            return ui.div(
                ui.tags.iframe(
                    src="/starguard_about.html",
                    width="100%",
                    height="800px",
                    style="border: none; min-height: 600px;",
                    title="About StarGuard AI",
                ),
                style="width: 100%;",
                id="about-page"
            )
        elif page == "services":
            return ui.div(
                ui.tags.iframe(
                    src="/starguard_services.html",
                    width="100%",
                    height="800px",
                    style="border: none; min-height: 600px;",
                    title="Services & Market Insights",
                ),
                style="width: 100%;",
                id="services-page"
            )
        return ui.div(executive_dashboard_ui(), id="dashboard-page")


app_dir = Path(__file__).resolve().parent
app = App(app_ui, server, static_assets=app_dir / "www")
