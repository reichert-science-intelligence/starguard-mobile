"""ROI Portfolio Optimizer - Interactive priority matrix, budget allocation, financial forecasting."""

from shiny import ui, render, reactive
from ..components.mobile_layout import (
    mobile_page,
    mobile_card,
    mobile_input_group,
    mobile_button,
    metric_box,
    info_row,
    alert_box,
    divider,
    progress_bar
)

# 7 HEDIS Measures for portfolio optimization (Impact vs Effort)
# Impact: 1-10 scale from roi_per_point, star_impact, gap. Effort: 1-4 from difficulty
PORTFOLIO_MEASURES = {
    "CCS": {
        "name": "Colorectal Cancer Screening",
        "impact": 7.2,
        "effort": 2,
        "current_rate": 67.3,
        "benchmark": 75.0,
        "roi_per_point": 125000,
        "star_impact": 0.5,
        "population": 8450,
    },
    "HBD": {
        "name": "Hemoglobin A1c Control",
        "impact": 8.1,
        "effort": 3,
        "current_rate": 58.2,
        "benchmark": 70.0,
        "roi_per_point": 95000,
        "star_impact": 0.6,
        "population": 5230,
    },
    "MAD": {
        "name": "Medication Adherence - Diabetes",
        "impact": 6.5,
        "effort": 1,
        "current_rate": 71.5,
        "benchmark": 80.0,
        "roi_per_point": 110000,
        "star_impact": 0.4,
        "population": 4890,
    },
    "BCS": {
        "name": "Breast Cancer Screening",
        "impact": 6.8,
        "effort": 1,
        "current_rate": 73.8,
        "benchmark": 78.0,
        "roi_per_point": 105000,
        "star_impact": 0.5,
        "population": 6720,
    },
    "CBP": {
        "name": "Controlling High Blood Pressure",
        "impact": 8.7,
        "effort": 2,
        "current_rate": 62.4,
        "benchmark": 72.0,
        "roi_per_point": 140000,
        "star_impact": 0.7,
        "population": 7650,
    },
    "OMW": {
        "name": "Osteoporosis Management",
        "impact": 5.4,
        "effort": 3,
        "current_rate": 55.6,
        "benchmark": 68.0,
        "roi_per_point": 85000,
        "star_impact": 0.3,
        "population": 3420,
    },
    "COL": {
        "name": "Follow-Up After ED - Mental Health",
        "impact": 5.8,
        "effort": 3,
        "current_rate": 48.9,
        "benchmark": 65.0,
        "roi_per_point": 75000,
        "star_impact": 0.4,
        "population": 2180,
    },
}

# Preset allocation scenarios (% of budget per measure)
SCENARIOS = {
    "Conservative": {"CCS": 15, "HBD": 10, "MAD": 20, "BCS": 15, "CBP": 20, "OMW": 10, "COL": 10},
    "Balanced": {"CCS": 18, "HBD": 18, "MAD": 15, "BCS": 15, "CBP": 20, "OMW": 7, "COL": 7},
    "Aggressive": {"CCS": 10, "HBD": 22, "MAD": 12, "BCS": 10, "CBP": 28, "OMW": 10, "COL": 8},
}


def _is_on_roi_page(input):
    """Check if we're on the ROI Portfolio Optimizer page."""
    try:
        return input.page_nav() == "roi"
    except Exception:
        return False


def _get_quadrant(impact: float, effort: float) -> str:
    """Return quadrant label for priority matrix."""
    hi, le = impact >= 6.5, effort <= 2
    if hi and le:
        return "Quick Wins"
    if hi and not le:
        return "Major Projects"
    if not hi and le:
        return "Fill-Ins"
    return "Hard Slogs"


