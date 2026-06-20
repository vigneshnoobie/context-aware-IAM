import sys
import os
import random
import matplotlib.pyplot as plt

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ml.atfe import evaluate_trust_score, get_trust_trajectory

# === CONFIG ===
user_id = "user@example.com"
risk_scores = [round(random.uniform(0.1, 0.9), 2) for _ in range(10)]  # Simulate 10 varying risk scores

print("Simulating Trust Trajectory")
trust_scores = []

for i, risk in enumerate(risk_scores):
    trust = evaluate_trust_score(user_id, risk)
    trust_scores.append(trust)
    print(f"Attempt {i+1}: Risk={risk} → Trust={round(trust, 3)}")

# === Visualize the Trust Score Curve ===
plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), trust_scores, marker='o', linestyle='-', color='blue', label='Trust Score')
plt.axhline(0.5, color='gray', linestyle='--', label='Initial Trust (0.5)')
plt.title(' ATFE: Trust Score Trajectory Over 10 Sessions')
plt.xlabel('Login Attempt')
plt.ylabel('Trust Score')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("trust_trajectory.png")
print("✅ Chart saved as trust_trajectory.png")
