import os
import sys
import json
import hashlib
from datetime import datetime

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.auth.utils.access_logger import LOG_FILE

print(" Benchmark 8: Log Auditability & Transparency")

# step 1: Load original logs
try:
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        logs = [json.loads(line.strip()) for line in lines]
    print(f" Loaded {len(logs)} logs.")
except Exception as e:
    print(f"[❌] Failed to load logs: {e}")
    sys.exit(1)

# step 2: Check audit trail completeness
fields_required = ["user_id", "timestamp", "context", "risk_score", "trust_score", "decision", "method"]
incomplete_logs = [log for log in logs if not all(field in log for field in fields_required)]

completeness_score = 100 - (len(incomplete_logs) / len(logs)) * 100 if logs else 0
print(f"📋 Log Completeness Score: {round(completeness_score, 2)}%")

# step 3: Create hash-based integrity chain
tampered = False
previous_hash = ""

for idx, entry in enumerate(logs):
    log_string = json.dumps(entry, sort_keys=True)
    current_hash = hashlib.sha256((previous_hash + log_string).encode()).hexdigest()
    if "hash" in entry and entry["hash"] != current_hash:
        print(f"[⚠️] Tampering detected at index {idx}")
        tampered = True
        break
    previous_hash = current_hash

if not tampered:
    print("✅ No tampering detected in logs.")

# step 4: Output auditability score
integrity_score = 100 if not tampered else 70
audit_score = (completeness_score + integrity_score) / 2
print(f" Final Auditability Score: {round(audit_score, 2)} / 100")
