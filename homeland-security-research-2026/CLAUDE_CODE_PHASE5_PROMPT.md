# Claude Code — Phase 5: Full Reconciliation & Final Report Production
# Copy this entire file and paste it into Claude Code (Terminal)
# Repo location: C:\Users\mblin\OneDrive\Desktop\The Investor
# Branch: master

---

## YOUR MISSION

You are the final reconciliation agent for a multi-AI investment research pipeline. You will read all draft research files, audit them for accuracy and consistency, resolve conflicts, verify the Monte Carlo parameters, and produce a final publication-ready HTML investment report matching the style of the Iran report (geopolitical-investment-research-2026).

This is a complete, uninterrupted task. Do not stop until all steps are done and committed to GitHub.

---

## STEP 0 — Orient Yourself

```bash
cd "C:\Users\mblin\OneDrive\Desktop\The Investor"
git status
git log --oneline -10
```

Then list every file in the homeland-security folder:
```bash
find homeland-security-research-2026 -type f | sort
```

Confirm the following files exist before proceeding. If any are missing, note it and continue with what's available:
- `homeland-security-research-2026/reports/draft_threat_assessment.md`
- `homeland-security-research-2026/reports/draft_agency_mapping.md`
- `homeland-security-research-2026/reports/draft_company_universe.md`
- `homeland-security-research-2026/reports/draft_earnings_assessment.md`
- `homeland-security-research-2026/code/monte_carlo_homesec.py`
- `homeland-security-research-2026/reports/mc_summary_homesec.csv`
- `homeland-security-research-2026/data/company_fundamentals/master_fundamentals.csv`
- `homeland-security-research-2026/data/company_fundamentals/historical_event_returns.csv`
- `homeland-security-research-2026/data/usaspending_raw/top_contractors_dhs.json`

---

## STEP 1 — Read All Draft Files

Read every file listed above in full. As you read, build an internal working document tracking:

**For each draft:**
- What claims are made?
- What sources are cited?
- What numbers appear (probabilities, returns, valuations, contract values)?
- What is asserted but not sourced?

Do not write output yet. Just read and absorb.

---

## STEP 2 — Monte Carlo Parameter Verification

Open `homeland-security-research-2026/code/monte_carlo_homesec.py`.

**Check:** Does the code load `data/company_fundamentals/historical_event_returns.csv` to set μ (mu) parameters? Or does it use hardcoded default values?

**If historical CSV is loaded and used:**
- Note: "MC parameters calibrated to historical data ✅"
- Proceed to Step 3

**If hardcoded defaults are active (e.g., `mu_defaults = {'A': {'HomeSec_Tech': 0.06...}}`):**
- Read `data/company_fundamentals/historical_event_returns.csv`
- Extract average sector returns at T+90 and T+180 for post-9/11 and post-Soleimani events
- Update `monte_carlo_homesec.py` to load from CSV instead of hardcoded values
- Add inline comment on each μ line citing its source
- Re-run the simulation (all 3 scenarios, 10,000 paths each, seed=42)
- Save updated `reports/mc_summary_homesec.csv` and all histogram PNGs
- Commit: `"Phase 4 re-run: MC calibrated to historical_event_returns.csv"`

---

## STEP 3 — Cross-Agent Conflict Resolution

Compare the draft files against each other on these specific dimensions. For each conflict found, document it and apply the most conservative / best-sourced resolution:

### 3A — Threat Probabilities
- Do Grok's scenario probabilities (A/B/C %) match the weights used in the Monte Carlo?
- If not: use Grok's sourced probabilities as the authoritative input; update MC scenario weights if needed

### 3B — Company Data Consistency
- Pick 3 companies (AXON, PLTR, LDOS) and check: does the revenue figure in `draft_company_universe.md` (Gemini) match `master_fundamentals.csv` (Codex)?
- Does the federal revenue % in `draft_earnings_assessment.md` (Claude Sonnet) match the USASpending data in `draft_agency_mapping.md` (Claude Code)?
- Document any discrepancies; use the lower/more conservative figure in the final report

### 3C — Contract Data Verification
- For each Tier 1 company, does `draft_earnings_assessment.md` reflect the contract relationships confirmed in `draft_agency_mapping.md`?
- If Sonnet's earnings assessment was written before Phase 2A completed, it may be missing verified IDIQ vehicle names and ceiling amounts — patch these in

