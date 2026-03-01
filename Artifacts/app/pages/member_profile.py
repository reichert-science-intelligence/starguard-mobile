"""Member 360° Profile - Mobile optimized."""

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

# Sample member profiles
MEMBER_PROFILES = {
    "M001847": {
        "name": "Patricia Anderson",
        "age": 68,
        "gender": "Female",
        "member_id": "M001847",
        "photo": "👤",
        "risk_tier": "Very High",
        "risk_score": 3.2,
        "hcc_codes": ["HCC 18", "HCC 85", "HCC 111", "HCC 134", "HCC 96"],
        "conditions": ["Diabetes (Type 2)", "CHF", "COPD", "CKD Stage 4", "CAD"],
        "last_hospitalization": 45,
        "er_visits_12m": 3,
        "predictive_trend": "Rising",
        "open_gaps": [
            {"code": "HBD", "name": "Hemoglobin A1c Control", "due_date": "30 days", "overdue": 5, "value": 890, "intervention": "Phone + PCP"},
            {"code": "CBP", "name": "Controlling Blood Pressure", "due_date": "45 days", "overdue": 0, "value": 1120, "intervention": "Office Visit"},
            {"code": "BCS", "name": "Breast Cancer Screening", "due_date": "90 days", "overdue": 0, "value": 650, "intervention": "Direct Mail"}
        ],
        "closed_gaps": 2,
        "gap_closure_rate": 40.0,
        "pcp": {"name": "Dr. Sarah Mitchell", "quality": 92.4, "last_visit": 12, "next_visit": 30},
        "specialists": ["Cardiology - Dr. Emily Chen", "Endocrinology - Dr. Michael Thompson"],
        "star_contribution": 0.18,
        "annual_revenue": 2890,
        "revenue_at_risk": 2660,
        "cost_of_care": 45600,
        "high_utilizer": True,
        "contact_pref": "Phone",
        "best_time": "Afternoons",
        "language": "English",
        "last_contact": 8,
        "response_rate": 65,
        "sdoh": {"transportation": True, "food": False, "housing": "Stable", "isolation": "Low"},
        "ai_recommendation": "Schedule PCP visit for overdue HbA1c test. High priority intervention.",
        "closure_probability": 78,
        "recommended_channel": "Phone + PCP coordination"
    },
    "M002156": {
        "name": "James Martinez",
        "age": 72,
        "gender": "Male",
        "member_id": "M002156",
        "photo": "👤",
        "risk_tier": "High",
        "risk_score": 2.8,
        "hcc_codes": ["HCC 18", "HCC 85", "HCC 108"],
        "conditions": ["Diabetes (Type 2)", "CHF", "Vascular Disease"],
        "last_hospitalization": 120,
        "er_visits_12m": 1,
        "predictive_trend": "Stable",
        "open_gaps": [
            {"code": "CCS", "name": "Colorectal Cancer Screening", "due_date": "60 days", "overdue": 0, "value": 780, "intervention": "Patient Portal"},
            {"code": "HBD", "name": "Hemoglobin A1c Control", "due_date": "45 days", "overdue": 2, "value": 890, "intervention": "Phone Outreach"}
        ],
        "closed_gaps": 3,
        "gap_closure_rate": 60.0,
        "pcp": {"name": "Dr. James Rodriguez", "quality": 88.6, "last_visit": 25, "next_visit": 60},
        "specialists": ["Cardiology - Dr. Emily Chen"],
        "star_contribution": 0.15,
        "annual_revenue": 1815,
        "revenue_at_risk": 1670,
        "cost_of_care": 32400,
        "high_utilizer": False,
        "contact_pref": "Phone",
        "best_time": "Mornings",
        "language": "Spanish",
        "last_contact": 6,
        "response_rate": 82,
        "sdoh": {"transportation": False, "food": False, "housing": "Stable", "isolation": "Low"},
        "ai_recommendation": "Portal message for CCS screening. Member is portal-active.",
        "closure_probability": 85,
        "recommended_channel": "Patient Portal"
    }
}

