"""Mobile-optimized layout components."""

from shiny import ui
from typing import Optional


def mobile_page(title: str, *args, **kwargs):
    """
    Create mobile-optimized page layout (content only - no duplicate nav).
    Use with main app that provides header/nav.
    """
    return ui.div(
        ui.div(*args, class_="container-fluid", style="padding-top: 1rem; padding-bottom: 2rem;"),
        **kwargs
    )


def mobile_card(title: str, *content, id: Optional[str] = None, header_color: Optional[str] = None):
    """
    Create mobile-optimized card.

    Args:
        title: Card header text
        *content: Card body content
        id: Optional card ID
        header_color: Optional CSS background for header (e.g. gradient)

    Returns:
        Shiny card component
    """
    card_id = f"card-{id}" if id else None
    header_style = f"background: {header_color};" if header_color else None

    return ui.div(
        ui.div(title, class_="card-header", style=header_style),
        ui.div(*content, class_="card-body"),
        class_="card",
        id=card_id
    )


def mobile_input_group(label: str, input_widget, help_text: Optional[str] = None, required: bool = False):
    """Create mobile-friendly input group with label and optional help."""
    label_text = f"{label} *" if required else label
    return ui.div(
        ui.tags.label(label_text, style="font-weight: 600; display: block; margin-bottom: 0.5rem; color: #333;"),
        input_widget,
        ui.tags.small(help_text, class_="text-muted", style="display: block; margin-top: 0.25rem;") if help_text else None,
        class_="form-group",
        style="margin-bottom: 1.5rem;"
    )


def mobile_button(text: str, id: str, style: str = "primary", icon: Optional[str] = None):
    """Create touch-optimized button."""
    button_text = f"{icon} {text}" if icon else text
    return ui.input_action_button(
        id,
        button_text,
        class_=f"btn btn-{style} btn-block",
        style="width: 100%;"
    )


def metric_box(label: str, value: str, color: str = "#7c3aed", subtitle: Optional[str] = None, dark_labels: bool = False):
    """Create a metric display box."""
    label_color = "#000000" if dark_labels else "#666"
    subtitle_color = "#333" if dark_labels else "#999"
    return ui.div(
        ui.div(
            ui.tags.div(label, style=f"font-size: 0.875rem; color: {label_color}; font-weight: 700; margin-bottom: 0.25rem;"),
            ui.tags.div(
                value,
                class_="metric-value",
                style=f"font-size: 2rem; font-weight: 700; color: {color}; white-space: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch;"
            ),
            ui.tags.div(subtitle, style=f"font-size: 0.75rem; color: {subtitle_color}; margin-top: 0.25rem;") if subtitle else None,
        ),
        class_="metric-box",
        style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 1rem;"
    )


def info_row(label: str, value: str, highlight: bool = False):
    """Create a labeled information row."""
    bg = "#f8f9fa" if highlight else "transparent"
    return ui.div(
        ui.div(
            ui.tags.strong(f"{label}:", style="color: #666;"),
            ui.tags.span(f" {value}", style="color: #333; margin-left: 0.5rem;"),
            style="display: flex; justify-content: space-between; align-items: center;"
        ),
        style=f"padding: 0.75rem; background: {bg}; border-radius: 6px; margin-bottom: 0.5rem;"
    )


def alert_box(message: str, type: str = "info", dismissible: bool = False):
    """
    Create an alert/notification box.

    Args:
        message: Alert message text (can include HTML)
        type: Alert type (success, info, warning, danger)
        dismissible: Whether alert can be dismissed

    Returns:
        Formatted alert div
    """
    colors = {
        "success": "#d4edda",
        "info": "#cfe2ff",
        "warning": "#fff3cd",
        "danger": "#f8d7da"
    }
    text_colors = {
        "success": "#0f5132",
        "info": "#084298",
        "warning": "#664d03",
        "danger": "#842029"
    }
    icons = {
        "success": "✓",
        "info": "ℹ",
        "warning": "⚠",
        "danger": "✕"
    }
    bg_color = colors.get(type, colors["info"])
    text_color = text_colors.get(type, text_colors["info"])
    icon = icons.get(type, icons["info"])
    return ui.div(
        ui.div(
            ui.tags.span(icon, style=f"font-size: 1.25rem; margin-right: 0.75rem; color: {text_color};"),
            ui.tags.span(message, style=f"color: {text_color}; font-weight: 500;"),
            style="display: flex; align-items: center;"
        ),
        style=f"padding: 1rem; background: {bg_color}; color: {text_color}; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {text_color};"
    )


def divider(text: Optional[str] = None):
    """Create a horizontal divider, optionally with centered text."""
    if text:
        return ui.div(
            ui.div(
                ui.tags.span(text, style="background: white; padding: 0 1rem; color: #999; font-size: 0.875rem; font-weight: 600;"),
                style="display: flex; align-items: center; justify-content: center;"
            ),
            style="border-top: 2px solid #e0e0e0; margin: 1.5rem 0; text-align: center;"
        )
    return ui.tags.hr(style="border: none; border-top: 2px solid #e0e0e0; margin: 1.5rem 0;")


def progress_bar(
    value: float,
    max_value: float = 100.0,
    label: Optional[str] = None,
    color: str = "#7c3aed"
):
    """Create a horizontal progress bar (0-100%)."""
    pct = min(100, max(0, (value / max_value) * 100))
    header = ui.tags.div(
        label,
        style="font-size: 0.875rem; font-weight: 600; margin-bottom: 0.35rem; color: #333;"
    ) if label else None
    bar = ui.div(
        ui.div(
            style=f"width: {pct}%; height: 100%; background: {color}; border-radius: 6px; transition: width 0.3s ease;"
        ),
        style="height: 12px; background: #e0e0e0; border-radius: 6px; overflow: hidden;"
    )
    return ui.div(header, bar, style="margin-bottom: 1rem;")


def responsive_number(value: float, format_type: str = "currency"):
    """
    Format numbers to prevent wrapping on iPhone.

    Args:
        value: Number to format
        format_type: 'currency', 'percent', or 'number'

    Returns:
        Formatted number with nowrap styling
    """
    if format_type == "currency":
        formatted = f"${value:,.0f}" if value >= 1 else f"${value:,.2f}"
    elif format_type == "percent":
        formatted = f"{value:.1f}%"
    else:
        formatted = f"{value:,}" if isinstance(value, int) else f"{value:,.1f}"

    return ui.tags.span(
        formatted,
        style="white-space: nowrap; display: inline-block; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;"
    )


__all__ = [
    'mobile_page',
    'mobile_card',
    'mobile_input_group',
    'mobile_button',
    'metric_box',
    'info_row',
    'alert_box',
    'divider',
    'progress_bar',
    'responsive_number'
]
