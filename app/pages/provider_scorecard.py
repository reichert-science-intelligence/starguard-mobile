"""Provider Performance Scorecard - Mobile optimized."""

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

# Sample provider data
PROVIDER_NETWORK = [
    {
        "provider_id": "NPI-1234567",
        "name": "Dr. Sarah Mitchell",
        "specialty": "Family Medicine",
        "panel_size": 847,
        "avg_risk_score": 2.3,
        "quality_score": 92.4,
        "hedis_performance": {
            "HBD": 89.2,
            "CBP": 91.5,
            "CCS": 94.3,
            "BCS": 88.7,
            "MAD": 85.4
        },
        "gap_closure_rate": 78.3,
        "star_contribution": 0.18,
        "peer_ranking": "Top 10%"
    },
    {
        "provider_id": "NPI-2345678",
        "name": "Dr. James Rodriguez",
        "specialty": "Internal Medicine",
        "panel_size": 1203,
        "avg_risk_score": 2.8,
        "quality_score": 88.6,
        "hedis_performance": {
            "HBD": 85.1,
            "CBP": 87.9,
            "CCS": 91.2,
            "BCS": 82.4,
            "MAD": 79.8
        },
        "gap_closure_rate": 71.5,
        "star_contribution": 0.15,
        "peer_ranking": "Top 25%"
    },
    {
        "provider_id": "NPI-3456789",
        "name": "Dr. Emily Chen",
        "specialty": "Cardiology",
        "panel_size": 564,
        "avg_risk_score": 3.1,
        "quality_score": 95.2,
        "hedis_performance": {
            "HBD": 93.7,
            "CBP": 96.8,
            "CCS": 89.5,
            "BCS": 91.2,
            "MAD": 88.9
        },
        "gap_closure_rate": 84.7,
        "star_contribution": 0.22,
        "peer_ranking": "Top 5%"
    },
    {
        "provider_id": "NPI-4567890",
        "name": "Dr. Michael Thompson",
        "specialty": "Endocrinology",
        "panel_size": 423,
        "avg_risk_score": 2.6,
        "quality_score": 90.1,
        "hedis_performance": {
            "HBD": 94.3,
            "CBP": 88.2,
            "CCS": 87.6,
            "BCS": 90.5,
            "MAD": 92.1
        },
        "gap_closure_rate": 76.8,
        "star_contribution": 0.16,
        "peer_ranking": "Top 15%"
    },
    {
        "provider_id": "NPI-5678901",
        "name": "Dr. Jennifer Davis",
        "specialty": "Family Medicine",
        "panel_size": 982,
        "avg_risk_score": 2.1,
        "quality_score": 86.3,
        "hedis_performance": {
            "HBD": 81.4,
            "CBP": 84.6,
            "CCS": 88.9,
            "BCS": 85.1,
            "MAD": 77.3
        },
        "gap_closure_rate": 68.2,
        "star_contribution": 0.12,
        "peer_ranking": "Top 35%"
    },
    {
        "provider_id": "NPI-6789012",
        "name": "Dr. Robert Wilson",
        "specialty": "Internal Medicine",
        "panel_size": 1156,
        "avg_risk_score": 2.4,
        "quality_score": 93.7,
        "hedis_performance": {
            "HBD": 91.8,
            "CBP": 93.2,
            "CCS": 95.6,
            "BCS": 89.4,
            "MAD": 86.7
        },
        "gap_closure_rate": 81.4,
        "star_contribution": 0.19,
        "peer_ranking": "Top 10%"
    },
]

# Network summary metrics
NETWORK_METRICS = {
    "total_providers": len(PROVIDER_NETWORK),
    "total_panel": sum(p["panel_size"] for p in PROVIDER_NETWORK),
    "avg_quality_score": sum(p["quality_score"] for p in PROVIDER_NETWORK) / len(PROVIDER_NETWORK),
    "avg_gap_closure": sum(p["gap_closure_rate"] for p in PROVIDER_NETWORK) / len(PROVIDER_NETWORK),
    "top_performers": len([p for p in PROVIDER_NETWORK if p["quality_score"] >= 90]),
    "improvement_needed": len([p for p in PROVIDER_NETWORK if p["quality_score"] < 85])
}


