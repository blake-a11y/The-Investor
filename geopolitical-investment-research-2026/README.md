# Geopolitical Investment Research 2026

Research workflow combining Grok analysis, Monte Carlo simulations, and Claude audit to produce a validated investment report.

## Structure

```
geopolitical-investment-research-2026/
├── prompts/              # Instructions for Grok and Claude
│   ├── master_instructions.md
│   ├── grok_prompt_v1.md
│   └── claude_audit_prompt.md
├── data/                 # Input data
│   ├── sector_historical_data.csv
│   └── latest_prices_feb28_2026.csv
├── code/                 # Simulation and analysis
│   ├── monte_carlo_simulator.py
│   └── run_simulations.sh
├── reports/              # Outputs
│   ├── draft_grok_v1.md
│   ├── audit_claude.md
│   └── final_validated_report.md   ← Target output
├── audits/
│   └── feedback_round1/
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

**Windows PowerShell:**
```powershell
cd code
python monte_carlo_simulator.py --data ..\data\sector_historical_data.csv --days 252 --paths 10000 --output ..\reports
```

## Data

- `sector_historical_data.csv`: Historical OHLCV by sector
- `latest_prices_feb28_2026.csv`: Latest prices for cross-checking

Replace placeholder rows with your actual data before running analyses.
