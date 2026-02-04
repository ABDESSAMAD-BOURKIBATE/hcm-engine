from fastapi import FastAPI
from pydantic import BaseModel, Field

from hcm_engine.core.decision import HCMInput, HCMConfig, hcm_decide, to_dict
from hcm_engine.policy.learned import LearnedPolicy

app = FastAPI(
    title="HCM-Engine API",
    description="Governance-driven containment decision API for sociotechnical smart homes.",
    version="0.1.0",
)

# --- Optional Learned Policy (does not break if model file is missing) ---
LEARNED_POLICY = None
try:
    # Put your trained model here later:
    # models/containment_model.joblib
    LEARNED_POLICY = LearnedPolicy(
        model_path="models/containment_model.joblib",
        threshold=0.5,
    )
except Exception:
    LEARNED_POLICY = None


class DecisionRequest(BaseModel):
    device_id: str = Field(..., examples=["camera"])
    anomaly_score: float = Field(..., ge=0.0, le=1.0, examples=[0.78])
    trust_weight: float = Field(..., ge=0.0, le=1.0, examples=[0.9])
    centrality: float = Field(..., ge=0.0, le=1.0, examples=[0.6])
    theta_a: float = Field(0.5, ge=0.0, le=1.0)
    theta_I: float = Field(0.3, ge=0.0, le=1.0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decide")
def decide(req: DecisionRequest, mode: str = "rule"):
    """
    mode:
      - rule: use governance thresholds (default)
      - learned: use ML policy if available; otherwise fallback to rule
    """
    features = {
        "device_id": req.device_id,
        "anomaly_score": req.anomaly_score,
        "trust_weight": req.trust_weight,
        "centrality": req.centrality,
    }

    # Learned policy path (safe fallback)
    if mode == "learned" and LEARNED_POLICY is not None:
        return LEARNED_POLICY.decide(features)

    # Rule-based HCM decision
    cfg = HCMConfig(theta_a=req.theta_a, theta_I=req.theta_I)
    inp = HCMInput(**features)
    out = hcm_decide(inp, cfg)
    return to_dict(out)
