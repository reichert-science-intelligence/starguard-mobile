# StarGuard Mobile - Start Script
# Run from Artifacts/ directory so the app loads as a Python package (required for relative imports).
# Open http://localhost:8001 after starting.

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Starting StarGuard Mobile on http://localhost:8001 ..."
shiny run app.app:app --port 8001
