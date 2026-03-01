# Export final report to PDF via Pandoc
# Requires: pandoc (https://pandoc.org/installing.html)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$ReportPath = Join-Path $ProjectRoot "reports\final_validated_report.md"
$OutputPath = Join-Path $ProjectRoot "reports\final_validated_report.pdf"

if (-not (Test-Path $ReportPath)) {
    Write-Host "Report not found: $ReportPath" -ForegroundColor Red
    exit 1
}

$pandoc = Get-Command pandoc -ErrorAction SilentlyContinue
if (-not $pandoc) {
    Write-Host "Pandoc not installed. Use Cursor instead (zero extra installs):" -ForegroundColor Yellow
    Write-Host "  1. Open reports/final_validated_report.md" -ForegroundColor Cyan
    Write-Host "  2. Ctrl+K (or Cmd+K) -> type 'Markdown: Open Preview'" -ForegroundColor Cyan
    Write-Host "  3. In preview: Ctrl+P -> Print -> Save as PDF" -ForegroundColor Cyan
    exit 1
}

Set-Location $ProjectRoot
# Try pdflatex first; may need MiKTeX or TeX Live for PDF. Else use Cursor preview → Print to PDF.
& pandoc $ReportPath -o $OutputPath -f markdown -t pdf --pdf-engine=pdflatex 2>$null
if (-not (Test-Path $OutputPath)) {
    & pandoc $ReportPath -o $OutputPath -f markdown -t pdf 2>$null
}
if (Test-Path $OutputPath) {
    Write-Host "PDF saved: $OutputPath" -ForegroundColor Green
} else {
    Write-Host "Pandoc PDF failed (LaTeX may be missing). Use Cursor: Open report -> Ctrl+Shift+V -> Ctrl+P -> Save as PDF" -ForegroundColor Yellow
}
