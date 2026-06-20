# backend/auth/utils/access_control.py

def make_access_decision(risk_score: float, trust_score: float) -> str:
    """
    Decide access based on risk and trust thresholds.
    """
    if risk_score >= 0.9:
        return "deny"
    elif risk_score > 0.7 or trust_score < 0.5:
        return "challenge"
    return "allow"
