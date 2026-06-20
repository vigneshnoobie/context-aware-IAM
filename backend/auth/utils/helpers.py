import hashlib
import secrets
import string
from flask import Request
from werkzeug.security import generate_password_hash, check_password_hash
from user_agents import parse as parse_ua
import random

# password hashing
def hash_password(password: str) -> str:
    return generate_password_hash(password, method='scrypt')

def verify_password(password: str, hashed: str) -> bool:
    return check_password_hash(hashed, password)

# random password generator (optional)
def generate_random_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# simulated typing pattern for test users (mock data)
def simulate_behavioral_pattern(username: str) -> dict:
    # You can customize this further for more realistic behavior
    simulated = {
        "typing_speed": random.uniform(0.1, 0.4),  # seconds per key
        "error_rate": random.uniform(0, 0.1),
        "pattern_id": f"sim_{hashlib.md5(username.encode()).hexdigest()[:6]}"
    }
    return simulated

# sanitize usernames (optional utility)
def sanitize_username(username: str) -> str:
    return username.strip().lower()

# device fingerprinting using user-agent
def extract_device_fingerprint(req: Request) -> str:
    user_agent = req.headers.get("User-Agent", "")
    ip_address = req.remote_addr or "unknown"
    return hashlib.sha256((user_agent + ip_address).encode()).hexdigest()

# extract basic context
def extract_basic_context(req: Request) -> dict:
    user_agent_str = req.headers.get("User-Agent", "")
    user_agent = parse_ua(user_agent_str)

    return {
        "device": {
            "browser": user_agent.browser.family,
            "os": user_agent.os.family,
            "device_type": user_agent.device.family
        },
        "ip": req.remote_addr or "unknown",
        "user_agent": user_agent_str
    }

# detect risky environments based on IP or unusual agent (demo only)
def detect_environment_risk(req: Request) -> dict:
    ip = req.remote_addr or ""
    is_tor = ip.startswith("185.")  # fake check
    is_outdated_browser = "MSIE" in req.headers.get("User-Agent", "")
    risk_factors = []

    if is_tor:
        risk_factors.append("Tor Network")
    if is_outdated_browser:
        risk_factors.append("Outdated Browser")

    return {
        "is_risky": len(risk_factors) > 0,
        "risk_factors": risk_factors
    }

# aggregate context
def collect_full_context(req: Request, typing_data: str) -> dict:
    basic = extract_basic_context(req)
    fingerprint = extract_device_fingerprint(req)
    env_risk = detect_environment_risk(req)

    return {
        "device": basic["device"],
        "ip": basic["ip"],
        "user_agent": basic["user_agent"],
        "fingerprint": fingerprint,
        "typing_profile": typing_data,
        "environment_risk": env_risk
    }

# access decision logic
def make_access_decision(risk_score: float, trust_score: float) -> str:
    """
    Simplified access decision logic.
    """
    if risk_score >= 0.8:
        return "deny"
    elif risk_score >= 0.6 or trust_score < 0.4:
        return "challenge"
    else:
        return "allow"