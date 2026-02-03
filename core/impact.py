def clamp01(x: float) -> float:
    """Clamp numeric value to [0,1]."""
    x = float(x)
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def compute_impact(anomaly_score: float, trust_weight: float, centrality: float) -> float:
    """
    HCM Impact:
        I = a * T(s) * C(s)
    All inputs are clamped to [0,1].
    """
    a = clamp01(anomaly_score)
    T = clamp01(trust_weight)
    C = clamp01(centrality)
    return a * T * C
