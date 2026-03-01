# Remediation Plan — Homeland Security Research 2026
**Created:** March 1, 2026
**Author:** Claude External (Reconciliation Agent)
**Purpose:** Correct out-of-order execution errors and fill missing phases before final reconciliation
**Status:** PRE-RECONCILIATION — Do not run Phase 5 until all items below are resolved

---

## Current Execution State (Audited from git log)

| Commit | Phase | Agent | Order Run | Status |
|--------|-------|-------|-----------|--------|
| `e955282` | Phase 3 — Company Universe | Gemini | 2nd | ✅ Complete |
| `d3d045f` | Phase 2B — Earnings Model | ChatGPT Codex | 1st | ✅ Complete |
| `89f9f62` | Scaffold + Prompts | Cursor | Setup | ✅ Complete |
| `draft_threat_assessment.md` | Phase 1 — Threat Assessment | Grok | 1st (correct) | ✅ Complete |
| Phase 2A — Agency Mapping | Claude Code | — | 🔴 **NEVER RUN** |
| Phase 3B — Fundamentals | Claude Sonnet | — | 🔴 **NEVER RUN** |
| Phase 4 — Monte Carlo | Claude Code | Before 3B | ⚠️ **RUN OUT OF ORDER** |
| Phase 5 — Reconciliation | Claude External | — | 🔴 **BLOCKED** |

---

## Problem 1 — CRITICAL: Phase 2A Was Never Executed
**Impact: HIGH**

### What's Missing
`reports/draft_agency_mapping.md` does not exist.
`data/usaspending_raw/` is empty.

### Why It Matters
Phase 2A is the **agency → contract → publicly traded company** chain. It answers:
- Which agencies surge spend post-event and by how much?
- Which IDIQ vehicles get activated?
- Which prime contractors hold those vehicles?

Without it, the final report has no verified contract flow data. Claude Sonnet's fundamentals (Phase 3B) and the final reconciliation both reference this data. Skipping it creates an unverifiable gap in the supply chain thesis — the core investment argument of this report.

### Fix
**Run Phase 2A now, before anything else.**
Assign Claude Code to: `prompts/claude_code_usaspending.md`
Expected output: `reports/draft_agency_mapping.md` + `data/usaspending_raw/`

---

## Problem 2 — CRITICAL: Phase 3B Was Never Executed
**Impact: HIGH**

### What's Missing
`reports/draft_earnings_assessment.md` does not exist.

### Why It Matters
This is the **earnings-based layer** that differentiates this report from the Iran event-driven analysis. It contains:
- Fundamental scorecards for all Tier 1 companies
- Investment theses with bull/base/bear cases
- Valuation analysis (EV/EBITDA vs. peers)
- Portfolio construction recommendation

Without it, Phase 5 reconciliation cannot produce the earnings section of the final report. The report would be event-driven only — no better than the Iran report.

### Fix — Run AFTER Phase 2A completes
Assign Claude Sonnet to: `prompts/claude_sonnet_fundamentals.md`

**Important:** Claude Sonnet's prompt requires reading two input files first:
- `data/company_fundamentals/master_fundamentals.csv` (from Codex — ✅ exists)
- `reports/draft_agency_mapping.md` (from Claude Code — 🔴 must exist first)

**Do not run Phase 3B until Phase 2A is committed.**

---

## Problem 3 — MODERATE: Phase 4 Monte Carlo Used Unanchored Parameters
**Impact: MEDIUM**

### What Happened
Phase 4 (Monte Carlo) ran **before** Phase 3B (Claude Sonnet fundamentals) and before Phase 2A was confirmed complete. The MC prompt instructs Claude Code to:

> *"Pull from Codex output: `data/company_fundamentals/historical_event_returns.csv` — Use average sector return post-9/11 as Scenario C anchor"*

### The Risk
If `historical_event_returns.csv` did not exist when Phase 4 ran, Claude Code fell back to hardcoded default parameters:
```python
mu_defaults = {
    'A': {'HomeSec_Tech': 0.06, ...},
    'B': {'HomeSec_Tech': 0.15, ...},
    'C': {'HomeSec_Tech': 0.28, ...},
}
```
These defaults are reasonable but **not calibrated to actual post-event historical data**. The simulation may be valid in structure but the inputs are unverified.

### How to Check
Open `code/monte_carlo_homesec.py` and search for:
```python
historical_event_returns.csv
```
If that file is loaded and used → MC is calibrated correctly → **no re-run needed**.
If the defaults section is active and the CSV load is commented out or missing → **re-run Phase 4**.

### Fix (Conditional)
1. Check if `data/company_fundamentals/historical_event_returns.csv` exists and has data
2. Check `monte_carlo_homesec.py` to confirm which parameters were used
3. If defaults were used: re-run Phase 4 after Phase 2B data is confirmed complete
4. Commit updated MC outputs with message: `"Phase 4 re-run: MC calibrated to historical event returns"`

