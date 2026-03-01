"""Member Risk Stratification Dashboard - Mobile optimized."""

from shiny import ui, render
from ..components.mobile_layout import (
    mobile_page,
    mobile_card,
    mobile_button,
    metric_box,
    info_row,
    alert_box,
    divider,
    progress_bar
)


def _is_on_risk_page(input):
    """Check if we're on the risk stratification page."""
    try:
        return input.page_nav() == "risk"
    except Exception:
        return False


# HCC Risk Categories and Sample Data
RISK_CATEGORIES = {
    "Very High": {
        "threshold": "≥3.0",
        "color": "#dc3545",
        "count": 1247,
        "avg_raf": 3.84,
        "revenue_pmpm": 2890,
        "description": "Multiple chronic conditions, high utilization"
    },
    "High": {
        "threshold": "2.0-2.99",
        "color": "#ff6b00",
        "count": 3821,
        "avg_raf": 2.41,
        "revenue_pmpm": 1815,
        "description": "Complex chronic conditions, moderate utilization"
    },
    "Medium": {
        "threshold": "1.0-1.99",
        "color": "#ffc107",
        "count": 8934,
        "avg_raf": 1.38,
        "revenue_pmpm": 1040,
        "description": "Stable chronic conditions, routine care"
    },
    "Low": {
        "threshold": "<1.0",
        "color": "#28a745",
        "count": 4782,
        "avg_raf": 0.67,
        "revenue_pmpm": 505,
        "description": "Healthy or minimal conditions"
    }
}

# Top HCC Categories (V28 model)
HCC_CATEGORIES = [
    {"code": "HCC 18", "name": "Diabetes with Chronic Complications", "prevalence": 18.7, "avg_weight": 0.318, "members": 3542, "revenue_impact": 11264000},
    {"code": "HCC 85", "name": "Congestive Heart Failure", "prevalence": 14.2, "avg_weight": 0.323, "members": 2689, "revenue_impact": 8684000},
    {"code": "HCC 111", "name": "Chronic Obstructive Pulmonary Disease", "prevalence": 12.8, "avg_weight": 0.328, "members": 2425, "revenue_impact": 7952000},
    {"code": "HCC 134", "name": "Chronic Kidney Disease Stage 4", "prevalence": 9.3, "avg_weight": 0.237, "members": 1761, "revenue_impact": 4174000},
    {"code": "HCC 96", "name": "Ischemic Heart Disease", "prevalence": 8.6, "avg_weight": 0.166, "members": 1629, "revenue_impact": 2704000},
    {"code": "HCC 19", "name": "Diabetes without Complication", "prevalence": 7.4, "avg_weight": 0.104, "members": 1402, "revenue_impact": 1458000},
    {"code": "HCC 108", "name": "Vascular Disease", "prevalence": 6.9, "avg_weight": 0.288, "members": 1307, "revenue_impact": 3765000},
    {"code": "HCC 23", "name": "Other Endocrine/Metabolic/Nutritional", "prevalence": 5.8, "avg_weight": 0.207, "members": 1098, "revenue_impact": 2273000},
]

# Member Segments (Risk Trajectory)
MEMBER_SEGMENTS = {
    "Rising Risk": {"count": 2847, "pct": 15.0, "description": "RAF increasing >0.5 in past 6 months", "action": "Proactive intervention recommended", "priority": "High", "color": "#dc3545"},
    "Stable High Risk": {"count": 4126, "pct": 21.8, "description": "RAF ≥2.0, stable ±0.2 variation", "action": "Continue current care management", "priority": "Medium", "color": "#ff6b00"},
    "Stable Medium Risk": {"count": 8934, "pct": 47.2, "description": "RAF 1.0-1.99, stable patterns", "action": "Routine monitoring", "priority": "Low", "color": "#ffc107"},
    "Improving": {"count": 1845, "pct": 9.7, "description": "RAF decreasing >0.3, positive trends", "action": "Maintain interventions", "priority": "Low", "color": "#28a745"},
    "Low Risk": {"count": 1782, "pct": 6.3, "description": "RAF <1.0, minimal utilization", "action": "Preventive care focus", "priority": "Low", "color": "#17a2b8"}
}


