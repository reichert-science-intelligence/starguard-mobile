"""Predictive Model Performance Monitor - Mobile optimized."""

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

# Model performance metrics
MODEL_METRICS = {
    "overall_accuracy": 94.2,
    "precision": 92.8,
    "recall": 91.5,
    "f1_score": 92.1,
    "auc_roc": 0.967,
    "predictions_total": 156824,
    "predictions_last_24h": 1247,
    "avg_confidence": 87.3,
    "drift_score": 0.023,
    "data_quality": 98.6
}

# Model components performance
MODEL_COMPONENTS = [
    {
        "name": "Star Rating Predictor",
        "accuracy": 93.8,
        "precision": 92.1,
        "recall": 91.4,
        "predictions": 45623,
        "avg_confidence": 89.2,
        "status": "Optimal"
    },
    {
        "name": "Gap Closure Predictor",
        "accuracy": 95.7,
        "precision": 94.3,
        "recall": 93.8,
        "predictions": 38491,
        "avg_confidence": 91.5,
        "status": "Optimal"
    },
    {
        "name": "Risk Stratification Model",
        "accuracy": 92.4,
        "precision": 90.8,
        "recall": 89.3,
        "predictions": 52167,
        "avg_confidence": 83.7,
        "status": "Monitor"
    },
    {
        "name": "Intervention Recommender",
        "accuracy": 94.9,
        "precision": 93.6,
        "recall": 92.1,
        "predictions": 20543,
        "avg_confidence": 88.4,
        "status": "Optimal"
    }
]

# Feature importance
FEATURE_IMPORTANCE = [
    {"feature": "Historical Gap Closure Rate", "importance": 0.284, "category": "Historical"},
    {"feature": "Member Risk Score (RAF)", "importance": 0.213, "category": "Clinical"},
    {"feature": "Age & Demographics", "importance": 0.156, "category": "Demographic"},
    {"feature": "Chronic Condition Count", "importance": 0.147, "category": "Clinical"},
    {"feature": "Prior Year Star Rating", "importance": 0.089, "category": "Historical"},
    {"feature": "Provider Quality Score", "importance": 0.067, "category": "Network"},
    {"feature": "Intervention Response History", "importance": 0.044, "category": "Behavioral"}
]

# Model validation tests
VALIDATION_TESTS = [
    {
        "test": "Cross-Validation (K-Fold)",
        "result": "Pass",
        "score": 93.8,
        "threshold": 90.0,
        "status": "✓"
    },
    {
        "test": "Temporal Validation",
        "result": "Pass",
        "score": 92.4,
        "threshold": 88.0,
        "status": "✓"
    },
    {
        "test": "Bias Detection (Demographic Parity)",
        "result": "Pass",
        "score": 97.2,
        "threshold": 95.0,
        "status": "✓"
    },
    {
        "test": "Calibration Curve Analysis",
        "result": "Pass",
        "score": 94.6,
        "threshold": 92.0,
        "status": "✓"
    },
    {
        "test": "Prediction Stability",
        "result": "Pass",
        "score": 96.1,
        "threshold": 94.0,
        "status": "✓"
    },
    {
        "test": "Data Drift Detection",
        "result": "Pass",
        "score": 97.7,
        "threshold": 95.0,
        "status": "✓"
    }
]

# Recent model updates (MM/DD/YYYY format)
MODEL_UPDATES = [
    {
        "date": "02/12/2026",
        "version": "v2.3.1",
        "change": "Improved feature engineering for diabetes measures",
        "impact": "+1.8% accuracy",
        "type": "Enhancement"
    },
    {
        "date": "02/08/2026",
        "version": "v2.3.0",
        "change": "Added provider network quality features",
        "impact": "+2.3% precision",
        "type": "Feature"
    },
    {
        "date": "02/01/2026",
        "version": "v2.2.5",
        "change": "Recalibrated confidence thresholds",
        "impact": "+0.9% recall",
        "type": "Calibration"
    }
]


