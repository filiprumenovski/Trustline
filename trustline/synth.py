import csv
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from trustline.schema import ALL_CATEGORIES, CSV_HEADERS

STUDENT_PERSONA = {"name": "student", "goal_week_base": 75, "income_day": 5, "income_amount": (250, 50), "spending_profile": {"day_of_week_bias": {0: 0.5, 1: 0.5, 2: 0.7, 3: 1.2, 4: 1.5, 5: 1.5, 6: 0.8}, "category_bias": {"delivery": 3, "bars": 3, "rideshare": 2, "shopping": 1.5, "groceries": 1, "misc": 0.5, "rent": 0.01, "utilities": 0.01}}}
GIG_PERSONA = {"name": "gig", "goal_week_base": 150, "income_day": None, "income_amount": (80, 40), "spending_profile": {"day_of_week_bias": {0: 0.8, 1: 0.8, 2: 1.0, 3: 1.2, 4: 1.2, 5: 1.0, 6: 1.0}, "category_bias": {"rideshare": 3, "delivery": 2, "misc": 1.5, "utilities": 1, "groceries": 1, "shopping": 0.5, "bars": 0.5, "rent": 0.01}}}
FAMILY_PERSONA = {"name": "family", "goal_week_base": 250, "income_day": 5, "income_amount": (1800, 100), "spending_profile": {"day_of_week_bias": {0: 0.9, 1: 0.8, 2: 0.8, 3: 1.0, 4: 1.5, 5: 1.8, 6: 1.5}, "category_bias": {"groceries": 4, "shopping": 2, "rent": 0.05, "utilities": 0.5, "entertainment": 1.5, "delivery": 1, "misc": 1}}}
CATEGORY_AMOUNTS = {"rent": (1200, 10), "utilities": (80, 20), "groceries": (90, 40), "shopping": (75, 50), "entertainment": (60, 30), "delivery": (35, 15), "bars": (45, 25), "rideshare": (25, 10), "misc": (20, 15)}

def generate_transactions(persona, start_date, end_date):
    transactions = []
    current_date = start_date
    goal_week = persona["goal_week_base"]
    while current_date < end_date:
        if persona["name"] == "gig" and random.random() < 0.25:
             income = abs(np.random.normal(*persona["income_amount"]))
             transactions.append([current_date, -income, "income", 1, goal_week])
        elif persona["income_day"] is not None and current_date.weekday() == persona["income_day"]:
            if persona["name"] == "family" and current_date.day % 2 == 0:
                 income = abs(np.random.normal(*persona["income_amount"]))
                 transactions.append([current_date, -income, "income", 1, goal_week])
            elif persona["name"] == "student":
                 income = abs(np.random.normal(*persona["income_amount"]))
                 transactions.append([current_date, -income, "income", 1, goal_week])
        profile = persona["spending_profile"]
        day_bias = profile["day_of_week_bias"].get(current_date.weekday(), 1.0)
        num_transactions_today = np.random.poisson(day_bias * 1.5)
        for _ in range(num_transactions_today):
            categories, weights = list(profile["category_bias"].keys()), list(profile["category_bias"].values())
            chosen_category = random.choices(categories, weights=weights, k=1)[0]
            amount_mean, amount_std = CATEGORY_AMOUNTS.get(chosen_category, (20, 10))
            amount = abs(np.random.normal(loc=amount_mean, scale=amount_std))
            transaction_time = current_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            transactions.append([transaction_time, round(amount, 2), chosen_category, 0, goal_week])
        if random.random() < 0.05: goal_week = persona["goal_week_base"] + random.choice([-25, 0, 25, 50])
        current_date += timedelta(days=1)
    df = pd.DataFrame(transactions, columns=CSV_HEADERS).sort_values(by="timestamp").reset_index(drop=True)
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    return df

def main():
    print("Generating synthetic data...")
    end_time = datetime.now(); start_time = end_time - timedelta(days=180)
    for p in [STUDENT_PERSONA, GIG_PERSONA, FAMILY_PERSONA]:
        print(f"Generating data for {p['name']}...")
        df = generate_transactions(p, start_time, end_time)
        df.to_csv(f"data/{p['name']}.csv", index=False)
    print("All data generated successfully.")

if __name__ == "__main__": main()
