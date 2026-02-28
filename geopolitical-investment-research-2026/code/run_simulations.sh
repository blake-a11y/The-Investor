#!/bin/bash
# Run Monte Carlo simulations for geopolitical investment research

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA="$PROJECT_ROOT/data/sector_historical_data.csv"
OUTPUT="$PROJECT_ROOT/reports"

echo "Running Monte Carlo simulations..."
python "$SCRIPT_DIR/monte_carlo_simulator.py" \
  --data "$DATA" \
  --days 252 \
  --paths 10000 \
  --output "$OUTPUT" \
  --seed 42

echo "Done."
