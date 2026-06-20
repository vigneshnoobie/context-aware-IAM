import json
import os
from datetime import datetime
import ipfshttpclient
from hashlib import sha256

LOG_FILE = "logs/access_logs.json"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def anonymize_email(email):
    if "@" not in email:
        return email
    user, domain = email.split('@')
    return user[0] + "***@" + domain

def hash_ip(ip):
    return sha256(ip.encode()).hexdigest()[:8]

#  Real-time monitoring
def check_for_policy_violation(log_entry):
    if log_entry["risk_score"] > 0.85 or log_entry["trust_score"] < 0.3:
        print(f"[🚨 ALERT] Suspicious activity: {log_entry['user_id']} — Risk: {log_entry['risk_score']} / Trust: {log_entry['trust_score']}")


def log_auth_attempt(user_id, timestamp, context, risk_score, trust_score, decision, method="password"):
    anonymized_user = anonymize_email(user_id)
    masked_context = {
    "device": context.get("user_agent", "unknown"),
    "ip": context.get("ip", "hidden"),  # Add this
    "ip_hash": hash_ip(context.get("ip", "0.0.0.0")),
    "geo": context.get("geo", "redacted"),
    "timestamp": timestamp.isoformat()
}

    log_entry = {
        "user_id": anonymized_user,
        "timestamp": timestamp.isoformat(),
        "context": masked_context,
        "risk_score": round(risk_score, 3),
        "trust_score": round(trust_score, 3),
        "decision": decision,
        "method": method
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"[❌] Failed to log attempt: {e}")

    # Trigger alert if necessary
    check_for_policy_violation(log_entry)

#  Load recent logs
def get_recent_logs(limit=20):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-limit:]
            return [json.loads(line.strip()) for line in lines]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[⚠️] Error reading logs: {e}")
        return []

#  Archive logs to IPFS
def archive_logs_to_ipfs():
    try:
        with open(LOG_FILE, "r") as f:
            logs = [json.loads(line.strip()) for line in f.readlines()]
            client = ipfshttpclient.connect()
            ipfs_hash = client.add_json({
                "archived_at": datetime.utcnow().isoformat(),
                "logs": logs
            })
            print(f"[✅] Logs archived to IPFS: {ipfs_hash}")
            return ipfs_hash
    except Exception as e:
        print(f"[❌] Failed to archive logs to IPFS: {e}")
        return None

#  Wrapper for logging from elsewhere
def log_access(user_id, username, method, context, risk, trust, decision):
    timestamp = datetime.utcnow()
    log_auth_attempt(
        user_id=user_id,
        timestamp=timestamp,
        context=context,
        risk_score=risk,
        trust_score=trust,
        decision=decision,
        method=method
    )
