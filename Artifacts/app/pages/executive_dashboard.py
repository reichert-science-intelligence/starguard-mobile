"""Executive Dashboard - Mobile optimized."""

from shiny import ui, render, reactive
from ..components.mobile_layout import (
    mobile_page,
    mobile_card,
    mobile_button,
    metric_box,
    alert_box,
    progress_bar
)

# Executive KPIs
EXECUTIVE_METRICS = {
    "current_star_rating": 3.5,
    "projected_star_rating": 4.0,
    "confidence": 87,
    "total_members": 18934,
    "high_risk_members": 5068,
    "open_gaps": 14237,
    "gaps_closed_ytd": 8942,
    "revenue_opportunity": 11647000,
    "revenue_captured_ytd": 6823000,
    "ai_accuracy": 94.2,
    "system_uptime": 99.7,
    "active_campaigns": 12
}

# Top opportunities
TOP_OPPORTUNITIES = [
    {
        "measure": "HBD - Hemoglobin A1c Control",
        "gap": 12.3,
        "members": 2341,
        "revenue": 2083690,
        "priority": "Critical"
    },
    {
        "measure": "CBP - Controlling Blood Pressure",
        "gap": 9.7,
        "members": 1876,
        "revenue": 2101120,
        "priority": "High"
    },
    {
        "measure": "BCS - Breast Cancer Screening",
        "gap": 8.4,
        "members": 1534,
        "revenue": 997100,
        "priority": "High"
    }
]

# Recent alerts
ALERTS = [
    {
        "type": "warning",
        "message": "2,847 members showing rising risk scores",
        "action": "Review risk stratification",
        "time": "2 hours ago"
    },
    {
        "type": "success",
        "message": "Q1 Diabetes campaign closed 234 gaps",
        "action": "View campaign details",
        "time": "5 hours ago"
    },
    {
        "type": "info",
        "message": "AI model accuracy improved to 94.2%",
        "action": "View validation report",
        "time": "1 day ago"
    }
]


def executive_dashboard_ui():
    """UI for executive dashboard."""
    return mobile_page(
        "Executive Dashboard",

        # Star Rating Trajectory
        mobile_card(
            "Star Rating Trajectory",
            ui.output_ui("star_trajectory"),
            header_color="linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
        ),

        # Key Performance Indicators
        mobile_card(
            "Key Performance Indicators",
            ui.output_ui("kpi_summary")
        ),

        # Top 3 Opportunities
        mobile_card(
            "Top Revenue Opportunities",
            ui.output_ui("top_opportunities"),
            header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
        ),

        # System Health
        mobile_card(
            "AI System Health",
            ui.output_ui("system_health")
        ),

        # Recent Alerts
        mobile_card(
            "Recent Alerts & Actions",
            ui.output_ui("recent_alerts"),
            header_color="linear-gradient(135deg, #ff6b00 0%, #cc5500 100%)"
        ),

        # QTD Performance
        mobile_card(
            "Quarter-to-Date Performance",
            ui.output_ui("qtd_performance")
        )
    )


