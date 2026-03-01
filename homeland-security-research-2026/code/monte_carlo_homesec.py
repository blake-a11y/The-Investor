#!/usr/bin/env python3
"""
Monte Carlo Simulator — Homeland Security Investment Research (Phase 4)
Agent: Claude Code | Date: 2026-03-01
10,000 paths | 3 domestic scenarios (A/B/C) | 4 sectors | Full risk metrics
Output: reports/mc_summary_homesec.csv + histogram PNGs + allocation pie
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

np.random.seed(42)  # Reproducible

ROOT = Path(__file__).parent.parent
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = ROOT / "data"

# ---------------------------------------------------------------------------
# Scenario Framework
# Source: Grok Phase 1 threat probability tree (draft_threat_assessment.md)
# ---------------------------------------------------------------------------

SCENARIOS = {
    "A_minor_incident": {
        "key": "A",
        "probability": 0.40,
        "description": "IED, cyber, infrastructure sabotage — contained response",
        "duration_months": 6,
        "t_years": 0.5,
    },
    "B_coordinated": {
        "key": "B",
        "probability": 0.35,
        "description": "Multi-city coordinated attack — major federal response",
        "duration_months": 12,
        "t_years": 1.0,
    },
    "C_mass_casualty": {
        "key": "C",
        "probability": 0.25,
        "description": "Mass casualty event — 9/11-scale federal mobilization",
        "duration_months": 24,
        "t_years": 2.0,
    },
}

# ---------------------------------------------------------------------------
# Sector Definitions & Portfolio Weights
# ---------------------------------------------------------------------------

SECTORS = ["HomeSec_Tech", "Intel_Analytics", "FirstResponder", "Fed_Comms_Cyber"]
SECTOR_LABELS = {
    "HomeSec_Tech":    "Homeland Security Tech\n(AXON + ITA blend)",
    "Intel_Analytics": "Intelligence & Analytics\n(PLTR + BAH + LDOS)",
    "FirstResponder":  "First Responder\n(MSA + PSN blend)",
    "Fed_Comms_Cyber": "Fed Comms & Cyber\n(LHX + CRWD blend)",
}
WEIGHTS = np.array([0.35, 0.25, 0.20, 0.20])  # Must sum to 1.0

# ---------------------------------------------------------------------------
# Return Parameters (mu annualized) — loaded from historical_event_returns.csv
# Calibration rules:
#   Scenario A: Soleimani T+30 sector averages (minor geopolitical event; pre-COVID window)
#               NOTE: Soleimani T+90 / T+180 are COVID-contaminated (March 2020 crash falls
#               within those windows); T+30 (ending ~Feb 3 2020) is clean.
#   Scenario C: 9/11 T+90 for HomeSec_Tech (AXON+MSI both public post-9/11)
#               9/11 T+180 for FirstResponder/Fed_Comms_Cyber (delayed procurement cycle)
#               BM 2013 T+90 * empirical severity scale for Intel_Analytics (BAH/LDOS
#               were not publicly traded in Sep 2001)
#   Scenario B: arithmetic mean of A and C, bounded [0.05, 0.25]
#   Floors/caps: A=[0.03, 0.15], B=[0.05, 0.25], C=[0.05, 0.35]
# Source file: data/company_fundamentals/historical_event_returns.csv
# ---------------------------------------------------------------------------

def load_historical_mu(csv_path: Path) -> dict:
    """
    Derive annualized mu parameters from historical_event_returns.csv.

    Returns dict: {"A": {sector: mu}, "B": {...}, "C": {...}}
    Falls back to conservative defaults if CSV is missing or malformed.
    """
    FALLBACK = {
        "A": {"HomeSec_Tech": 0.060, "Intel_Analytics": 0.055, "FirstResponder": 0.030, "Fed_Comms_Cyber": 0.060},
        "B": {"HomeSec_Tech": 0.168, "Intel_Analytics": 0.203, "FirstResponder": 0.071, "Fed_Comms_Cyber": 0.149},
        "C": {"HomeSec_Tech": 0.275, "Intel_Analytics": 0.350, "FirstResponder": 0.112, "Fed_Comms_Cyber": 0.214},
    }
    if not csv_path.exists():
        print(f"  [WARN] historical_event_returns.csv not found at {csv_path}; using fallback defaults")
        return FALLBACK

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        print(f"  [WARN] Could not read CSV ({exc}); using fallback defaults")
        return FALLBACK

    def ticker_val(ticker, event, window):
        row = df[(df["ticker"] == ticker) & (df["event"] == event)]
        if row.empty:
            return None
        v = row[window].values[0]
        return float(v) / 100.0 if pd.notna(v) else None

    def sector_mean(tickers, event, window):
        vals = [ticker_val(t, event, window) for t in tickers]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if vals else None

    def bounded(v, lo, hi, fallback):
        return max(lo, min(float(v), hi)) if v is not None else fallback

    # -- Scenario A: Soleimani T+30 (clean pre-COVID window) --
    # HomeSec_Tech: AXON T+30=+4.95%, MSI T+30=+7.09% -> avg +6.02%
    mu_a_ht = sector_mean(["AXON", "MSI"], "post_soleimani_2020", "window_30d")
    # Intel_Analytics: BAH T+30=+8.09%, LDOS T+30=+3.00% -> avg +5.54%
    mu_a_ia = sector_mean(["BAH", "LDOS"], "post_soleimani_2020", "window_30d")
    # FirstResponder: MSA T+30=+7.05%, PSN T+30=-5.08% -> avg +0.99% (floor applied)
    mu_a_fr = sector_mean(["MSA", "PSN"], "post_soleimani_2020", "window_30d")
    # Fed_Comms_Cyber: LHX T+30=+4.95%, CRWD T+30=+20.36% (Iran cyber fears), PANW T+30=-0.36%
    mu_a_fc = sector_mean(["LHX", "CRWD", "PANW"], "post_soleimani_2020", "window_30d")

    # -- Scenario C: 9/11 anchors (different windows by sector) --
    # HomeSec_Tech: AXON T+90=+42.38%, MSI T+90=+12.65% -> avg +27.52%
    mu_c_ht = sector_mean(["AXON", "MSI"], "9_11_2001", "window_90d")
    # FirstResponder: MSA T+180=+11.19% (T+90=+3.09% understates delayed procurement surge)
    mu_c_fr = sector_mean(["MSA"], "9_11_2001", "window_180d")
    # Fed_Comms_Cyber: LHX T+180=+21.43% (L-3 Comms full demand surge; CRWD/PANW pre-IPO in 2001)
    mu_c_fc = sector_mean(["LHX"], "9_11_2001", "window_180d")
    # Intel_Analytics: BAH/LDOS pre-IPO in 2001; proxy via Boston Marathon T+90 x severity scale
    ht_911  = sector_mean(["AXON", "MSI"], "9_11_2001", "window_90d")
    ht_bm   = sector_mean(["AXON", "MSI"], "boston_marathon_2013", "window_90d")
    sev_scale = (ht_911 / ht_bm) if (ht_bm and abs(ht_bm) > 0.01) else 3.0
    ia_bm   = sector_mean(["BAH", "LDOS"], "boston_marathon_2013", "window_90d")
    mu_c_ia_raw = (ia_bm * sev_scale) if ia_bm is not None else None

    # Apply floors / caps
    a_ht = bounded(mu_a_ht, 0.030, 0.150, FALLBACK["A"]["HomeSec_Tech"])
    a_ia = bounded(mu_a_ia, 0.030, 0.150, FALLBACK["A"]["Intel_Analytics"])
    a_fr = bounded(mu_a_fr, 0.030, 0.150, FALLBACK["A"]["FirstResponder"])
    a_fc = bounded(mu_a_fc, 0.030, 0.150, FALLBACK["A"]["Fed_Comms_Cyber"])

    c_ht = bounded(mu_c_ht,      0.050, 0.350, FALLBACK["C"]["HomeSec_Tech"])
    c_ia = bounded(mu_c_ia_raw,  0.050, 0.350, FALLBACK["C"]["Intel_Analytics"])
    c_fr = bounded(mu_c_fr,      0.050, 0.350, FALLBACK["C"]["FirstResponder"])
    c_fc = bounded(mu_c_fc,      0.050, 0.350, FALLBACK["C"]["Fed_Comms_Cyber"])

    b_ht = bounded((a_ht + c_ht) / 2, 0.050, 0.250, FALLBACK["B"]["HomeSec_Tech"])
    b_ia = bounded((a_ia + c_ia) / 2, 0.050, 0.250, FALLBACK["B"]["Intel_Analytics"])
    b_fr = bounded((a_fr + c_fr) / 2, 0.050, 0.250, FALLBACK["B"]["FirstResponder"])
    b_fc = bounded((a_fc + c_fc) / 2, 0.050, 0.250, FALLBACK["B"]["Fed_Comms_Cyber"])

    mu_out = {
        "A": {
            "HomeSec_Tech":    round(a_ht, 4),  # source: AXON+MSI Soleimani T+30 avg
            "Intel_Analytics": round(a_ia, 4),  # source: BAH+LDOS Soleimani T+30 avg
            "FirstResponder":  round(a_fr, 4),  # source: MSA+PSN Soleimani T+30 avg (floor applied)
            "Fed_Comms_Cyber": round(a_fc, 4),  # source: LHX+CRWD+PANW Soleimani T+30 avg
        },
        "B": {
            "HomeSec_Tech":    round(b_ht, 4),  # source: interpolated A+C mean
            "Intel_Analytics": round(b_ia, 4),  # source: interpolated A+C mean
            "FirstResponder":  round(b_fr, 4),  # source: interpolated A+C mean
            "Fed_Comms_Cyber": round(b_fc, 4),  # source: interpolated A+C mean
        },
        "C": {
            "HomeSec_Tech":    round(c_ht, 4),  # source: AXON+MSI 9/11 T+90 avg
            "Intel_Analytics": round(c_ia, 4),  # source: BAH+LDOS BM T+90 x severity_scale (capped at 0.35)
            "FirstResponder":  round(c_fr, 4),  # source: MSA 9/11 T+180 (delayed procurement cycle)
            "Fed_Comms_Cyber": round(c_fc, 4),  # source: LHX 9/11 T+180 (L-3 Comms full demand surge)
        },
    }

    print(f"\n[MC] mu parameters calibrated from historical_event_returns.csv")
    print(f"     Empirical 9/11-vs-BM severity scale: {sev_scale:.2f}x")
    for scen in ["A", "B", "C"]:
        vals = " | ".join(f"{s}={mu_out[scen][s]:.4f}" for s in SECTORS)
        print(f"     Scenario {scen}: {vals}")
    return mu_out


MU = load_historical_mu(DATA_DIR / "company_fundamentals" / "historical_event_returns.csv")

# ---------------------------------------------------------------------------
# Volatility (σ annualized)
# Source: 5-year realized volatility from Yahoo Finance (2019–2024)
# Note: Scenario C applies 20% upward scalar (crisis correlation compression)
# ---------------------------------------------------------------------------

SIGMA_BASE = {
    "HomeSec_Tech":    0.28,  # Source: AXON 5yr realized vol; Yahoo Finance
    "Intel_Analytics": 0.35,  # Source: PLTR-heavy; higher vol; Yahoo Finance
    "FirstResponder":  0.20,  # Source: MSA/PSN blended 5yr vol; Yahoo Finance
    "Fed_Comms_Cyber": 0.30,  # Source: LHX + CRWD blended 5yr vol; Yahoo Finance
}

CRISIS_VOL_SCALAR = 1.20  # 20% upward vol adjustment for Scenario C crisis regime

# ---------------------------------------------------------------------------
# Correlation Matrix (Normal Regime)
# Source: 5-year rolling correlations from Yahoo Finance blended proxies (2019–2024)
# Note: Crisis-period correlations rise 0.10–0.20 (documented in report caveat)
# ---------------------------------------------------------------------------

CORR_MATRIX = np.array([
    [1.00, 0.65, 0.45, 0.55],   # HomeSec_Tech
    [0.65, 1.00, 0.40, 0.60],   # Intel_Analytics
    [0.45, 0.40, 1.00, 0.35],   # FirstResponder
    [0.55, 0.60, 0.35, 1.00],   # Fed_Comms_Cyber
])

N_SIM = 10_000
STYLE = {
    "A": {"color": "#2196F3", "label": "Scenario A — Minor Incident"},
    "B": {"color": "#FF9800", "label": "Scenario B — Coordinated Attack"},
    "C": {"color": "#F44336", "label": "Scenario C — Mass Casualty (9/11 Analog)"},
}


# ---------------------------------------------------------------------------
# Core Simulation
# ---------------------------------------------------------------------------

def build_cholesky(corr: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """Covariance matrix → Cholesky decomposition."""
    cov = np.diag(sigma) @ corr @ np.diag(sigma)
    return np.linalg.cholesky(cov)


def run_mc(scenario_key: str, n_sim: int = N_SIM) -> dict:
    """
    Run Monte Carlo simulation for a single scenario.

    Returns dict with: mean, median, std, p_profit, var_5pct, worst_1pct, sharpe,
                       returns array (for histogram)
    """
    s = SCENARIOS[scenario_key]
    key = s["key"]
    t = s["t_years"]
    mu_vec = np.array([MU[key][sec] for sec in SECTORS])
    sigma_vec = np.array([SIGMA_BASE[sec] for sec in SECTORS])

    # Apply crisis vol scalar for Scenario C
    if key == "C":
        sigma_vec = sigma_vec * CRISIS_VOL_SCALAR

    # Cholesky decomposition
    L = build_cholesky(CORR_MATRIX, sigma_vec)

    # Generate correlated standard normals: shape (n_sim, n_sectors)
    Z = np.random.standard_normal((n_sim, len(SECTORS)))
    corr_Z = Z @ L.T  # Correlated shocks

    # GBM log-return per sector per path
    # ln(S_t/S_0) ~ N((μ - σ²/2)t, σ²t)
    drift = (mu_vec - 0.5 * sigma_vec**2) * t
    diffusion = corr_Z * np.sqrt(t)
    sector_log_returns = drift + diffusion          # shape (n_sim, n_sectors)
    sector_returns = np.exp(sector_log_returns) - 1  # Simple return

    # Portfolio return (weighted)
    portfolio_returns = sector_returns @ WEIGHTS     # shape (n_sim,)

    # Risk metrics
    mean_r = np.mean(portfolio_returns)
    median_r = np.median(portfolio_returns)
    std_r = np.std(portfolio_returns)
    p_profit = np.mean(portfolio_returns > 0)
    var_5pct = np.percentile(portfolio_returns, 5)   # 5% VaR (loss threshold)
    worst_1pct = np.percentile(portfolio_returns, 1)
    sharpe = mean_r / std_r if std_r > 0 else 0.0

    return {
        "scenario": scenario_key,
        "scenario_key": key,
        "probability": s["probability"],
        "duration_months": s["duration_months"],
        "description": s["description"],
        "mean": mean_r,
        "median": median_r,
        "std": std_r,
        "p_profit": p_profit,
        "var_5pct": var_5pct,
        "worst_1pct": worst_1pct,
        "sharpe": sharpe,
        "returns": portfolio_returns,
    }


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def generate_histogram(result: dict, save_path: Path):
    """Generate and save individual scenario histogram."""
    returns = result["returns"]
    key = result["scenario_key"]
    color = STYLE[key]["color"]
    label = STYLE[key]["label"]
    median_r = result["median"]
    var_5pct = result["var_5pct"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(returns, bins=80, color=color, alpha=0.75, edgecolor="white", linewidth=0.3)

    ax.axvline(median_r, color="black", linewidth=2, linestyle="--",
               label=f"Median: {median_r*100:.1f}%")
    ax.axvline(var_5pct, color="darkred", linewidth=1.5, linestyle=":",
               label=f"5% VaR: {var_5pct*100:.1f}%")

    ax.set_title(f"{label}\n{result['description']}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Portfolio Return", fontsize=11)
    ax.set_ylabel("Frequency (paths)", fontsize=11)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x*100:.0f}%"))
    ax.legend(fontsize=10)

    stats_text = (
        f"n = {N_SIM:,} paths | t = {result['duration_months']} months\n"
        f"Mean: {result['mean']*100:.1f}%  |  σ: {result['std']*100:.1f}%\n"
        f"P(profit): {result['p_profit']*100:.0f}%  |  Sharpe: {result['sharpe']:.2f}\n"
        f"Worst 1%: {result['worst_1pct']*100:.1f}%"
    )
    ax.text(0.97, 0.95, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment="top", horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {save_path.name}")


def generate_three_panel(results: list[dict], save_path: Path):
    """3-panel overview histogram (matching Iran report style)."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(
        "Homeland Security Portfolio — Monte Carlo Simulation (10,000 Paths)",
        fontsize=14, fontweight="bold", y=1.02
    )

    for ax, result in zip(axes, results):
        key = result["scenario_key"]
        color = STYLE[key]["color"]
        returns = result["returns"]

        ax.hist(returns, bins=60, color=color, alpha=0.75, edgecolor="white", linewidth=0.2)
        ax.axvline(result["median"], color="black", linewidth=1.8, linestyle="--",
                   label=f"Median: {result['median']*100:.1f}%")
        ax.axvline(result["var_5pct"], color="darkred", linewidth=1.2, linestyle=":",
                   label=f"VaR 5%: {result['var_5pct']*100:.1f}%")

        ax.set_title(f"Scenario {key} — {result['duration_months']}mo", fontsize=11, fontweight="bold")
        ax.set_xlabel("Portfolio Return", fontsize=9)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x*100:.0f}%"))
        ax.legend(fontsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        stats = (
            f"P(profit): {result['p_profit']*100:.0f}%\n"
            f"Sharpe: {result['sharpe']:.2f}"
        )
        ax.text(0.96, 0.95, stats, transform=ax.transAxes, fontsize=8,
                va="top", ha="right", bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {save_path.name}")


def generate_allocation_pie(save_path: Path):
    """Sector allocation pie chart."""
    colors = ["#1565C0", "#283593", "#0288D1", "#0097A7"]
    labels = [SECTOR_LABELS[s] for s in SECTORS]
    explode = [0.02] * len(SECTORS)

    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        WEIGHTS, labels=labels, autopct="%1.0f%%",
        colors=colors, explode=explode, startangle=140,
        textprops={"fontsize": 10}, pctdistance=0.82,
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
        at.set_fontsize(11)

    ax.set_title(
        "Homeland Security Portfolio — Sector Allocation",
        fontsize=13, fontweight="bold", pad=20
    )

    # Ticker legend
    ticker_note = (
        "HomeSec Tech: AXON, MSI, ITA\n"
        "Intel & Analytics: PLTR, BAH, LDOS\n"
        "First Responder: MSA, PSN\n"
        "Fed Comms & Cyber: LHX, CRWD, PANW"
    )
    ax.text(-1.6, -1.3, ticker_note, fontsize=8.5, color="gray",
            verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="#f5f5f5", alpha=0.6))

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {save_path.name}")


# ---------------------------------------------------------------------------
# Summary CSV
# ---------------------------------------------------------------------------

def save_summary_csv(results: list[dict], weighted_mean: float, save_path: Path):
    rows = []
    for r in results:
        rows.append({
            "scenario":          r["scenario"],
            "probability":       r["probability"],
            "duration_months":   r["duration_months"],
            "mean_return":       round(r["mean"], 4),
            "median_return":     round(r["median"], 4),
            "std":               round(r["std"], 4),
            "p_profit":          round(r["p_profit"], 4),
            "var_5pct":          round(r["var_5pct"], 4),
            "worst_1pct":        round(r["worst_1pct"], 4),
            "sharpe":            round(r["sharpe"], 4),
            "description":       r["description"],
        })

    df = pd.DataFrame(rows)
    df.to_csv(save_path, index=False)
    print(f"  Saved → {save_path.name}")
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_all_scenarios() -> tuple[list[dict], float]:
    print("\n[Simulation] Running 10,000-path Monte Carlo across 3 scenarios...")
    scenario_order = ["A_minor_incident", "B_coordinated", "C_mass_casualty"]
    results = []
    for name in scenario_order:
        key = SCENARIOS[name]["key"]
        print(f"  Scenario {key}: {SCENARIOS[name]['description']}")
        r = run_mc(name)
        results.append(r)
        print(f"    Mean: {r['mean']*100:.1f}%  |  Median: {r['median']*100:.1f}%  "
              f"|  P(profit): {r['p_profit']*100:.0f}%  |  Sharpe: {r['sharpe']:.2f}")

    # Probability-weighted expected return
    weighted_mean = sum(r["probability"] * r["mean"] for r in results)
    print(f"\n  Probability-weighted expected return: {weighted_mean*100:.2f}%")
    return results, weighted_mean


def main():
    print("=" * 60)
    print("Phase 4: Monte Carlo Simulation — Homeland Security 2026")
    print("=" * 60)

    results, weighted_mean = run_all_scenarios()

    print("\n[Charts] Generating histograms and allocation chart...")
    scenario_filenames = {
        "A_minor_incident": "mc_histogram_a_minor.png",
        "B_coordinated":    "mc_histogram_b_coordinated.png",
        "C_mass_casualty":  "mc_histogram_c_mass_casualty.png",
    }
    for r in results:
        fname = scenario_filenames[r["scenario"]]
        generate_histogram(r, REPORTS_DIR / fname)

    generate_three_panel(results, REPORTS_DIR / "mc_portfolio_histograms_homesec.png")
    generate_allocation_pie(REPORTS_DIR / "mc_allocation_pie_homesec.png")

    print("\n[CSV] Saving summary statistics...")
    df = save_summary_csv(results, weighted_mean, REPORTS_DIR / "mc_summary_homesec.csv")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(df[["scenario", "probability", "duration_months", "mean_return",
              "p_profit", "var_5pct", "sharpe"]].to_string(index=False))
    print(f"\nProbability-weighted expected return: {weighted_mean*100:.2f}%")
    print("\n✓ Phase 4 complete")
    print(f"  Reports: {REPORTS_DIR}")


if __name__ == "__main__":
    main()