# Timeline events (MM/DD/YYYY format)
TIMELINE_EVENTS = [
    {"date": "02/14/2026", "type": "Contact", "detail": "Phone outreach - Left voicemail", "outcome": "Pending"},
    {"date": "02/10/2026", "type": "Lab", "detail": "HbA1c result: 8.2% (Above target)", "outcome": "Alert"},
    {"date": "02/03/2026", "type": "Visit", "detail": "PCP Office Visit - Dr. Mitchell", "outcome": "Completed"},
    {"date": "01/28/2026", "type": "Contact", "detail": "Direct mail sent - BCS reminder", "outcome": "Delivered"},
    {"date": "01/15/2026", "type": "Gap Closed", "detail": "MAD - Medication Adherence confirmed", "outcome": "Success"},
    {"date": "01/08/2026", "type": "Contact", "detail": "Phone outreach - Spoke with member", "outcome": "Success"}
]


def member_profile_ui():
    """UI for member 360° profile."""
    return mobile_page(
        "👤 Member 360° Profile",

        # Member selector
        mobile_card(
            "Select Member",
            ui.input_select(
                "selected_member",
                "",
                choices={
                    "M001847": "Patricia Anderson - Age 68, Very High Risk",
                    "M002156": "James Martinez - Age 72, High Risk"
                },
                selected="M001847"
            )
        ),

        # Member header
        mobile_card(
            "",
            ui.output_ui("member_header"),
            header_color="linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
        ),

        # Risk & Clinical Summary
        mobile_card(
            "🏥 Risk & Clinical Summary",
            ui.output_ui("risk_clinical")
        ),

        # Care Gaps
        mobile_card(
            "📋 Care Gap Status",
            ui.output_ui("care_gaps"),
            header_color="linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
        ),

        # Intervention Timeline
        mobile_card(
            "📅 Intervention Timeline",
            ui.output_ui("timeline")
        ),

        # Care Team
        mobile_card(
            "👨‍⚕️ Care Team",
            ui.output_ui("care_team"),
            header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
        ),

        # Quality Performance
        mobile_card(
            "⭐ Quality Measures Performance",
            ui.output_ui("quality_performance")
        ),

        # Financial Impact
        mobile_card(
            "💰 Financial Impact",
            ui.output_ui("financial_impact"),
            header_color="linear-gradient(135deg, #ff6b00 0%, #cc5500 100%)"
        ),

        # Communication
        mobile_card(
            "📞 Communication Preferences",
            ui.output_ui("communication")
        ),

        # SDOH
        mobile_card(
            "🏠 Social Determinants",
            ui.output_ui("sdoh")
        ),

        # AI Recommendations
        mobile_card(
            "🤖 AI-Powered Recommendations",
            ui.output_ui("ai_recommendations"),
            header_color="linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
        )
    )


