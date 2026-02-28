# Research Methodology — Geopolitical Investment Report (Feb 28, 2026)

**Document purpose:** Exhaustive description of the methodology used to create the Event-Driven Allocation research report. Includes AI agents, models, resources, and Monte Carlo specification.

---

## 1. Workflow Overview

The report was produced via a **multi-AI peer-reviewed pipeline** with four distinct phases:

| Phase | Description | Output |
|-------|-------------|--------|
| **1. Primary Draft** | Single AI generates initial research report from master instructions | `reports/draft_grok_v1.md` |
| **2. Parallel Audits** | Three independent AIs audit the draft in parallel | `reports/audit_claude.md`, `audit_gemini.md`, `audit_chatgpt.md` |
| **3. Reconciliation** | Primary AI incorporates audit feedback and resolves discrepancies | `reports/final_validated_report.md` |
| **4. Validation** | Independent Python Monte Carlo execution; PDF export | Files in `reports/` |

---

## 2. AI Agents Used

### 2.1 Primary Draft Agent

| Attribute | Value |
|-----------|-------|
| **Agent** | Grok |
| **Provider** | xAI |
| **Model** | Not explicitly versioned in repo; Grok Web interface (grok.com) |
| **Role** | Primary research author; geopolitical context; sector analysis; allocation recommendation; initial MC framework |
| **Input** | `prompts/master_instructions.md` + `prompts/grok_prompt_v1.md` + shared conversation history (Grok Web share link) |
| **Output** | `reports/draft_grok_v1.md` (12–18 page equivalent); partial MC code in appendix |

### 2.2 Audit Agents (Parallel)

| Agent | Provider | Model (as specified in CURSOR_ORCHESTRATION.md) | Role | Output |
|-------|----------|-------------------------------------------------|------|--------|
| **Claude** | Anthropic | Claude Opus 4.5 / Claude 4 (or nearest available) | Factual accuracy; MC validity; single-source flagging; suitability verification | `reports/audit_claude.md` |
| **Gemini** | Google | Gemini 3.5 (or integrated Cursor model) | Audience alignment; factual accuracy; MC logic; investor profile verification | `reports/audit_gemini.md` |
| **ChatGPT** | OpenAI | GPT-4o / o1 (or latest) | Factual accuracy; MC validity; claim verification ledger; 2025–2026 source upgrades | `reports/audit_chatgpt.md` |

*Note: Exact model versions at execution time depend on Cursor subscription and external app versions (Claude external, ChatGPT, Gemini).*

### 2.3 Reconciliation Agent

| Attribute | Value |
|-----------|-------|
| **Agent** | Grok |
| **Role** | Incorporate all three audit outputs; resolve 13+ Claude flags, 3 Gemini flags, 20+ ChatGPT items; produce v1.0 |
| **Input** | Draft + `audit_claude.md` + `audit_gemini.md` + `audit_chatgpt.md` |
| **Output** | `reports/final_validated_report.md` |

### 2.4 Orchestrator

| Attribute | Value |
|-----------|-------|
| **Agent** | Cursor Composer (default) |
| **Role** | Project coordination; prompt creation; file management; MC execution; commit/push; PDF export |
| **Workspace** | `The Investor` (parent) / `geopolitical-investment-research-2026` (repo) |

---

## 3. Prompts & Instructions

### 3.1 Master Instructions

**File:** `prompts/master_instructions.md`

**Key mandates:**
- Project role: senior institutional portfolio manager / quant (20+ years geopolitical event-driven investing)
- Tone: data-driven, skeptical; favor multiple data points; no optimism/pessimism
- Audience: Wealth-Tech Operations Leader (see `persona_wealth_tech_operations.md`)
- Research: ≥12–15 high-quality sources; ≥2 independent sources per material claim
- Monte Carlo: 10,000+ paths; 6-month horizon; 3 scenario sets (A Base, B Escalation-weighted, C Sensitivity)
- Report structure: 11 sections including Investor Profile & Suitability Assessment

### 3.2 Persona

**File:** `prompts/persona_wealth_tech_operations.md`

**Profile:** Wealth-Tech Operations Leader (30+ years TAMP/platform; advisor-platform lens; data-driven; operator-investor). Used by all agents to align tone, risk framing, and operational language (e.g., Core-Satellite, repeatable processes).

### 3.3 Audit Prompts

**Files:** `prompts/claude_audit_prompt.md`, `gemini_audit_prompt.md`, `chatgpt_audit_prompt.md`

**Common focus:**
- Factual accuracy, logical gaps, MC validity
- Investor Profile / Suitability verification
- Flag claims with single-source support; require ≥2 data points

**ChatGPT add-on:** Suggest stronger 2025–2026 sources.

### 3.4 Reconciliation Prompt

**File:** `prompts/reconciliation_prompt.md`

**Mandates:** Incorporate valid feedback; resolve discrepancies; ensure Investor Profile complete; resolve single-source flags; preserve data-driven tone.

---

## 4. Data & Resources Cited

### 4.1 Primary Data Files (Repo)