def provider_scorecard_ui():
    """UI for provider performance scorecard."""
    return mobile_page(
        "👨‍⚕️ Provider Performance Scorecard",

        # Introduction
        mobile_card(
            "Network Quality Analytics",
            ui.markdown("""
            **Provider-level performance measurement** for network optimization and quality improvement.

            Analyzes HEDIS attribution, gap closure rates, and Star Rating contributions
            across your provider network.
            """)
        ),

        # Network summary
        mobile_card(
            "Network Overview",
            ui.output_ui("network_summary")
        ),

        # Specialty filter
        mobile_card(
            "Filter by Specialty",
            ui.input_radio_buttons(
                "specialty_filter",
                "",
                choices={
                    "All": "All Specialties",
                    "Family Medicine": "Family Medicine",
                    "Internal Medicine": "Internal Medicine",
                    "Cardiology": "Cardiology",
                    "Endocrinology": "Endocrinology"
                },
                selected="All",
                inline=False
            ),
            ui.output_ui("filtered_provider_count")
        ),

        # Provider list
        mobile_card(
            "Provider Performance Rankings",
            ui.output_ui("provider_list"),
            header_color="linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
        ),

        # Top performers
        mobile_card(
            "⭐ Top Performers",
            ui.output_ui("top_performers"),
            header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
        ),

        # Improvement opportunities
        mobile_card(
            "📈 Improvement Opportunities",
            ui.output_ui("improvement_opportunities"),
            header_color="linear-gradient(135deg, #ff6b00 0%, #cc5500 100%)"
        )
    )