def member_profile_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for member 360° profile."""

    def _is_on_profile_page():
        """Check if we're on the profile page."""
        try:
            return get_current_page() == "profile"
        except Exception:
            return False

    def get_member():
        """Get selected member data."""
        member_id = input.selected_member()
        return MEMBER_PROFILES.get(member_id, MEMBER_PROFILES["M001847"])

    @output
    @render.ui
    def member_header():
        """Display member header card."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        risk_colors = {
            "Very High": "#dc3545",
            "High": "#ff6b00",
            "Medium": "#ffc107",
            "Low": "#28a745"
        }

        return ui.div(
            # Member photo and name
            ui.div(
                ui.tags.div(
                    member["photo"],
                    style="font-size: 4rem; text-align: center; margin-bottom: 1rem;"
                ),
                ui.tags.h2(
                    member["name"],
                    style="color: #666 !important; text-align: center; margin: 0 0 0.5rem 0; font-size: 1.5rem; font-weight: 600;"
                ),
                ui.tags.div(
                    f"{member['age']} years old • {member['gender']} • ID: {member['member_id']}",
                    style="color: #666; text-align: center; font-size: 0.875rem; margin-bottom: 1rem;"
                ),
                ui.tags.div(
                    ui.tags.span(
                        f"{member['risk_tier']} Risk",
                        style=f"background: {risk_colors[member['risk_tier']]}; color: white; padding: 0.5rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 1rem; display: inline-block;"
                    ),
                    style="text-align: center; margin-bottom: 1.5rem;"
                ),

                # Quick actions
                ui.div(
                    ui.tags.div(
                        mobile_button("📞 Contact", "contact_btn", "primary"),
                        ui.tags.div(
                            "💡 Initiates outreach workflow with member's preferred contact method and best time",
                            style="color: #666; font-size: 0.75rem; font-style: italic; margin-top: 0.25rem; padding: 0.5rem; background: #f8f9fa; border-radius: 4px;"
                        ),
                        style="margin-bottom: 0.75rem;"
                    ),
                    ui.tags.div(
                        mobile_button("📋 Assign Task", "assign_btn", "secondary"),
                        ui.tags.div(
                            "💡 Creates care management task and assigns to appropriate team member based on gap type",
                            style="color: #666; font-size: 0.75rem; font-style: italic; margin-top: 0.25rem; padding: 0.5rem; background: #f8f9fa; border-radius: 4px;"
                        ),
                        style="margin-bottom: 0.75rem;"
                    ),
                    ui.tags.div(
                        mobile_button("📊 View Full History", "history_btn", "secondary"),
                        ui.tags.div(
                            "💡 Opens complete member history including claims, encounters, and all care interactions",
                            style="color: #666; font-size: 0.75rem; font-style: italic; margin-top: 0.25rem; padding: 0.5rem; background: #f8f9fa; border-radius: 4px;"
                        ),
                    ),
                )
            )
        )

    @output
    @render.ui
    def risk_clinical():
        """Display risk and clinical summary."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        return ui.div(
            metric_box(
                "RAF Score",
                f"{member['risk_score']:.1f}",
                color="#dc3545",
                subtitle=f"{member['risk_tier']} Risk"
            ),
            metric_box(
                "Active HCC Codes",
                f"{len(member['hcc_codes'])}",
                color="#ff6b00",
                subtitle=", ".join(member['hcc_codes'][:3]) + "..."
            ),
            metric_box(
                "ER Visits (12M)",
                f"{member['er_visits_12m']}",
                color="#ffc107",
                subtitle=f"Last hospitalization: {member['last_hospitalization']} days ago"
            ),
            metric_box(
                "Predictive Trend",
                member['predictive_trend'],
                color="#7c3aed" if member['predictive_trend'] == "Rising" else "#28a745",
                subtitle="AI prediction"
            ),

            ui.tags.h3(
                "Chronic Conditions",
                style="color: #666 !important; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0;"
            ),

            ui.div(
                *[
                    ui.div(
                        f"• {condition}",
                        style="padding: 0.5rem 0; color: #666 !important; font-weight: 500;"
                    )
                    for condition in member['conditions']
                ]
            ),

            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def care_gaps():
        """Display care gap status."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        return ui.div(
            # Summary metrics
            ui.div(
                metric_box(
                    "Open Gaps",
                    f"{len(member['open_gaps'])}",
                    color="#dc3545",
                    subtitle="Requiring closure"
                ),
                metric_box(
                    "Closed YTD",
                    f"{member['closed_gaps']}",
                    color="#28a745",
                    subtitle=f"{member['gap_closure_rate']:.0f}% closure rate"
                ),
                metric_box(
                    "Revenue at Risk",
                    f"${sum(g['value'] for g in member['open_gaps']):,}",
                    color="#ff6b00",
                    subtitle="Potential revenue"
                ),
                style="display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.5rem;"
            ),

            ui.tags.h3(
                "Open Care Gaps",
                style="color: #666 !important; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0;"
            ),

            # Individual gaps
            *[
                ui.div(
                    ui.tags.h4(
                        gap['name'],
                        style="color: #000000 !important; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 700;"
                    ),

                    ui.div(
                        ui.tags.strong("Measure Code: ", style="color: #666; font-weight: 600;"),
                        ui.tags.span(gap['code'], style="color: #7c3aed; font-weight: 700;"),
                        style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Due Date: ", style="color: #666; font-weight: 600;"),
                        ui.tags.span(
                            gap['due_date'] + (f" (Overdue: {gap['overdue']} days)" if gap['overdue'] > 0 else " (On track)"),
                            style=f"color: {'#dc3545' if gap['overdue'] > 0 else '#28a745'}; font-weight: 700;"
                        ),
                        style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Closure Value: ", style="color: #666; font-weight: 600;"),
                        ui.tags.span(
                            f"${gap['value']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.25rem;"
                        ),
                        style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Recommended: ", style="color: #666; font-weight: 600;"),
                        ui.tags.span(gap['intervention'], style="color: #7c3aed; font-weight: 700;"),
                        style="padding: 0.5rem 0;"
                    ),

                    class_="member-profile-card",
                    style="padding: 1.25rem; background: white; border-left: 4px solid #dc3545; border-radius: 8px; margin-bottom: 1rem;"
                )
                for gap in member['open_gaps']
            ]
        )

    @output
    @render.ui
    def timeline():
        """Display intervention timeline."""
        if not _is_on_profile_page():
            return None

        outcome_colors = {
            "Success": "#28a745",
            "Pending": "#ffc107",
            "Alert": "#dc3545",
            "Completed": "#7c3aed",
            "Delivered": "#0066cc"
        }

        type_icons = {
            "Contact": "📞",
            "Visit": "🏥",
            "Lab": "🔬",
            "Gap Closed": "✅"
        }

        return ui.div(
            *[
                ui.div(
                    ui.div(
                        ui.tags.span(
                            type_icons.get(event['type'], "📋"),
                            style="font-size: 1.5rem; margin-right: 0.75rem;"
                        ),
                        ui.tags.div(
                            ui.tags.div(
                                f"{event['type']} • {event['date']}",
                                style="font-weight: 700; color: #000000 !important; margin-bottom: 0.25rem; font-size: 0.9rem;"
                            ),
                            ui.tags.div(
                                event['detail'],
                                style="color: #666; font-size: 0.875rem; margin-bottom: 0.25rem;"
                            ),
                            ui.tags.div(
                                ui.tags.span(
                                    event['outcome'],
                                    style=f"background: {outcome_colors[event['outcome']]}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 600;"
                                )
                            ),
                            style="flex: 1;"
                        ),
                        style="display: flex; align-items: flex-start;"
                    ),
                    class_="member-profile-card",
                    style="padding: 1rem; background: #f8f9fa; border-left: 3px solid #7c3aed; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for event in TIMELINE_EVENTS
            ]
        )

    @output
    @render.ui
    def care_team():
        """Display care team information."""
        if not _is_on_profile_page():
            return None

        member = get_member()
        pcp = member['pcp']

        return ui.div(
            # PCP info
            ui.div(
                ui.tags.h4(
                    "Primary Care Physician",
                    style="color: #666; margin: 0 0 0.75rem 0; font-size: 0.875rem; font-weight: 600; text-transform: uppercase;"
                ),

                ui.tags.div(
                    pcp['name'],
                    style="color: #000000 !important; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;"
                ),

                ui.div(
                    ui.tags.strong("Quality Score: ", style="color: #666; font-weight: 600;"),
                    ui.tags.span(
                        f"{pcp['quality']}%",
                        style="color: #000000 !important; font-weight: 900 !important; font-size: 1.25rem;"
                    ),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),

                ui.div(
                    ui.tags.strong("Last Visit: ", style="color: #666; font-weight: 600;"),
                    ui.tags.span(f"{pcp['last_visit']} days ago", style="color: #000000 !important; font-weight: 700;"),
                    style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                ),

                ui.div(
                    ui.tags.strong("Next Scheduled: ", style="color: #666; font-weight: 600;"),
                    ui.tags.span(f"In {pcp['next_visit']} days", style="color: #7c3aed; font-weight: 700;"),
                    style="padding: 0.5rem 0;"
                ),

                class_="member-profile-card",
                style="padding: 1.25rem; background: #f0f7f0; border-radius: 12px; margin-bottom: 1rem;"
            ),

            # Specialists
            ui.tags.h3(
                "Specialists",
                style="color: #666 !important; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0;"
            ),

            ui.div(
                *[
                    ui.div(
                        f"• {specialist}",
                        style="padding: 0.5rem 0; color: #666 !important; font-weight: 500;"
                    )
                    for specialist in member['specialists']
                ]
            )
        )

    @output
    @render.ui
    def quality_performance():
        """Display quality measures performance."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        return ui.div(
            metric_box(
                "Star Contribution",
                f"+{member['star_contribution']:.2f}",
                color="#28a745",
                subtitle="Impact on plan rating"
            ),
            metric_box(
                "Gap Closure Rate",
                f"{member['gap_closure_rate']:.0f}%",
                color="#7c3aed",
                subtitle=f"{member['closed_gaps']} of {len(member['open_gaps']) + member['closed_gaps']} closed"
            ),

            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def financial_impact():
        """Display financial impact."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        return ui.div(
            metric_box(
                "Annual Revenue",
                f"${member['annual_revenue']:,}",
                color="#28a745",
                subtitle="Risk-adjusted capitation"
            ),
            metric_box(
                "Revenue at Risk",
                f"${member['revenue_at_risk']:,}",
                color="#dc3545",
                subtitle="Open gap opportunity"
            ),
            metric_box(
                "Cost of Care (12M)",
                f"${member['cost_of_care']:,}",
                color="#ff6b00",
                subtitle="Total medical expenses"
            ),

            ui.div(
                alert_box(
                    "⚠️ High Utilizer Flag: Member exceeds 90th percentile for cost",
                    type="warning"
                ) if member['high_utilizer'] else alert_box(
                    "✓ Normal Utilization Pattern",
                    type="success"
                )
            ),

            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def communication():
        """Display communication preferences."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        return ui.div(
            ui.div(
                ui.tags.strong("Preferred Method: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    member['contact_pref'],
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.25rem; display: block; margin-top: 0.25rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Best Time: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    member['best_time'],
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.25rem; display: block; margin-top: 0.25rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Language: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    member['language'],
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.25rem; display: block; margin-top: 0.25rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Last Contact: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    f"{member['last_contact']} days ago",
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.25rem; display: block; margin-top: 0.25rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Response Rate: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    f"{member['response_rate']}%",
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.25rem; display: block; margin-top: 0.25rem;"
                ),
                progress_bar(
                    member['response_rate'],
                    label="",
                    color="#28a745"
                ),
                style="padding: 0.75rem 0;"
            )
        )

    @output
    @render.ui
    def sdoh():
        """Display social determinants of health."""
        if not _is_on_profile_page():
            return None

        member = get_member()
        sdoh = member['sdoh']

        return ui.div(
            ui.div(
                ui.tags.strong("Transportation Barrier: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    "Yes - Flagged" if sdoh['transportation'] else "No",
                    style="color: #999; font-weight: 600; font-size: 1.1rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Food Insecurity: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    "Yes - Flagged" if sdoh['food'] else "No",
                    style="color: #999; font-weight: 600; font-size: 1.1rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Housing Stability: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    sdoh['housing'],
                    style="color: #999; font-weight: 600; font-size: 1.1rem;"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
            ),

            ui.div(
                ui.tags.strong("Social Isolation Risk: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    sdoh['isolation'],
                    style="color: #999; font-weight: 600; font-size: 1.1rem;"
                ),
                style="padding: 0.75rem 0;"
            ),

            ui.div(
                alert_box(
                    "⚠️ Transportation barrier identified - consider home health or telehealth options",
                    type="warning"
                ) if sdoh['transportation'] else None
            )
        )

    @output
    @render.ui
    def ai_recommendations():
        """Display AI-powered recommendations."""
        if not _is_on_profile_page():
            return None

        member = get_member()

        return ui.div(
            # Next best action
            ui.div(
                ui.tags.h4(
                    "Next Best Action",
                    style="color: #7c3aed; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 700;"
                ),
                ui.tags.div(
                    member['ai_recommendation'],
                    style="color: #666 !important; font-weight: 600; font-size: 1.1rem; line-height: 1.5; margin-bottom: 1rem;"
                ),
                class_="member-profile-card",
                style="padding: 1.25rem; background: #f5f3ff; border-left: 4px solid #7c3aed; border-radius: 12px; margin-bottom: 1rem;"
            ),

            # Prediction metrics
            ui.div(
                ui.tags.strong("Predicted Success: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    f"{member['closure_probability']}%",
                    style="color: #999 !important; font-weight: 600 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                ),
                progress_bar(
                    member['closure_probability'],
                    label="",
                    color="#28a745"
                ),
                style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 0.75rem;"
            ),

            ui.div(
                ui.tags.strong("Recommended Channel: ", style="color: #666; font-weight: 600;"),
                ui.tags.span(
                    member['recommended_channel'],
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.25rem; display: block; margin-top: 0.25rem;"
                ),
                style="padding: 0.75rem 0;"
            ),

            # Action button
            ui.div(
                mobile_button(
                    "Execute Recommendation",
                    "execute_btn",
                    "primary",
                    icon="🚀"
                ),
                ui.tags.div(
                    "💡 Triggers AI-recommended intervention: schedules PCP appointment, sends member reminder, creates care manager task, and updates workflow queue",
                    style="color: #666; font-size: 0.75rem; font-style: italic; margin-top: 0.5rem; padding: 0.5rem; background: #f5f3ff; border-radius: 4px; border-left: 3px solid #7c3aed;"
                ),
                style="margin-top: 1rem;"
            )
        )


__all__ = ['member_profile_ui', 'member_profile_server']