---

## Remediation Sequence — Exact Order

```
STEP 1 — Run Phase 2A (Claude Code)
  Prompt: prompts/claude_code_usaspending.md
  Output: reports/draft_agency_mapping.md + data/usaspending_raw/
  Commit: "Phase 2A complete: Agency mapping and USASpending data"
  ↓

STEP 2 — Run Phase 3B (Claude Sonnet)
  Prompt: prompts/claude_sonnet_fundamentals.md
  Requires: draft_agency_mapping.md (from Step 1) + master_fundamentals.csv (exists)
  Output: reports/draft_earnings_assessment.md
  Commit: "Phase 3B complete: Claude Sonnet fundamental analysis"
  ↓

STEP 3 — Check Monte Carlo (conditional)
  Open: code/monte_carlo_homesec.py
  Check: Were historical_event_returns.csv parameters used or defaults?
  If defaults used → re-run Phase 4
  Prompt: prompts/claude_code_monte_carlo.md
  Output: Updated mc_summary_homesec.csv + histograms
  Commit: "Phase 4 re-run: MC recalibrated to historical data"
  ↓

STEP 4 — Full push to GitHub master
  git add -A
  git commit -m "Remediation complete: Phases 2A, 3B added; Phase 4 recalibrated"
  git push origin master
  ↓

STEP 5 — Notify Claude External
  Post git log --oneline -10 to Claude.ai chat
  Claude External runs Phase 5: full audit + reconciliation + HTML report
```

---

## File Inventory — Complete vs. Incomplete

### ✅ COMPLETE
| File | Phase | Agent |
|------|-------|-------|
| `PROJECT_SCOPE.md` | Setup | Cursor |
| `METHODOLOGY.md` | Setup | Placeholder — will be completed in Phase 5 |
| `prompts/grok_threat_assessment.md` | Setup | Created |
| `prompts/claude_code_usaspending.md` | Setup | Created |
| `prompts/chatgpt_codex_earnings_model.md` | Setup | Created |
| `prompts/gemini_company_screen.md` | Setup | Created |
| `prompts/claude_sonnet_fundamentals.md` | Setup | Created |
| `prompts/claude_code_monte_carlo.md` | Setup | Created |
| `prompts/reconciliation_prompt.md` | Setup | Created |
| `reports/draft_threat_assessment.md` | Phase 1 | Grok ✅ |
| `reports/draft_company_universe.md` | Phase 3 | Gemini ✅ |
| `code/earnings_model.py` | Phase 2B | Codex ✅ |
| `data/company_fundamentals/` | Phase 2B | Codex ✅ |
| `code/monte_carlo_homesec.py` | Phase 4 | Claude Code ⚠️ verify params |
| `reports/mc_summary_homesec.csv` | Phase 4 | Claude Code ⚠️ verify params |

### 🔴 MISSING — Must Create Before Phase 5
| File | Phase | Agent | Blocker? |
|------|-------|-------|----------|
| `reports/draft_agency_mapping.md` | Phase 2A | Claude Code | **YES — blocks Phase 3B and final report** |
| `data/usaspending_raw/` | Phase 2A | Claude Code | YES |
| `reports/draft_earnings_assessment.md` | Phase 3B | Claude Sonnet | **YES — blocks final report** |

### 🔴 NOT STARTED — Created in Phase 5 by Claude External
| File | Phase | Agent |
|------|-------|-------|
| `reports/final_validated_report.md` | Phase 5 | Claude External |
| `reports/investment_report_homesec.html` | Phase 5 | Claude External |
| `audits/audit_claude.md` | Phase 5 | Claude External |
| `audits/audit_gemini.md` | Phase 5 | Claude External |
| `audits/audit_chatgpt.md` | Phase 5 | Claude External |
| `METHODOLOGY.md` (full) | Phase 5 | Claude External |

---

## Answer to "Should I Run Claude Sonnet First?"

**No. Run Phase 2A (Claude Code / USASpending) first.**

Claude Sonnet's fundamentals prompt explicitly reads `draft_agency_mapping.md` to verify contract concentration data for each company. If you run Sonnet without that file, it will produce a weaker analysis based only on public knowledge — missing the verified agency-contract-company chain that makes this report institutional quality.

Correct order from here:
1. **Claude Code** → Phase 2A (USASpending)
2. **Claude Sonnet** → Phase 3B (Fundamentals) — reads Phase 2A output
3. **Check + optionally re-run** → Phase 4 (Monte Carlo)
4. **Push everything** → `git push origin master`
5. **Come back here** → Phase 5 reconciliation

---

*Remediation plan authored by Claude External · blake-a11y/The-Investor · March 1, 2026*