def roi_portfolio_optimizer_ui():
    """UI for ROI Portfolio Optimizer page."""
    return mobile_page(
        "ROI Portfolio Optimizer",
        mobile_card(
            "Portfolio Optimization & Budget Allocation",
            ui.markdown("""
            **Optimize HEDIS investment** using an Impact vs Effort priority matrix.
            Allocate budget across 7 measures, model resource constraints, and forecast
            portfolio-level financial outcomes. Maximize ROI through strategic prioritization.
            """)
        ),
        mobile_card("Priority Matrix: Impact vs Effort", ui.output_ui("roi_priority_matrix")),
        mobile_card(
            "Budget Allocation Simulator",
            ui.tags.p("Set total budget and allocation % per measure.", style="margin-bottom: 0.75rem; color: #666; font-size: 0.9rem;"),
            ui.input_numeric("roi_total_budget", "Total Budget ($)", value=500000, min=50000, max=5000000, step=25000),
            ui.output_ui("roi_total_budget_display"),
            ui.output_ui("roi_allocation_sliders"),
            ui.div(
                mobile_button("Apply Conservative", "roi_scenario_conservative", "secondary", icon=""),
                mobile_button("Apply Balanced", "roi_scenario_balanced", "primary", icon=""),
                mobile_button("Apply Aggressive", "roi_scenario_agg", "secondary", icon=""),
                style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 1rem;"
            ),
            header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
        ),
        mobile_card(
            "Resource Constraints",
            ui.input_numeric("roi_max_budget", "Max Budget Constraint ($)", value=750000, min=100000, max=10000000, step=50000),
            ui.output_ui("roi_max_budget_display"),
            ui.input_numeric("roi_min_allocation_pct", "Min Allocation % per Measure", value=5, min=0, max=30, step=1),
            ui.output_ui("roi_constraint_status"),
        ),
        mobile_card(
            "Investment Scenarios & ROI Projections",
            ui.output_ui("roi_scenario_results"),
            header_color="#8b5cf6"
        ),
        mobile_card(
            "Portfolio Financial Forecast",
            ui.output_ui("roi_portfolio_forecast")
        ),
    )