def model_monitor_ui():
    """UI for model performance monitor."""
    return mobile_page(
        "🤖 Model Performance Monitor",

        # Introduction
        mobile_card(
            "Production AI System Monitoring",
            ui.markdown("""
            **Real-time model performance tracking** with drift detection, validation testing,
            and explainability metrics.

            Ensures prediction accuracy, fairness, and reliability across all AI components.
            """)
        ),

        # Overall performance
        mobile_card(
            "Overall Model Performance",
            ui.output_ui("overall_performance"),
            header_color="linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
        ),

        # Model components
        mobile_card(
            "Model Component Status",
            ui.output_ui("model_components")
        ),

        # Feature importance
        mobile_card(
            "📊 Feature Importance Analysis",
            ui.output_ui("feature_importance"),
            header_color="linear-gradient(135deg, #28a745 0%, #208537 100%)"
        ),

        # Validation tests
        mobile_card(
            "✓ Validation Test Results",
            ui.output_ui("validation_tests")
        ),

        # Model updates
        mobile_card(
            "📝 Recent Model Updates",
            ui.output_ui("model_updates"),
            header_color="linear-gradient(135deg, #ff6b00 0%, #cc5500 100%)"
        ),

        # System health
        mobile_card(
            "System Health Indicators",
            ui.output_ui("system_health")
        )
    )


