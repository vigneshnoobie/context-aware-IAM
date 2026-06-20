# backend/auth/utils/context_engine.py

import platform
import uuid
import time
import requests
from flask import request
import os

def collect_context_data(req, typing_data: str) -> dict:
    """
    Collect contextual data for the login attempt.
    """
    geo = get_geo_location(req)
    access_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    return {
        "ip_address": get_ip_address(req),
        "device_id": get_device_id(),
        "os": get_os_info(),
        "browser": req.user_agent.browser,
        "platform": req.user_agent.platform,
        "user_agent": str(req.user_agent),
        "network_type": req.headers.get('X-Network-Type', 'unknown'),
        "access_time": access_time,
        "geo_location": geo,
        "session_id": str(uuid.uuid4()),
        "typing_speed": calculate_typing_speed(typing_data)
    }


def get_ip_address(req):
    if req.headers.getlist("X-Forwarded-For"):
        return req.headers.getlist("X-Forwarded-For")[0]
    return req.remote_addr


def get_device_id():
    return hex(uuid.getnode())


def get_os_info():
    return f"{platform.system()} {platform.release()}"


def calculate_typing_speed(typing_data: str) -> float:
    try:
        times = list(map(int, typing_data.strip().split(',')))
        return round(sum(times) / len(times), 2) if times else 0.0
    except:
        return 0.0


def get_geo_location(req):
    """
    Uses IP geolocation API (e.g., ipinfo) if enabled.
    """
    ip = get_ip_address(req)
    if not os.getenv("ENABLE_GEOLOCATION", "True") == "True":
        return "unknown"
    try:
        ipstack_key = os.getenv("IPSTACK_API_KEY")
        if not ipstack_key:
            return "unknown"
        response = requests.get(f"http://api.ipstack.com/{ip}?access_key={ipstack_key}")
        if response.status_code == 200:
            data = response.json()
            return data.get("country_name", "unknown")
        return "unknown"
    except Exception as e:
        print(f"[Geo Error] {e}")
        return "unknown"
