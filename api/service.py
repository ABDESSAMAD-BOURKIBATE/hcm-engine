from fastapi import FastAPI
from pydantic import BaseModel, Field

from core.decision import HCMInput, HCMConfig, hcm_decide, to_dict

app = FastAPI(
    title="HCM-Engine API",
    description="Governance-driven containment decision API for sociotechnical smart homes.",
    version="0.1.0",
)

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
def decide(req: DecisionRequest):
    cfg = HCMConfig(theta_a=req.theta_a, theta_I=req.theta_I)
    inp = HCMInput(
        device_id=req.device_id,
        anomaly_score=req.anomaly_score,
        trust_weight=req.trust_weight,
        centrality=req.centrality,
    )
    out = hcm_decide(inp, cfg)
    return to_dict(out)
