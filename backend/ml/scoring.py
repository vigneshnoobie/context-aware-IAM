# backend/ml/scoring.py

import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# correct model path
MODEL_PATH = 'backend/ml/risk_model.pkl'

print(f"[ℹ️] Loading ML model from: {MODEL_PATH}")

try:
    risk_model = joblib.load(MODEL_PATH)
    print("[✅] ML model loaded successfully.")
except Exception as e:
    print(f"[⚠️] Failed to load ML model: {e}")
    risk_model = None

# In-memory caches (demo use only)
user_risk_memory = {}
user_trust_scores = {}

def compute_risk_score(context: dict, behavior_score: float) -> float:
    """
    Predict risk score using the trained ML model based on contextual and behavioral features.
    """
    if not risk_model:
        print("[⚠️] No ML model loaded, returning default score.")
        return 0.5

    try:
        input_df = pd.DataFrame([{
            "typing_speed": float(context.get("typing_speed", 0)),
            "ip_risk": float(context.get("environment_risk", {}).get("ip_risk", 0)),
            "time_risk": float(context.get("environment_risk", {}).get("time_risk", 0)),
            "device_change": float(context.get("environment_risk", {}).get("device_change", 0)),
            "location_distance": float(context.get("environment_risk", {}).get("location_distance", 0)),
        }])

        risk_score = risk_model.predict_proba(input_df)[0][1]
        return round(risk_score, 3)

    except Exception as e:
        print(f"[❌] ML scoring failed: {e}")
        return 0.5  # Neutral default score


def is_behavior_anomalous(context: dict, behavior_score: float) -> bool:
    """
    Determine if behavior is anomalous based on model prediction threshold.
    """
    risk_score = compute_risk_score(context, behavior_score)
    return risk_score >= 0.7


def update_trust_score(user_id: str, risk_score: float) -> float:
    """
    Adjust trust score based on new risk assessment.
    """
    decay_rate = 0.01
    boost_threshold = 0.3

    current_score = user_trust_scores.get(user_id, 0.5)

    if risk_score < boost_threshold:
        current_score += 0.02  # reward low risk
    else:
        current_score -= decay_rate * risk_score  # decay for higher risk

    updated_score = min(max(current_score, 0), 1)
    user_trust_scores[user_id] = updated_score
    return updated_score


def store_risk_history(user_id: str, risk_score: float):
    """
    Store user's recent risk scores for trend analysis.
    """
    history = user_risk_memory.get(user_id, [])
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "risk_score": risk_score
    })

    if len(history) > 50:
        history.pop(0)  # keep only latest 50

    user_risk_memory[user_id] = history


def get_user_risk_trend(user_id: str):
    return user_risk_memory.get(user_id, [])
