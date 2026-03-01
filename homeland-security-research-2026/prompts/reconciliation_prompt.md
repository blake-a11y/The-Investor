# Reconciliation Prompt — Phase 5: Final Audit & Report Production
**Agent:** Claude External (Anthropic — outside Cursor, repo access via GitHub)
**Project:** Homeland Security Investment Research 2026
**Input:** All committed draft files from Phases 1–4
**Output:** `reports/final_validated_report.md` + `reports/investment_report_homesec.html`

---

## Your Role
You are the final audit and report production agent. You receive all draft outputs from the parallel research agents, run a structured reconciliation audit, resolve conflicts, and produce the final validated report in the same format as the Iran event-driven report.

---

## Step 1 — Read All Drafts (In This Order)
1. `reports/draft_threat_assessment.md` (Grok)
2. `reports/draft_agency_mapping.md` (Claude Code)
3. `reports/draft_company_universe.md` (Gemini)
4. `reports/draft_earnings_assessment.md` (Claude Sonnet)
5. `reports/mc_summary_homesec.csv` (Claude Code)
6. `data/company_fundamentals/master_fundamentals.csv` (Codex)
7. `data/company_fundamentals/historical_event_returns.csv` (Codex)

---

## Step 2 — Cross-Agent Conflict Resolution

Flag and resolve any conflicts between agents on these dimensions:

| Dimension | Check |
|-----------|-------|
| Threat probability | Does Grok's probability tree align with Gemini's event sensitivity ratings? |
| Company data | Do Codex fundamentals match Gemini market data for the same companies? |
| Contract figures | Does Claude Code's USASpending data align with Gemini's contract profile claims? |
| Valuation | Does Codex earnings model align with Claude Sonnet's fundamental assessment? |
| MC inputs | Do Monte Carlo μ parameters align with Codex historical event return data? |

For each conflict: document it in `audits/audit_claude.md` and apply the most conservative / best-sourced resolution.

---

## Step 3 — Factual Audit Checklist

For every material claim in the final report, verify:
- [ ] ≥2 independent sources cited
- [ ] No Wikipedia as primary source
- [ ] All MC parameters (μ, σ) explicitly disclosed with source citations
- [ ] All company data timestamped
- [ ] Historical event return data sourced from primary (Yahoo Finance / SEC) not secondary
- [ ] Threat probability estimates cited to academic/government sources
- [ ] All contract figures verifiable via USASpending.gov

---

## Step 4 — Final Report Production

Produce `reports/final_validated_report.md` with these sections:

```markdown
# Homeland Security Investment Research — Final Report
**Date:** [date]
**Event Trigger:** U.S.–Israel strikes on Iran + Ayatollah death confirmed
**Prepared for:** Wealth-Tech Operations Leader

## Change Log (Drafts → v1.0)

## 1. Executive Summary
   - Threat probability summary (from Grok)
   - Recommended portfolio (from Claude Sonnet)
   - MC results summary table (3 scenarios)
   - Confidence score

## 2. Threat Assessment
   - Probability tree (from Grok, reconciled)
   - Historical analogs
   - Timing assessment

## 3. Agency Response Chain
   - Event → Agency → Contract → Publicly Traded Beneficiary map
   - Surge multipliers by scenario

## 4. Company Universe & Market Data
   - Tier 1, 2, 3 profiles (from Gemini, reconciled)

## 5. Earnings-Based Assessment (NEW vs. Iran report)
   - Fundamental scorecards
   - Investment theses
   - Valuation analysis

## 6. Monte Carlo Results
   - 3 scenarios × 4 sectors
   - Full parameter disclosure
   - Histogram references

## 7. Portfolio Recommendations
   - ETF-first option
   - Concentrated option
   - Integration with existing Iran allocation

## 8. Risk Management & Exit Rules

## 9. Sources Verification Table

## 10. Methodology
    - All 5 agents + roles
    - Data sources by category
    - MC technical summary

## Disclaimer
```

---

## Step 5 — HTML Report Production

Using the same template as `geopolitical-investment-research-2026/reports/investment_report_v1.html`:
- Produce `reports/investment_report_homesec.html`
- Same print-optimized format (EB Garamond + Source Sans 3)
- Same navy/gold color scheme
- Add new section for Earnings-Based Assessment
- Include agency response chain as a visual flow table
- Add company scorecards as structured tables

---

## Step 6 — Confidence Scoring

Score the final report 0–100:
- Start at 100
- Deduct 5 per unresolved single-source claim
- Deduct 10 per unresolved agent conflict
- Deduct 3 per MC parameter without source citation
- Add 5 if historical event return data is present (vs. assumed)
- Add 5 if earnings model is fully parameterized

Target: ≥80/100 before publishing.

---

## Commit Instructions
```
git add homeland-security-research-2026/reports/final_validated_report.md
git add homeland-security-research-2026/reports/investment_report_homesec.html
git add homeland-security-research-2026/audits/audit_claude.md
git commit -m "Phase 5 complete: Final validated report — homeland security"
git push origin master
```
