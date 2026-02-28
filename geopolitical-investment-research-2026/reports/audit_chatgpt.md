## ChatGPT Audit (Draft Review)

**Audited document:** `reports/draft_grok_v1.md` (dated Feb 28, 2026)  
**Audience:** Wealth-Tech Operations Leader (`prompts/persona_wealth_tech_operations.md`)  
**Audit focus:** Factual accuracy, logical gaps, and Monte Carlo (MC) validity. Mark every claim needing verification. Flag one-source support. Require ≥2 independent data points for material assertions.

### 1) Executive assessment (what to fix first)

- **High-risk factual integrity gaps (must verify before any use)**
  - **Event facts**: the described “direct U.S.–Israel joint strikes on Iran” + “immediate retaliation” are treated as settled facts but are not validated in-document with primary confirmations (official releases) and independent outlet corroboration.
  - **Market levels**: specific spot/ETF prices, “oil risk premium +$4–10/bbl,” “gold ~\$5,100–\$5,278/oz,” sector YTD numbers, and ETF AUM/ER/yield are **material** and must be verified with primary/issuer data.
  - **Historical analog returns**: claims like “Gulf +60%+ oil” or “Ukraine +60%” are presented as crisp facts without a clear methodology (window, instrument, index) and appear directionally plausible but **not audit-grade** as written.

- **High-risk methodology gaps (MC results not currently decision-grade)**
  - The MC section states “multivariate normal with correlations” but **does not disclose the volatility vector** (sigmas), the mean vector derivation (mus), the return definition (simple vs log), nor the full code (appendix is truncated). As a result, **the reported VaR / worst-1% / Sharpe-like figures are not reproducible and cannot be validated**.
  - Multiple outputs look mechanically suspicious (e.g., **mean = median exactly** in Scenario A; and the Executive Summary range repeats mean/median identically).

- **Internal consistency issues (easy to correct, but undermines trust)**
  - Executive says **“Total cost ~$99,980”** but allocation math later totals **$99,878** and also shows XAR **“$35,000 → 124 shares ($35,084; slight over)”** which contradicts “exact” $100k deployment framing.
  - The doc claims “Every material claim cross-referenced ≥2 sources,” but several items are single-source or weak-source (e.g., Wikipedia, “EIA implied,” “IISS analogs”).

### 2) Claim verification ledger (marking every material claim needing verification)

**Legend:** Priority = H (material), M (important), L (nice-to-have). “Two-point rule” = ≥2 independent data points (e.g., issuer factsheet + SEC filing; or Reuters + AP; or EIA + ICE settlement).

#### 2.1 Event + geopolitical facts (all Priority H)

- **Claim**: “Direct U.S.–Israel joint strikes on Iranian nuclear, missile, and leadership targets (Feb 28, 2026).”
  - **Why verify**: foundation for the entire thesis.
  - **Two-point rule**: (1) official statement(s) (U.S. DoD/CENTCOM; Israel MoD/IDF) + (2) at least two independent wire/services (Reuters + AP recommended).
  - **Stronger 2025–2026 sources**: Reuters/AP dispatches + official press releases; UN Security Council statements if convened; IAEA statements if nuclear sites involved.

- **Claim**: “Immediate Iranian retaliation against U.S. bases and regional targets.”
  - **Verify**: official host nation / U.S. military confirmation + at least one independent outlet + geolocated evidence where possible.

- **Claim**: “Trump statements: regime-change rhetoric.”
  - **Verify**: primary transcript/video + an established outlet transcript.

- **Claim**: “Targets: Tehran/Isfahan leadership compounds; nuclear/missile sites.”
  - **Verify**: satellite imagery providers + official statements; avoid Wikipedia as a primary citation.

#### 2.2 Market levels + price claims (Priority H unless noted)

- **Claim**: “Oil risk premium estimated +$4–10/bbl.”
  - **Verify**: define method (e.g., implied from Brent/WTI options skew, or forward-curve shift vs counterfactual). Must cite method.
  - **Two-point rule**: ICE/CME options or futures data + independent analyst note (IEA/OPEC/major bank commodity desk).

