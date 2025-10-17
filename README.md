# Trustline — A Wells Fargo ML Foresight System

## Origin — The I-75 Moment
Millions of people live one unexpected bill away from crisis. As an international student driving a failing car down I-75 in Michigan, every engine knock felt like a financial cliff. One breakdown could have ended everything.

That moment became the seed for **Trustline** — a system built not just to offer cash, but to **replace anxiety with foresight**. Trustline isn’t about quick fixes. It’s about building stability through behavior, coaching, and earned support.

---

## Mission Statement
> "Trustline transforms a bank from a last-resort lender into a **partner in progress**."

Instead of reacting to overdrafts and crisis moments, Trustline **predicts risk before it happens**, nudges users toward better choices, and rewards discipline with **Coach Credit** — a living trust signal that unlocks fair, fast micro-advances.

This repo contains the **first working ML prototype** of that system.

---

## What This Repo Demonstrates
This GitHub repository hosts a **logistic regression model** designed to:

- Ingest anonymized transaction data  
- Engineer **time-sensitive behavioral features** (late-night spending spikes, irregular withdrawals, risky transaction categories)  
- Predict **overspending risk within the next 3 hours**  
- Trigger **context-aware nudges**, similar to production behavior

This is a **lightweight, explainable** ML system — deployable with current Wells Fargo infrastructure and built to scale.

---

## System Architecture — High Level
### 1. Data Ingestion
- Uses CSV/transaction logs (expandable to Wells Fargo’s internal feed)  
- Categorizes transactions with **nuanced weighting** (essentials vs. discretionary)

### 2. Feature Engineering
- Extracts behavioral signals like:
  - `spend_velocity_change`
  - `late_night_discretionary_ratio`
  - `goal_alignment_score`

### 3. Risk Prediction
- Logistic Regression (explainable, regulator-friendly)  
- Outputs a probability of crisis within a **3-hour prediction window**

### 4. Nudge Generation
- Risk < 30% → Positive reinforcement nudge  
- 30%–60% → Gentle redirection  
- 60% → Urgent alert + Coach Credit at stake

### 5. Micro-Advance Gateway
- If Coach Credit ≥ threshold → Instant cash access via existing rails  
- Decision backed by both **FICO** and a **real-time behavioral trust score**

---

## Coach Credit — Trust You Can See
**Coach Credit** isn’t like FICO. It's **dynamic** and **behavior-based**, designed to show **who a user is becoming**, not just who they were.

Actions like *skipping a risky purchase after a nudge* or *moving $20 to savings* increase Coach Credit immediately. This makes progress **feel real and motivating**.

---

## How to Run Locally
```bash
# Clone the project
git clone https://github.com/your-handle/trustline-ml
cd trustline-ml

# Optional: create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the simulation demo
python run_demo.py
