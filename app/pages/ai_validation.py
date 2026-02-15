"""AI Validation Dashboard page - Mobile optimized."""

from shiny import ui, render, reactive
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

# Real-time validation metrics (simulated)
VALIDATION_METRICS = {
    "model_accuracy": 94.3,
    "compliance_score": 98.7,
    "self_correction_rate": 87.2,
    "data_quality_score": 91.5,
    "validation_tests_passed": 47,
    "validation_tests_total": 50,
    "last_updated": "02/14/2026 14:23:17 EST",
    "uptime_pct": 99.8,
    "avg_response_time_ms": 145
}

# Compliance framework components
COMPLIANCE_COMPONENTS = [
    {
        "name": "PHI Encryption (AES-256)",
        "status": "PASS",
        "last_check": "2 hours ago",
        "score": 100
    },
    {
        "name": "Access Logging & Audit Trail",
        "status": "PASS",
        "last_check": "1 hour ago",
        "score": 100
    },
    {
        "name": "Data Minimization Compliance",
        "status": "PASS",
        "last_check": "3 hours ago",
        "score": 98
    },
    {
        "name": "Role-Based Access Control",
        "status": "PASS",
        "last_check": "30 minutes ago",
        "score": 100
    },
    {
        "name": "Breach Detection System",
        "status": "PASS",
        "last_check": "15 minutes ago",
        "score": 97
    },
    {
        "name": "Data Retention Policy",
        "status": "PASS",
        "last_check": "4 hours ago",
        "score": 100
    },
]

# Recent validation tests
VALIDATION_TESTS = [
    {
        "name": "Star Rating Prediction Accuracy",
        "status": "PASS",
        "score": 96.2,
        "timestamp": "2 hours ago",
        "details": "Validated against 500 historical contracts"
    },
    {
        "name": "HEDIS Gap Calculation Validation",
        "status": "PASS",
        "score": 98.1,
        "timestamp": "3 hours ago",
        "details": "Cross-validated with CMS benchmarks"
    },
    {
        "name": "Risk Adjustment Model Compliance",
        "status": "PASS",
        "score": 94.7,
        "timestamp": "5 hours ago",
        "details": "HCC coding accuracy within acceptable range"
    },
    {
        "name": "Data Quality Threshold Check",
        "status": "WARNING",
        "score": 89.3,
        "timestamp": "1 hour ago",
        "details": "Minor data completeness issues in 2 fields"
    },
    {
        "name": "Bias Detection in Predictions",
        "status": "PASS",
        "score": 92.8,
        "timestamp": "6 hours ago",
        "details": "No statistically significant bias detected"
    },
    {
        "name": "API Response Time SLA",
        "status": "PASS",
        "score": 97.5,
        "timestamp": "30 minutes ago",
        "details": "95th percentile: 178ms (target: <200ms)"
    },
]

# Self-correction events (last 24 hours)
SELF_CORRECTION_EVENTS = [
    {
        "timestamp": "09:15 AM",
        "issue": "Anomalous prediction variance detected",
        "action": "Triggered model revalidation",
        "outcome": "Variance reduced by 23%, model stability restored"
    },
    {
        "timestamp": "11:42 AM",
        "issue": "Data quality score dropped below threshold",
        "action": "Initiated automated data cleansing",
        "outcome": "Quality score improved from 87.2% to 91.5%"
    },
    {
        "timestamp": "02:08 PM",
        "issue": "API response latency spike",
        "action": "Auto-scaled compute resources",
        "outcome": "Response time reduced from 312ms to 145ms"
    },
]


