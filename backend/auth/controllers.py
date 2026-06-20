import uuid
import datetime
from flask import session, request
from flask import Request  # ✅ Correct type for annotation

from backend.auth.utils.helpers import collect_full_context
from backend.auth.utils.behavioral_model import analyze_behavior
from backend.auth.utils.helpers import simulate_behavioral_pattern, sanitize_username
from backend.ml.scoring import compute_risk_score
from backend.ml.atfe import update_trust_score
from backend.auth.utils.logger import log_auth_attempt
from backend.auth.utils.token_manager import issue_token

# environment thresholds
RISK_THRESHOLD = 0.7
TRUST_THRESHOLD = 0.5


def authenticate_user(username: str, raw_typing_data: str, flask_request: Request) -> str:
    """
    Pipeline for passwordless authentication using contextual and behavioral data.
    """
    sanitized_username = sanitize_username(username)
    user_id = f"user_{sanitized_username}"


    stored_pattern = simulate_behavioral_pattern(sanitized_username)

    
    full_context = collect_full_context(flask_request, raw_typing_data)

    
    behavior_similarity = analyze_behavior(raw_typing_data, stored_pattern)

    
    risk_score = compute_risk_score(sanitized_username, full_context, behavior_similarity)

   
    trust_score = update_trust_score(sanitized_username, risk_score)

    
    decision = access_decision(risk_score, trust_score)

    
    session['user_id'] = user_id
    session['risk_score'] = risk_score
    session['trust_score'] = trust_score
    session['decision'] = decision
    session['context'] = full_context

    
    if decision == "ALLOW":
        token = issue_token(user_id, full_context)
        session['token'] = token
    else:
        session['token'] = None

    
    log_auth_attempt(
        user_id=user_id,
        timestamp=datetime.datetime.utcnow(),
        context=full_context,
        risk_score=risk_score,
        trust_score=trust_score,
        decision=decision
    )

    return decision


def access_decision(risk_score: float, trust_score: float) -> str:
    """
    Combine ML risk score and ATFE trust score to determine access outcome.
    """
    if risk_score >= 0.9:
        return "DENY"
    elif risk_score > RISK_THRESHOLD or trust_score < TRUST_THRESHOLD:
        return "CHALLENGE"
    return "ALLOW"