def executive_dashboard_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for executive dashboard."""

    def _is_on_dashboard_page():
        """Check if we're on the dashboard page."""
        try:
            return get_current_page() == "dashboard"
        except Exception:
            return False

    @output
    @render.ui
    def star_trajectory():
        """Display star rating projection."""
        if not _is_on_dashboard_page():
            return None

        current = EXECUTIVE_METRICS["current_star_rating"]
        projected = EXECUTIVE_METRICS["projected_star_rating"]
        confidence = EXECUTIVE_METRICS["confidence"]
        improvement = projected - current

        return ui.div(
            ui.div(
                ui.tags.div(
                    "Current Rating",
                    style="color: #000000 !important; font-size: 0.875rem; text-align: center; margin-bottom: 0.5rem; font-weight: 900 !important;"
                ),
                ui.tags.div(
                    f"⭐ {current}",
                    style="font-size: 3rem; font-weight: 900; color: #000000 !important; text-align: center;"
                ),
                style="padding: 1.5rem; background: #fff8f0; border-radius: 12px; margin-bottom: 1rem;"
            ),
            ui.div(
                "↓",
                style="font-size: 2rem; text-align: center; color: #28a745; margin: 0.5rem 0;"
            ),
            ui.div(
                ui.tags.div(
                    "Projected Rating",
                    style="color: #000000 !important; font-size: 0.875rem; text-align: center; margin-bottom: 0.5rem; font-weight: 900 !important;"
                ),
                ui.tags.div(
                    f"⭐ {projected}",
                    style="font-size: 3rem; font-weight: 900; color: #000000 !important; text-align: center;"
                ),
                ui.tags.div(
                    f"+{improvement} improvement • {confidence}% confidence",
                    style="color: #000000 !important; font-size: 0.95rem; text-align: center; margin-top: 0.5rem; font-weight: 700;"
                ),
                style="padding: 1.5rem; background: #f0f7f0; border-radius: 12px;"
            ),
            ui.div(
                ui.tags.p(
                    f"Achieving 4.0 stars unlocks ${EXECUTIVE_METRICS['revenue_opportunity']:,} in bonus revenue",
                    style="text-align: center; color: #999 !important; margin: 1rem 0 0 0; font-weight: 600; font-size: 1rem;"
                )
            )
        )

    @output
    @render.ui
    def kpi_summary():
        """Display key performance indicators."""
        if not _is_on_dashboard_page():
            return None

        return ui.div(
            metric_box("Total Members", f"{EXECUTIVE_METRICS['total_members']:,}", color="#7c3aed", subtitle="Enrolled population", dark_labels=True),
            metric_box("High Risk Members", f"{EXECUTIVE_METRICS['high_risk_members']:,}", color="#dc3545", subtitle=f"{(EXECUTIVE_METRICS['high_risk_members']/EXECUTIVE_METRICS['total_members']*100):.1f}% of population", dark_labels=True),
            metric_box("Open Care Gaps", f"{EXECUTIVE_METRICS['open_gaps']:,}", color="#ff6b00", subtitle="Requiring closure", dark_labels=True),
            metric_box("Gaps Closed YTD", f"{EXECUTIVE_METRICS['gaps_closed_ytd']:,}", color="#28a745", subtitle=f"{(EXECUTIVE_METRICS['gaps_closed_ytd']/(EXECUTIVE_METRICS['gaps_closed_ytd']+EXECUTIVE_METRICS['open_gaps'])*100):.1f}% closure rate", dark_labels=True),
            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def top_opportunities():
        """Display top 3 revenue opportunities."""
        if not _is_on_dashboard_page():
            return None

        priority_colors = {
            "Critical": "#dc3545",
            "High": "#ff6b00",
            "Medium": "#ffc107"
        }

        return ui.div(
            *[
                ui.div(
                    ui.div(
                        ui.tags.span(opp["measure"], style="font-weight: 700; font-size: 1rem; color: #000000 !important;"),
                        ui.tags.span(
                            opp["priority"],
                            style=f"background: {priority_colors[opp['priority']]}; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;"
                        ),
                        style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;"
                    ),
                    ui.div(
                        ui.tags.strong("Gap to Benchmark: ", style="color: #000000 !important; font-weight: 700;"),
                        ui.tags.span(
                            f"{opp['gap']:.1f}%",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),
                    ui.div(
                        ui.tags.strong("Affected Members: ", style="color: #000000 !important; font-weight: 700;"),
                        ui.tags.span(
                            f"{opp['members']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),
                    ui.div(
                        ui.tags.strong("Revenue Opportunity: ", style="color: #000000 !important; font-weight: 700;"),
                        ui.tags.span(
                            f"${opp['revenue']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.75rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0;"
                    ),
                    class_="opportunity-card",
                    style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
                )
                for opp in TOP_OPPORTUNITIES
            ],
            ui.div(
                ui.tags.p(
                    f"Total Opportunity: ${sum(o['revenue'] for o in TOP_OPPORTUNITIES):,}",
                    style="text-align: center; color: #28a745; margin: 1rem 0 0 0; font-weight: 700; font-size: 1.25rem;"
                )
            )
        )

    @output
    @render.ui
    def system_health():
        """Display AI system health metrics."""
        if not _is_on_dashboard_page():
            return None

        return ui.div(
            metric_box("Model Accuracy", f"{EXECUTIVE_METRICS['ai_accuracy']}%", color="#28a745", subtitle="Prediction validation", dark_labels=True),
            metric_box("System Uptime", f"{EXECUTIVE_METRICS['system_uptime']}%", color="#7c3aed", subtitle="Availability", dark_labels=True),
            metric_box("Active Campaigns", f"{EXECUTIVE_METRICS['active_campaigns']}", color="#ff6b00", subtitle="Running workflows", dark_labels=True),
            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def recent_alerts():
        """Display recent alerts and notifications."""
        if not _is_on_dashboard_page():
            return None

        alert_colors = {
            "warning": "#ffc107",
            "success": "#28a745",
            "info": "#7c3aed"
        }

        alert_icons = {
            "warning": "⚠️",
            "success": "✅",
            "info": "ℹ️"
        }

        return ui.div(
            *[
                ui.div(
                    ui.div(
                        ui.tags.span(alert_icons[alert["type"]], style="font-size: 1.5rem; margin-right: 0.75rem;"),
                        ui.tags.div(
                            ui.tags.div(alert["message"], style="font-weight: 600; color: #666; margin-bottom: 0.25rem;"),
                            ui.tags.div(alert["action"], style="color: #999; font-size: 0.875rem; font-weight: 500; cursor: pointer;"),
                            ui.tags.div(alert["time"], style="color: #999; font-size: 0.75rem; margin-top: 0.25rem;"),
                            style="flex: 1;"
                        ),
                        style="display: flex; align-items: flex-start;"
                    ),
                    style=f"padding: 1rem; background: white; border-left: 4px solid {alert_colors[alert['type']]}; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for alert in ALERTS
            ]
        )

    @output
    @render.ui
    def qtd_performance():
        """Display quarter-to-date performance summary."""
        if not _is_on_dashboard_page():
            return None

        revenue_captured = EXECUTIVE_METRICS["revenue_captured_ytd"]
        revenue_opportunity = EXECUTIVE_METRICS["revenue_opportunity"]
        capture_rate = (revenue_captured / revenue_opportunity) * 100
        gaps_closed = EXECUTIVE_METRICS["gaps_closed_ytd"]
        total_gaps = EXECUTIVE_METRICS["gaps_closed_ytd"] + EXECUTIVE_METRICS["open_gaps"]
        gap_closure_rate = (gaps_closed / total_gaps) * 100

        return ui.div(
            ui.div(
                ui.tags.strong("Revenue Captured", style="color: #000000 !important; font-weight: 700; display: block; margin-bottom: 0.5rem;"),
                ui.tags.div(
                    f"${revenue_captured:,}",
                    style="color: #000000 !important; font-weight: 900 !important; font-size: 2rem; display: block; margin-bottom: 0.5rem;"
                ),
                progress_bar(capture_rate, label=f"{capture_rate:.1f}% of opportunity", color="#28a745"),
                style="padding: 1.25rem; background: #f0f7f0; border-radius: 12px; margin-bottom: 1rem;"
            ),
            ui.div(
                ui.tags.strong("Gap Closure Rate", style="color: #666; font-weight: 600; display: block; margin-bottom: 0.5rem;"),
                ui.tags.div(
                    f"{gap_closure_rate:.1f}%",
                    style="color: #999 !important; font-weight: 700 !important; font-size: 2rem; display: block; margin-bottom: 0.5rem;"
                ),
                progress_bar(gap_closure_rate, label=f"{gaps_closed:,} of {total_gaps:,} gaps closed", color="#7c3aed"),
                style="padding: 1.25rem; background: #f5f3ff; border-radius: 12px;"
            )
        )


__all__ = ['executive_dashboard_ui', 'executive_dashboard_server']
