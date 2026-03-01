# Phase 5 Readiness Audit & Remediation Plan
**Project:** Homeland Security Investment Research 2026
**Auditor:** Claude External
**Date:** March 1, 2026
**Status:** PRE-RECONCILIATION AUDIT

---

## Task 1 — What Type of Report Is the Iran PDF?

The attached PDF ("Geopolitical Investment Research — February 28, 2026") is an **Event-Driven Geopolitical Investment Research Report**. This is a specific institutional document format with the following characteristics:

### Formal Definition
An Event-Driven Geopolitical Investment Research Report is a time-sensitive, institutional-grade investment thesis triggered by a discrete geopolitical event (military strike, leadership death, sanctions, treaty collapse) that:

1. **Quantifies market impact** of the event on specific asset classes within a defined time horizon
2. **Constructs an actionable portfolio** with specific instruments, weightings, entry rules, and exit rules
3. **Stress-tests the thesis** using simulation (Monte Carlo) across multiple probability-weighted scenarios
4. **Verifies all claims** to ≥2 independent sources — no unsourced assertions
5. **Discloses all model parameters** (μ, σ, correlation matrix, seed) for reproducibility
6. **Assigns a confidence score** reflecting audit-verified analytical rigor

### How It Differs from Standard Research
| Standard Equity Research | Event-Driven Geo Report |
|--------------------------|------------------------|
| Quarterly earnings focus | Triggered by discrete event |
| 12-month price targets | 3–12 month event resolution horizon |
| Single stock | Multi-asset portfolio |
| Analyst opinion | Monte Carlo probability distribution |
| No simulation | 10,000-path simulation required |
| Passive risk language | Explicit VaR and worst-1% disclosure |

### The Homeland Security Report — Hybrid Format
This project requires a **hybrid report** that adds a second layer not present in the Iran report:

| Layer | Iran Report | Homeland Security Report |
|-------|-------------|--------------------------|
| Event-driven thesis | ✅ Geopolitical strike | ✅ Sleeper cell activation risk |
| Monte Carlo simulation | ✅ 3 scenarios | ✅ 3 domestic scenarios |
| Earnings-based thesis | ❌ Not included | ✅ **REQUIRED — new layer** |
| Agency contract chain | ❌ Not included | ✅ **REQUIRED — new layer** |
| Fundamental scorecards | ❌ Not included | ✅ **REQUIRED — new layer** |

---

## Task 2 — What Must Be in This Report (Data Requirements)

### Section 1: Executive Summary
**Required data:**
- Threat probability summary (single number + scenario tree)
- Recommended portfolio allocation (tickers + weights + $ amounts)
- Monte Carlo results table (mean return, VaR 5%, worst 1%, Sharpe — per scenario)
- Confidence score (0–100)
- One-page investment case

### Section 2: Event Context & Threat Assessment
**Required data:**
- Trigger event description with timestamp and source citations
- Current market conditions at time of trigger (prices, YTD moves)
- Probability tree: 3 scenarios with % weights, sourced to historical analogs
- Historical base rate data (how often do sleeper cells activate post-trigger?)
- Timing analysis (0–30 day vs. 30–90 day vs. 90–180 day activation window)
- Target profile (infrastructure vs. soft targets vs. government)
- ≥2 independent sources per probability estimate

### Section 3: Agency Response Chain (NEW — not in Iran report)
**Required data:**
- Event → Agency → Contract Vehicle → Prime Contractor map
- 8 agencies: DHS, FBI, FEMA, TSA, CBP, NORTHCOM, CISA, Secret Service
- Surge multiplier per agency per scenario (sourced from GAO/CRS)
- IDIQ vehicle names and ceiling amounts
- USASpending.gov contract obligation data FY2022–2025

### Section 4: Company Universe & Market Data
**Required data (per company, 3 tiers):**
- Ticker, market cap, 52-week range, YTD performance
- % revenue from federal/DHS contracts
- Contract backlog ($M and months of coverage)
- Historical event return (post-9/11, post-Soleimani, T+30/90/180)
- Analyst consensus (Buy/Hold/Sell, price target, implied upside)
- Most significant contract wins last 12 months

### Section 5: Earnings-Based Assessment (NEW — not in Iran report)
**Required data (per Tier 1 company):**
- 3-year revenue CAGR
- EV/EBITDA current vs. 5-year average (premium/discount)
- FCF yield vs. 10-year treasury spread
- Contract backlog coverage ratio
- Fundamental scorecard (1–10 business quality rating)
- Investment thesis: bull / base / bear case with price targets
- Key risks to earnings (continuing resolution, rebid, margin compression)

### Section 6: Monte Carlo Simulation
**Required data:**
- 3 scenarios × 4 sectors, 10,000 paths each
- Full μ/σ parameter table with source citations for each value
- Correlation matrix with time period and crisis-period caveat
- Scenario probability weights (sourced from threat assessment)
- Output: mean, median, P(profit), VaR 5%, worst 1%, Sharpe ratio
- 4 histogram PNGs + portfolio overview PNG + allocation pie chart