| File | Content | Use |
|------|---------|-----|
| `data/latest_prices_feb28_2026.csv` | ETF closing prices as of 2026-02-27 (ITA, XAR, XLE, GLD, XLU) | Share-count calculations; allocation |
| `data/sector_historical_data.csv` | Historical OHLCV (sample from 2025) | Reference for sector data availability |

**Latest prices (from CSV):**
- XAR: $282.94
- XLE: $55.92
- GLD: $483.75
- XLU: $47.73

### 4.2 External Sources (Report Sources Verification Table)

| Claim Category | Source 1 | Source 2 | Timestamp |
|----------------|----------|----------|-----------|
| U.S.–Israel strikes & retaliation | Reuters live | AP live + CNN live | 02/28/26 |
| Oil risk premium +$4–10/bbl | IEA Oil Market Report Feb 2026 | JPMorgan Commodity Research 02/28/26 | 02/28/26 |
| WTI ~$67.02 | CME/NYMEX settlement | EIA Weekly Petroleum Status | 02/27 close |
| Defense budgets record ramp | SIPRI Military Expenditure Database 2025 | NATO Defence Expenditure Report 2025 | 2025 editions |
| XAR +17.60% YTD / 74% 1-yr | Yahoo Finance | Morningstar + SSGA factsheet | 02/27/26 |
| Gold near ATH $5,100–$5,278 | LBMA PM fix + Trading Economics | World Gold Council data | 02/27–28/26 |
| Correlation matrix | Yahoo Finance (5-yr daily) | Morningstar validation | Ending 02/27/26 |

**Additional cited sources (draft/final):** NBC, NYT, WaPo, Al Jazeera, Fortune, Goldprice.org, IISS Military Balance 2026, ETF.com, BlackRock iShares (ITA).

---

## 5. Monte Carlo Models — Exhaustive Breakdown

### 5.1 Implementation

**File:** `code/monte_carlo_simulator.py`

**Runtime:** `.\code\run_mc.ps1` (PowerShell) → invokes Python with `--paths 10000 --output reports`

**Dependencies:** numpy, pandas, matplotlib, scipy (`requirements.txt`)

### 5.2 Mathematical Specification

**Return model:**
- **Distribution:** Multivariate normal (Gaussian)
- **Horizon:** 6 months (t = 0.5 years)
- **Paths:** 10,000 per scenario
- **Scaling:** 
  - Mean: μ_6m = μ_annual × 0.5
  - Volatility: σ_6m = σ_annual × √0.5
- **Covariance:** Σ = diag(σ) × Corr × diag(σ)
- **Sampling:** `np.random.multivariate_normal(means, cov, n_sim)` with fixed seed per scenario
- **Return definition:** Simple (arithmetic) returns, not log returns
- **Portfolio return:** r_port = w' × r, where w = sector weights

**Sharpe-like ratio:**
- Formula: mean(r) / std(r) × √2
- Rationale: 6-month Sharpe scaled to approximate annualized; √2 adjustment for 6‑month horizon

### 5.3 Correlation Matrix

**Base matrix (5-year historical, defense-energy positive, gold negative to equities):**

```
         Defense  Energy  Gold  Utilities
Defense    1.00    0.45  -0.15     0.10
Energy     0.45    1.00  -0.25     0.05
Gold      -0.15   -0.25   1.00   -0.10
Utilities  0.10    0.05  -0.10     1.00
```

**Scenario C adjustment:** Defense–Energy correlation raised to 0.60; Defense–Gold to -0.25 (flight to safety).

### 5.4 Scenario Parameters

| Scenario | Label | μ (annualized) [Defense, Energy, Gold, Utilities] | σ (annualized) | Correlation | Seed |
|----------|-------|---------------------------------------------------|-----------------|-------------|------|
| **A** | Base historical | [0.18, 0.12, 0.08, 0.09] | [0.20, 0.28, 0.16, 0.12] | Base | 42 |
| **B** | Escalation-weighted | [0.28, 0.32, 0.35, 0.09] | [0.22, 0.35, 0.18, 0.12] | Base | 43 |
| **C** | Sensitivity (higher severe) | [0.32, 0.40, 0.40, 0.08] | [0.28, 0.42, 0.22, 0.14] | Adjusted | 44 |

**Probability tree alignment:**
- A: Quick de-escalation (25%) — lower means/vols
- B: Mild ongoing (45%) + Severe (30%) — weighted blend of 2026 escalation
- C: Higher severe probability — elevated means/vols; stronger defense–energy correlation

### 5.5 Portfolio Weights (Simulator)

**Implemented weights:** 40% Defense, 25% Energy, 20% Gold, 15% Utilities

*Note: The final report recommends 35/30/20/15. The MC simulator uses 40/25/20/15 from the original design. Reported MC outputs are from the simulator run; narrative in the final report references 35/30/20/15 as the recommended allocation.*

### 5.6 Output Metrics (Per Scenario)

