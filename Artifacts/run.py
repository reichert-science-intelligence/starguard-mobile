"""
StarGuard AI Mobile - Launch script.
Run with: shiny run run:app --port 8000
Or: python -c "from run import app; from shiny import run_app; run_app(app, port=8000)"
"""
from app.app import app