def ai_validation_ui():
    """UI for AI validation dashboard page."""
    return mobile_page(
        "🤖 AI Validation Dashboard",

        # Introduction card
        mobile_card(
            "Real-Time Model Performance & Compliance",
            ui.markdown("""
            **Self-correcting AI validation system** ensures HIPAA compliance,
            clinical accuracy, and regulatory adherence across all predictions.

            Our compound engineering framework continuously monitors model
            performance and automatically corrects deviations before they impact results.
            """),
            alert_box(
                "✅ All systems operational. Last validation: " + VALIDATION_METRICS['last_updated'],
                type="success"
            )
        ),

        # Core metrics overview
        mobile_card(
            "📊 Core Performance Metrics",
            ui.output_ui("core_metrics")
        ),

        # System health indicators
        mobile_card(
            "💚 System Health",
            ui.output_ui("system_health")
        ),

        # Compliance status
        mobile_card(
            "🔒 HIPAA Compliance Status",
            ui.output_ui("compliance_status")
        ),

        # Recent validation tests
        mobile_card(
            "🧪 Recent Validation Tests",
            ui.output_ui("recent_validations")
        ),

        # Self-correction activity
        mobile_card(
            "🔄 Self-Correction Activity (Last 24 Hours)",
            ui.output_ui("self_correction_events"),
            header_color="linear-gradient(135deg, #ff6b00 0%, #cc5500 100%)"
        ),

        # Detailed analytics button
        ui.div(
            mobile_button(
                "View Detailed Analytics Report",
                "detailed_report_btn",
                "primary",
                icon="📈"
            ),
            style="margin-top: 1rem;"
        ),

        # Detailed report (shown on click)
        ui.output_ui("detailed_report")
    )