- **Claim**: “WTI ~$67.02 (+2.78% Feb 27 close).”
  - **Verify**: CME/NYMEX settlement (or EIA price table) + a second market data source (Refinitiv/Bloomberg or exchange settlement summary).

- **Claim**: “Gold near all-time highs (~$5,100–$5,278/oz).”
  - **Verify**: LBMA PM fix/spot + World Gold Council dataset; specify whether USD/oz spot, futures, or local currency.

- **Claim**: “Defense sector already +13–18% YTD on record global budgets.”
  - **Verify**: define “defense sector” (index or ETF). Use index provider or ETF issuer YTD total return.
  - **Budget linkage**: separate “record budgets” (macro fact) from “sector +% YTD” (market fact); each needs its own verification.

#### 2.3 Portfolio construction + trade math (Priority H)

- **Claim**: Allocation is “$100,000 exact” and “Total cost ~$99,980 … remainder cash.”
  - **Verify**: reconcile share rounding and totals; if “exact” is not possible with whole shares, state “target weights” and show cash residual explicitly.

- **Claim**: Share counts and prices (XAR 124 @ ~$282.94; XLE 536 @ ~$55.92; GLD 41 @ ~$483.75; XLU 314 @ ~$47.73).
  - **Verify**: price timestamps (close vs pre-open), and whether totals align with weights; use the same timestamp for all instruments.

- **Claim**: “Buy at next open or limit orders …”
  - **Audit note (M)**: execution guidance should include spreads, limit logic, and a contingency for gap risk; otherwise it reads like advice without operational guardrails.

#### 2.4 MC setup + outputs (Priority H)

- **Claim**: “Monte Carlo, 10k paths per scenario…”
  - **Verify**: the code is incomplete in the appendix; you must include full runnable code or store it in-repo and reference the path.

- **Claim**: “6-month horizon, multivariate normal with correlations.”
  - **Audit**: normal returns understate tail risk for event-driven commodities/defense; at minimum, justify or switch to fat-tailed / regime-switching / bootstrapped returns.

- **Claim**: “Portfolio Expected 6-Month Statistics … Mean 5.7–7.9%, P(Profit) 73–76%, 5% VaR –8.4 to –10.4, Worst 1% –15.8 to –18.5.”
  - **Verify**: cannot validate without (a) mus/sigmas per sector, (b) correlation derivation window, (c) whether returns include dividends, (d) whether results are simple vs log returns.
  - **Red flags**: mean = median exactly (Scenario A) suggests rounding artifacts or a calculation/reporting error.

- **Claim**: “Scenario A/B/C” and “weighted 40/25/20/15 base adjusted to recommended.”
  - **Audit**: unclear. State one set of recommended weights; define scenarios as parameter sets (mus/sigmas/corr) or regimes.

#### 2.5 Correlation matrix + “5-year” claims (Priority H)

- **Claim**: “5-Year Sector Correlation Matrix (approximate, derived from historical ETF data).”
  - **Verify**: specify window, frequency, return type, and source; provide a reproducible script.
  - **Two-point rule**: computed from raw prices + sanity check vs a second provider (Bloomberg/Refinitiv/Morningstar).

#### 2.6 Historical analog performance claims (Priority H)

- **Claim**: “Gulf War +15–25% defense 6m; oil +60%+; gold +5–10%.”
  - **Verify**: define proxy and exact start/end; results vary widely by chosen instrument.
  - **Two-point rule**: primary price series + a reputable historical market note (index provider/academic).

#### 2.7 ETF facts (Priority M/H depending on use)

- **Claim**: AUM, expense ratios, yields, 1-yr returns for XAR/ITA/XLE/GLD/XLU.
  - **Verify**: issuer factsheets + SEC filings for ER; ensure returns are **total return** vs price return.

#### 2.8 Risk rules + stress tests (Priority H)

- **Claim**: “Stop/Exit: full exit if de-escalation confirmed and portfolio +15% … or if oil < $60 sustained.”
  - **Audit**: “de-escalation confirmed” and “sustained” are undefined; must operationalize (sources + number of closes + instrument).
  - **Verify**: backtest or scenario-test triggers; otherwise arbitrary.

