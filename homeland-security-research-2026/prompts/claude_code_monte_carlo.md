# Claude Code Prompt — Phase 4: Monte Carlo Simulation
**Agent:** Claude Code (Anthropic)
**Project:** Homeland Security Investment Research 2026
**Input:** `data/company_fundamentals/master_fundamentals.csv` + `reports/draft_threat_assessment.md`
**Output files:** `code/monte_carlo_homesec.py` + `reports/mc_summary_homesec.csv` + histogram PNGs

---

## Your Role
You are the simulation agent. Using the threat probability tree from Grok (Phase 1) and the company fundamentals from Codex (Phase 2B), run a fully parameterized Monte Carlo simulation for the homeland security portfolio.

---

## Scenario Framework

Use the probability tree from `reports/draft_threat_assessment.md`. If not yet available, use these defaults (update when Grok draft is committed):

```python
scenarios = {
    'A_minor_incident': {
        'probability': 0.40,
        'description': 'IED, cyber, infrastructure sabotage — contained response',
        'duration_months': 6,
    },
    'B_coordinated': {
        'probability': 0.35,
        'description': 'Multi-city coordinated attack — major federal response',
        'duration_months': 12,
    },
    'C_mass_casualty': {
        'probability': 0.25,
        'description': 'Mass casualty event — 9/11-scale federal mobilization',
        'duration_months': 24,
    }
}
```

---

## Sector Definitions for Simulation

```python
sectors = {
    'HomeSec_Tech':    {'weight': 0.35, 'etf_proxy': 'ITA+AXON blend'},
    'Intel_Analytics': {'weight': 0.25, 'etf_proxy': 'PLTR+BAH+LDOS blend'},
    'FirstResponder':  {'weight': 0.20, 'etf_proxy': 'MSA+PSN blend'},
    'Fed_Comms_Cyber': {'weight': 0.20, 'etf_proxy': 'LHX+CRWD blend'},
}
```

---

## Parameter Calibration

### Base Returns (μ annualized) — Calibrate from historical_event_returns.csv
```python
# Pull from Codex output: data/company_fundamentals/historical_event_returns.csv
# Use average sector return post-9/11 (T+180) as Scenario C anchor
# Use post-Soleimani (T+90) as Scenario A anchor
# Interpolate for Scenario B

# If historical data not yet available, use these conservative defaults:
mu_defaults = {
    'A': {'HomeSec_Tech': 0.06, 'Intel_Analytics': 0.08, 'FirstResponder': 0.04, 'Fed_Comms_Cyber': 0.05},
    'B': {'HomeSec_Tech': 0.15, 'Intel_Analytics': 0.18, 'FirstResponder': 0.10, 'Fed_Comms_Cyber': 0.12},
    'C': {'HomeSec_Tech': 0.28, 'Intel_Analytics': 0.32, 'FirstResponder': 0.18, 'Fed_Comms_Cyber': 0.22},
}
```

### Volatility (σ annualized)
```python
sigma = {
    'HomeSec_Tech':    0.28,
    'Intel_Analytics': 0.35,  # PLTR-heavy; higher vol
    'FirstResponder':  0.20,
    'Fed_Comms_Cyber': 0.30,
}
# Scale σ upward by 20% for Scenario C (crisis correlation compression)
```

### Correlation Matrix
```python
# Normal-regime baseline (update with actual data from Codex output)
corr_matrix = np.array([
    [1.00, 0.65, 0.45, 0.55],  # HomeSec_Tech
    [0.65, 1.00, 0.40, 0.60],  # Intel_Analytics
    [0.45, 0.40, 1.00, 0.35],  # FirstResponder
    [0.55, 0.60, 0.35, 1.00],  # Fed_Comms_Cyber
])
# Note: crisis-period correlations rise 0.10-0.20; add caveat in output
```

---

## Simulation Code Requirements

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)  # Reproducible

def run_mc(scenario_key, n_sim=10000, t=0.5):
    """
    Parameters:
    - scenario_key: 'A', 'B', or 'C'
    - n_sim: number of simulation paths
    - t: horizon in years (0.5 = 6 months; scale per scenario duration)
    
    Returns: dict with mean, median, p_profit, var_5pct, worst_1pct, sharpe
    """
    # Cholesky decomposition of correlation matrix
    # Generate correlated normal returns
    # Apply scenario weights
    # Calculate portfolio return per path
    # Output statistics

def generate_histogram(returns, scenario_key, scenario_desc):
    """Generate and save histogram PNG matching Iran report style"""
    # Right-skewed bell curve
    # Mark median with vertical line
    # Save to reports/mc_histogram_[scenario].png

def run_all_scenarios():
    """Run all three scenarios, output master summary CSV"""
    # Returns DataFrame with all stats
    # Save to reports/mc_summary_homesec.csv

# Also generate allocation pie chart
# Save to reports/mc_allocation_pie_homesec.png
```

---

## Required Outputs

1. **`code/monte_carlo_homesec.py`** — Full runnable code with all parameters
2. **`reports/mc_summary_homesec.csv`** — All scenario stats (mean, median, P(profit), VaR, worst 1%, Sharpe)
3. **`reports/mc_histogram_a_minor.png`**
4. **`reports/mc_histogram_b_coordinated.png`**
5. **`reports/mc_histogram_c_mass_casualty.png`**
6. **`reports/mc_portfolio_histograms_homesec.png`** — 3-panel overview
7. **`reports/mc_allocation_pie_homesec.png`**

---

## Documentation in Code
Every μ and σ input must have an inline comment citing its source:
```python
mu_A_homesec_tech = 0.06  # Source: avg HomeSec sector return T+90 post-Soleimani (Yahoo Finance)
```

Commit with message: `"Phase 4 complete: Monte Carlo simulation — homeland security"`
