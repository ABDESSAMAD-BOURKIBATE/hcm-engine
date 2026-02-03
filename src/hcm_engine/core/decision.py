from dataclasses import dataclass, asdict
from typing import Literal, Dict, Any

from .impact import clamp01, compute_impact

DecisionType = Literal["ALLOW", "DEFER", "CONTAIN"]


@dataclass(frozen=True)
class HCMConfig:
    """Governance thresholds."""
    theta_a: float = 0.5   # anomaly threshold
    theta_I: float = 0.3   # impact threshold


@dataclass(frozen=True)
class HCMInput:
    """Single event input for HCM decision."""
    device_id: str
    anomaly_score: float   # a in [0,1]
    trust_weight: float    # T(s) in [0,1]
    centrality: float      # C(s) in [0,1]


@dataclass(frozen=True)
class HCMOutput:
    """Decision output with audit-friendly explanation."""
    decision: DecisionType
    impact: float
    reason: str
    details: Dict[str, Any]


def hcm_decide(inp: HCMInput, cfg: HCMConfig = HCMConfig()) -> HCMOutput:
    """
    Formal HCM decision logic:
      1) If a <= theta_a => ALLOW
      2) Else if I < theta_I => DEFER
      3) Else => CONTAIN
    Where I = a * T(s) * C(s)
    """
    a = clamp01(inp.anomaly_score)
    T = clamp01(inp.trust_weight)
    C = clamp01(inp.centrality)
    I = compute_impact(a, T, C)

    details = {
        "device_id": inp.device_id,
        "a": a,
        "T": T,
        "C": C,
        "theta_a": cfg.theta_a,
        "theta_I": cfg.theta_I,
    }

    if a <= cfg.theta_a:
        return HCMOutput(
            decision="ALLOW",
            impact=I,
            reason="benign (below anomaly threshold)",
            details=details,
        )

    if I < cfg.theta_I:
        return HCMOutput(
            decision="DEFER",
            impact=I,
            reason="anomalous but below impact threshold",
            details=details,
        )

    return HCMOutput(
        decision="CONTAIN",
        impact=I,
        reason="impact exceeds governance threshold",
        details=details,
    )


def to_dict(out: HCMOutput) -> Dict[str, Any]:
    """Convenience export for APIs."""
    return asdict(out)
