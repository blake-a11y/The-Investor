# Methodology — Homeland Security Investment Research (2026)

**Version:** 1.0 Final | **Date:** 2026-03-01 | **Confidence:** 87/100

---

## AI Agent Pipeline

| Phase | Agent | Role | Output |
|-------|-------|------|--------|
| 1 | Grok (xAI) | Threat probability tree; domestic security activation base rates; 18+ cited government/academic sources | `reports/draft_threat_assessment.md` |
| 2A | Claude Code | USASpending.gov live API pull (4 endpoints); agency mapping; surge multiplier model | `code/usaspending_pull.py`, `reports/draft_agency_mapping.md`, `data/usaspending_raw/*.json` |
| 2B | Codex (OpenAI) | SEC EDGAR XBRL fundamentals extraction; scenario earnings model | `code/earnings_model.py`, `data/company_fundamentals/*.csv` |
| 3 | Gemini (Google) | Company universe screen (stub — integrated Phase 5) | `reports/draft_company_universe.md` |
| 3B | Claude Sonnet | Fundamental assessment; investment theses (stub — integrated Phase 5) | `reports/draft_earnings_assessment.md` |
| 4 | Claude Code | Monte Carlo simulation (10,000 paths; 3 scenarios; 4 sectors; seed=42) | `code/monte_carlo_homesec.py`, `reports/mc_*.csv`, `reports/mc_*.png` |
| 5 | Claude (External) | Phase 5 reconciliation: conflict resolution; MC recalibration; final report; HTML | `reports/final_validated_report.md`, `reports/investment_report_homesec.html`, `audits/audit_claude.md` |

---

## Monte Carlo Simulation

**Engine:** Python 3.12.10 / NumPy / Pandas / Matplotlib
**Distribution:** Geometric Brownian Motion log-return — `ln(S_t/S_0) ~ N((mu - sigma^2/2)t, sigma^2 t)`
**Correlation structure:** Cholesky decomposition of 4x4 sector correlation matrix
**Paths:** 10,000 | **Seed:** 42 (fully reproducible)
**Horizons:** Scenario A = 0.5yr | Scenario B = 1.0yr | Scenario C = 2.0yr

**mu Calibration (Phase 5 re-run 2026-03-01):**
- mu parameters computed programmatically from `data/company_fundamentals/historical_event_returns.csv`
- Scenario A: Soleimani T+30 sector averages (pre-COVID clean window; T+90/T+180 excluded — COVID crash dominates those windows)
- Scenario C: 9/11 T+90 (HomeSec_Tech); 9/11 T+180 (FirstResponder, Fed_Comms_Cyber); Boston Marathon T+90 x empirical severity scale for Intel_Analytics (BAH/LDOS pre-IPO 2001)
- Scenario B: arithmetic mean of A and C, bounded [0.05, 0.25]
- All parameters with inline source comments in `code/monte_carlo_homesec.py`

**sigma Calibration:** 5-year realized volatility from Yahoo Finance (2019-2024) — hardcoded; single source flag
**Correlation matrix:** 5-year rolling correlations from Yahoo Finance blended proxies (2019-2024) — single source flag
**Crisis adjustment:** Scenario C sigma scaled x1.20 (documented crisis vol regime uplift)

---

## Audit Standard

- 2+ independent sources per material claim
- No Wikipedia as primary source
- All MC mu/sigma values with inline citations in code
- All company data timestamped (as_of_utc field in master_fundamentals.csv)
- Conflict log maintained in `audits/audit_claude.md`
- Confidence score: start 100, deduct per methodology in audit

---

## Data Sources

| Source | Usage | Access Method |
|--------|-------|--------------|
| USASpending.gov API | DHS obligations FY2022-2025; top contractors; award search | Public REST API — no key required |
| SEC EDGAR XBRL | Company fundamentals (revenue, backlog, EV/EBITDA) | EDGAR full-text search API |
| Yahoo Finance | Historical event returns; 5-yr realized volatility | Historical price download |
| DHS Budget-in-Brief | Agency spending baseline | Public PDF — dhs.gov |
| GAO-03-1091T | Post-9/11 surge multipliers | GAO public reports |
| CRS R44993 | Surge multiplier corroboration | Congressional Research Service |
| DOJ press releases | Disrupted IRGC plot count | justice.gov public record |
| DHS Homeland Threat Assessment 2025 | Domestic threat probability anchoring | dhs.gov/hta |
| DNI Annual Threat Assessment 2025 | IC threat level calibration | dni.gov/ata |
| START Global Terrorism Database | Historical base rate for mass casualty events | start.umd.edu |

---

*Methodology approved for publication at confidence 87/100.*
*Repository: blake-a11y/The-Investor | Branch: master*
