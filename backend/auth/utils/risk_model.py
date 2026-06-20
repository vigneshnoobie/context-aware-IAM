# backend/auth/utils/risk_model.py

def compute_risk_score(username: str, context: dict, behavior_score: float) -> float:
    """
    Simplified risk score computation based on:
    - Typing behavior
    - Access time
    """

    risk = 0.0

    #  typing behavior (bot-like or erratic)
    if behavior_score < 50:
        print(f"[RISK] Fast/erratic typing for {username}: behavior_score={behavior_score}")
        risk += 0.3

    #  VPN or untrusted region check
    country = context.get('geo_location', 'Unknown')
    if country not in ['Ireland', 'India']:
        print(f"[RISK] Unfamiliar location for {username}: {country}")
        risk += 0.4

    # time of login (odd hours increase risk)
    access_time = context.get("access_time", "12:00")
    try:
        hour = int(access_time.split(":")[0])
        if hour < 6 or hour > 22:
            print(f"[RISK] Login at risky hour {hour} for {username}")
            risk += 0.2
    except Exception:
        print(f"[WARN] Unable to parse access_time for {username}: {access_time}")

    # final capped score
    return round(min(risk, 1.0), 2)
