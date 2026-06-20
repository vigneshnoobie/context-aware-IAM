# backend/auth/utils.py

import re
import time
import platform
import hashlib
import datetime
from statistics import mean
from user_agents import parse as parse_user_agent
from flask import Request
from werkzeug.security import generate_password_hash, check_password_hash


def calculate_typing_speed(typing_data: str) -> float:
    """
    Calculate average typing speed from keystroke durations (in ms).
    Returns a value representing average key press duration.
    """
    try:
        times = list(map(int, typing_data.strip().split(',')))
        if not times:
            return 0.0
        return round(mean(times), 2)
    except Exception as e:
        print(f"[Typing Speed Error] {e}")
        return 0.0


def extract_device_fingerprint(req: Request) -> str:
    """
    Extract user device fingerprint from request headers.
    Returns a hashed string representing the fingerprint.
    """
    user_agent = req.headers.get('User-Agent', '')
    parsed_agent = parse_user_agent(user_agent)

    fingerprint_parts = [
        parsed_agent.browser.family,
        parsed_agent.browser.version_string,
        parsed_agent.os.family,
        parsed_agent.os.version_string,
        parsed_agent.device.family,
        str(parsed_agent.is_mobile),
        str(parsed_agent.is_tablet),
        str(parsed_agent.is_pc)
    ]

    raw_fingerprint = '|'.join(fingerprint_parts)
    hashed_fingerprint = hashlib.sha256(raw_fingerprint.encode()).hexdigest()
    return hashed_fingerprint


def sanitize_username(username: str) -> str:
    """Sanitize input to allow only alphanumeric usernames."""
    return re.sub(r'\W+', '', username.lower())


def hash_password(password: str) -> str:
    """Return a hashed password using Werkzeug."""
    return generate_password_hash(password)


def verify_password(password: str, hash_value: str) -> bool:
    """Verify a password against the stored hash."""
    return check_password_hash(hash_value, password)


def simulate_behavioral_pattern(username: str) -> str:
    """
    Simulate or retrieve a stored behavioral pattern.
    In real deployment, this should query from a behavior DB.
    """
    # Demo pattern: "100,90,85,100,95"
    return "100,90,85,100,95"  # Replace with dynamic DB query


def extract_basic_context(req: Request) -> dict:
    """
    Extract IP, headers, and minimal context features from request.
    """
    return {
        "ip": req.remote_addr,
        "user_agent": req.headers.get('User-Agent'),
        "method": req.method,
        "endpoint": req.path,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


def detect_environment_risk(req: Request) -> dict:
    """
    Simple environment anomaly detector (basic PoC).
    """
    unusual_time = not (6 <= time.localtime().tm_hour <= 22)
    suspicious_headers = any([
        'curl' in req.headers.get('User-Agent', '').lower(),
        'sqlmap' in req.headers.get('User-Agent', '').lower(),
    ])

    return {
        "after_hours_access": unusual_time,
        "suspicious_headers": suspicious_headers
    }


def collect_full_context(req: Request, typing_data: str) -> dict:
    """
    Combine typing, device, and environment context for full evaluation.
    """
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "typing_speed": calculate_typing_speed(typing_data),
        "device_fingerprint": extract_device_fingerprint(req),
        "basic_context": extract_basic_context(req),
        "env_risk_flags": detect_environment_risk(req)
    }
