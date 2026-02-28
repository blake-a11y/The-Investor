# Cursor Orchestration Guide

Step-by-step instructions to run the geopolitical investment research workflow in Cursor.

---

## ✅ Checklist: Your Intent

| # | Intent | Status | How |
|---|--------|--------|-----|
| 1 | Use Cursor's Composer + @ codebase for everything | ✅ Ready | See [Section 1](#1-composer--codebase) |
| 2 | Version-control every AI response (commit after each audit round) | ✅ Ready | See [Section 2](#2-version-control) + `code/commit_audit_round.ps1` |
| 3 | Run Python MC locally with one click | ✅ Ready | See [Section 3](#3-one-click-monte-carlo) + `code/run_mc.ps1` |
| 4 | Export to PDF via Markdown → Pandoc or Cursor preview | ✅ Ready | See [Section 4](#4-export-to-pdf) + `code/export_to_pdf.ps1` |
| 5 | Share GitHub repo privately with advisor/family — full audit trail | ✅ Ready | See [Section 5](#5-share-repo-privately) |

---

## 1. Composer + @ Codebase

**Use Composer for every AI interaction:**

1. Open Composer (`Ctrl+I` or `Cmd+I`).
2. **@ codebase** at the start of your prompt to give the model access to the whole project.
3. Reference specific files: `@ prompts/master_instructions.md`, `@ data/sector_historical_data.csv`, etc.
4. Example prompt: *"@codebase Using @ prompts/master_instructions.md and @ data/sector_historical_data.csv, produce the Grok draft per grok_prompt_v1 and save to reports/draft_grok_v1.md"*

**Suggested prompt templates:**
- Draft: *"@codebase @ prompts/grok_prompt_v1.md Generate draft report → reports/draft_grok_v1.md"*
- Audit: *"@codebase @ prompts/claude_audit_prompt.md Audit reports/draft_grok_v1.md → reports/audit_claude.md"*
- Final: *"@codebase Merge draft + audit into reports/final_validated_report.md per master_instructions structure"*

---

## 2. Version Control

**Commit after each audit round:**

```powershell
# From project root (geopolitical-investment-research-2026) or repo root (The Investor)
.\code\commit_audit_round.ps1 -Message "Audit round 1 complete"
```

**Manual alternative:**
```powershell
git add -A
git status
git commit -m "Audit round N: [describe changes]"
git push
```

**Suggested commit points:**
- After Grok draft saved
- After each Claude audit round
- After Monte Carlo results added
- After final validated report completed

---

## 3. One-Click Monte Carlo

**Option A — PowerShell script (recommended):**
```powershell
cd geopolitical-investment-research-2026
.\code\run_mc.ps1
```

**Option B — Cursor terminal:**
1. Open terminal (`Ctrl+`` or View → Terminal).
2. Run:
   ```powershell
   cd geopolitical-investment-research-2026
   python code\monte_carlo_simulator.py --data data\sector_historical_data.csv --days 126 --paths 10000 --output reports
   ```
   *Note: `--days 126` ≈ 6 months.*

**Output:** Plots saved to `reports/`; console prints mean/percentiles per sector.

---

## 4. Export to PDF

**Option A — Pandoc (best quality):**
1. Install Pandoc: https://pandoc.org/installing.html  
2. Run:
   ```powershell
   .\code\export_to_pdf.ps1
   ```
   Creates `reports/final_validated_report.pdf`.

**Option B — Cursor preview:**
1. Open `reports/final_validated_report.md`.
2. `Ctrl+Shift+V` (or right-click → Open Preview) for Markdown preview.
3. Print to PDF: `Ctrl+P` → Save as PDF.

---

## 5. Share Repo Privately

**GitHub repo visibility:**

1. Go to https://github.com/blake-a11y/The-Investor
2. **Settings** → **General** → **Danger Zone**
3. Change visibility to **Private** (if not already)
4. **Settings** → **Collaborators** → **Add people**
5. Add advisor/family by GitHub username or email

**They get:** Full repo access, commit history, all reports and audit trail.

**They need:** GitHub account; they clone via:
```bash
git clone https://github.com/blake-a11y/The-Investor.git
```

---

## Quick Reference

| Task | Command / Action |
|------|------------------|
| Run MC | `.\code\run_mc.ps1` |
| Commit audit | `.\code\commit_audit_round.ps1 -Message "Round N"` |
| Export PDF | `.\code\export_to_pdf.ps1` |
| Push all | `git push` |

---

## File Locations

- **Diagram:** `REPO_DIAGRAM.md`
- **This guide:** `CURSOR_ORCHESTRATION.md`
- **Master instructions:** `prompts/master_instructions.md`