| Metric | Definition |
|--------|------------|
| Mean Return | Average of 10,000 portfolio return paths |
| Median Return | 50th percentile |
| P(Profit) | Fraction of paths with return > 0 |
| 5% VaR | 5th percentile (tail loss) |
| Worst 1% | 1st percentile (extreme tail loss) |
| Sharpe-like | mean / std × √2 |

### 5.7 Monte Carlo Outputs (Actual Run)

**From `reports/mc_summary.csv`:**

| Metric | Scenario A | Scenario B | Scenario C |
|--------|------------|------------|------------|
| Mean Return | 6.51% | 13.64% | 15.95% |
| Median Return | 6.40% | 13.78% | 16.01% |
| P(Profit) | 76.4% | 90.5% | 88.6% |
| 5% VaR | -8.07% | -3.67% | -5.87% |
| Worst 1% | -14.34% | -10.66% | -14.70% |
| Sharpe-like | 1.02 | 1.85 | 1.70 |

### 5.8 Per-Sector Stats (Scenario B Example)

| Sector | Mean | Median | P(Profit) | 5% VaR | Worst 1% | Sharpe-like |
|--------|------|--------|-----------|--------|----------|-------------|
| Defense | 13.83% | 13.91% | 81.3% | -12.06% | -22.51% | 1.25 |
| Energy | 15.67% | 15.72% | 73.6% | -25.18% | -40.96% | 0.90 |
| Gold | 17.54% | 17.49% | 91.5% | -3.62% | -11.87% | 1.94 |
| Utilities | 4.56% | 4.66% | 70.6% | -9.65% | -14.94% | 0.76 |

### 5.9 Visual Outputs

| File | Description |
|------|-------------|
| `mc_summary.csv` | Portfolio-level metrics for A, B, C |
| `mc_portfolio_histograms.png` | Three-panel histogram (A, B, C) |
| `mc_histogram_a_base.png` | Scenario A distribution |
| `mc_histogram_b_escalation.png` | Scenario B distribution |
| `mc_histogram_c_sensitivity.png` | Scenario C distribution |
| `mc_allocation_pie.png` | Pie chart of sector weights |

### 5.10 Model Limitations (Per Audit Feedback)

- **Distribution:** Multivariate normal may understate fat tails in crisis regimes.
- **Dividends:** Treated as +0.4–0.8% total-return add-on; not explicitly in MC path generation.
- **Reproducibility:** Achieved via fixed seeds (42, 43, 44) and published parameters.

---

## 6. Audit Resolution Summary

| Auditor | Flags Raised | Resolution |
|---------|--------------|------------|
| Claude | 13 | Wikipedia removed; second sources added; MC params disclosed; exit rules separated; risk tolerance evidenced |
| Gemini | 3 | Second source for defense budgets; VaR vs mean return clarified; repeatable-process framing added |
| ChatGPT | 20+ | Sources Verification Table; full MC parameter disclosure; claim ledger items addressed |

**Confidence:** Raised from 78 (draft) to 85 (final) post-reconciliation.

---

## 7. File Inventory (Methodology-Relevant)

```
geopolitical-investment-research-2026/
├── METHODOLOGY.md                  ← This document
├── CURSOR_ORCHESTRATION.md         ← Workflow + model mapping
├── REPO_DIAGRAM.md                 ← Visual workflow
├── README.md
├── requirements.txt                ← numpy, pandas, matplotlib, scipy
├── prompts/
│   ├── master_instructions.md
│   ├── persona_wealth_tech_operations.md
│   ├── grok_prompt_v1.md
│   ├── claude_audit_prompt.md
│   ├── gemini_audit_prompt.md
│   ├── chatgpt_audit_prompt.md
│   └── reconciliation_prompt.md
├── data/
│   ├── latest_prices_feb28_2026.csv
│   └── sector_historical_data.csv
├── code/
│   ├── monte_carlo_simulator.py    ← Full MC implementation
│   ├── run_mc.ps1                  ← MC launcher
│   ├── run_simulations.sh          ← Unix MC launcher
│   ├── commit_audit_round.ps1
│   └── export_to_pdf.ps1
└── reports/
    ├── draft_grok_v1.md
    ├── audit_claude.md
    ├── audit_gemini.md
    ├── audit_chatgpt.md
    ├── final_validated_report.md
    ├── mc_summary.csv
    ├── mc_portfolio_histograms.png
    ├── mc_histogram_a_base.png
    ├── mc_histogram_b_escalation.png
    ├── mc_histogram_c_sensitivity.png
    └── mc_allocation_pie.png
```

---

## 8. Execution Environment

| Component | Version / Detail |
|-----------|------------------|
| Python | 3.12 (via winget install Python.Python.3.12) |
| numpy | ≥1.24.0 |
| pandas | ≥2.0.0 |
| matplotlib | ≥3.7.0 |
| scipy | ≥1.10.0 |
| OS | Windows 10 |
| Repo | GitHub (blake-a11y/The-Investor), branch master |

---

**Document generated:** February 28, 2026  
**Status:** Methodology documented; report v1.0 audit-complete.
