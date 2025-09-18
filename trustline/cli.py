import json
import click
import pandas as pd
from trustline.features import create_feature_matrix
from trustline.model import TrustlineModel
from trustline.attribution import find_top_leak_category
from trustline.policy import generate_nudge

@click.group()
def cli(): pass

@cli.command()
@click.option('--csv', required=True)
@click.option('--out', required=True)
def train(csv, out):
    click.echo(f"Loading data from {csv}..."); transactions_df = pd.read_csv(csv)
    click.echo("Engineering features..."); full_features_df = create_feature_matrix(transactions_df)
    X, y = full_features_df.drop(columns=['y']), full_features_df['y']
    model_feature_names = [col for col in X.columns if not col.startswith('ewma_') and not col in ['rent', 'utilities', 'groceries', 'misc', 'income', 'entertainment']]
    X_model = X[model_feature_names]
    model = TrustlineModel()
    model.train(X_model, y)
    model.save(out)
    click.echo(f"\n✅ Training complete. Model saved to {out}")

@cli.command()
@click.option('--csv', required=True)
@click.option('--model', required=True)
@click.option('--now', required=True)
@click.option('--hours', default=24) # Default to a 24-hour forecast
@click.option('--out', required=True)
def score(csv, model, now, hours, out):
    click.echo(f"Loading model from {model}..."); tl_model = TrustlineModel.load(model)
    click.echo(f"Loading data from {csv}..."); transactions_df = pd.read_csv(csv)
    click.echo(f"Engineering features for the next {hours} hours..."); full_features_df = create_feature_matrix(transactions_df)
    try:
        start_time = pd.to_datetime(now).floor('h'); start_index = full_features_df.index.get_loc(start_time)
    except KeyError:
        click.echo(f"Error: Timestamp '{now}' not found. Use a date between {full_features_df.index.min()} and {full_features_df.index.max()}."); return
    score_window = full_features_df.iloc[start_index : start_index + hours]
    if score_window.empty: click.echo("Error: Not enough data to score."); return
    model_feature_names = tl_model.model.named_steps['scaler'].feature_names_in_
    X_score = score_window[model_feature_names]
    probabilities = tl_model.predict_proba(X_score)
    nudges = []
    for i, prob in enumerate(probabilities):
        window_data, window_start_time = score_window.iloc[i], score_window.index[i]
        attribution = find_top_leak_category(window_data)
        nudge = generate_nudge(prob=prob, top_category=attribution['top_category'], expected_spend_total=attribution['expected_spend_total'], window_start=window_start_time)
        nudges.append(nudge)
    high_risk_nudges = [n for n in nudges if n['level'] in ['alert', 'redirect']]
    sorted_nudges = sorted(high_risk_nudges, key=lambda x: x['prob'], reverse=True)
    with open(out, 'w') as f: json.dump(sorted_nudges, f, indent=4)
    click.echo(f"\n✅ Scoring complete. Found {len(sorted_nudges)} high-risk windows:")
    for nudge in sorted_nudges:
        click.echo(f"  - {nudge['window']} | Risk: {nudge['prob']:.0%} | {nudge['message']}")
    click.echo(f"\nFull high-risk forecast saved to {out}")

if __name__ == '__main__': cli()
