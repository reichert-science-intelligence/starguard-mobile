"""Care Gap Closure Workflow - Mobile optimized."""

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

# Sample member data with open care gaps
MEMBER_QUEUE = [
    {
        "member_id": "M001847",
        "name": "Patricia Anderson",
        "age": 68,
        "risk_score": 3.2,
        "open_gaps": 3,
        "priority": "High",
        "gaps": ["HBD", "CBP", "BCS"],
        "last_contact": "14 days ago",
        "phone": "(412) 555-0198",
        "preferred_contact": "Phone"
    },
    {
        "member_id": "M002156",
        "name": "James Martinez",
        "age": 72,
        "risk_score": 2.8,
        "open_gaps": 2,
        "priority": "High",
        "gaps": ["CCS", "HBD"],
        "last_contact": "8 days ago",
        "phone": "(412) 555-0234",
        "preferred_contact": "Phone"
    },
    {
        "member_id": "M003421",
        "name": "Mary Johnson",
        "age": 65,
        "risk_score": 1.9,
        "open_gaps": 2,
        "priority": "Medium",
        "gaps": ["MAD", "BCS"],
        "last_contact": "21 days ago",
        "phone": "(412) 555-0167",
        "preferred_contact": "Mail"
    },
    {
        "member_id": "M004892",
        "name": "Robert Chen",
        "age": 70,
        "risk_score": 2.5,
        "open_gaps": 1,
        "priority": "Medium",
        "gaps": ["CBP"],
        "last_contact": "6 days ago",
        "phone": "(412) 555-0289",
        "preferred_contact": "Portal"
    },
    {
        "member_id": "M005234",
        "name": "Linda Williams",
        "age": 66,
        "risk_score": 1.4,
        "open_gaps": 1,
        "priority": "Low",
        "gaps": ["CCS"],
        "last_contact": "45 days ago",
        "phone": "(412) 555-0312",
        "preferred_contact": "Phone"
    },
    {
        "member_id": "M006745",
        "name": "David Thompson",
        "age": 69,
        "risk_score": 3.5,
        "open_gaps": 4,
        "priority": "High",
        "gaps": ["HBD", "CBP", "CCS", "OMW"],
        "last_contact": "3 days ago",
        "phone": "(412) 555-0445",
        "preferred_contact": "Phone"
    },
    {
        "member_id": "M007123",
        "name": "Sarah Davis",
        "age": 67,
        "risk_score": 2.1,
        "open_gaps": 2,
        "priority": "Medium",
        "gaps": ["BCS", "MAD"],
        "last_contact": "12 days ago",
        "phone": "(412) 555-0556",
        "preferred_contact": "Mail"
    },
    {
        "member_id": "M008901",
        "name": "Michael Brown",
        "age": 71,
        "risk_score": 1.6,
        "open_gaps": 1,
        "priority": "Low",
        "gaps": ["CCS"],
        "last_contact": "30 days ago",
        "phone": "(412) 555-0678",
        "preferred_contact": "Portal"
    },
]

# Gap definitions
GAP_DEFINITIONS = {
    "HBD": {
        "name": "Hemoglobin A1c Control",
        "due_date": "30 days",
        "closure_value": "$890",
        "difficulty": "Medium"
    },
    "CBP": {
        "name": "Controlling Blood Pressure",
        "due_date": "45 days",
        "closure_value": "$1,120",
        "difficulty": "Medium"
    },
    "CCS": {
        "name": "Colorectal Cancer Screening",
        "due_date": "60 days",
        "closure_value": "$780",
        "difficulty": "Low"
    },
    "BCS": {
        "name": "Breast Cancer Screening",
        "due_date": "90 days",
        "closure_value": "$650",
        "difficulty": "Low"
    },
    "MAD": {
        "name": "Medication Adherence - Diabetes",
        "due_date": "15 days",
        "closure_value": "$420",
        "difficulty": "High"
    },
    "OMW": {
        "name": "Osteoporosis Management",
        "due_date": "60 days",
        "closure_value": "$560",
        "difficulty": "High"
    }
}

# Intervention strategies
INTERVENTION_STRATEGIES = {
    "Phone Outreach": {
        "success_rate": 42,
        "avg_time": "3 days",
        "cost": "$12"
    },
    "Automated IVR": {
        "success_rate": 28,
        "avg_time": "1 day",
        "cost": "$3"
    },
    "Direct Mail": {
        "success_rate": 18,
        "avg_time": "14 days",
        "cost": "$8"
    },
    "Patient Portal Message": {
        "success_rate": 35,
        "avg_time": "5 days",
        "cost": "$2"
    },
    "PCP Office Visit": {
        "success_rate": 65,
        "avg_time": "21 days",
        "cost": "$45"
    }
}