### Section 7: Portfolio Recommendations
**Required data:**
- Two portfolio options: ETF-first and concentrated (4–6 names)
- $ allocation per instrument
- Entry rules (market order vs. limit ±1%)
- Exit rules: profit-lock trigger AND de-escalation trigger (separate)
- Position sizing rationale
- Overlap analysis vs. existing Iran report allocation

### Section 8: Risk Management
**Required data:**
- Event risk: What ends the thesis early?
- Budget risk: Continuing resolution, DOGE spending cuts
- Model risk: MC assumptions, correlation compression in crisis
- Portfolio risk: Concentration, liquidity, slippage estimates

### Section 9: Sources Verification Table
**Required data:**
- Every material claim: Source 1, Source 2, Verified Y/N
- No Wikipedia as primary source
- All earnings data from 10-K or earnings call transcripts only

### Section 10: Methodology
**Required data:**
- All 5 AI agents + roles
- Data sources by category
- MC technical summary (Cholesky decomposition, seed, parameters)
- Audit process documentation
- Confidence score breakdown

---

## Task 3 — GitHub Audit: What's Present vs. Missing

### Confirmed COMPLETE (from commit history + agent reports)

| File | Phase | Agent | Evidence |
|------|-------|-------|----------|
| `reports/draft_threat_assessment.md` | 1 | Grok | URL confirmed live on GitHub |
| `reports/draft_company_universe.md` | 3 | Gemini | Commit `e955282` |
| `code/earnings_model.py` | 2B | ChatGPT Codex | Commit `d3d045f` |
| `data/company_fundamentals/master_fundamentals.csv` | 2B | ChatGPT Codex | Confirmed by Codex agent report |
| `data/company_fundamentals/historical_event_returns.csv` | 2B | ChatGPT Codex | Confirmed by Codex agent report |
| `reports/draft_agency_mapping.md` | 2A | Claude Code | Confirmed complete — all 4 tasks done, 8 agencies, 11 tickers |
| `data/usaspending_raw/*.json` (4 files) | 2A | Claude Code | Confirmed: DHS obligations, top contractors, 9/11 analog, IDIQ vehicles |
| `code/usaspending_pull.py` | 2A | Claude Code | Confirmed complete |
| `reports/draft_earnings_assessment.md` | 3B | Claude Sonnet | Confirmed complete per user report |
| `code/monte_carlo_homesec.py` | 4 | Claude Code | Exists locally, pushed |
| `reports/mc_summary_homesec.csv` | 4 | Claude Code | Exists — parameters need verification |
| `REMEDIATION_PLAN.md` | Admin | Claude External | Commit `f001f01` confirmed pushed |
| All 7 prompt files | Setup | Cursor | Committed |
| `PROJECT_SCOPE.md` | Setup | Cursor | Committed |

### ⚠️ NEEDS VERIFICATION BEFORE PHASE 5

| File | Issue | Action Required |
|------|-------|----------------|
| `code/monte_carlo_homesec.py` | Unknown whether historical_event_returns.csv was loaded or defaults used | **Open file, check parameter source** |
| `reports/mc_summary_homesec.csv` | If defaults used, numbers are unanchored | **Re-run Phase 4 if defaults confirmed** |
| `reports/draft_earnings_assessment.md` | Ran before Phase 2A was complete — may be missing agency contract data | **Check if USASpending data was incorporated** |

### 🔴 NOT YET CREATED (Created by Claude External in Phase 5)

| File | Phase | Notes |
|------|-------|-------|
| `reports/final_validated_report.md` | 5 | Final reconciled report |
| `reports/investment_report_homesec.html` | 5 | Print-ready HTML (same template as Iran report) |
| `audits/audit_claude.md` | 5 | Claude's audit flags |
| `audits/audit_gemini.md` | 5 | Gemini's audit flags |
| `audits/audit_chatgpt.md` | 5 | ChatGPT's audit flags |
| `METHODOLOGY.md` (full) | 5 | Full methodology documentation |

---

## Task 4 — Remediation Assessment

### Verdict: ONE conditional remediation action, then READY FOR PHASE 5

All major research phases are complete. The only remaining uncertainty is the Monte Carlo parameter calibration. Here is the complete pre-Phase 5 checklist:

---

### Remediation Item 1 — REQUIRED: Verify Monte Carlo Parameters
**Priority: HIGH | Estimated time: 15 minutes**

**Action:** Open this file in Cursor:
```
C:\Users\mblin\OneDrive\Desktop\The Investor\homeland-security-research-2026\code\monte_carlo_homesec.py
```

Search for this section:
```python
historical_event_returns.csv
```

