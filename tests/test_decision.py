from core.decision import HCMInput, HCMConfig, hcm_decide

def test_allow_when_below_anomaly_threshold():
    cfg = HCMConfig(theta_a=0.5, theta_I=0.3)
    inp = HCMInput(device_id="camera", anomaly_score=0.2, trust_weight=0.9, centrality=0.9)
    out = hcm_decide(inp, cfg)
    assert out.decision == "ALLOW"

def test_defer_when_anomalous_but_low_impact():
    cfg = HCMConfig(theta_a=0.5, theta_I=0.3)
    inp = HCMInput(device_id="sensor", anomaly_score=0.9, trust_weight=0.2, centrality=0.1)
    out = hcm_decide(inp, cfg)
    assert out.decision == "DEFER"

def test_contain_when_anomalous_and_high_impact():
    cfg = HCMConfig(theta_a=0.5, theta_I=0.3)
    inp = HCMInput(device_id="router", anomaly_score=0.9, trust_weight=0.9, centrality=0.6)
    out = hcm_decide(inp, cfg)
    assert out.decision == "CONTAIN"
