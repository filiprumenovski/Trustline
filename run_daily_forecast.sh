#!/bin/bash

# This script automates the daily nudge generation process.

# Ensure we are running from the correct directory
cd ~/Documents/trustline

# Activate the Python virtual environment
source venv/bin/activate

echo "--- Starting Daily Trustline Forecast: Thu Sep 18 13:47:56 EDT 2025 ---"

# --- Step 1: Update Data (Placeholder) ---
# In a real system, a script would run here to pull the last 24 hours of
# transactions from a database and append them to the user's CSV.
echo "[1/2] Simulating daily data update..."
# Example: python -m trustline.update_data --user student

# --- Step 2: Generate Nudges for the Next 24 Hours ---
# Get the current date at midnight to start the forecast
# Note: Using a fixed date for this demo since our data is static
# In a real system, you'd use: NOW_ISO=2025-09-18T00:00:00
NOW_ISO="2025-09-17T00:00:00"

echo "[2/2] Generating forecast for the next 24 hours from $NOW_ISO..."

python -m trustline.cli score \
  --csv data/student.csv \
  --model outputs/student_model.pkl \
  --now "$NOW_ISO" \
  --out outputs/daily_student_nudges.json

echo "--- Daily forecast complete. Results are in outputs/daily_student_nudges.json ---"
