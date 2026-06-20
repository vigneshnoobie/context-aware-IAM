# backend/auth/utils/token_manager.py

import jwt
import datetime
from flask import current_app

def issue_token(user_id, context):
    """
    Generate a JWT token with embedded context for session tracking.
    """
    payload = {
        "sub": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        "context": context
    }

    try:
        secret_key = current_app.config.get("JWT_SECRET_KEY", "default_secret_key")
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
    except Exception as e:
        print(f"[Token Error] {e}")
        return None


def verify_token(token):
    """
    Decode and verify JWT token. Returns payload if valid, otherwise None.
    """
    try:
        secret_key = current_app.config.get("JWT_SECRET_KEY", "default_secret_key")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("[Token Error] Token expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"[Token Error] Invalid token: {e}")
        return None


def revoke_token(user_id):
    """
    Simulate token revocation (expand for real DB/session blacklist).
    """
    print(f"[Session Revoked] User ID: {user_id}")
