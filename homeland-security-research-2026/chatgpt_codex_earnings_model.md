# ChatGPT 5.3 Codex Prompt — Phase 2B: Earnings Model Automation
**Agent:** ChatGPT 5.3 Codex (OpenAI)
**Project:** Homeland Security Investment Research 2026
**Output files:** `code/earnings_model.py` + `data/company_fundamentals/`

---

## Your Role
You are the quantitative modeling agent. Your job is to build a reusable earnings impact model that quantifies how a domestic security event translates into revenue and EPS changes for each company in the homeland security universe. This is the earnings-based layer that differentiates this report from the pure event-driven Iran analysis.

---

## Task 1 — Build the Earnings Model Script

Create `code/earnings_model.py` — a fully runnable Python script that:

### Input Data Structure
```python
companies = {
    'AXON': {
        'ticker': 'AXON',
        'federal_rev_pct': 0.XX,      # Pull from 10-K
        'total_revenue_ttm': XX,       # $M TTM
        'contract_backlog': XX,        # $M disclosed backlog
        'gross_margin': 0.XX,
        'fcf_margin': 0.XX,
        'ev_ebitda_current': XX,
        'ev_ebitda_5yr_avg': XX,
    },
    # Repeat for: MSI, PLTR, LDOS, BAH, SAIC, MSA, PSN, LHX, CRWD, PANW
}

scenario_revenue_impacts = {
    'A_minor':          {'surge_pct': 0.08, 'duration_months': 6},
    'B_coordinated':    {'surge_pct': 0.22, 'duration_months': 12},
    'C_mass_casualty':  {'surge_pct': 0.55, 'duration_months': 24},
}
```

### Model Logic
```python
def calculate_event_impact(company, scenario):
    """
    For each company and scenario:
    1. Apply surge_pct to federal_revenue only (not commercial)
    2. Hold margins constant (conservative) 
    3. Calculate incremental EBITDA
    4. Apply sector P/E multiple to get implied stock impact
    5. Layer onto current price for price target
    """
    federal_rev = company['total_revenue_ttm'] * company['federal_rev_pct']
    incremental_rev = federal_rev * scenario['surge_pct'] * (scenario['duration_months'] / 12)
    incremental_ebitda = incremental_rev * company['gross_margin']
    # Apply EV/EBITDA multiple to incremental EBITDA
    # Back into per-share impact
```

### Outputs per company per scenario:
- Incremental revenue ($M)
- Incremental EBITDA ($M)
- Implied EPS impact
- Implied stock price target
- % upside from current price
- Backlog coverage ratio (backlog / annual revenue)

---

## Task 2 — Pull Fundamental Data

For each company, pull from these **free public sources**:

**SEC EDGAR (edgar.sec.gov):**
```
https://efts.sec.gov/LATEST/search-index?q=%22[TICKER]%22&dateRange=custom&startdt=2024-01-01&forms=10-K
```
From most recent 10-K extract:
- Total revenue (TTM)
- Government/federal revenue segment or %
- Contract backlog (often in MD&A section)
- Gross margin
- Operating margin
- FCF

**Macrotrends.net (free historical data):**
- 5-year revenue CAGR
- Historical P/E and EV/EBITDA

**Save each company to:** `data/company_fundamentals/[TICKER]_fundamentals.json`

---

## Task 3 — Post-Event Historical Analysis

For each Tier 1 company that existed during these events, calculate actual stock performance:

```python
historical_events = {
    '9_11_2001': {
        'date': '2001-09-11',
        'window_30d':  None,  # % return T to T+30
        'window_90d':  None,  # % return T to T+90
        'window_180d': None,  # % return T to T+180
    },
    'boston_marathon_2013': {'date': '2013-04-15'},
    'post_soleimani_2020':  {'date': '2020-01-03'},
}
# Use Yahoo Finance API (yfinance) for historical prices
# pip install yfinance
```

Output a comparison table: each company × each event × 30/90/180d return.
Save to `data/company_fundamentals/historical_event_returns.csv`

---

## Task 4 — Relative Valuation Table

Build a valuation comparison table:

| Ticker | Current EV/EBITDA | 5yr Avg EV/EBITDA | Premium/Discount | P/E Current | FCF Yield | Backlog (months) |
|--------|-------------------|-------------------|------------------|-------------|-----------|------------------|

Flag any company trading at >20% discount to 5yr average as potential value entry.

---

## Coding Standards
- Use pandas, numpy, yfinance, requests
- All data pulls must include timestamp and source URL in output
- Handle API failures gracefully (try/except with fallback to cached data)
- Output a master `data/company_fundamentals/master_fundamentals.csv` with all companies
- Include a `README` in `data/company_fundamentals/` explaining each file

---

## Output Format
`data/company_fundamentals/` — all JSON + CSV files
`code/earnings_model.py` — fully runnable, documented

Commit with message: `"Phase 2B complete: Earnings model and fundamentals data"`
