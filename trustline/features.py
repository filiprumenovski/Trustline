import numpy as np
import pandas as pd
from trustline.schema import DISCRETIONARY_CATEGORIES, ALL_CATEGORIES

def create_feature_matrix(transactions_df: pd.DataFrame):
    df = transactions_df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    hourly_grid = pd.DataFrame(index=pd.date_range(start=df.index.min().floor('h'), end=df.index.max().ceil('h'), freq='h'))
    spend_df = df[df['amount'] > 0].copy()
    spend_df['disc_spend'] = spend_df.apply(lambda row: row['amount'] if row['category'] in DISCRETIONARY_CATEGORIES else 0, axis=1)
    category_spend = spend_df.pivot_table(index='timestamp', columns='category', values='amount', aggfunc='sum').resample('h').sum().fillna(0)
    for cat in ALL_CATEGORIES:
        if cat not in category_spend.columns: category_spend[cat] = 0
    hourly_spend = spend_df[['disc_spend']].resample('h').sum().fillna(0)
    hourly_txn_counts = spend_df[['amount']].resample('h').count().rename(columns={'amount': 'txn_count'})
    features_df = hourly_grid.join(hourly_spend).join(hourly_txn_counts).join(category_spend).fillna(0)
    roll_windows = {'3h': 3, '24h': 24, '7d': 24 * 7}
    for name, window in roll_windows.items():
        features_df[f'disc_spend_{name}'] = features_df['disc_spend'].rolling(window=window, min_periods=1).sum()
        features_df[f'txn_count_{name}'] = features_df['txn_count'].rolling(window=window, min_periods=1).sum()
    features_df['hour_of_day'] = features_df.index.hour
    features_df['day_of_week'] = features_df.index.dayofweek
    features_df['is_weekend'] = features_df['day_of_week'].isin([5, 6]).astype(int)
    features_df['hour_sin'], features_df['hour_cos'] = np.sin(2*np.pi*features_df['hour_of_day']/24), np.cos(2*np.pi*features_df['hour_of_day']/24)
    features_df['day_sin'], features_df['day_cos'] = np.sin(2*np.pi*features_df['day_of_week']/7), np.cos(2*np.pi*features_df['day_of_week']/7)
    grouped = features_df.groupby(['day_of_week', 'hour_of_day'])
    features_df['ewma_disc_spend_4w'] = grouped['disc_spend'].transform(lambda x: x.ewm(span=4, min_periods=1).mean())
    for category in DISCRETIONARY_CATEGORIES:
        if category in features_df.columns: features_df[f'ewma_{category}_4w'] = grouped[category].transform(lambda x: x.ewm(span=4, min_periods=1).mean())
    goal_df = df[['goal_week']].resample('h').ffill()
    features_df = features_df.join(goal_df).ffill()
    features_df['remaining_buffer'] = np.maximum(0, features_df['goal_week'] - features_df['disc_spend_7d'])
    features_df['pace_vs_goal'] = features_df['disc_spend_7d'] / np.maximum(1, features_df['goal_week'])
    future_spend = features_df['disc_spend'].rolling(window=3, min_periods=1).sum().shift(-3)
    overspend_by_buffer = future_spend > features_df['remaining_buffer']
    spend_percentile_75 = spend_df[spend_df['disc_spend'] > 0]['disc_spend'].quantile(0.75)
    overspend_by_percentile = future_spend > spend_percentile_75
    features_df['y'] = (overspend_by_buffer | overspend_by_percentile).astype(int)
    model_features_to_drop = list(ALL_CATEGORIES) + list(DISCRETIONARY_CATEGORIES) + ['disc_spend', 'txn_count', 'goal_week', 'hour_of_day', 'day_of_week'] + [f'ewma_{cat}_4w' for cat in DISCRETIONARY_CATEGORIES]
    model_features = features_df.drop(columns=[col for col in model_features_to_drop if col in features_df.columns])
    final_full_df = features_df.iloc[(28*24):-4].dropna(subset=model_features.columns.drop('y', errors='ignore'))
    return final_full_df
