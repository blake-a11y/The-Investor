#!/usr/bin/env python3
"""
Monte Carlo Simulator for $100k Geopolitical Investment Research (Feb 28 2026)

Runs 3 scenario sets per master instructions:
(A) Base historical
(B) Current-escalation weighted (25% quick de-escalation, 45% mild, 30% severe)
(C) Sensitivity (higher severe probability / correlation shift)

Output: mean, median, P(profit), 5% VaR, worst 1%, Sharpe-like per sector + portfolio.
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

np.random.seed(42)
n_sim = 10000
horizon = 0.5  # 6 months

sectors = ['Defense', 'Energy', 'Gold', 'Utilities']

# Base correlation matrix (5yr historical: defense-energy +, gold - to equities)
corr_base = np.array([
    [1.00, 0.45, -0.15, 0.10],
    [0.45, 1.00, -0.25, 0.05],
    [-0.15, -0.25, 1.00, -0.10],
    [0.10, 0.05, -0.10, 1.00],
])

portfolio_weights = np.array([0.40, 0.25, 0.20, 0.15])


def run_scenario(means_annual, vols_annual, corr, label, seed=42):
    """Run single scenario; return portfolio stats + per-sector returns."""
    np.random.seed(seed)
    means = means_annual * horizon
    vols = vols_annual * np.sqrt(horizon)
    cov = np.diag(vols) @ corr @ np.diag(vols)
    returns = np.random.multivariate_normal(means, cov, n_sim)
    port_returns = returns @ portfolio_weights

    # Per-sector stats
    sector_stats = {}
    for i, sec in enumerate(sectors):
        r = returns[:, i]
        sr = np.mean(r) / np.std(r) * np.sqrt(2) if np.std(r) > 0 else 0  # 6-mo Sharpe-like
        sector_stats[sec] = {
            'mean': np.mean(r), 'median': np.median(r), 'p_profit': (r > 0).mean(),
            'var_5': np.percentile(r, 5), 'worst_1': np.percentile(r, 1), 'sharpe_like': sr,
        }

    port_sr = np.mean(port_returns) / np.std(port_returns) * np.sqrt(2) if np.std(port_returns) > 0 else 0
    port_stats = {
        'Mean Return': port_returns.mean(),
        'Median Return': np.median(port_returns),
        'Prob Profit': (port_returns > 0).mean(),
        '5% VaR': np.percentile(port_returns, 5),
        'Worst 1%': np.percentile(port_returns, 1),
        'Sharpe-like': port_sr,
    }
    return port_stats, sector_stats, port_returns, returns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=None)
    parser.add_argument('--paths', type=int, default=10000)
    args = parser.parse_args()
    global n_sim
    n_sim = args.paths

    # --- Scenario A: Base historical (pre-2026 typical) ---
    means_a = np.array([0.18, 0.12, 0.08, 0.09])
    vols_a = np.array([0.20, 0.28, 0.16, 0.12])
    stats_a, sectors_a, port_a, rets_a = run_scenario(means_a, vols_a, corr_base, 'A', seed=42)

    # --- Scenario B: Escalation weighted (25% quick / 45% mild / 30% severe) ---
    # Weighted blend of parameters; 2026-adjusted premiums
    means_b = np.array([0.28, 0.32, 0.35, 0.09])  # defense 28%, energy 32%, gold 35%, util 9%
    vols_b = np.array([0.22, 0.35, 0.18, 0.12])
    stats_b, sectors_b, port_b, rets_b = run_scenario(means_b, vols_b, corr_base, 'B', seed=43)

    # --- Scenario C: Sensitivity (higher severe / correlation stress) ---
    means_c = np.array([0.32, 0.40, 0.40, 0.08])  # worse escalation
    vols_c = np.array([0.28, 0.42, 0.22, 0.14])
    corr_c = corr_base.copy()
    corr_c[0, 1] = corr_c[1, 0] = 0.60  # defense-energy correlation up
    corr_c[0, 2] = corr_c[2, 0] = -0.25  # gold flight to safety
    stats_c, sectors_c, port_c, rets_c = run_scenario(means_c, vols_c, corr_c, 'C', seed=44)

    # Print all results
    print("\n========== SCENARIO A: Base Historical ==========")
    print(pd.Series(stats_a))
    print("\n========== SCENARIO B: Current Escalation Weighted ==========")
    print(pd.Series(stats_b))
    print("\n========== SCENARIO C: Sensitivity (Higher Severe) ==========")
    print(pd.Series(stats_c))

    # Per-sector table for Scenario B (primary recommendation)
    print("\n========== Sector Stats (Scenario B) ==========")
    for sec in sectors:
        print(sec, sectors_b[sec])

    # Save combined results for report appendix
    out_dir = args.output or Path(__file__).parent.parent / "reports"
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame({
        'Scenario A': stats_a,
        'Scenario B': stats_b,
        'Scenario C': stats_c,
    })
    summary.to_csv(out_dir / "mc_summary.csv")
    print(f"\nSummary saved: {out_dir / 'mc_summary.csv'}")

    # Combined 3-panel histograms
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, port, title in zip(axes, [port_a, port_b, port_c], ['A: Base', 'B: Escalation', 'C: Sensitivity']):
        ax.hist(port * 100, bins=80, edgecolor='black', alpha=0.7)
        ax.axvline(0, color='red', linestyle='--')
        ax.set_title(f'Portfolio Return 6mo — {title}')
        ax.set_xlabel('Return (%)')
    plt.tight_layout()
    plt.savefig(out_dir / "mc_portfolio_histograms.png", dpi=150)
    plt.close()
    print(f"Histograms saved: {out_dir / 'mc_portfolio_histograms.png'}")

    # Enhanced per-scenario histograms (report-quality)
    for port_returns, scen_name in [
        (port_a, 'A_Base'),
        (port_b, 'B_Escalation'),
        (port_c, 'C_Sensitivity'),
    ]:
        port_mean = np.mean(port_returns)
        plt.figure(figsize=(10, 6))
        plt.hist(port_returns * 100, bins=60, alpha=0.75, color='navy', edgecolor='black')
        plt.axvline(port_mean * 100, color='red', linewidth=2, linestyle='--',
                    label=f'Mean: {port_mean * 100:.1f}%')
        plt.title(f'{scen_name.replace("_", " ")} — Portfolio 6-Month Return Distribution')
        plt.xlabel('Return (%)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(out_dir / f'mc_histogram_{scen_name.lower()}.png', dpi=300, bbox_inches='tight')
        plt.close()
    print(f"Per-scenario histograms saved: mc_histogram_a_base.png, mc_histogram_b_escalation.png, mc_histogram_c_sensitivity.png")

    # Allocation pie chart
    labels = ['Defense 40%', 'Energy 25%', 'Gold 20%', 'Utilities 15%']
    sizes = portfolio_weights * 100
    colors = ['#2e86ab', '#e94f37', '#ffc93c', '#6b9080']
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title('Recommended $100k Allocation (40/25/20/15)')
    plt.savefig(out_dir / "mc_allocation_pie.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Allocation pie chart saved: {out_dir / 'mc_allocation_pie.png'}")


if __name__ == "__main__":
    main()
