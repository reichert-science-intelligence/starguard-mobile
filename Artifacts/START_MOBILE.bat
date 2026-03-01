@echo off
REM StarGuard Mobile - Use module path so relative imports work
cd /d "%~dp0"
call venv\Scripts\activate
shiny run run:app --port 8000
