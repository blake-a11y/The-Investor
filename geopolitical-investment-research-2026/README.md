# Geopolitical Investment Research 2026

Research workflow combining Grok analysis, Monte Carlo simulations, and Claude audit to produce a validated investment report.

**→ Full diagram:** [REPO_DIAGRAM.md](REPO_DIAGRAM.md) | **→ Cursor orchestration:** [CURSOR_ORCHESTRATION.md](CURSOR_ORCHESTRATION.md)

## Structure

```
geopolitical-investment-research-2026/
├── prompts/              # Instructions for Grok and Claude
├── data/                  # Input data
├── code/                  # Simulation and analysis
│   ├── monte_carlo_simulator.py
│   ├── run_simulations.sh    # Unix
│   ├── run_mc.ps1            # Windows one-click
│   ├── commit_audit_round.ps1
│   └── export_to_pdf.ps1
├── reports/               # Outputs (incl. final_validated_report.md)
├── audits/
├── REPO_DIAGRAM.md        # Workflow diagram
├── CURSOR_ORCHESTRATION.md # Step-by-step Cursor guide
└── requirements.txt
```

## Workflow

1. **Grok**: Run `grok_prompt_v1.md` with sector data → `reports/draft_grok_v1.md`
2. **Monte Carlo**: Run simulations → use outputs to inform/validate draft
3. **Claude**: Run `claude_audit_prompt.md` on draft → `reports/audit_claude.md`
4. **Final**: Merge draft + audit corrections → `reports/final_validated_report.md`

## Setup

```bash
pip install -r requirements.txt
```

## Run Monte Carlo Simulations

**Unix / WSL / Git Bash:**
```bash
cd code && bash run_simulations.sh
```

**Windows one-click:**
```powershell
.\code\run_mc.ps1
```

**Manual:**
```powershell
cd geopolitical-investment-research-2026
python code\monte_carlo_simulator.py --data data\sector_historical_data.csv --days 126 --paths 10000 --output reports
```

## Export to PDF

```powershell
.\code\export_to_pdf.ps1   # Requires Pandoc
```
Or: Open `reports/final_validated_report.md` → `Ctrl+Shift+V` preview → `Ctrl+P` Save as PDF.

## Data

- `sector_historical_data.csv`: Historical OHLCV by sector
- `latest_prices_feb28_2026.csv`: Latest prices for cross-checking

Replace placeholder rows with your actual data before running analyses.
