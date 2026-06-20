# backend/utils/logger.py

import json
import os
from datetime import datetime

LOG_FILE = "access_logs.json"

def log_auth_attempt(user_id, timestamp, context, risk_score, trust_score, decision):
    log_entry = {
        "user_id": user_id,
        "timestamp": timestamp.isoformat(),
        "context": context,
        "risk_score": risk_score,
        "trust_score": trust_score,
        "decision": decision
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
