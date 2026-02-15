"""HEDIS Gap Analyzer page - Mobile optimized."""

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

# HEDIS Measures Database with current performance metrics
HEDIS_MEASURES = {
    "CCS": {
        "name": "Colorectal Cancer Screening",
        "category": "Preventive Care",
        "current_rate": 67.3,
        "benchmark": 75.0,
        "national_avg": 70.2,
        "weight": "High",
        "star_impact": 0.5,
        "roi_per_point": 125000,
        "population": 8450,
        "difficulty": "Medium"
    },
    "HBD": {
        "name": "Hemoglobin A1c Control for Diabetes",
        "category": "Diabetes Care",
        "current_rate": 58.2,
        "benchmark": 70.0,
        "national_avg": 64.5,
        "weight": "High",
        "star_impact": 0.6,
        "roi_per_point": 95000,
        "population": 5230,
        "difficulty": "High"
    },
    "MAD": {
        "name": "Medication Adherence - Diabetes",
        "category": "Medication Management",
        "current_rate": 71.5,
        "benchmark": 80.0,
        "national_avg": 75.8,
        "weight": "Medium",
        "star_impact": 0.4,
        "roi_per_point": 110000,
        "population": 4890,
        "difficulty": "Low"
    },
    "BCS": {
        "name": "Breast Cancer Screening",
        "category": "Preventive Care",
        "current_rate": 73.8,
        "benchmark": 78.0,
        "national_avg": 76.2,
        "weight": "High",
        "star_impact": 0.5,
        "roi_per_point": 105000,
        "population": 6720,
        "difficulty": "Low"
    },
    "CBP": {
        "name": "Controlling High Blood Pressure",
        "category": "Chronic Disease Management",
        "current_rate": 62.4,
        "benchmark": 72.0,
        "national_avg": 68.1,
        "weight": "High",
        "star_impact": 0.7,
        "roi_per_point": 140000,
        "population": 7650,
        "difficulty": "Medium"
    },
    "OMW": {
        "name": "Osteoporosis Management in Women",
        "category": "Chronic Disease Management",
        "current_rate": 55.6,
        "benchmark": 68.0,
        "national_avg": 62.3,
        "weight": "Medium",
        "star_impact": 0.3,
        "roi_per_point": 85000,
        "population": 3420,
        "difficulty": "High"
    },
    "COL": {
        "name": "Follow-Up After ED Visit - Mental Health",
        "category": "Care Coordination",
        "current_rate": 48.9,
        "benchmark": 65.0,
        "national_avg": 58.7,
        "weight": "Medium",
        "star_impact": 0.4,
        "roi_per_point": 75000,
        "population": 2180,
        "difficulty": "High"
    },
}


def hedis_analyzer_ui():
    """UI for HEDIS gap analyzer page."""
    avg_gap = sum((m['benchmark'] - m['current_rate']) for m in HEDIS_MEASURES.values()) / len(HEDIS_MEASURES)
    total_pop = sum(m['population'] for m in HEDIS_MEASURES.values())

    return mobile_page(
        "📊 HEDIS Gap Analyzer",

        # Introduction card
        mobile_card(
            "Quality Gap Identification & ROI Analysis",
            ui.markdown("""
            Identify **highest-ROI HEDIS measure improvement opportunities** for
            Medicare Advantage Star Ratings optimization.

            Our analytics prioritize gaps based on gap size, financial impact,
            Star Rating influence, and improvement feasibility.
            """)
        ),

        # Quick stats overview
        mobile_card(
            "Portfolio Overview",
            ui.div(
                metric_box("Total Measures", str(len(HEDIS_MEASURES)), color="#7c3aed"),
                metric_box("Avg Gap to Benchmark", f"{avg_gap:.1f}%", color="#ff6b00"),
                metric_box("Total Population", f"{total_pop:,}", color="#28a745"),
                style="display: flex; flex-direction: column; gap: 0.75rem;"
            )
        ),

        # Measure selection card
        mobile_card(
            "Select HEDIS Measure",
            mobile_input_group(
                "Choose Measure to Analyze",
                ui.input_select(
                    "hedis_measure",
                    "",
                    choices={
                        "": "-- Select a measure --",
                        **{k: f"{v['name']} ({v['category']})" for k, v in HEDIS_MEASURES.items()}
                    }
                ),
                help_text="Select a HEDIS measure to view detailed gap analysis and improvement scenarios",
                required=True
            ),

            # Measure overview (shown when selected)
            ui.output_ui("measure_overview"),

            divider(),

            mobile_button(
                "Analyze Gaps & ROI",
                "analyze_btn",
                "success",
                icon="📈"
            )
        ),

        # Analysis results (shown after clicking button)
        ui.output_ui("gap_analysis")
    )


