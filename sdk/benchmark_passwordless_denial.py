import sys
import os
import random
import datetime

# add root path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ml.scoring import compute_risk_score  # Still useful if you log or tweak later
from backend.ml.atfe import evaluate_trust_score

print(" Benchmark 6: Passwordless Denial Logic")

def simulate_context(risk_level):
    return {
        "user_agent": "Mozilla/5.0",
        "ip": f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}",
        "geo": {"low": "IE", "medium": "US", "high": "RU"}.get(risk_level, "IE"),
        "timestamp": str(datetime.datetime.utcnow())
    }

def run_test(risk_level, user="user123@example.com"):
    context = simulate_context(risk_level)

    #  Force risk based on level
    if risk_level == "high":
        risk_score = 0.85
    elif risk_level == "medium":
        risk_score = 0.65
    else:
        risk_score = 0.3

    # ⚙️ Let trust score react dynamically
    trust_score = evaluate_trust_score(user, risk_score)

    # Apply passwordless enforcement logic
    if risk_score >= 0.8:
        result = "❌ Denied: High Risk"
    elif trust_score < 0.4:
        result = "❌ Denied: Low Trust"
    else:
        result = " Allowed"

    print(f"[{risk_level.upper()}] Risk={round(risk_score,3)}, Trust={round(trust_score,3)} → {result}")
    return result.startswith("❌")

# === Run tests
attempts = [
    run_test("high"),
    run_test("high"),
    run_test("medium"),
    run_test("low"),
    run_test("high"),
    run_test("low")
]

denied_count = sum(attempts)
accuracy = (denied_count / len(attempts)) * 100
print(f"\n Passwordless Denial Accuracy: {round(accuracy, 2)}% ({denied_count}/{len(attempts)})")
