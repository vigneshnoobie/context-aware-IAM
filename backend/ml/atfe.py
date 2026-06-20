# backend/ml/atfe.py

from collections import deque

# In-memory store for trust scores and their history
user_trust_scores = {}
trust_trajectory_memory = {}

def evaluate_trust_score(user_id: str, risk_score: float, current_score: float = None) -> float:
    decay_rate = 0.01
    boost_threshold = 0.3

    if current_score is None:
        current_score = user_trust_scores.get(user_id, 0.5)

    if risk_score < boost_threshold:
        current_score += 0.02
    else:
        current_score -= decay_rate * risk_score

    updated_score = max(0.0, min(current_score, 1.0))
    user_trust_scores[user_id] = updated_score

    # Store trajectory
    history = trust_trajectory_memory.get(user_id, deque(maxlen=50))
    history.append(updated_score)
    trust_trajectory_memory[user_id] = history

    return updated_score

def update_trust_score(user_id: str, trust_score: float):
    trust_score = max(0.0, min(trust_score, 1.0))
    user_trust_scores[user_id] = trust_score

    history = trust_trajectory_memory.get(user_id, deque(maxlen=50))
    history.append(trust_score)
    trust_trajectory_memory[user_id] = history

    return trust_score

def get_trust_score(user_id: str) -> float:
    return user_trust_scores.get(user_id, 0.5)

def get_trust_trajectory(user_id: str):
    """
    Returns a list of previous trust scores (for visualization).
    """
    return list(trust_trajectory_memory.get(user_id, []))
