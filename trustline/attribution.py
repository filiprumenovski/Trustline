import pandas as pd
from trustline.schema import DISCRETIONARY_CATEGORIES

def find_top_leak_category(window_features: pd.Series):
    top_category, max_expected_spend = "misc", 0.0
    for category in DISCRETIONARY_CATEGORIES:
        ewma_col = f'ewma_{category}_4w'
        if ewma_col in window_features and window_features[ewma_col] > max_expected_spend:
            max_expected_spend = window_features[ewma_col]
            top_category = category
    total_expected_spend = window_features.get('ewma_disc_spend_4w', 0.0)
    return {"top_category": top_category, "expected_spend_category": max_expected_spend, "expected_spend_total": total_expected_spend}
