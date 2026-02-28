# Commit after audit round — version-control AI responses
# Run from: geopolitical-investment-research-2026/ or repo root (The Investor)

param(
    [Parameter(Mandatory=$false)]
    [string]$Message = "Audit round complete"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$RepoRoot = Split-Path -Parent $ProjectRoot

# Use repo root if .git exists there (The Investor)
if (Test-Path (Join-Path $RepoRoot ".git")) {
    Set-Location $RepoRoot
} else {
    Set-Location $ProjectRoot
}

git add -A
$status = git status --short
if ($status) {
    git commit -m $Message
    git push
    Write-Host "Committed and pushed: $Message" -ForegroundColor Green
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}