def roi_portfolio_optimizer_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for ROI Portfolio Optimizer."""

    def _apply_scenario(scenario_name: str):
        """Update sliders to match preset scenario."""
        scenario = SCENARIOS[scenario_name]
        for code, pct in scenario.items():
            ui.update_slider(f"roi_alloc_{code}", value=pct, session=session)

    @reactive.Effect
    def _on_conservative():
        try:
            if _is_on_roi_page(input) and input.roi_scenario_conservative() > 0:
                _apply_scenario("Conservative")
        except Exception:
            pass

    @reactive.Effect
    def _on_balanced():
        try:
            if _is_on_roi_page(input) and input.roi_scenario_balanced() > 0:
                _apply_scenario("Balanced")
        except Exception:
            pass

    @reactive.Effect
    def _on_aggressive():
        try:
            if _is_on_roi_page(input) and input.roi_scenario_agg() > 0:
                _apply_scenario("Aggressive")
        except Exception:
            pass

    @output
    @render.ui
    def roi_priority_matrix():
        if not _is_on_roi_page(input):
            return None
        quadrants = {
            "Quick Wins": [],
            "Major Projects": [],
            "Fill-Ins": [],
            "Hard Slogs": [],
        }
        for code, m in PORTFOLIO_MEASURES.items():
            q = _get_quadrant(m["impact"], m["effort"])
            quadrants[q].append((code, m))
        colors = {
            "Quick Wins": "#28a745",
            "Major Projects": "#ff6b00",
            "Fill-Ins": "#17a2b8",
            "Hard Slogs": "#6c757d",
        }
        matrix_html = []
        for qname, measures in quadrants.items():
            c = colors[qname]
            tiles = []
            for code, m in measures:
                tiles.append(ui.div(
                    ui.tags.strong(code, style=f"color: {c}; font-size: 1rem;"),
                    ui.tags.div(m["name"], style="font-size: 0.8rem; color: #555; margin-top: 0.25rem;"),
                    ui.tags.div(f"Impact {m['impact']} | Effort {m['effort']}", style="font-size: 0.75rem; color: #999; margin-top: 0.25rem;"),
                    style=f"padding: 0.75rem; background: #f8f9fa; border-left: 4px solid {c}; border-radius: 8px; margin-bottom: 0.5rem;"
                ))
            matrix_html.append(ui.div(
                ui.tags.h4(qname, style=f"color: {c}; font-size: 1rem; margin: 0 0 0.5rem 0;"),
                *tiles,
                style="margin-bottom: 1.25rem;"
            ))
        return ui.div(
            ui.div(
                ui.tags.span("High Impact", style="font-weight: 700; color: #28a745;"),
                ui.tags.span("  Low Effort", style="color: #666; font-size: 0.85rem;"),
                style="margin-bottom: 0.5rem;"
            ),
            *matrix_html,
            alert_box("Prioritize Quick Wins first, then Major Projects for maximum ROI.", type="info")
        )

    @output
    @render.ui
    def roi_allocation_sliders():
        if not _is_on_roi_page(input):
            return None
        sliders = []
        for code, m in PORTFOLIO_MEASURES.items():
            sliders.append(
                ui.div(
                    ui.tags.label(f"{code}: {m['name']}", style="font-weight: 600; color: #333; font-size: 0.9rem;"),
                    ui.input_slider(
                        f"roi_alloc_{code}",
                        "",
                        min=0,
                        max=100,
                        value=100 // len(PORTFOLIO_MEASURES),
                        step=1
                    ),
                    style="margin-bottom: 1rem;"
                )
            )
        return ui.div(*sliders)

    def _get_allocations():
        """Get current allocation % from sliders."""
        out = {}
        for code in PORTFOLIO_MEASURES:
            try:
                inp = getattr(input, f"roi_alloc_{code}", None)
                out[code] = inp() if inp is not None else 100 // len(PORTFOLIO_MEASURES)
            except Exception:
                out[code] = 100 // len(PORTFOLIO_MEASURES)
        return out

    @output
    @render.ui
    def roi_total_budget_display():
        """Display Total Budget with comma separator."""
        if not _is_on_roi_page(input):
            return None
        try:
            val = input.roi_total_budget() or 500000
        except Exception:
            val = 500000
        return ui.tags.div(
            f"Selected: ${val:,.0f}",
            style="font-size: 0.875rem; color: #666; margin-top: -0.5rem; margin-bottom: 1rem;"
        )

    @output
    @render.ui
    def roi_max_budget_display():
        """Display Max Budget Constraint with comma separator."""
        if not _is_on_roi_page(input):
            return None
        try:
            val = input.roi_max_budget() or 750000
        except Exception:
            val = 750000
        return ui.tags.div(
            f"Limit: ${val:,.0f}",
            style="font-size: 0.875rem; color: #666; margin-top: -0.5rem; margin-bottom: 1rem;"
        )

    @output
    @render.ui
    def roi_constraint_status():
        if not _is_on_roi_page(input):
            return None
        try:
            total_budget = input.roi_total_budget() or 500000
            max_budget = input.roi_max_budget() or 750000
            min_pct = input.roi_min_allocation_pct() or 5
        except Exception:
            total_budget, max_budget, min_pct = 500000, 750000, 5
        over_budget = total_budget > max_budget
        return ui.div(
            ui.div(
                "Budget within limit" if not over_budget else "Exceeds max budget",
                style=f"padding: 0.75rem; border-radius: 8px; font-weight: 600; background: {'#d4edda' if not over_budget else '#f8d7da'}; color: {'#0f5132' if not over_budget else '#842029'};"
            ),
            ui.div(
                f"Total: ${total_budget:,.0f} / Max: ${max_budget:,.0f}",
                style="font-size: 0.875rem; color: #666; margin-top: 0.5rem;"
            ),
            ui.div(
                f"Min allocation: {min_pct}% per measure",
                style="font-size: 0.875rem; color: #666; margin-top: 0.25rem;"
            )
        )

    @output
    @render.ui
    def roi_scenario_results():
        if not _is_on_roi_page(input):
            return None
        try:
            total_budget = input.roi_total_budget() or 500000
            allocations = _get_allocations()
        except Exception:
            total_budget = 500000
            allocations = {m: 100 // len(PORTFOLIO_MEASURES) for m in PORTFOLIO_MEASURES}
        total_pct = sum(allocations.values())
        scale = (total_pct / 100.0) if total_pct else 1.0
        rows = []
        total_revenue = 0
        for code, m in PORTFOLIO_MEASURES.items():
            pct = allocations.get(code, 0)
            alloc_dollars = (total_budget * (pct / 100.0)) / scale if scale else 0
            gap = m["benchmark"] - m["current_rate"]
            rev_per_pt = m["roi_per_point"]
            est_improvement = min(gap, 3.0)
            rev_impact = rev_per_pt * est_improvement * (pct / 100.0)
            total_revenue += rev_impact
            rows.append(ui.div(
                ui.div(
                    ui.tags.strong(code, style="color: #7c3aed;"),
                    ui.tags.span(f" ${alloc_dollars:,.0f}", style="color: #333;"),
                    style="margin-bottom: 0.25rem;"
                ),
                ui.div(
                    f"Est. revenue impact: ${rev_impact:,.0f}",
                    style="font-size: 0.9rem; color: #28a745; font-weight: 600;"
                ),
                class_="scenario-row",
                style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid #7c3aed;"
            ))
        return ui.div(
            metric_box("Total Budget", f"${total_budget:,.0f}", color="#7c3aed", subtitle="Allocated across measures"),
            metric_box("Projected Revenue", f"${total_revenue:,.0f}", color="#28a745", subtitle="Est. from improvements"),
            metric_box("ROI Ratio", f"{(total_revenue / total_budget):.1f}x" if total_budget else "N/A", color="#ff6b00", subtitle="Return on investment"),
            ui.tags.h4("By Measure", style="color: #1a1a1a; margin: 1rem 0 0.5rem 0; font-size: 1.1rem;"),
            *rows
        )

    @output
    @render.ui
    def roi_portfolio_forecast():
        if not _is_on_roi_page(input):
            return None
        try:
            total_budget = input.roi_total_budget() or 500000
            allocations = _get_allocations()
        except Exception:
            total_budget = 500000
            allocations = {m: 100 // len(PORTFOLIO_MEASURES) for m in PORTFOLIO_MEASURES}
        total_pct = sum(allocations.values())
        scale = (total_pct / 100.0) if total_pct else 1.0
        total_revenue = 0
        for code, m in PORTFOLIO_MEASURES.items():
            pct = allocations.get(code, 0)
            gap = m["benchmark"] - m["current_rate"]
            rev_per_pt = m["roi_per_point"]
            est_improvement = min(gap, 3.0)
            total_revenue += rev_per_pt * est_improvement * (pct / 100.0)
        roi_ratio = total_revenue / total_budget if total_budget else 0
        net_benefit = total_revenue - total_budget
        return ui.div(
            ui.div(
                ui.tags.h3("Portfolio Summary", style="color: #7c3aed; text-align: center; margin: 0 0 1rem 0; font-size: 1.25rem;"),
                ui.div(
                    ui.div("Total Investment", style="font-size: 0.875rem; color: #666;"),
                    ui.div(f"${total_budget:,.0f}", style="font-size: 2rem; font-weight: 700; color: #1a1a1a;"),
                    style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem;"
                ),
                ui.div(
                    ui.div("Projected Revenue", style="font-size: 0.875rem; color: #666;"),
                    ui.div(f"${total_revenue:,.0f}", style="font-size: 2rem; font-weight: 700; color: #28a745;"),
                    style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem;"
                ),
                ui.div(
                    ui.div("Net Benefit", style="font-size: 0.875rem; color: #666;"),
                    ui.div(f"${net_benefit:,.0f}", style=f"font-size: 2rem; font-weight: 700; color: {'#28a745' if net_benefit >= 0 else '#dc3545'};"),
                    style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem;"
                ),
                ui.div(
                    ui.div("Portfolio ROI", style="font-size: 0.875rem; color: #666;"),
                    ui.div(f"{roi_ratio:.2f}x", style="font-size: 2rem; font-weight: 700; color: #ff6b00;"),
                    style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px;"
                ),
                style="margin-bottom: 1.5rem;"
            ),
            alert_box("Forecasts assume 1–3% improvement per measure based on allocation weight. Actual results vary by intervention execution.", type="info")
        )


__all__ = ['roi_portfolio_optimizer_ui', 'roi_portfolio_optimizer_server']