def hedis_analyzer_server(input, output, session, get_current_page=lambda: "hedis"):
    """Server logic for HEDIS gap analyzer."""

    @output
    @render.ui
    def measure_overview():
        """Show measure overview when one is selected."""
        if get_current_page() != "hedis":
            return None
        measure_code = input.hedis_measure()

        if not measure_code or measure_code == "":
            return None

        measure = HEDIS_MEASURES[measure_code]
        gap = measure['benchmark'] - measure['current_rate']

        # Determine status color
        if measure['current_rate'] >= measure['benchmark']:
            status = "✅ Exceeding Benchmark"
            status_color = "#28a745"
        elif measure['current_rate'] >= measure['national_avg']:
            status = "⚠️ Above National Average"
            status_color = "#ffc107"
        else:
            status = "🔴 Below National Average"
            status_color = "#dc3545"

        return ui.div(
            ui.tags.h4(
                "Measure Overview",
                style="color: #7c3aed; margin: 1rem 0 0.75rem 0; font-size: 1.1rem;"
            ),

            info_row("Measure Code", measure_code),
            info_row("Full Name", measure['name']),
            info_row("Category", measure['category']),

            divider(),

            ui.div(
                ui.tags.strong("Current Performance: ", style="color: #666;"),
                ui.tags.span(
                    f"{measure['current_rate']}%",
                    style="font-size: 1.5rem; font-weight: 700; color: #7c3aed;"
                ),
                style="margin-bottom: 0.5rem;"
            ),

            progress_bar(
                measure['current_rate'],
                label=f"{measure['current_rate']}%",
                color="#7c3aed"
            ),

            info_row("Benchmark Target", f"{measure['benchmark']}%", highlight=True),
            info_row("National Average", f"{measure['national_avg']}%"),
            info_row("Gap to Close", f"{gap:.1f} percentage points"),

            divider(),

            ui.div(
                ui.tags.div(
                    status,
                    style=f"background: {status_color}; color: white; padding: 0.75rem; border-radius: 8px; text-align: center; font-weight: 600; margin-bottom: 1rem;"
                )
            ),

            info_row("Eligible Population", f"{measure['population']:,} members"),
            info_row("Star Impact Weight", measure['weight']),
            info_row("Implementation Difficulty", measure['difficulty']),

            style="margin-top: 1rem;"
        )

    @output
    @render.ui
    @reactive.event(input.analyze_btn)
    def gap_analysis():
        """Display comprehensive gap analysis with ROI scenarios."""
        if get_current_page() != "hedis":
            return None
        measure_code = input.hedis_measure()

        # Validation
        if not measure_code or measure_code == "":
            return mobile_card(
                "⚠️ Selection Required",
                alert_box(
                    "Please select a HEDIS measure before running the analysis.",
                    type="warning"
                )
            )

        measure = HEDIS_MEASURES[measure_code]
        gap = measure['benchmark'] - measure['current_rate']

        # Calculate improvement scenarios
        scenarios = [
            {
                "level": "Conservative (1% improvement)",
                "improvement_pct": 1.0,
                "new_rate": measure['current_rate'] + 1.0,
                "revenue": round(measure['roi_per_point'] * 1),
                "effort": "Low",
                "timeline": "3-6 months"
            },
            {
                "level": "Moderate (3% improvement)",
                "improvement_pct": 3.0,
                "new_rate": measure['current_rate'] + 3.0,
                "revenue": round(measure['roi_per_point'] * 3),
                "effort": "Medium",
                "timeline": "6-9 months"
            },
            {
                "level": "Aggressive (5% improvement)",
                "improvement_pct": 5.0,
                "new_rate": measure['current_rate'] + 5.0,
                "revenue": round(measure['roi_per_point'] * 5),
                "effort": "High",
                "timeline": "9-12 months"
            },
            {
                "level": f"Full Gap Closure ({gap:.1f}% improvement)",
                "improvement_pct": gap,
                "new_rate": measure['benchmark'],
                "revenue": round(measure['roi_per_point'] * gap),
                "effort": "Very High",
                "timeline": "12-18 months"
            }
        ]

        # Calculate star rating impact
        total_star_impact = measure['star_impact'] * (gap / 10)

        return ui.div(
            mobile_card(
                "📊 Gap Analysis Results",

                ui.div(
                    ui.tags.h3(
                        f"{gap:.1f}% Gap to Benchmark",
                        style="color: #dc3545; text-align: center; margin: 0 0 1rem 0;"
                    ),
                    ui.tags.p(
                        f"Closing this gap could improve overall Star Rating by up to {total_star_impact:.2f} stars",
                        style="text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;"
                    ),
                    style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;"
                ),

                ui.markdown(f"""
                **Performance Gap Details:**
                - Gap size: **{gap:.1f} percentage points**
                - Relative to national avg: **{measure['current_rate'] - measure['national_avg']:.1f}pp**
                - Members affected: **{measure['population']:,}**
                - Revenue at risk: **${round(measure['roi_per_point'] * gap):,.0f}**
                """)
            ),

            mobile_card(
                "💰 ROI Improvement Scenarios",

                *[
                    ui.div(
                        ui.div(
                            ui.tags.h4(
                                scenario['level'],
                                style="color: #7c3aed; margin: 0 0 0.75rem 0; font-size: 1rem;"
                            ),

                            ui.div(
                                ui.tags.div(
                                    "Projected Revenue Impact",
                                    class_="scenario-subtitle",
                                    style="font-size: 0.875rem; color: #666; margin-bottom: 0.25rem;"
                                ),
                                ui.tags.div(
                                    f"${scenario['revenue']:,.0f}",
                                    class_="scenario-revenue",
                                    style="font-size: 2rem; font-weight: 700; color: #28a745; margin-bottom: 0.5rem;"
                                ),
                                class_="scenario-revenue-box",
                                style="text-align: center; background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;"
                            ),

                            ui.div(
                                ui.tags.strong("New Performance Rate: ", class_="scenario-label", style="color: #333;"),
                                ui.tags.span(f"{scenario['new_rate']:.1f}%", class_="scenario-value", style="color: #7c3aed; font-weight: 600;"),
                                class_="scenario-detail",
                                style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                            ),
                            ui.div(
                                ui.tags.strong("Improvement: ", class_="scenario-label", style="color: #333;"),
                                ui.tags.span(f"+{scenario['improvement_pct']:.1f}pp", class_="scenario-value", style="color: #28a745; font-weight: 600;"),
                                class_="scenario-detail scenario-highlight",
                                style="padding: 0.5rem 0; background: #f5f3ff; border-bottom: 1px solid #e0e0e0;"
                            ),
                            ui.div(
                                ui.tags.strong("Effort Level: ", class_="scenario-label", style="color: #333;"),
                                ui.tags.span(scenario['effort'], class_="scenario-value", style="color: #555; font-weight: 600;"),
                                class_="scenario-detail",
                                style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                            ),
                            ui.div(
                                ui.tags.strong("Timeline: ", class_="scenario-label", style="color: #333;"),
                                ui.tags.span(scenario['timeline'], class_="scenario-value", style="color: #555; font-weight: 600;"),
                                class_="scenario-detail",
                                style="padding: 0.5rem 0;"
                            ),

                            class_="scenario-card",
                            style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem; width: 100%;"
                        )
                    )
                    for scenario in scenarios
                ],

                header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
            ),

            style="margin-top: 1.5rem;"
        )


__all__ = ['hedis_analyzer_ui', 'hedis_analyzer_server']