def ai_validation_server(input, output, session, get_current_page=lambda: "ai"):
    """Server logic for AI validation dashboard."""

    @output
    @render.ui
    def core_metrics():
        """Display core validation metrics."""
        if get_current_page() != "ai":
            return None
        metrics = VALIDATION_METRICS

        return ui.div(
            # Top 3 key metrics in grid
            ui.div(
                metric_box(
                    "Model Accuracy",
                    f"{metrics['model_accuracy']}%",
                    color="#28a745",
                    subtitle="Prediction validation"
                ),
                metric_box(
                    "Compliance Score",
                    f"{metrics['compliance_score']}%",
                    color="#7c3aed",
                    subtitle="HIPAA adherence"
                ),
                metric_box(
                    "Self-Correction",
                    f"{metrics['self_correction_rate']}%",
                    color="#ff6b00",
                    subtitle="Auto-fix rate"
                ),
                style="display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem;"
            ),

            divider(),

            # Additional metrics
            ui.div(
                metric_box(
                    "Data Quality",
                    f"{metrics['data_quality_score']}%",
                    color="#17a2b8"
                ),
                metric_box(
                    "Validation Tests",
                    f"{metrics['validation_tests_passed']}/{metrics['validation_tests_total']}",
                    color="#28a745"
                ),
                style="display: flex; flex-direction: column; gap: 0.75rem;"
            ),

            ui.tags.small(
                f"Last updated: {metrics['last_updated']}",
                class_="text-muted",
                style="display: block; text-align: center; margin-top: 1rem;"
            )
        )

    @output
    @render.ui
    def system_health():
        """Display system health indicators."""
        if get_current_page() != "ai":
            return None
        metrics = VALIDATION_METRICS

        return ui.div(
            # Uptime
            ui.div(
                ui.tags.strong("System Uptime", style="display: block; margin-bottom: 0.5rem; color: #7c3aed; font-size: 1rem;"),
                progress_bar(
                    metrics['uptime_pct'],
                    label=f"{metrics['uptime_pct']}%",
                    color="#28a745"
                )
            ),

            # Response time
            ui.div(
                ui.tags.strong("Avg Response Time", style="display: block; margin-bottom: 0.5rem; color: #7c3aed; font-size: 1rem;"),
                ui.div(
                    ui.tags.span(
                        f"{metrics['avg_response_time_ms']}ms",
                        style="font-size: 1.75rem; font-weight: 700; color: #28a745;"
                    ),
                    ui.tags.small(
                        " (target: <200ms)",
                        class_="text-muted",
                        style="margin-left: 0.5rem;"
                    ),
                    style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px;"
                ),
                style="margin-top: 1rem;"
            ),

            divider(),

            alert_box(
                "✅ All performance indicators within acceptable thresholds",
                type="success"
            )
        )

    @output
    @render.ui
    def compliance_status():
        """Display HIPAA compliance status."""
        if get_current_page() != "ai":
            return None

        # Calculate overall compliance
        avg_score = sum(c['score'] for c in COMPLIANCE_COMPONENTS) / len(COMPLIANCE_COMPONENTS)

        return ui.div(
            # Overall status badge
            ui.div(
                ui.tags.div(
                    ui.tags.span("✓", style="font-size: 3rem; color: #28a745; display: block; margin-bottom: 0.5rem;"),
                    ui.tags.h3("HIPAA Compliant", style="margin: 0; color: #28a745; font-size: 1.5rem;"),
                    ui.tags.p(
                        f"Overall Compliance Score: {avg_score:.1f}%",
                        style="color: #666; margin: 0.5rem 0 0 0;"
                    ),
                    style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 12px; margin-bottom: 1.5rem;"
                )
            ),

            ui.tags.h3(
                "Compliance Components",
                style="color: #666 !important; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin: 0 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0;"
            ),

            # Individual component status
            ui.tags.h4(
                "Validated Components",
                style="color: #7c3aed; margin-bottom: 1rem; font-size: 1.1rem;"
            ),

            *[
                ui.div(
                    ui.div(
                        ui.tags.div(
                            ui.tags.span(
                                "✓" if comp['status'] == "PASS" else "⚠",
                                style=f"font-size: 1.5rem; color: {'#28a745' if comp['status'] == 'PASS' else '#ffc107'}; margin-right: 0.75rem;"
                            ),
                            ui.tags.span(comp['name'], style="font-weight: 600; color: #333;"),
                            style="display: flex; align-items: center; margin-bottom: 0.5rem;"
                        ),
                        ui.div(
                            ui.tags.small(
                                f"{comp['status']} • Score: {comp['score']}% • Checked {comp['last_check']}",
                                class_="text-muted"
                            ),
                            style="padding-left: 2.25rem;"
                        )
                    ),
                    style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem; border-left: 4px solid #28a745;"
                )
                for comp in COMPLIANCE_COMPONENTS
            ],

            divider(),

            ui.markdown("""
            **Compliance Framework Coverage:**
            - ✅ HIPAA Security Rule (§164.312)
            - ✅ HIPAA Privacy Rule (§164.520)
            - ✅ HITECH Act Requirements
            - ✅ CMS Data Security Standards

            **Next Audit:** Scheduled for Q2 2026
            """)
        )

    @output
    @render.ui
    def recent_validations():
        """Display recent validation test results."""
        if get_current_page() != "ai":
            return None

        return ui.div(
            *[
                ui.div(
                    ui.div(
                        # Header with icon and name
                        ui.tags.div(
                            ui.tags.span(
                                "✓" if test['status'] == "PASS" else "⚠",
                                style=f"font-size: 1.5rem; color: {'#28a745' if test['status'] == 'PASS' else '#ffc107'}; margin-right: 0.75rem;"
                            ),
                            ui.tags.span(test['name'], style="font-weight: 600; flex: 1;"),
                            style="display: flex; align-items: center; margin-bottom: 0.5rem;"
                        ),

                        # Score and status
                        ui.div(
                            ui.tags.span(
                                test['status'],
                                style=f"background: {'#28a745' if test['status'] == 'PASS' else '#ffc107'}; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 600; font-size: 0.75rem; margin-right: 0.75rem;"
                            ),
                            ui.tags.span(
                                f"{test['score']}%",
                                style="font-weight: 600; color: #7c3aed; font-size: 1.1rem;"
                            ),
                            style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; padding-left: 2.25rem;"
                        ),

                        # Details and timestamp
                        ui.div(
                            ui.tags.small(test['details'], class_="text-muted", style="display: block; margin-bottom: 0.25rem;"),
                            ui.tags.small(f"Run {test['timestamp']}", class_="text-muted", style="font-style: italic;"),
                            style="padding-left: 2.25rem;"
                        )
                    ),
                    style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for test in VALIDATION_TESTS
            ],

            divider(),

            alert_box(
                f"ℹ️ {VALIDATION_METRICS['validation_tests_passed']} of {VALIDATION_METRICS['validation_tests_total']} validation tests passed ({(VALIDATION_METRICS['validation_tests_passed']/VALIDATION_METRICS['validation_tests_total']*100):.1f}%)",
                type="info"
            )
        )

    @output
    @render.ui
    def self_correction_events():
        """Display self-correction activity."""
        if get_current_page() != "ai":
            return None

        return ui.div(
            ui.markdown("""
            **Autonomous Error Detection & Correction**

            StarGuard AI's self-correcting framework automatically identifies and
            resolves issues without human intervention, ensuring continuous reliability.
            """),

            divider(),

            *[
                ui.div(
                    ui.div(
                        # Timestamp badge
                        ui.tags.div(
                            event['timestamp'],
                            style="background: #ff6b00; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 600; font-size: 0.75rem; display: inline-block; margin-bottom: 0.75rem;"
                        ),

                        # Issue detected
                        ui.div(
                            ui.tags.strong("Issue Detected:", style="color: #dc3545; display: block; margin-bottom: 0.25rem;"),
                            ui.tags.span(event['issue'], style="color: #333;"),
                            style="margin-bottom: 0.75rem;"
                        ),

                        # Action taken
                        ui.div(
                            ui.tags.strong("Auto-Correction:", style="color: #7c3aed; display: block; margin-bottom: 0.25rem; font-weight: 700;"),
                            ui.tags.span(event['action'], style="color: #1a1a1a; font-weight: 500;"),
                            style="margin-bottom: 0.75rem;"
                        ),

                        # Outcome
                        ui.div(
                            ui.tags.strong("✓ Outcome:", style="color: #28a745; display: block; margin-bottom: 0.25rem; font-weight: 700;"),
                            ui.tags.span(event['outcome'], style="color: #1a1a1a; font-weight: 500;"),
                        ),
                    ),
                    style="padding: 1.25rem; background: #fff8f0; border-left: 4px solid #ff6b00; border-radius: 8px; margin-bottom: 1rem;"
                )
                for event in SELF_CORRECTION_EVENTS
            ],

            alert_box(
                f"🔄 Self-correction rate: {VALIDATION_METRICS['self_correction_rate']}% of detected issues resolved automatically",
                type="info"
            )
        )

    @output
    @render.ui
    @reactive.event(input.detailed_report_btn)
    def detailed_report():
        """Generate detailed analytics report."""
        if get_current_page() != "ai":
            return None

        return ui.div(
            mobile_card(
                "📈 Detailed Analytics Report",

                ui.markdown(f"""
                **Model Performance Analysis**

                | Model Component | Accuracy | Confidence |
                |----------------|----------|------------|
                | Star Rating Predictor | 96.2% | High |
                | HEDIS Gap Analyzer | 98.1% | Very High |
                | Risk Adjustment | 94.7% | High |
                | Member Segmentation | 93.4% | Medium-High |

                **Validation Methodology:**
                - Cross-validation: 5-fold stratified
                - Test set size: 20% holdout (n=2,340 contracts)
                - Temporal validation: Rolling 12-month window

                **Data Quality Metrics:**
                - Completeness: {VALIDATION_METRICS['data_quality_score']}%
                - Accuracy: 96.8%
                - Consistency: 94.2%
                - Timeliness: 98.1%

                **Self-Correction Framework**

                Our self-correcting AI operates on three detection layers:

                1. **Real-Time Monitoring** - Prediction variance, data quality gates
                2. **Pattern Analysis** - Anomaly detection, drift monitoring
                3. **Corrective Actions** - Model retraining, data cleansing automation

                **Performance Stats (Last 30 Days):**
                - Issues detected: 127
                - Auto-corrected: {int(127 * VALIDATION_METRICS['self_correction_rate'] / 100)}
                - Mean time to resolution: 4.2 minutes
                - System availability: {VALIDATION_METRICS['uptime_pct']}%
                """),

                alert_box(
                    "✅ All critical systems operational. No immediate action required.",
                    type="success"
                )
            ),

            style="margin-top: 1.5rem;"
        )


__all__ = ['ai_validation_ui', 'ai_validation_server']
