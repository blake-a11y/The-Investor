#!/usr/bin/env python3
"""
Monte Carlo Simulator for Geopolitical Investment Research

Simulates portfolio/sector returns under various geopolitical scenarios.
Uses historical data to estimate volatility and run thousands of paths.
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def load_historical_data(data_path: Path) -> pd.DataFrame:
    """Load sector historical data CSV."""
    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def compute_returns(df: pd.DataFrame) -> dict[str, tuple]:
    """
    Compute log returns, mean, and std by sector.
    Returns: {sector: (mean_daily_return, std_daily_return)}
    """
    results = {}
    for sector, group in df.groupby("sector"):
        group = group.sort_values("date").drop_duplicates("date", keep="last")
        prices = group["close"].values
        if len(prices) < 2:
            continue
        log_returns = np.diff(np.log(prices))
        mean_ret = np.mean(log_returns)
        std_ret = np.std(log_returns)
        results[sector] = (mean_ret, std_ret)
    return results


def run_monte_carlo(
    mean_return: float,
    std_return: float,
    days: int = 252,
    n_paths: int = 10000,
    seed: int | None = 42,
) -> np.ndarray:
    """
    Run Monte Carlo simulation for a single sector.

    Returns: (n_paths, days+1) array of simulated price paths (index 0 = 1.0).
    """
    if seed is not None:
        np.random.seed(seed)
    dt = 1 / 252
    paths = np.zeros((n_paths, days + 1))
    paths[:, 0] = 1.0
    for t in range(1, days + 1):
        z = np.random.standard_normal(n_paths)
        paths[:, t] = paths[:, t - 1] * np.exp(
            (mean_return - 0.5 * std_return**2) * dt + std_return * np.sqrt(dt) * z
        )
    return paths


def summarize_paths(paths: np.ndarray, percentiles: tuple = (5, 25, 50, 75, 95)) -> dict:
    """Compute percentile bands across paths."""
    final_prices = paths[:, -1]
    return {
        "mean": np.mean(final_prices),
        "std": np.std(final_prices),
        "percentiles": {
            p: np.percentile(final_prices, p) for p in percentiles
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Investment Simulator")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "sector_historical_data.csv",
        help="Path to sector historical data CSV",
    )
    parser.add_argument("--days", type=int, default=252, help="Simulation horizon in days")
    parser.add_argument("--paths", type=int, default=10000, help="Number of Monte Carlo paths")
    parser.add_argument("--output", type=Path, default=None, help="Output directory for plots")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    df = load_historical_data(args.data)
    sector_stats = compute_returns(df)

    results = {}
    for sector, (mean_ret, std_ret) in sector_stats.items():
        paths = run_monte_carlo(
            mean_ret, std_ret,
            days=args.days,
            n_paths=args.paths,
            seed=args.seed,
        )
        summary = summarize_paths(paths)
        results[sector] = {"paths": paths, "summary": summary, "mean_ret": mean_ret, "std_ret": std_ret}
        print(f"\n{sector}:")
        print(f"  Mean return (annualized): {mean_ret * 252:.4f}")
        print(f"  Volatility (annualized):  {std_ret * np.sqrt(252):.4f}")
        print(f"  Final price (mean):       {summary['mean']:.4f}")
        print(f"  5th / 95th percentile:   {summary['percentiles'][5]:.4f} / {summary['percentiles'][95]:.4f}")

    # Optional: save plots
    if args.output:
        args.output = Path(args.output)
        args.output.mkdir(parents=True, exist_ok=True)
        for sector, data in results.items():
            fig, ax = plt.subplots(figsize=(10, 5))
            paths_arr = data["paths"]
            ax.plot(paths_arr[:100].T, alpha=0.3, color="blue")
            ax.plot(np.median(paths_arr, axis=0), color="red", linewidth=2, label="Median")
            ax.set_title(f"Monte Carlo: {sector}")
            ax.set_xlabel("Days")
            ax.set_ylabel("Price (normalized)")
            ax.legend()
            fig.savefig(args.output / f"monte_carlo_{sector.lower()}.png", dpi=150)
            plt.close()
        print(f"\nPlots saved to {args.output}")

    return results


if __name__ == "__main__":
    main()