def risk_stratification_ui():
    """UI for member risk stratification dashboard."""
    return mobile_page(
        "📊 Member Risk Stratification",
        mobile_card("HCC-Based Risk Analysis & Revenue Optimization",
            ui.markdown("""
            **Risk-adjust your Medicare Advantage population** using CMS HCC V28 model
            to identify high-value intervention opportunities and optimize capitation revenue.
            Analyzes RAF scores, condition prevalence, and risk trajectories.
            """)
        ),
        mobile_card("Portfolio Risk Summary", ui.output_ui("risk_portfolio_summary")),
        mobile_card("Risk Category Distribution", ui.output_ui("risk_distribution")),
        mobile_card("Top HCC Categories by Revenue Impact",
            ui.output_ui("risk_top_hcc_categories"),
            ui.div(
                mobile_button("View Detailed HCC Analysis", "hcc_detail_btn", "primary", icon="🔍"),
                style="margin-top: 1rem;"
            ),
            ui.output_ui("risk_hcc_detailed_analysis"),
            header_color="#8b5cf6"
        ),
        mobile_card("Member Segmentation by Risk Trajectory", ui.output_ui("risk_member_segments"),
            header_color="linear-gradient(135deg, #ff6b00 0%, #cc5500 100%)"),
        mobile_card("Risk-Adjusted Revenue Opportunity", ui.output_ui("risk_revenue_opportunity"))
    )


