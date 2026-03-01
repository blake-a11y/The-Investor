#!/bin/bash
# Run Monte Carlo (3 scenarios A/B/C, 10k paths, 6-month horizon)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT="$PROJECT_ROOT/reports"

echo "Running Monte Carlo (A/B/C scenarios, 10k paths, 6mo)..."
python "$SCRIPT_DIR/monte_carlo_simulator.py" --paths 10000 --output "$OUTPUT"

echo "Done. Check reports/ for mc_summary.csv and histograms."