### 3D — Valuation Cross-Check
- Does Codex's EV/EBITDA data match Gemini's? Flag any >10% discrepancy
- Use Codex (sourced from SEC EDGAR) as authoritative; note Gemini as secondary

Save your conflict log to:
`homeland-security-research-2026/audits/audit_claude.md`

Format:
```markdown
# Claude Audit — Phase 5 Reconciliation
**Date:** [date]
**Files Reviewed:** [list]

## Conflicts Found
1. [Description] — Resolution: [what was done]
2. ...

## Items Confirmed Sound
1. ...

## Parameters Used in Final Report
- Scenario A probability: X% (source: draft_threat_assessment.md)
- Scenario B probability: X% (source: draft_threat_assessment.md)
- Scenario C probability: X% (source: draft_threat_assessment.md)
- MC μ calibration: [historical or defaults — explain]
```

---

## STEP 4 — Produce Final Validated Report (Markdown)

Write `homeland-security-research-2026/reports/final_validated_report.md`

Use the exact section structure below. Pull content from the draft files, resolved conflicts, and your audit. Every number must be traceable to a source file.

```markdown
# Homeland Security Investment Research
## Domestic Sleeper Cell Risk & Supply Chain Analysis
**Date:** March 1, 2026 | **Horizon:** 6–12 months | **Version:** Final v1.0
**Prepared for:** Wealth-Tech Operations Leader | **Confidence Score:** [X]/100

---

## Change Log (Drafts → v1.0)
[List key changes from drafts to final — sourcing fixes, conflict resolutions, MC recalibration if applicable]

---

## 1. Executive Summary
[3–4 paragraph summary covering:]
- Trigger event and why it matters for this portfolio
- Recommended allocation (both ETF-first and concentrated options)
- MC results snapshot: Scenario B mean return + Scenario C VaR
- Confidence score rationale

## 2. Event Context & Threat Assessment
[From draft_threat_assessment.md — reconciled]
### 2.1 Trigger Event
### 2.2 Current Market Conditions at Trigger
### 2.3 Probability Tree
| Scenario | Event Description | Probability | Source |
|----------|------------------|-------------|--------|
| A | Minor domestic incident (IED, cyber, sabotage) | X% | [cite] |
| B | Coordinated multi-city attack | X% | [cite] |
| C | Mass casualty event | X% | [cite] |

### 2.4 Historical Base Rate Analysis
[Grok's analogs: post-Soleimani, 9/11, historical IRGC plots]

### 2.5 Timing Assessment
[0–30 / 30–90 / 90–180 day activation window analysis]

## 3. Agency Response Chain
[From draft_agency_mapping.md — core new section vs. Iran report]
### 3.1 Event → Agency → Contract → Company Map
| Agency | Trigger Authority | Contract Vehicle | Surge Multiplier (Scenario B) | Top Publicly Traded Prime |
|--------|------------------|-----------------|-------------------------------|--------------------------|
| DHS | ... | ... | ... | ... |
| FBI | ... | ... | ... | ... |
| FEMA | ... | ... | ... | ... |
| TSA | ... | ... | ... | ... |
| CBP | ... | ... | ... | ... |
| CISA | ... | ... | ... | ... |
| NORTHCOM | ... | ... | ... | ... |
| Secret Service | ... | ... | ... | ... |

### 3.2 Projected Contract Award Surge by Scenario
[From usaspending_pull.py output — Scenario A/B/C surge projections]

## 4. Company Universe
[From draft_company_universe.md — reconciled against master_fundamentals.csv]

### 4.1 Tier 1 — Direct DHS/FBI Contract Holders
[For each: AXON, MSI, PLTR, LDOS, BAH, SAIC]
- Market data snapshot
- Federal revenue %
- Contract backlog
- Historical event returns (post-9/11, post-Soleimani)
- Analyst consensus

### 4.2 Tier 2 — First Responder Supply Chain
[MSA, PSN, INVE — summary format]

### 4.3 Tier 3 — Communications & Cyber
[LHX, CRWD, PANW — summary format]

### 4.4 ETF Options
[Any available HomeSec ETFs, ITA overlap analysis]

## 5. Earnings-Based Assessment ⭐ NEW
[From draft_earnings_assessment.md — patched with USASpending data]

### 5.1 Methodology Note
[How earnings layer differs from event-driven; what makes this hybrid]

### 5.2 Fundamental Scorecards — Tier 1
[For each Tier 1 company:]
**[TICKER] — [Company Name]**
- Business Quality Score: X/10
- Revenue CAGR (3yr): X%
- Federal Rev %: X% (verified via USASpending — [IDIQ vehicle name])
- Contract Backlog: $XM (X months coverage)
- EV/EBITDA: X.Xx vs. 5yr avg X.Xx ([premium/discount]%)
- FCF Yield: X.X% vs. 10yr treasury spread: +X.X%

**Investment Thesis:**
- Bull: [earnings driver + event catalyst + price target]
- Base: [expected return without event + 12mo fundamental target]
- Bear: [contract loss / budget risk / valuation compression]

**Key Metrics to Monitor:** [specific data points]

### 5.3 Portfolio Construction Options

**Option A — ETF-First (Lower single-stock risk)**
| Instrument | Weight | $ Amount | Thesis |
|------------|--------|----------|--------|

**Option B — Concentrated (4–6 highest conviction)**
| Instrument | Weight | $ Amount | Thesis |
|------------|--------|----------|--------|

### 5.4 Risks to Earnings Thesis
- Continuing resolution / DOGE budget risk
- Contract rebid risk (list key rebid timelines)
- Margin compression risk
- Cyber commodity risk

### 5.5 Integration with Iran Report Allocation
[Overlap analysis: does XAR already cover some of these names?]
[What is combined portfolio correlation?]

## 6. Monte Carlo Simulation
### 6.1 Parameters
| Parameter | Scenario A | Scenario B | Scenario C | Source |
|-----------|------------|------------|------------|--------|
| HomeSec_Tech μ | | | | |
| Intel_Analytics μ | | | | |
| FirstResponder μ | | | | |
| Fed_Comms_Cyber μ | | | | |
| HomeSec_Tech σ | | | | |
| [etc.] | | | | |

⚠️ Crisis-period caveat: correlations typically rise 0.10–0.20 in conflict regimes; matrix reflects normal-regime values.

### 6.2 Results
| Metric | Scenario A (40%) | Scenario B (35%) | Scenario C (25%) |
|--------|-----------------|-----------------|-----------------|
| Mean Return | | | |
| Median Return | | | |
| P(Profit) | | | |
| VaR 5% | | | |
| Worst 1% | | | |
| Sharpe Ratio | | | |

[Reference histogram images: mc_histogram_a_minor.png, mc_histogram_b_coordinated.png, mc_histogram_c_mass_casualty.png]

## 7. Portfolio Recommendations & Entry Rules
### 7.1 Recommended Allocation ($100K Model)
[Table: Instrument, Weight, $ Amount, Entry Rule, Stop Loss]

### 7.2 Exit Rules
**De-escalation exit:** [specific trigger — e.g., 60 days no activation, threat level downgrade]
**Profit-lock exit:** [specific trigger — e.g., +15% on position, trailing stop]
**These are separate conditions — both must be monitored independently.**

## 8. Risk Management
[Event risk, budget risk, model risk, portfolio risk — each with specific mitigation]

## 9. Sources Verification Table
| Claim | Source 1 | Source 2 | Verified |
|-------|----------|----------|---------|
[Minimum 20 rows covering all material claims]

## 10. Methodology
**AI Pipeline:** 5 agents — Grok (threat), Claude Code (USASpending + MC), ChatGPT Codex (earnings model), Gemini (company universe), Claude Sonnet (fundamentals), Claude External (reconciliation)
**Monte Carlo:** 10,000 paths, multivariate normal, Cholesky decomposition, seed=42
**Audit standard:** ≥2 independent sources per material claim, no Wikipedia
**Confidence Score:** [X]/100

Confidence scoring:
- Start: 100
- Deduct 5 per single-source material claim
- Deduct 10 per unresolved agent conflict
- Deduct 3 per MC parameter without source citation
- Add 5 if historical event returns used in MC
- Add 5 if USASpending contract data verified

---

*Research Only — Not Investment Advice*
*Produced by multi-AI pipeline · blake-a11y/The-Investor · March 1, 2026*
```