def risk_stratification_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for risk stratification dashboard."""

    @output
    @render.ui
    def risk_portfolio_summary():
        if not _is_on_risk_page(input):
            return None
        total_members = sum(cat["count"] for cat in RISK_CATEGORIES.values())
        weighted_raf = sum(cat["count"] * cat["avg_raf"] for cat in RISK_CATEGORIES.values()) / total_members
        total_revenue = sum(cat["count"] * cat["revenue_pmpm"] * 12 for cat in RISK_CATEGORIES.values())
        high_risk_count = RISK_CATEGORIES["Very High"]["count"] + RISK_CATEGORIES["High"]["count"]
        high_risk_pct = (high_risk_count / total_members) * 100
        return ui.div(
            metric_box("Total Members", f"{total_members:,}", color="#7c3aed", subtitle="Enrolled population"),
            metric_box("Average RAF Score", f"{weighted_raf:.2f}", color="#ff6b00", subtitle="Portfolio risk level"),
            metric_box("Annual Revenue", f"${total_revenue:,.0f}", color="#28a745", subtitle="Risk-adjusted capitation"),
            metric_box("High Risk Members", f"{high_risk_pct:.1f}%", color="#dc3545", subtitle=f"{high_risk_count:,} members"),
            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def risk_distribution():
        if not _is_on_risk_page(input):
            return None
        total_members = sum(cat["count"] for cat in RISK_CATEGORIES.values())
        return ui.div(
            *[
                ui.div(
                    ui.div(ui.tags.div(
                        ui.tags.span(category, style=f"font-weight: 700; font-size: 1.1rem; color: {data['color']};"),
                        ui.tags.span(data['threshold'], style="color: #666; font-size: 0.875rem; margin-left: 0.5rem;"),
                        style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"
                    )),
                    progress_bar((data["count"] / total_members) * 100, label=f"{(data['count'] / total_members) * 100:.1f}% ({data['count']:,} members)", color=data["color"]),
                    ui.div(
                        ui.div(ui.tags.strong("Avg RAF: ", class_="risk-label"), ui.tags.span(f"{data['avg_raf']:.2f}", class_="risk-value", style="color: #7c3aed; font-weight: 600;"), style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"),
                        ui.div(ui.tags.strong("Revenue PMPM: ", class_="risk-label"), ui.tags.span(f"${data['revenue_pmpm']:,}", class_="risk-value", style="color: #28a745; font-weight: 600;"), style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"),
                        ui.div(ui.tags.small(data['description'], class_="text-muted"), style="padding: 0.5rem 0;"),
                        style="margin-top: 0.75rem;"
                    ),
                    class_="risk-category-card", style=f"padding: 1.25rem; background: white; border-left: 4px solid {data['color']}; border-radius: 8px; margin-bottom: 1rem;"
                )
                for category, data in RISK_CATEGORIES.items()
            ]
        )

    @output
    @render.ui
    def risk_top_hcc_categories():
        """Display top HCC categories summary."""
        if not _is_on_risk_page(input):
            return None
        return ui.div(
            *[
                ui.div(
                    ui.div(
                        ui.tags.span(hcc["code"], class_="hcc-code", style="font-weight: 700; color: #1a1a1a; font-size: 1rem;"),
                        ui.tags.span(f"{hcc['prevalence']}%", class_="hcc-prevalence", style="font-weight: 600; color: #7c3aed; font-size: 0.875rem;"),
                        style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;"
                    ),
                    ui.div(
                        hcc["name"],
                        class_="hcc-name",
                        style="color: #1a1a1a; font-size: 0.95rem; margin-bottom: 0.75rem; font-weight: 500;"
                    ),
                    ui.div(
                        ui.tags.div(
                            ui.tags.small("Members: ", class_="hcc-metric-label", style="color: #1a1a1a; font-weight: 600;"),
                            ui.tags.span(f"{hcc['members']:,}", class_="hcc-metric-value", style="font-weight: 600; color: #1a1a1a;"),
                            style="margin-right: 1rem;"
                        ),
                        ui.tags.div(
                            ui.tags.small("Weight: ", class_="hcc-metric-label", style="color: #1a1a1a; font-weight: 600;"),
                            ui.tags.span(f"{hcc['avg_weight']:.3f}", class_="hcc-metric-value", style="font-weight: 600; color: #7c3aed;"),
                            style="margin-right: 1rem;"
                        ),
                        ui.tags.div(
                            ui.tags.small("Revenue: ", class_="hcc-metric-label", style="color: #1a1a1a; font-weight: 600;"),
                            ui.tags.span(f"${hcc['revenue_impact']:,.0f}", class_="hcc-metric-value", style="font-weight: 600; color: #28a745;"),
                        ),
                        style="display: flex; flex-wrap: wrap; gap: 0.5rem;"
                    ),
                    class_="hcc-category-card",
                    style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid #7c3aed;"
                )
                for hcc in HCC_CATEGORIES[:5]
            ]
        )

    @output
    @render.ui
    def risk_hcc_detailed_analysis():
        if not _is_on_risk_page(input):
            return None
        try:
            clicks = input.hcc_detail_btn()
            if clicks == 0:
                return None
        except Exception:
            return None
        total_revenue = sum(hcc["revenue_impact"] for hcc in HCC_CATEGORIES)
        total_members_with_hcc = sum(hcc["members"] for hcc in HCC_CATEGORIES)
        return ui.div(
            mobile_card("Complete HCC Category Analysis",
                ui.div(
                    metric_box("Total HCC Revenue", f"${total_revenue:,.0f}", color="#28a745", subtitle="Annual impact"),
                    metric_box("Members with HCCs", f"{total_members_with_hcc:,}", color="#1a1a1a", subtitle="Coded conditions"),
                    style="display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.5rem;"
                ),
                ui.div(
                    ui.tags.h3(
                        "All HCC Categories",
                        class_="hcc-detailed-title",
                        style="color: #1a1a1a; font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #7c3aed;"
                    )
                ),
                ui.div(*[
                    ui.div(
                        ui.tags.h4(f"{hcc['code']}: {hcc['name']}", style="color: #1a1a1a; margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 700;"),
                        ui.div(
                            ui.tags.strong("Prevalence: ", style="color: #1a1a1a; font-weight: 700;"),
                            ui.tags.span(f"{hcc['prevalence']}%", style="color: #7c3aed; font-weight: 600;"),
                            style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                        ),
                        ui.div(
                            ui.tags.strong("Affected Members: ", style="color: #1a1a1a; font-weight: 700;"),
                            ui.tags.span(f"{hcc['members']:,}", style="color: #1a1a1a; font-weight: 600;"),
                            style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                        ),
                        ui.div(
                            ui.tags.strong("RAF Weight: ", style="color: #1a1a1a; font-weight: 700;"),
                            ui.tags.span(f"{hcc['avg_weight']:.3f}", style="color: #1a1a1a; font-weight: 600;"),
                            style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                        ),
                        ui.div(
                            ui.tags.strong("Revenue Impact: ", style="color: #1a1a1a; font-weight: 700;"),
                            ui.tags.span(f"${hcc['revenue_impact']:,.0f}", style="color: #28a745; font-weight: 700; font-size: 1.1rem;"),
                            style="padding: 0.5rem 0;"
                        ),
                        class_="hcc-detailed-tile",
                        style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
                    )
                    for hcc in HCC_CATEGORIES
                ])
            ), style="margin-top: 1.5rem;"
        )

    @output
    @render.ui
    def risk_member_segments():
        if not _is_on_risk_page(input):
            return None
        return ui.div(
            *[
                ui.div(
                    ui.div(
                        ui.tags.span(segment_name, style=f"font-weight: 700; font-size: 1.1rem; color: {data['color']};"),
                        ui.tags.span(f"{data['pct']}%", style="font-weight: 600; color: #666; font-size: 0.875rem;"),
                        style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;"
                    ),
                    ui.div(f"{data['count']:,} members", style="color: #666; font-size: 0.9rem; margin-bottom: 0.75rem;"),
                    progress_bar(data["pct"], label=f"{data['pct']}%", color=data["color"]),
                    ui.div(
                        ui.div(ui.tags.strong("Description: ", class_="segment-label"), ui.tags.span(data['description'], class_="segment-value", style="color: #555;"), style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"),
                        ui.div(ui.tags.strong("Recommended Action: ", class_="segment-label"), ui.tags.span(data['action'], class_="segment-value", style="color: #7c3aed; font-weight: 600;"), style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"),
                        ui.div(ui.tags.strong("Priority: ", class_="segment-label"), ui.tags.span(data['priority'], class_="segment-value", style=f"color: {'#dc3545' if data['priority'] == 'High' else '#ffc107' if data['priority'] == 'Medium' else '#28a745'}; font-weight: 600;"), style="padding: 0.5rem 0;"),
                        style="margin-top: 0.75rem;"
                    ),
                    class_="segment-card", style=f"padding: 1.25rem; background: white; border-left: 4px solid {data['color']}; border-radius: 8px; margin-bottom: 1rem;"
                )
                for segment_name, data in MEMBER_SEGMENTS.items()
            ]
        )

    @output
    @render.ui
    def risk_revenue_opportunity():
        if not _is_on_risk_page(input):
            return None
        rising_risk = MEMBER_SEGMENTS["Rising Risk"]
        rising_risk_opportunity = rising_risk["count"] * 150 * 12
        low_risk_wellness = MEMBER_SEGMENTS["Low Risk"]["count"] * 25 * 12
        total_opportunity = rising_risk_opportunity + low_risk_wellness
        return ui.div(
            ui.div(
                ui.tags.h3("Annual Revenue Optimization Potential", style="color: #7c3aed; text-align: center; margin: 0 0 1rem 0; font-size: 1.25rem;"),
                ui.tags.div(f"${total_opportunity:,.0f}", style="font-size: 3rem; font-weight: 700; color: #28a745; text-align: center; margin-bottom: 1.5rem;"),
                style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;"
            ),
            ui.div(
                ui.tags.h3(
                    "Opportunity Breakdown",
                    style="color: #1a1a1a; font-size: 1.25rem; font-weight: 700; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #7c3aed;"
                )
            ),
            ui.div(
                ui.tags.h4("Rising Risk Intervention Program", style="color: #000000 !important; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 700;"),
                ui.div(
                    ui.tags.strong("Target Population: ", style="color: #1a1a1a; font-weight: 700;"),
                    ui.tags.span(f"{rising_risk['count']:,} members", style="color: #7c3aed; font-weight: 600;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),
                ui.div(
                    ui.tags.strong("Intervention Strategy: ", style="color: #1a1a1a; font-weight: 700;"),
                    ui.tags.span("Proactive care management, condition monitoring", style="color: #333; font-weight: 500;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),
                ui.div(
                    ui.tags.strong("Expected Value: ", style="color: #1a1a1a; font-weight: 700;"),
                    ui.tags.span("$150 PMPM risk mitigation", style="color: #333; font-weight: 600;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),
                ui.div(
                    ui.div(
                        ui.tags.strong("Annual Revenue Impact: ", style="color: #999; font-weight: 600; display: block; margin-bottom: 0.5rem;"),
                        ui.tags.span(f"${rising_risk_opportunity:,.0f}", style="color: #999 !important; font-weight: 700 !important; font-size: 1.5rem; display: block;"),
                        style="text-align: center;"
                    ),
                    style="padding: 0.75rem; background: #f0f7ff; border-radius: 8px; margin-top: 0.5rem;"
                ),
                class_="opportunity-card",
                style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
            ),
            ui.div(
                ui.tags.h4("Preventive Wellness Program", style="color: #000000 !important; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 700;"),
                ui.div(
                    ui.tags.strong("Target Population: ", style="color: #1a1a1a; font-weight: 700;"),
                    ui.tags.span(f"{MEMBER_SEGMENTS['Low Risk']['count']:,} members", style="color: #7c3aed; font-weight: 600;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),
                ui.div(
                    ui.tags.strong("Intervention Strategy: ", style="color: #1a1a1a; font-weight: 700;"),
                    ui.tags.span("Annual wellness visits, preventive screenings", style="color: #333; font-weight: 500;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),
                ui.div(
                    ui.tags.strong("Expected Value: ", style="color: #1a1a1a; font-weight: 700;"),
                    ui.tags.span("$25 PMPM prevention value", style="color: #333; font-weight: 600;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),
                ui.div(
                    ui.div(
                        ui.tags.strong("Annual Revenue Impact: ", style="color: #999; font-weight: 600; display: block; margin-bottom: 0.5rem;"),
                        ui.tags.span(f"${low_risk_wellness:,.0f}", style="color: #999 !important; font-weight: 700 !important; font-size: 1.5rem; display: block;"),
                        style="text-align: center;"
                    ),
                    style="padding: 0.75rem; background: #f0f7ff; border-radius: 8px; margin-top: 0.5rem;"
                ),
                class_="opportunity-card",
                style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
            ),
            alert_box("💡 Targeting high-risk and low-risk members with tailored interventions maximizes both quality outcomes and revenue optimization.", type="info")
        )


__all__ = ['risk_stratification_ui', 'risk_stratification_server']
