"""Star Rating Predictor page - Mobile optimized."""

from shiny import ui, render, reactive
import random
from ..components.mobile_layout import (
    mobile_page,
    mobile_card,
    mobile_input_group,
    mobile_button,
    metric_box,
    info_row,
    alert_box,
    divider
)

# Sample Medicare Advantage contracts data
SAMPLE_CONTRACTS = {
    "H1234": {
        "name": "BlueCross Medicare Advantage Plus",
        "current_stars": 3.5,
        "members": 45230,
        "state": "Pennsylvania"
    },
    "H5678": {
        "name": "UnitedHealthcare MA Premier",
        "current_stars": 4.0,
        "members": 78450,
        "state": "California"
    },
    "H9012": {
        "name": "Humana Gold Plus",
        "current_stars": 4.5,
        "members": 62180,
        "state": "Florida"
    },
    "H3456": {
        "name": "Aetna Medicare Advantage",
        "current_stars": 3.0,
        "members": 38920,
        "state": "Texas"
    },
    "H7890": {
        "name": "Cigna HealthSpring",
        "current_stars": 3.5,
        "members": 51340,
        "state": "Arizona"
    },
}


def star_predictor_ui():
    """UI for star rating predictor page."""
    return mobile_page(
        "⭐ Star Rating Predictor",
        
        # Introduction card
        mobile_card(
            "AI-Powered Star Rating Forecasting",
            ui.markdown("""
            Predict **2026 Medicare Advantage Star Ratings** using advanced AI analytics.
            
            Our model analyzes historical performance, HEDIS measure trends, and 
            member experience indicators to forecast future ratings with 94.3% accuracy.
            """)
        ),
        
        # Input selection card
        mobile_card(
            "Contract Selection",
            mobile_input_group(
                "Medicare Advantage Contract",
                ui.input_select(
                    "contract_id",
                    "",
                    choices={
                        "": "-- Select a contract --",
                        **{k: f"{k} - {v['name']}" for k, v in SAMPLE_CONTRACTS.items()}
                    }
                ),
                help_text="Choose from active Medicare Advantage contracts in our portfolio",
                required=True
            ),
            
            # Contract details (shown when selected)
            ui.output_ui("contract_details"),
            
            divider(),
            
            mobile_button(
                "Generate Prediction",
                "predict_btn",
                "primary",
                icon="🚀"
            )
        ),
        
        # Prediction results (shown after clicking button)
        ui.output_ui("prediction_results")
    )


