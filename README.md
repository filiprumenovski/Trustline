# Trustline Nudging Demo

This project is a command-line application that predicts the risk of discretionary overspending for different user personas. It uses a calibrated logistic regression model to generate time-sensitive "nudges" to help users stay on track with their financial goals.

This project was built following the blueprint in .

## How to Use

### 1. Setup

First, clone the repository and set up the Python virtual environment:

```bash
# Navigate to the project directory
cd trustline-nudging-demo

# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### 2. Generate Data

The project uses synthetic data. Generate the CSV files for each persona:

```bash
python -m trustline.synth
```

### 3. Train a Model

Train a specialized model for a persona (e.g., the student):

```bash
python -m trustline.cli train --csv data/student.csv --out outputs/student_model.pkl
```

### 4. Generate Nudges

Use a trained model to generate a forecast of high-risk nudges:

```bash
# Generate a 24-hour forecast from a specific time
python -m trustline.cli score \
  --csv data/student.csv \
  --model outputs/student_model.pkl \
  --now "2025-09-17T20:00:00" \
  --out outputs/student_nudges.json
```

The results will be saved in .