def provider_scorecard_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for provider scorecard."""

    def _is_on_provider_page():
        """Check if we're on the provider page."""
        try:
            return get_current_page() == "providers"
        except Exception:
            return False

    @output
    @render.ui
    def network_summary():
        """Display network-level metrics."""
        if not _is_on_provider_page():
            return None

        return ui.div(
            metric_box(
                "Total Providers",
                f"{NETWORK_METRICS['total_providers']}",
                color="#7c3aed",
                subtitle="Active in network"
            ),
            metric_box(
                "Total Panel Size",
                f"{NETWORK_METRICS['total_panel']:,}",
                color="#0066cc",
                subtitle="Attributed members"
            ),
            metric_box(
                "Avg Quality Score",
                f"{NETWORK_METRICS['avg_quality_score']:.1f}%",
                color="#28a745",
                subtitle="Network performance"
            ),
            metric_box(
                "Avg Gap Closure",
                f"{NETWORK_METRICS['avg_gap_closure']:.1f}%",
                color="#ff6b00",
                subtitle="HEDIS effectiveness"
            ),
            metric_box(
                "Top Performers",
                f"{NETWORK_METRICS['top_performers']}",
                color="#28a745",
                subtitle="Quality score ≥90%"
            ),
            metric_box(
                "Needs Support",
                f"{NETWORK_METRICS['improvement_needed']}",
                color="#dc3545",
                subtitle="Quality score <85%"
            ),
            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def filtered_provider_count():
        """Show count of filtered providers."""
        if not _is_on_provider_page():
            return None

        specialty = input.specialty_filter()

        if specialty == "All":
            count = len(PROVIDER_NETWORK)
        else:
            count = len([p for p in PROVIDER_NETWORK if p["specialty"] == specialty])

        return ui.div(
            ui.tags.p(
                f"Showing {count} provider{'s' if count != 1 else ''}",
                style="text-align: center; color: #666; margin: 0.5rem 0 0 0; font-size: 0.875rem;"
            )
        )

    @output
    @render.ui
    def provider_list():
        """Display filtered provider list."""
        if not _is_on_provider_page():
            return None

        specialty = input.specialty_filter()

        # Filter providers
        if specialty == "All":
            filtered_providers = PROVIDER_NETWORK
        else:
            filtered_providers = [p for p in PROVIDER_NETWORK if p["specialty"] == specialty]

        # Sort by quality score descending
        sorted_providers = sorted(filtered_providers, key=lambda x: x["quality_score"], reverse=True)

        # Ranking colors
        ranking_colors = {
            "Top 5%": "#28a745",
            "Top 10%": "#4ade80",
            "Top 15%": "#86efac",
            "Top 25%": "#ffc107",
            "Top 35%": "#ff6b00"
        }

        return ui.div(
            *[
                ui.div(
                    # Provider header
                    ui.div(
                        ui.tags.div(
                            ui.tags.span(
                                provider["name"],
                                style="font-weight: 700; font-size: 1.1rem; color: #1a1a1a;"
                            ),
                            ui.tags.span(
                                provider["peer_ranking"],
                                style=f"background: {ranking_colors.get(provider['peer_ranking'], '#999')}; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;"
                            ),
                            style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"
                        ),
                        ui.tags.div(
                            f"{provider['specialty']} • NPI: {provider['provider_id']}",
                            style="color: #666; font-size: 0.875rem; margin-bottom: 0.75rem;"
                        )
                    ),

                    # Key metrics
                    ui.div(
                        ui.tags.strong("Quality Score: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{provider['quality_score']:.1f}%",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Panel Size: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{provider['panel_size']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Gap Closure Rate: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{provider['gap_closure_rate']:.1f}%",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        progress_bar(
                            provider['gap_closure_rate'],
                            label="",
                            color="#28a745"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Star Contribution: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"+{provider['star_contribution']:.2f}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0;"
                    ),

                    # HEDIS Performance
                    ui.div(
                        ui.tags.strong("HEDIS Performance:", style="color: #1a1a1a; font-weight: 700; display: block; margin-bottom: 0.75rem;"),
                        *[
                            ui.div(
                                ui.tags.span(f"{measure}: ", style="color: #666; font-size: 0.875rem;"),
                                ui.tags.span(f"{score:.1f}%", style="color: #7c3aed; font-weight: 600; font-size: 0.875rem;"),
                                style="padding: 0.25rem 0;"
                            )
                            for measure, score in provider["hedis_performance"].items()
                        ],
                        style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #e0e0e0;"
                    ),

                    class_="provider-card",
                    style=f"padding: 1.25rem; background: white; border-left: 4px solid {ranking_colors.get(provider['peer_ranking'], '#999')}; border-radius: 8px; margin-bottom: 1rem;"
                )
                for provider in sorted_providers
            ]
        )

    @output
    @render.ui
    def top_performers():
        """Highlight top performing providers."""
        if not _is_on_provider_page():
            return None

        top = [p for p in PROVIDER_NETWORK if p["quality_score"] >= 90]
        sorted_top = sorted(top, key=lambda x: x["quality_score"], reverse=True)

        return ui.div(
            ui.markdown(f"""
            **{len(top)} providers** achieving quality scores ≥90% are driving network excellence.
            """),

            divider(),

            *[
                ui.div(
                    ui.tags.h4(
                        provider["name"],
                        style="color: #999 !important; margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 500;"
                    ),
                    ui.tags.div(
                        f"{provider['specialty']} • Quality: {provider['quality_score']:.1f}% • Star Impact: +{provider['star_contribution']:.2f}",
                        style="color: #666; font-size: 0.875rem;"
                    ),
                    style="padding: 1rem; background: #f0f7f0; border-left: 4px solid #28a745; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for provider in sorted_top[:3]
            ]
        )

    @output
    @render.ui
    def improvement_opportunities():
        """Identify providers needing support."""
        if not _is_on_provider_page():
            return None

        need_support = [p for p in PROVIDER_NETWORK if p["quality_score"] < 85]

        if len(need_support) == 0:
            return alert_box(
                "✅ All providers meeting quality standards (≥85%)",
                type="success"
            )

        return ui.div(
            ui.markdown(f"""
            **{len(need_support)} provider{'s' if len(need_support) != 1 else ''}** below 85% quality threshold.
            Targeted support can improve network performance.
            """),

            divider(),

            *[
                ui.div(
                    ui.tags.h4(
                        provider["name"],
                        style="color: #000000 !important; margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 700;"
                    ),
                    ui.tags.div(
                        f"{provider['specialty']} • Quality: {provider['quality_score']:.1f}% • Gap Closure: {provider['gap_closure_rate']:.1f}%",
                        style="color: #666; font-size: 0.875rem; margin-bottom: 0.5rem;"
                    ),
                    ui.tags.div(
                        "📋 Recommended Action: Quality improvement coaching and HEDIS gap closure support",
                        style="color: #ff6b00; font-size: 0.875rem; font-weight: 600;"
                    ),
                    style="padding: 1rem; background: #fff8f0; border-left: 4px solid #ff6b00; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for provider in need_support
            ]
        )


__all__ = ['provider_scorecard_ui', 'provider_scorecard_server']