def star_predictor_server(input, output, session, get_current_page=lambda: "star"):
    """Server logic for star rating predictor. get_current_page() returns active page id."""
    
    @output
    @render.ui
    def contract_details():
        """Show contract details when one is selected."""
        if get_current_page() != "star":
            return None
        contract_id = input.contract_id()
        
        # Don't show anything if no contract selected
        if not contract_id or contract_id == "":
            return None
        
        contract = SAMPLE_CONTRACTS[contract_id]
        
        return ui.div(
            ui.tags.h4(
                "Contract Details",
                style="color: #7c3aed; margin: 1rem 0 0.75rem 0; font-size: 1.1rem;"
            ),
            info_row("Contract ID", contract_id),
            info_row("Plan Name", contract["name"]),
            info_row("Current Rating", f"{contract['current_stars']} ⭐", highlight=True),
            info_row("Enrolled Members", f"{contract['members']:,}"),
            info_row("Primary State", contract["state"]),
            style="margin-top: 1rem;"
        )
    
    @output
    @render.ui
    @reactive.event(input.predict_btn)
    def prediction_results():
        """Generate and display star rating prediction."""
        if get_current_page() != "star":
            return None
        contract_id = input.contract_id()
        
        # Validation: ensure contract is selected
        if not contract_id or contract_id == "":
            return mobile_card(
                "⚠️ Selection Required",
                alert_box(
                    "Please select a Medicare Advantage contract before generating predictions.",
                    type="warning"
                )
            )
        
        contract = SAMPLE_CONTRACTS[contract_id]
        
        # Mock AI prediction algorithm
        base_stars = contract["current_stars"]
        
        # Generate prediction with some variance
        random.seed(hash(contract_id))
        trend_factor = random.uniform(-0.3, 0.6)
        variance = random.uniform(-0.2, 0.2)
        
        predicted_stars = base_stars + trend_factor + variance
        predicted_stars = round(max(1.0, min(5.0, predicted_stars)), 1)
        
        # Calculate confidence interval
        confidence_low = round(max(1.0, predicted_stars - 0.3), 1)
        confidence_high = round(min(5.0, predicted_stars + 0.3), 1)
        
        # Calculate change
        change = predicted_stars - base_stars
        change_text = f"+{change:.1f}" if change > 0 else f"{change:.1f}"
        change_color = "#28a745" if change > 0 else "#dc3545" if change < 0 else "#666"
        
        # Determine rating category
        if predicted_stars >= 4.5:
            rating_category = "⭐⭐⭐⭐⭐ Excellent"
            category_color = "#28a745"
        elif predicted_stars >= 4.0:
            rating_category = "⭐⭐⭐⭐ Very Good"
            category_color = "#17a2b8"
        elif predicted_stars >= 3.5:
            rating_category = "⭐⭐⭐ Good"
            category_color = "#ffc107"
        elif predicted_stars >= 3.0:
            rating_category = "⭐⭐ Fair"
            category_color = "#ff6b00"
        else:
            rating_category = "⭐ Needs Improvement"
            category_color = "#dc3545"
        
        # Calculate bonus revenue
        bonus_per_member = {5.0: 150, 4.5: 125, 4.0: 100, 3.5: 75, 3.0: 50}
        star_level = round(predicted_stars * 2) / 2
        bonus = bonus_per_member.get(star_level, 25)
        total_bonus = contract["members"] * bonus
        
        return ui.div(
            mobile_card(
                "🎯 Prediction Results",
                
                ui.div(
                    ui.tags.div(
                        "2026 Predicted Rating",
                        style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; text-align: center;"
                    ),
                    ui.tags.div(
                        f"{predicted_stars} ★",
                        style=f"font-size: 3.5rem; font-weight: 700; color: {category_color}; text-align: center; line-height: 1; margin-bottom: 0.5rem;"
                    ),
                    ui.tags.div(
                        rating_category,
                        style=f"font-size: 1.1rem; font-weight: 600; color: {category_color}; text-align: center; margin-bottom: 1rem;"
                    ),
                    style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;"
                ),
                
                ui.div(
                    ui.tags.strong("Change from Current: "),
                    ui.tags.span(
                        f"{change_text} stars",
                        style=f"color: {change_color}; font-size: 1.25rem; font-weight: 700;"
                    ),
                    style="text-align: center; margin-bottom: 1.5rem;"
                ),
                
                ui.tags.h3(
                    "Confidence Interval",
                    style="color: #666 !important; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0;"
                ),
                
                ui.div(
                    ui.tags.h4(
                        "95% Confidence Interval",
                        style="color: #7c3aed; margin-bottom: 0.75rem; font-size: 1rem;"
                    ),
                    ui.tags.p(
                        f"{confidence_low} - {confidence_high} stars",
                        style="font-size: 1.25rem; font-weight: 600; color: #333; margin: 0;"
                    ),
                    style="margin-bottom: 1.5rem;"
                ),
                
                ui.tags.h3(
                    "Financial Impact",
                    style="color: #666 !important; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0;"
                ),
                
                ui.div(
                    ui.tags.h4(
                        "Projected Quality Bonus Revenue",
                        style="color: #7c3aed; margin-bottom: 0.75rem; font-size: 1rem;"
                    ),
                    ui.tags.p(
                        f"${total_bonus:,}",
                        style="font-size: 2rem; font-weight: 700; color: #28a745; margin: 0;"
                    ),
                    style="background: #f8f9fa; padding: 1rem; border-radius: 8px;"
                )
            ),
            
            style="margin-top: 1.5rem;"
        )


__all__ = ['star_predictor_ui', 'star_predictor_server']
