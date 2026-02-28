# Repository Diagram

## Workflow Overview

```mermaid
flowchart TB
    subgraph inputs["📥 INPUTS"]
        master["prompts/master_instructions.md"]
        grok_prompt["prompts/grok_prompt_v1.md"]
        audit_prompt["prompts/claude_audit_prompt.md"]
        hist_data["data/sector_historical_data.csv"]
        prices["data/latest_prices_feb28_2026.csv"]
    end

    subgraph cursor["🖥️ CURSOR ORCHESTRATION"]
        composer["Composer + @ codebase"]
        terminal["Built-in Terminal"]
    end

    subgraph ai["🤖 AI PIPELINE"]
        grok["Grok Draft"]
        mc["Monte Carlo (Python)"]
        claude["Claude Audit"]
    end

    subgraph outputs["📤 OUTPUTS"]
        draft["reports/draft_grok_v1.md"]
        audit["reports/audit_claude.md"]
        final["reports/final_validated_report.md"]
        pdf["final_validated_report.pdf"]
    end

    subgraph vc["📦 VERSION CONTROL"]
        commit1["git commit (after draft)"]
        commit2["git commit (after audit round)"]
        commit3["git commit (after final)"]
        push["git push → GitHub"]
    end

    master --> composer
    grok_prompt --> grok
    hist_data --> mc
    prices --> grok
    composer --> grok
    grok --> draft
    mc --> draft
    terminal --> mc
    draft --> audit_prompt
    audit_prompt --> claude
    claude --> audit
    audit --> final
    draft --> final
    final --> pdf

    draft --> commit1
    audit --> commit2
    final --> commit3
    commit1 --> push
    commit2 --> push
    commit3 --> push
```

## Directory Structure

```
geopolitical-investment-research-2026/
├── prompts/
│   ├── master_instructions.md     ← Canonical instructions
│   ├── grok_prompt_v1.md          ← Grok analysis prompt
│   └── claude_audit_prompt.md     ← Audit prompt
├── data/
│   ├── sector_historical_data.csv
│   └── latest_prices_feb28_2026.csv
├── code/
│   ├── monte_carlo_simulator.py   ← Run via one-click script
│   ├── run_simulations.sh         ← Unix/WSL/Git Bash
│   ├── run_mc.ps1                ← Windows one-click
│   ├── commit_audit_round.ps1    ← Version control helper
│   └── export_to_pdf.ps1         ← Markdown → PDF
├── reports/
│   ├── draft_grok_v1.md
│   ├── audit_claude.md
│   └── final_validated_report.md  ← TARGET OUTPUT
├── audits/
│   └── feedback_round1/
├── REPO_DIAGRAM.md               ← This file
├── CURSOR_ORCHESTRATION.md       ← Step-by-step instructions
├── README.md
└── requirements.txt
```

## One-Click Scripts Map

| Action              | Script / Command                              |
|---------------------|-----------------------------------------------|
| Run Monte Carlo     | `.\code\run_mc.ps1` (or `python code\monte_carlo_simulator.py ...`) |
| Commit audit round  | `.\code\commit_audit_round.ps1 -Message "Round N"` |
| Export to PDF       | `.\code\export_to_pdf.ps1` (requires Pandoc; else use Cursor preview → Print) |