def care_gap_workflow_ui():
    """UI for care gap closure workflow page."""
    return mobile_page(
        "Care Gap Closure Workflow",

        # Introduction card
        mobile_card(
            "Automated Care Gap Management",
            ui.markdown("""
            **AI-powered workflow automation** for HEDIS gap closure and member outreach.

            Prioritizes members by risk score and gap value, recommends optimal
            intervention strategies, and tracks closure success in real-time.
            """)
        ),

        # Queue summary
        mobile_card(
            "Current Gap Closure Queue",
            ui.output_ui("queue_summary")
        ),

        # Priority filter
        mobile_card(
            "Filter Members by Priority",
            ui.input_radio_buttons(
                "priority_filter",
                "",
                choices={
                    "All": "All Members",
                    "High": "High Priority",
                    "Medium": "Medium Priority",
                    "Low": "Low Priority"
                },
                selected="All",
                inline=False
            ),
            ui.output_ui("filtered_count")
        ),

        # Member queue
        mobile_card(
            "Member Queue",
            ui.output_ui("member_queue"),
            header_color="linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
        ),

        # Intervention recommendations
        mobile_card(
            "Recommended Intervention Strategies",
            ui.output_ui("intervention_recommendations")
        ),

        # Campaign performance
        mobile_card(
            "Active Campaign Performance",
            ui.output_ui("campaign_performance"),
            header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
        )
    )


