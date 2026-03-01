# One-click Monte Carlo (3 scenarios, 10k paths, 6-month horizon)
# Requires: Python 3.x with numpy, pandas, matplotlib (pip install -r requirements.txt)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$OutputPath = Join-Path $ProjectRoot "reports"

# Find Python (try py launcher, then python, then python3)
$PythonCmd = $null
foreach ($cmd in @("py", "python", "python3")) {
    $result = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($result) {
        $PythonCmd = $cmd
        break
    }
}

if (-not $PythonCmd) {
    Write-Host "ERROR: Python not found." -ForegroundColor Red
    Write-Host "Install Python from https://www.python.org/downloads/ or: winget install Python.Python.3.12" -ForegroundColor Yellow
    Write-Host "Then run: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Set-Location $ProjectRoot
Write-Host "Running Monte Carlo (A/B/C scenarios, 10k paths, 6mo)..." -ForegroundColor Cyan
& $PythonCmd "$ScriptDir\monte_carlo_simulator.py" --paths 10000 --output $OutputPath
if ($LASTEXITCODE -eq 0) {
    Write-Host "Done. Check reports/ for mc_summary.csv and histograms." -ForegroundColor Green
} else {
    Write-Host "Monte Carlo failed. Ensure dependencies: pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}