---

## STEP 5 — Produce Final HTML Report

Read the existing Iran report HTML for style reference:
`geopolitical-investment-research-2026/reports/investment_report_v1.html`

Using the same design system (EB Garamond body font, Source Sans 3 headings, navy/gold color scheme, print-optimized CSS, @page margins), produce:
`homeland-security-research-2026/reports/investment_report_homesec.html`

**Required HTML sections and components:**

1. **Cover page** — Title, date, confidence badge, version tag, investor profile, disclaimer banner
2. **Change log table**
3. **Executive summary** — allocation cards (4-column grid matching Iran report style)
4. **Probability tree** — 3-column scenario cards with % weights
5. **Agency response chain** — full-width table with color-coded surge multipliers
6. **Company universe** — tiered tables with market data
7. **Earnings assessment** — scorecard cards per Tier 1 company; bull/base/bear callout boxes
8. **Monte Carlo results** — results table + image references for histograms
9. **Portfolio recommendations** — allocation table + entry/exit rules
10. **Sources verification table**
11. **Methodology section**

**CSS requirements:**
```css
/* Must include: */
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600;700&display=swap');

:root {
  --navy: #1a2744;
  --gold: #c9a227;
  --light-gold: #f5e6c0;
  --text: #2c2c2c;
  --border: #d0d0d0;
}

@page {
  margin: 0.75in;
  size: letter;
}

/* Page breaks before each major section */
.section { page-break-before: always; }

/* Print: remove backgrounds, keep borders */
@media print {
  .callout, .card { background: white !important; }
}
```