- **Claim**: Stress test outcomes (“Oil disruption 30 days: +4–6% portfolio… 180 days: +15%+”).
  - **Verify**: material performance claims require explicit mechanics/inputs; currently unsubstantiated.

### 3) One-source / weak-source flags (must be corrected)

- **Wikipedia as event source (H)**: acceptable only as a pointer, not corroboration.
- **“EIA implied” / “IISS Military Balance 2026 analogs” (H)**: needs explicit citations (table/page) or replace with direct references.
- **“Every material claim cross-referenced ≥2 sources” (H)**: not satisfied as written; either supply the second independent point per claim or remove the assertion.

### 4) Monte Carlo validity review (what’s missing / what to change)

#### 4.1 Reproducibility requirements (non-negotiable for ops-grade use)

- Provide **full code** (not truncated) or store it in-repo and reference the exact path and run command.
- Disclose:
  - **mu vector** per sector (and derivation)
  - **sigma vector** per sector (and derivation)
  - **return definition** (log vs simple), and whether distributions/dividends are included
  - **time scaling** assumptions (daily → 6 months)
  - **scenario definitions** (what changes between A/B/C and why)

#### 4.2 Model-form risk (normality + event risk)

- Multivariate normal returns are typically **anti-conservative** in conflict-driven regimes (fat tails, jumps, skew, clustering).
- Minimum upgrade options (pick one and justify):
  - **Bootstrapped historical returns** with block bootstrap
  - **Student‑t innovations** (fat tails)
  - **Regime mixture** (calm vs crisis) with explicit regime probabilities
  - **Jump component** for oil/gold around escalation

#### 4.3 Output sanity checks to add

- Report **standard deviation**, **expected shortfall (CVaR)**, and **max drawdown distribution**.
- Add an **inputs/outputs tear sheet** per scenario (one-page, audit-friendly).

### 5) Investor Profile / Suitability audit (evidence gaps)

- **Risk tolerance “7/10” (H)**: not evidenced. Replace with a short explicit drawdown tolerance statement tied to validated tail loss, plus operational constraints (liquidity, governance, rebal cadence).
- **Time horizon “6 months primary with 2–3 year tail” (M/H)**: define what “tail suitability” means (hold vs rotate) and add decision gates.
- **Behavioral factor “requires 2+ sources per claim (met)” (H)**: remove or make true via a citations/verification table.

### 6) Stronger 2025–2026 source upgrades (recommended)

Use these as “second points” (or replacements for weak sources):

- **Defense spending / budgets**
  - SIPRI Yearbook 2025 (`https://www.sipri.org/yearbook/2025`)
  - NATO defence expenditure reports through 2025 (`https://www.nato.int/` finance/defence expenditure PDFs)

- **Oil prices / inventories / term structure**
  - EIA Weekly Petroleum Status Report (`https://www.eia.gov/petroleum/supply/weekly/`)
  - ICE/CME settlement + curve snapshots (front/back spreads)

- **Gold price + demand**
  - World Gold Council datasets (`https://www.gold.org/goldhub/data`)
  - LBMA price references (PM fix/spot)

- **Event confirmation**
  - Official releases (U.S. DoD/CENTCOM; Israel IDF/MoD) + Reuters + AP (minimum)

### 7) Recommended edits to the Grok draft (tight, ops-friendly)

- Add a **“Sources & verification table”** mapping each material claim → 2 independent sources → timestamp.
- Replace “Confidence: 78” with a defined rubric (data completeness, model validation, execution feasibility).
- Reframe “exact $100,000” as **target weights** with explicit cash residual (or state fractional-share assumption).
- Make all triggers operational:
  - define “de-escalation confirmed”
  - define “oil < $60 sustained” (e.g., N consecutive settles on front-month)
  - define VaR monitoring inputs + recalculation cadence

### 8) Audit conclusion

The draft has a solid operator-friendly structure, but it is **not audit-grade yet** because key factual claims and the MC methodology are not currently reproducible or properly sourced. Once the verification ledger is satisfied and MC inputs/code are fully disclosed and validated, the recommendation can be revisited with higher confidence.
