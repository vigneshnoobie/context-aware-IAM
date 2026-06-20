# backend/ml/role_mapper.py

def determine_role(user_profile, context, risk_score):
    """
    Dummy logic to assign role based on identity provider and risk score.
    You can expand this based on email domain, org, etc.
    """
    provider = context.get("provider", "unknown")

    if provider == "GitHub":
        if risk_score < 0.4:
            return "developer"
        else:
            return "restricted"

    elif provider == "Slack":
        if "admin" in user_profile.get("name", "").lower():
            return "admin"
        else:
            return "employee"

    return "guest"