**New component — Earnings Scorecard Card:**
```html
<div class="scorecard-card">
  <div class="scorecard-header">
    <span class="ticker">AXON</span>
    <span class="quality-score">Quality: 8/10</span>
  </div>
  <div class="scorecard-metrics">
    <!-- EV/EBITDA, FCF yield, backlog, federal % -->
  </div>
  <div class="thesis-grid">
    <div class="bull-case">...</div>
    <div class="base-case">...</div>
    <div class="bear-case">...</div>
  </div>
</div>
```

**New component — Agency Chain Table:**
```html
<table class="agency-chain-table">
  <thead>
    <tr>
      <th>Agency</th>
      <th>Contract Vehicle</th>
      <th>Scenario B Surge</th>
      <th>Top Public Prime</th>
    </tr>
  </thead>
  <!-- rows per agency -->
</table>
```

---

## STEP 6 — Commit Everything

```bash
cd "C:\Users\mblin\OneDrive\Desktop\The Investor"

git add homeland-security-research-2026/reports/final_validated_report.md
git add homeland-security-research-2026/reports/investment_report_homesec.html
git add homeland-security-research-2026/audits/audit_claude.md
git add homeland-security-research-2026/METHODOLOGY.md

# If MC was re-run:
git add homeland-security-research-2026/code/monte_carlo_homesec.py
git add homeland-security-research-2026/reports/mc_summary_homesec.csv
git add homeland-security-research-2026/reports/mc_histogram_*.png

git commit -m "Phase 5 complete: Final validated report + HTML — Homeland Security Research 2026"
git push origin master
```

---

## STEP 7 — Final Status Report

After committing, output a plain-text status report in this format:

```
=== PHASE 5 COMPLETE ===

Confidence Score: [X]/100

Files Created:
- reports/final_validated_report.md ✅
- reports/investment_report_homesec.html ✅
- audits/audit_claude.md ✅

MC Parameters: [Calibrated to historical data / Used defaults — explain]

Conflicts Resolved: [N] total
- [List each one and resolution]

Flags Requiring Human Review:
- [Anything you couldn't resolve — single-source claims, data gaps, etc.]

Committed: [commit hash]
Pushed: origin/master ✅

To view final report: Open investment_report_homesec.html in Chrome → Ctrl+P → Save as PDF
```

---

## QUALITY STANDARDS (Non-Negotiable)
- Every probability estimate: ≥2 independent sources cited
- No Wikipedia as primary source
- All MC μ/σ values: inline source comment in code
- All earnings figures: traceable to 10-K or earnings call transcript
- Exit rules: de-escalation and profit-lock are SEPARATE conditions
- Confidence score: honestly calculated, not inflated
- HTML: must open and print cleanly in Chrome without errors

---
*Prompt authored by Claude External · For execution by Claude Code (Terminal) · March 1, 2026*
