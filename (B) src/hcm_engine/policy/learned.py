import joblib
from typing import Dict, Any


class LearnedPolicy:
    """
    Learned containment policy.
    Expects a trained binary classifier with predict_proba().
    """

    def __init__(self, model_path: str, threshold: float = 0.5):
        self.model = joblib.load(model_path)
        self.threshold = threshold

    def decide(self, features: Dict[str, Any]) -> Dict[str, Any]:
        X = [[
            features["anomaly_score"],
            features["trust_weight"],
            features["centrality"],
        ]]

        proba = float(self.model.predict_proba(X)[0, 1])
        decision = "CONTAIN" if proba >= self.threshold else "DEFER"

        return {
            "decision": decision,
            "confidence": proba,
            "policy": "learned",
        }
