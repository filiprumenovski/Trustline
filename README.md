Trustline — A Wells Fargo ML Foresight System

Origin — The I-75 Moment

Millions of people live one unexpected bill away from crisis. As an international student driving a failing car down I-75 in Michigan, every engine knock felt like a financial cliff. One breakdown could have ended everything.

That moment became the seed for Trustline — a system built not just to offer cash, but to replace anxiety with foresight. Trustline isn’t about quick fixes. It’s about building stability through behavior, coaching, and earned support.

Mission Statement

"Trustline transforms a bank from a last-resort lender into a partner in progress."

Instead of reacting to overdrafts and crisis moments, Trustline predicts risk before it happens, nudges users toward better choices, and rewards discipline with Coach Credit — a living trust signal that unlocks fair, fast micro-advances.

This repo contains the first working ML prototype of that system.

What This Repo Demonstrates

This GitHub repository hosts a logistic regression model designed to:

Ingest anonymized transaction data

Engineer time-sensitive behavioral features (late-night spending spikes, irregular withdrawals, risky transaction categories)

Predict overspending risk within the next 3 hours

Trigger context-aware nudges, similar to production behavior

This is a lightweight, explainable ML system — deployable with current Wells Fargo infrastructure and built to scale.

System Architecture — High Level

[Data Ingestion] → [Feature Engineering Layer] → [ML Risk Predictor]
 → [Behavior Scoring / Coach Credit] → [Nudge Generator] → [Micro-Advance Gateway]

1. Data Ingestion

Uses CSV/transaction logs (expandable to Wells Fargo’s internal feed)

Categorizes transactions with nuanced weighting (essentials vs discretionary)

2. Feature Engineering

Extracts behavioral signals like:

spend_velocity_change

late_night_discretionary_ratio

goal_alignment_score

3. Risk Prediction

Logistic Regression  (Explainable, regulator-friendly)

Outputs a probability of crisis within a 3-hour prediction window

4. Nudge Generation

If risk < 30% → Positive reinforcement nudge

30%–60% → Gentle redirection



60% → Urgent alert + Coach Credit at stake

5. Micro-Advance Gateway

If Coach Credit ≥ Threshold → Instant cash access via existing rails

Decision backed by both FICO and real-time behavioral trust score

Coach Credit — Trust You Can See

Coach Credit isn’t like FICO. It's dynamic and behavior-based, designed to show who a user is becoming, not just who they were.

Actions like skipping a risky purchase after a nudge or moving $20 to savings increase Coach Credit immediately. This makes progress feel real and motivating.

Repo Contents (Technical Overview)

├── data/                     # Sample transaction logs
├── models/                   # Logistic Regression & baseline models
├── feature_engineering/     # Behavioral extraction scripts
├── nudging_system/          # Nudge logic based on risk thresholds
├── coach_credit/            # Scoring functions + thresholds
├── run_demo.py              # CLI entry to simulate user scenario
└── README.md                # You are here

How to Run Locally

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

The demo will:

Load synthetic transaction data

Simulate behavior drift

Predict overspending risk

Trigger nudges + update Coach Credit

Determine whether a micro-advance would be approved

Roadmap — What’s Next

Expand dataset categories with goal tagging and category weighting automation

Integrate visual dashboard for nudge patterns and risk trajectory visualization

Add REST API layer for real-time scoring and micro-advance eligibility checks

Experiment with LSTM / temporal fusion models for sequence-based behavioral prediction

Implement user-facing CLI or minimal web UI to simulate Trustline experience

Prepare compliance / explainability brief for regulator-facing clarity

Philosophy

This isn’t just code — it’s a philosophy of financial partnership. A bank shouldn’t wait for failure and then charge fees. It should quietly nudge users toward stability, catch them early when patterns shift, and reward effort in real time.

Trustline is that philosophy, made executable.

Connect & Contribute

This repo is a proof-of-concept intended for ML engineers, financial product designers, and Wells Fargo innovation stakeholders interested in building the next generation of customer partnership systems.

Contributions, architectural critiques, and model scaling discussions are welcomed.

"No more sweating on I-75 — just forward momentum."