**If you see the CSV being loaded and used to set μ values → NO RE-RUN NEEDED.**
The MC is calibrated to actual historical data. Proceed directly to Phase 5.

**If you see this block active (defaults in use):**
```python
mu_defaults = {
    'A': {'HomeSec_Tech': 0.06, ...},
    'B': {'HomeSec_Tech': 0.15, ...},
    'C': {'HomeSec_Tech': 0.28, ...},
}
```
→ **Re-run Phase 4.** Use this prompt (paste directly to Claude Code in Cursor):

---

#### Phase 4 Re-Run Prompt (If Needed)
```
Read the file: data/company_fundamentals/historical_event_returns.csv

Extract the average sector return for HomeSec_Tech, Intel_Analytics, 
FirstResponder, and Fed_Comms_Cyber at T+90 and T+180 days for:
- Post-9/11 (Sep 2001)
- Post-Soleimani (Jan 2020)

Use these as your μ calibration anchors:
- Scenario A μ = average of post-Soleimani T+90 returns
- Scenario B μ = interpolated between Soleimani and 9/11 T+90
- Scenario C μ = average of post-9/11 T+180 returns

Update monte_carlo_homesec.py to load from historical_event_returns.csv 
instead of hardcoded defaults. Add inline comment citing the source for 
each μ value. Re-run all 3 scenarios (10,000 paths each). 

Save updated:
- code/monte_carlo_homesec.py
- reports/mc_summary_homesec.csv  
- reports/mc_histogram_a_minor.png
- reports/mc_histogram_b_coordinated.png
- reports/mc_histogram_c_mass_casualty.png
- reports/mc_portfolio_histograms_homesec.png
- reports/mc_allocation_pie_homesec.png

Commit with message: "Phase 4 re-run: MC calibrated to historical event returns"
```

---

### Remediation Item 2 — RECOMMENDED: Patch draft_earnings_assessment.md
**Priority: MEDIUM | Estimated time: 30 minutes**

Phase 3B (Claude Sonnet fundamentals) ran before Phase 2A (USASpending) was confirmed complete. The earnings assessment may be missing verified agency contract data for each company.

**Action:** Run this patch prompt in Claude Sonnet (Cursor):

```
Read: reports/draft_earnings_assessment.md (your previous output)
Read: reports/draft_agency_mapping.md (now complete — 8 agencies, 11 tickers)
Read: data/usaspending_raw/top_contractors_dhs.json

For each Tier 1 company (AXON, MSI, PLTR, LDOS, BAH, SAIC):

1. Check whether the agency contract data from draft_agency_mapping.md 
   is reflected in the fundamental scorecard and investment thesis

2. For any company where the contract relationship is NOW confirmed 
   via USASpending data but was missing in your first pass — 
   add a "Contract Verification" subsection citing the specific 
   IDIQ vehicle name, ceiling amount, and agency

3. Update the "Contract Concentration Risk" section to reflect 
   verified USASpending figures, not estimated percentages

Append a section: "## Amendment: Post-Phase 2A Contract Verification"
documenting what changed from the original draft.

Save as: reports/draft_earnings_assessment.md (overwrite)
Commit: "Phase 3B amendment: Contract data incorporated from USASpending"
```

---

### If Both Items Are Resolved — PHASE 5 IS READY

Push everything:
```powershell
cd "C:\Users\mblin\OneDrive\Desktop\The Investor"
git add -A
git commit -m "Pre-Phase 5: MC verified, earnings assessment patched with contract data"
git push origin master
```

Then paste `git log --oneline -10` here and I will:
1. Run full cross-agent conflict resolution audit
2. Produce `reports/final_validated_report.md`
3. Produce `reports/investment_report_homesec.html` (same template as Iran PDF)
4. Score confidence (target ≥80/100)
5. Commit everything and confirm repo is complete

---

## Report Structure — Final Output vs. Iran PDF

The final HTML/PDF will mirror the Iran report structure with these additions:

| Section | Iran Report | Homeland Security Report |
|---------|-------------|--------------------------|
| Cover page + confidence badge | ✅ | ✅ |
| Executive summary | ✅ | ✅ |
| Event context | ✅ | ✅ |
| Probability tree | ✅ | ✅ (with threat sourcing) |
| **Agency response chain** | ❌ | ✅ NEW |
| Correlation matrix | ✅ | ✅ |
| **Company universe (tiered)** | ❌ | ✅ NEW |
| **Earnings-based assessment** | ❌ | ✅ NEW |
| **Fundamental scorecards** | ❌ | ✅ NEW |
| Monte Carlo results | ✅ | ✅ |
| Portfolio allocation | ✅ | ✅ (2 options: ETF-first + concentrated) |
| Exit rules | ✅ | ✅ |
| Sources verification table | ✅ | ✅ |
| Methodology | ✅ | ✅ |
| Change log | ✅ | ✅ |

---

*Audit by Claude External · blake-a11y/The-Investor · March 1, 2026*
