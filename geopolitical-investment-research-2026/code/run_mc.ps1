# One-click Monte Carlo simulation (Windows PowerShell)
# Run from: geopolitical-investment-research-2026/ or repo root

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$DataPath = Join-Path $ProjectRoot "data\sector_historical_data.csv"
$OutputPath = Join-Path $ProjectRoot "reports"

Set-Location $ProjectRoot
Write-Host "Running Monte Carlo (10k paths, ~6 months)..." -ForegroundColor Cyan
python "$ScriptDir\monte_carlo_simulator.py" --data $DataPath --days 126 --paths 10000 --output $OutputPath --seed 42
Write-Host "Done. Check reports/ for outputs." -ForegroundColor Green
