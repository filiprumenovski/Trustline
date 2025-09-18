from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    timestamp: datetime
    amount: float
    category: str
    income_flag: int
    goal_week: float

DISCRETIONARY_CATEGORIES = {"bars", "delivery", "rideshare", "entertainment", "shopping"}
ALL_CATEGORIES = list(DISCRETIONARY_CATEGORIES) + ["groceries", "rent", "utilities", "misc", "income"]
CSV_HEADERS = ["timestamp", "amount", "category", "income_flag", "goal_week"]
