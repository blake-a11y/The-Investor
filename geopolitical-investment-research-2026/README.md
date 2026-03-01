# Geopolitical Investment Research 2026

Peer-reviewed, multi-AI audited, Monte Carlo–validated research report for $100k allocation (Defense/Energy/Gold/Utilities) based on Feb 28 2026 U.S.–Israel strikes on Iran.

**→ Diagram:** [REPO_DIAGRAM.md](REPO_DIAGRAM.md) | **→ Orchestration:** [CURSOR_ORCHESTRATION.md](CURSOR_ORCHESTRATION.md)

## Project Status: READY
**Date:** February 28, 2026

This repository contains a complete multi-AI peer-reviewed research framework for geopolitical event-driven investment analysis, specifically designed to analyze and allocate $100k across beneficiary sectors following the February 28, 2026 U.S.-Israel strikes on Iran. The report includes an explicit **Investor Profile & Suitability Assessment** section demonstrating investor-type assessment methodology for a Wealth-Tech Operations Leader Persona.

## Cursor Bot Setup

For detailed instructions on setting up Claude, Gemini, and ChatGPT research bots within Cursor to run parallel audits, see [CURSOR_ORCHESTRATION.md](CURSOR_ORCHESTRATION.md#cursor-bot-setup-instructions).

## Workflow

1. **Day 1:** Paste `prompts/master_instructions.md` to Grok → `reports/draft_grok_v1.md`
2. **Day 1–2:** Parallel audits (Claude, Gemini, ChatGPT) → `reports/audit_*.md`
3. **Day 2:** Reconcile in Grok → `reports/final_validated_report.md`
4. Run MC locally (`.\code\run_mc.ps1`), attach output, export to PDF

## Setup

```bash
pip install -r requirements.txt
```

## Run Monte Carlo

**Windows:** `.\code\run_mc.ps1`  
**Unix:** `cd code && bash run_simulations.sh`

Output: `reports/mc_summary.csv`, `mc_portfolio_histograms.png`, per-scenario histograms (`mc_histogram_*.png`), `mc_allocation_pie.png`

## Export to PDF

`.\code\export_to_pdf.ps1` (Pandoc). **Zero install:** Open report → Ctrl+K → "Markdown: Open Preview" → Ctrl+P → Save as PDF

## Cursor Bot Setup Cheat Sheet

### Prerequisites
- Cursor Pro (for Claude/GPT/Gemini access)
- Workspace: `geopolitical-investment-research-2026`
- `@codebase` available in Composer

### Quick Bot Setup

| Bot | Model Selection | Prompt File | Output File |
|-----|----------------|-------------|-------------|
| **Claude** | Opus 4.5/4 | `prompts/claude_audit_prompt.md` | `reports/audit_claude.md` |
| **ChatGPT** | GPT-4o/o1 | `prompts/chatgpt_audit_prompt.md` | `reports/audit_chatgpt.md` |
| **Gemini** | Gemini | `prompts/gemini_audit_prompt.md` | `reports/audit_gemini.md` |

### Steps for Each Bot
1. New Composer tab (Cmd+I/Ctrl+I)
2. Select model from dropdown
3. Type `@codebase`
4. Paste prompt file contents
5. Attach `reports/draft_grok_v1.md`
6. Run audit → Save to output file

## Data

- `data/sector_historical_data.csv` — Historical OHLCV
- `data/latest_prices_feb28_2026.csv` — Latest ETF prices (ITA, XAR, XLE, GLD, XLU as of Feb 27 2026 close)
