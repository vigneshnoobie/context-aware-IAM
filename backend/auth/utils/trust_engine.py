import json
import os
from datetime import datetime

TRUST_DB_FILE = "trust_db.json"

def load_trust_db():
    if os.path.exists(TRUST_DB_FILE):
        with open(TRUST_DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}}

def save_trust_db(data):
    with open(TRUST_DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user_id_by_email(trust_data, email):
    for user_id, user_data in trust_data["users"].items():
        if user_data.get("email") == email:
            return user_id
    return None

def update_trust_score(email, risk_score):
    trust_data = load_trust_db()
    user_id = get_user_id_by_email(trust_data, email)

    if not user_id:
        user_id = f"user_{len(trust_data['users'])+1:03}"
        trust_data["users"][user_id] = {
            "email": email,
            "trust_score": 60.0,
            "risk_score": risk_score,
            "trust_trajectory": [],
            "sessions": [],
            "anomaly_flags": {
                "typing_speed_anomaly": False,
                "location_deviation": False,
                "behavioral_drift": False
            }
        }

    user = trust_data["users"][user_id]
    current_score = user.get("trust_score", 60.0)

    if risk_score < 0.3:
        current_score += 5
    elif risk_score >= 0.7:
        current_score -= 3
    else:
        current_score -= 1

    current_score = round(max(0.0, min(100.0, current_score)), 2)
    user["trust_score"] = current_score
    user["risk_score"] = round(risk_score * 100, 2)

    user.setdefault("trust_trajectory", []).append({
        "timestamp": datetime.utcnow().isoformat(),
        "score": current_score,
        "event": "login_evaluated"
    })

    save_trust_db(trust_data)
    return current_score