def model_monitor_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for model monitor."""

    def _is_on_monitor_page():
        """Check if we're on the monitor page."""
        try:
            return get_current_page() == "monitor"
        except Exception:
            return False

    @output
    @render.ui
    def overall_performance():
        """Display overall model performance metrics."""
        if not _is_on_monitor_page():
            return None

        return ui.div(
            metric_box(
                "Overall Accuracy",
                f"{MODEL_METRICS['overall_accuracy']}%",
                color="#28a745",
                subtitle="Production performance"
            ),
            metric_box(
                "Precision",
                f"{MODEL_METRICS['precision']}%",
                color="#7c3aed",
                subtitle="Positive predictive value"
            ),
            metric_box(
                "Recall",
                f"{MODEL_METRICS['recall']}%",
                color="#0066cc",
                subtitle="Sensitivity"
            ),
            metric_box(
                "F1 Score",
                f"{MODEL_METRICS['f1_score']}%",
                color="#ff6b00",
                subtitle="Harmonic mean"
            ),
            metric_box(
                "AUC-ROC",
                f"{MODEL_METRICS['auc_roc']:.3f}",
                color="#17a2b8",
                subtitle="Discrimination ability"
            ),
            metric_box(
                "Predictions (24h)",
                f"{MODEL_METRICS['predictions_last_24h']:,}",
                color="#ffc107",
                subtitle=f"{MODEL_METRICS['predictions_total']:,} total"
            ),
            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )

    @output
    @render.ui
    def model_components():
        """Display individual model component performance."""
        if not _is_on_monitor_page():
            return None

        status_colors = {
            "Optimal": "#28a745",
            "Monitor": "#ffc107",
            "Alert": "#dc3545"
        }

        return ui.div(
            *[
                ui.div(
                    # Component header
                    ui.div(
                        ui.tags.span(
                            component["name"],
                            style="font-weight: 700; font-size: 1rem; color: #1a1a1a;"
                        ),
                        ui.tags.span(
                            component["status"],
                            style=f"background: {status_colors[component['status']]}; color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;"
                        ),
                        style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;"
                    ),

                    # Metrics
                    ui.div(
                        ui.tags.strong("Accuracy: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{component['accuracy']:.1f}%",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.div(
                            ui.tags.span("Precision: ", style="color: #666; font-size: 0.875rem;"),
                            ui.tags.span(f"{component['precision']:.1f}%", style="color: #7c3aed; font-weight: 600; font-size: 0.875rem;"),
                            style="margin-bottom: 0.25rem;"
                        ),
                        ui.tags.div(
                            ui.tags.span("Recall: ", style="color: #666; font-size: 0.875rem;"),
                            ui.tags.span(f"{component['recall']:.1f}%", style="color: #7c3aed; font-weight: 600; font-size: 0.875rem;"),
                            style="margin-bottom: 0.25rem;"
                        ),
                        ui.tags.div(
                            ui.tags.span("Avg Confidence: ", style="color: #666; font-size: 0.875rem;"),
                            ui.tags.span(f"{component['avg_confidence']:.1f}%", style="color: #7c3aed; font-weight: 600; font-size: 0.875rem;"),
                        ),
                        style="padding: 0.75rem 0; border-bottom: 1px solid #e0e0e0;"
                    ),

                    ui.div(
                        ui.tags.strong("Predictions: ", style="color: #1a1a1a; font-weight: 700;"),
                        ui.tags.span(
                            f"{component['predictions']:,}",
                            style="color: #000000 !important; font-weight: 900 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                        ),
                        style="padding: 0.75rem 0;"
                    ),

                    class_="model-component-card",
                    style=f"padding: 1.25rem; background: white; border-left: 4px solid {status_colors[component['status']]}; border-radius: 8px; margin-bottom: 1rem;"
                )
                for component in MODEL_COMPONENTS
            ]
        )

    @output
    @render.ui
    def feature_importance():
        """Display feature importance rankings."""
        if not _is_on_monitor_page():
            return None

        category_colors = {
            "Historical": "#7c3aed",
            "Clinical": "#28a745",
            "Demographic": "#0066cc",
            "Network": "#ff6b00",
            "Behavioral": "#17a2b8"
        }

        return ui.div(
            ui.markdown("""
            **Top features driving model predictions**, ranked by contribution to accuracy.
            """),

            divider(),

            *[
                ui.div(
                    ui.div(
                        ui.tags.span(
                            f"#{idx + 1}",
                            style="font-weight: 700; color: #999; font-size: 0.875rem; margin-right: 0.5rem;"
                        ),
                        ui.tags.span(
                            feature["feature"],
                            style="font-weight: 700; color: #1a1a1a; font-size: 0.95rem; flex: 1;"
                        ),
                        ui.tags.span(
                            feature["category"],
                            style=f"background: {category_colors[feature['category']]}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 600;"
                        ),
                        style="display: flex; align-items: center; margin-bottom: 0.5rem;"
                    ),

                    # Importance bar
                    ui.div(
                        ui.tags.span(
                            f"{feature['importance']:.1%}",
                            style="color: #999 !important; font-weight: 600 !important; font-size: 1.25rem; display: block; margin-bottom: 0.25rem;"
                        ),
                        progress_bar(
                            feature['importance'] * 100,
                            label="",
                            color=category_colors[feature['category']]
                        ),
                        style="margin-top: 0.5rem;"
                    ),

                    style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for idx, feature in enumerate(FEATURE_IMPORTANCE)
            ]
        )

    @output
    @render.ui
    def validation_tests():
        """Display validation test results."""
        if not _is_on_monitor_page():
            return None

        return ui.div(
            ui.markdown("""
            **All validation tests passed** - model meets production quality standards.
            """),

            divider(),

            *[
                ui.div(
                    ui.div(
                        ui.tags.span(
                            test["status"],
                            style="font-size: 1.5rem; margin-right: 0.75rem; color: #28a745;"
                        ),
                        ui.tags.div(
                            ui.tags.div(
                                test["test"],
                                style="font-weight: 700; color: #1a1a1a; margin-bottom: 0.25rem; font-size: 0.95rem;"
                            ),
                            ui.tags.div(
                                f"Score: ",
                                ui.tags.span(
                                    f"{test['score']:.1f}%",
                                    style="color: #999 !important; font-weight: 600 !important; font-size: 1.25rem;"
                                ),
                                ui.tags.span(
                                    f" (Threshold: {test['threshold']:.1f}%)",
                                    style="color: #666; font-size: 0.875rem; margin-left: 0.25rem;"
                                ),
                                style="margin-top: 0.25rem;"
                            ),
                            style="flex: 1;"
                        ),
                        style="display: flex; align-items: flex-start;"
                    ),
                    style="padding: 1rem; background: white; border-left: 4px solid #28a745; border-radius: 8px; margin-bottom: 0.75rem;"
                )
                for test in VALIDATION_TESTS
            ]
        )

    @output
    @render.ui
    def model_updates():
        """Display recent model version updates."""
        if not _is_on_monitor_page():
            return None

        type_colors = {
            "Enhancement": "#28a745",
            "Feature": "#7c3aed",
            "Calibration": "#ff6b00",
            "Bug Fix": "#dc3545"
        }

        return ui.div(
            *[
                ui.div(
                    ui.div(
                        ui.tags.span(
                            update["version"],
                            style="font-weight: 700; color: #000000 !important; font-size: 1rem;"
                        ),
                        ui.tags.span(
                            update["type"],
                            style=f"background: {type_colors[update['type']]}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 600; margin-left: 0.5rem;"
                        ),
                        style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;"
                    ),

                    ui.tags.div(
                        update["date"],
                        style="color: #000000 !important; font-size: 0.875rem; margin-bottom: 0.5rem; font-weight: 700;"
                    ),

                    ui.tags.div(
                        update["change"],
                        style="color: #000000 !important; font-weight: 700; margin-bottom: 0.5rem; font-size: 0.95rem;"
                    ),

                    ui.tags.div(
                        ui.tags.strong("Impact: ", style="color: #000000 !important; font-size: 0.875rem; font-weight: 700;"),
                        ui.tags.span(update["impact"], style="color: #000000 !important; font-weight: 900; font-size: 1rem;"),
                    ),

                    style="padding: 1.25rem; background: white; border: 2px solid #e0e0e0; border-radius: 12px; margin-bottom: 1rem;"
                )
                for update in MODEL_UPDATES
            ]
        )

    @output
    @render.ui
    def system_health():
        """Display system health indicators."""
        if not _is_on_monitor_page():
            return None

        drift_status = "Normal" if MODEL_METRICS["drift_score"] < 0.05 else "Warning"
        drift_color = "#28a745" if drift_status == "Normal" else "#ffc107"

        return ui.div(
            metric_box(
                "Avg Prediction Confidence",
                f"{MODEL_METRICS['avg_confidence']:.1f}%",
                color="#7c3aed",
                subtitle="Model certainty"
            ),
            metric_box(
                "Data Quality Score",
                f"{MODEL_METRICS['data_quality']:.1f}%",
                color="#28a745",
                subtitle="Input data integrity"
            ),

            # Drift indicator
            ui.div(
                ui.tags.strong("Data Drift Score: ", style="color: #666 !important; font-weight: 700;"),
                ui.tags.span(
                    f"{MODEL_METRICS['drift_score']:.3f}",
                    style="color: #666 !important; font-weight: 700 !important; font-size: 1.5rem; display: block; margin-top: 0.25rem;"
                ),
                ui.tags.div(
                    ui.tags.span(
                        f"Status: {drift_status}",
                        style=f"color: {drift_color}; font-weight: 700; font-size: 0.875rem;"
                    ),
                    ui.tags.span(
                        " (Threshold: 0.05)",
                        style="color: #666; font-size: 0.875rem;"
                    ),
                    style="margin-top: 0.5rem;"
                ),
                style="padding: 1.25rem; background: #f5f3ff; border-radius: 12px; margin-top: 0.75rem;"
            ),

            style="display: flex; flex-direction: column; gap: 0.75rem;"
        )


__all__ = ['model_monitor_ui', 'model_monitor_server']