def care_gap_workflow_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for care gap closure workflow."""

    def _is_on_workflow_page():
        """Check if we're on the workflow page."""
        try:
            return get_current_page() == "workflow"
        except Exception:
            return False

    @output
    @render.ui
    def queue_summary():
        """Display queue summary metrics."""
        if not _is_on_workflow_page():
            return None

        total_members = len(MEMBER_QUEUE)
        total_gaps = sum(m["open_gaps"] for m in MEMBER_QUEUE)
        high_priority = len([m for m in MEMBER_QUEUE if m["priority"] == "High"])
        avg_risk = sum(m["risk_score"] for m in MEMBER_QUEUE) / total_members

        return ui.div(
            metric_box("Total Members", f"{total_members}", color="#7c3aed", subtitle="In queue"),
            metric_box("Open Gaps", f"{total_gaps}", color="#ff6b00", subtitle="Requiring closure"),
            metric_box("High Priority", f"{high_priority}", color="#dc3545", subtitle="Urgent attention"),
            metric_box("Avg Risk Score", f"{avg_risk:.1f}", color="#ffc107", subtitle="RAF complexity"),
            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def filtered_count():
        """Show count of filtered members."""
        if not _is_on_workflow_page():
            return None

        priority = input.priority_filter()

        if priority == "All":
            count = len(MEMBER_QUEUE)
        else:
            count = len([m for m in MEMBER_QUEUE if m["priority"] == priority])

        return ui.div(
            ui.tags.p(
                f"Showing {count} member{'s' if count != 1 else ''}",
                style="text-align: center; color: #666; margin: 0.5rem 0 0 0; font-size: 0.875rem;"
            )
        )

    @output
    @render.ui
    def member_queue():
        """Display filtered member queue."""
        if not _is_on_workflow_page():
            return None

        priority = input.priority_filter()

        # Filter members
        if priority == "All":
            filtered_members = MEMBER_QUEUE
        else:
            filtered_members = [m for m in MEMBER_QUEUE if m["priority"] == priority]

        # Priority colors
        priority_colors = {
            "High": "#dc3545",
            "Medium": "#ffc107",
            "Low": "#28a745"
        }

        return ui.div(
            *[
                ui.div(
                    # Member header
                    ui.div(
                        ui.tags.div(
                            ui.tags.span(
                                member["name"],
                                style="font-weight: 700; font-size: 1.1rem; color: #1a1a1a;"
                            ),
                            ui.tags.span(
                                member["priority"],
                                style=f"background: {priority_colors[member['priority']]}; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;"
                            ),
                            style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;"
                        ),
                        ui.tags.div(
                            f"ID: {member['member_id']} • Age: {member['age']} • Risk Score: {member['risk_score']}",
                            style="color: #666; font-size: 0.875rem; margin-bottom: 0.75rem;"
                        )
                    ),

                    # Gap details
                    ui.div(
                        ui.tags.strong("Open Gaps: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(f"{member['open_gaps']}", style="color: #dc3545; font-weight: 700; font-size: 1.1rem;"),
                        style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    # Gap list
                    ui.div(
                        ui.tags.div(
                            *[
                                ui.tags.span(
                                    f"• {GAP_DEFINITIONS[gap]['name']}",
                                    style="display: block; color: #333; font-size: 0.9rem; padding: 0.25rem 0;"
                                )
                                for gap in member["gaps"]
                            ]
                        ),
                        style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    # Contact info
                    ui.div(
                        ui.tags.strong("Last Contact: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(member["last_contact"], style="color: #666;"),
                        style="padding: 0.5rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),
                    ui.div(
                        ui.tags.strong("Preferred Method: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(member["preferred_contact"], style="color: #7c3aed; font-weight: 600;"),
                        style="padding: 0.5rem 0;"
                    ),

                    # Action button with explanation
                    ui.div(
                        mobile_button(
                            "Assign Interventions",
                            f"assign_btn_{member['member_id']}",
                            "primary",
                            icon="📋"
                        ),
                        ui.tags.div(
                            f"💡 Assigns AI-recommended interventions for {member['open_gaps']} open gaps using member's preferred contact method ({member['preferred_contact']})",
                            style="color: #666; font-size: 0.75rem; font-style: italic; margin-top: 0.5rem; padding: 0.5rem; background: #f5f3ff; border-radius: 4px; border-left: 3px solid #7c3aed;"
                        ),
                        style="margin-top: 0.75rem;"
                    ),

                    class_="member-card",
                    style="padding: 1.25rem; background: white; border-left: 4px solid " + priority_colors[member["priority"]] + "; border-radius: 8px; margin-bottom: 1rem;"
                )
                for member in filtered_members
            ],

            alert_box(
                f"{len(filtered_members)} member{'s' if len(filtered_members) != 1 else ''} ready for outreach",
                type="info"
            ) if len(filtered_members) > 0 else alert_box(
                "No members match the selected priority filter",
                type="warning"
            )
        )

    @output
    @render.ui
    def intervention_recommendations():
        """Display AI-recommended intervention strategies."""
        if not _is_on_workflow_page():
            return None

        return ui.div(
            ui.markdown("""
            **AI-Optimized Intervention Mix**

            Based on member preferences, historical success rates, and cost-effectiveness analysis.
            """),

            divider(),

            *[
                ui.div(
                    ui.tags.h4(
                        strategy,
                        style="color: #1a1a1a; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 700;"
                    ),

                    ui.div(
                        ui.tags.strong("Success Rate: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{data['success_rate']}%",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),
                    ui.div(
                        ui.tags.strong("Avg Time to Close: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            data['avg_time'],
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),
                    ui.div(
                        ui.tags.strong("Cost per Contact: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            data['cost'],
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0;"
                    ),

                    class_="intervention-card",
                    style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
                )
                for strategy, data in INTERVENTION_STRATEGIES.items()
            ]
        )

    @output
    @render.ui
    def campaign_performance():
        """Display active campaign metrics."""
        if not _is_on_workflow_page():
            return None

        # Simulated campaign data
        campaigns = [
            {
                "name": "Q1 Diabetes Control",
                "active_members": 156,
                "gaps_closed": 87,
                "closure_rate": 55.8,
                "revenue_captured": 77580
            },
            {
                "name": "Blood Pressure Outreach",
                "active_members": 203,
                "gaps_closed": 98,
                "closure_rate": 48.3,
                "revenue_captured": 109760
            },
            {
                "name": "Cancer Screening Push",
                "active_members": 412,
                "gaps_closed": 234,
                "closure_rate": 56.8,
                "revenue_captured": 182520
            }
        ]

        return ui.div(
            *[
                ui.div(
                    ui.tags.h4(
                        campaign["name"],
                        style="color: #1a1a1a; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 700;"
                    ),

                    ui.div(
                        ui.tags.strong("Active Members: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{campaign['active_members']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),
                    ui.div(
                        ui.tags.strong("Gaps Closed: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{campaign['gaps_closed']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    # Progress bar for closure rate
                    ui.div(
                        ui.tags.strong("Closure Rate: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.div(
                            ui.tags.span(
                                f"{campaign['closure_rate']:.1f}%",
                                style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin: 0.5rem 0;"
                            ),
                            progress_bar(
                                campaign['closure_rate'],
                                label="",
                                color="#28a745"
                            ),
                            style="margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Revenue Captured: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"${campaign['revenue_captured']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.75rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0;"
                    ),

                    class_="campaign-card",
                    style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
                )
                for campaign in campaigns
            ],

            alert_box(
                f"Total gaps closed: {sum(c['gaps_closed'] for c in campaigns):,} • Revenue: ${sum(c['revenue_captured'] for c in campaigns):,}",
                type="success"
            )
        )


__all__ = ['care_gap_workflow_ui', 'care_gap_workflow_server']
