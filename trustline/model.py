import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV

class TrustlineModel:
    def __init__(self):
        self.model = Pipeline([('scaler', StandardScaler()), ('classifier', CalibratedClassifierCV(LogisticRegressionCV(cv=5, random_state=42, solver='liblinear'), method='sigmoid', cv=3))])
    def train(self, X: pd.DataFrame, y: pd.Series):
        self.model.fit(X, y); return self
    def predict_proba(self, X: pd.DataFrame) -> pd.Series:
        return self.model.predict_proba(X)[:, 1]
    def save(self, filepath: str):
        joblib.dump(self, filepath)
    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
    def get_feature_importance(self, feature_names: list) -> pd.DataFrame:
        # The actual classifier is inside the calibrator, which is inside the pipeline
        # The attribute is base_estimator_ (with a trailing underscore) after fitting.
        classifier = self.model.named_steps['classifier'].base_estimator_
        coefficients = classifier.coef_[0]
        return pd.DataFrame({'feature': feature_names, 'coefficient': coefficients}).sort_values(by='coefficient', ascending=False)
