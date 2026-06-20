import sys
import os
import json
import shutil
import ipfshttpclient
from datetime import datetime
from hashlib import sha256

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth.utils.access_logger import LOG_FILE

print(" Benchmark 4: Log Integrity with IPFS")

# Step 1: Read original logs
try:
    with open(LOG_FILE, "r") as f:
        original_lines = f.readlines()
        original_data = [json.loads(line.strip()) for line in original_lines]
except FileNotFoundError:
    print("❌ No access logs found. Run the app to generate log data first.")
    sys.exit(1)

# Step 2: Upload original logs to IPFS
client = ipfshttpclient.connect()
original_payload = {
    "logs": original_data,
    "timestamp": datetime.utcnow().isoformat()
}
original_hash = client.add_json(original_payload)
print(f"✅ Original Logs Uploaded: {original_hash}")

# Step 3: Backup and Tamper with Logs
tampered_file = "logs/tampered_logs.json"
shutil.copy(LOG_FILE, tampered_file)

with open(tampered_file, "a") as f:
    f.write(json.dumps({
        "user_id": "attacker@example.com",
        "timestamp": datetime.utcnow().isoformat(),
        "context": {"device": "spoofed", "ip_hash": "ffffeeee", "geo": "N/A"},
        "risk_score": 0.0,
        "trust_score": 1.0,
        "decision": "allow",
        "method": "injected"
    }) + "\n")

# Step 4: Upload tampered logs
with open(tampered_file, "r") as f:
    tampered_data = [json.loads(line.strip()) for line in f.readlines()]
tampered_payload = {
    "logs": tampered_data,
    "timestamp": datetime.utcnow().isoformat()
}
tampered_hash = client.add_json(tampered_payload)
print(f"⚠️ Tampered Logs Uploaded: {tampered_hash}")

# Step 5: Compare IPFS Hashes
if original_hash == tampered_hash:
    print("❌ Logs appear identical — integrity check failed!")
else:
    print("✅ Logs are tamper-evident — IPFS hashes DO NOT match!")

# cleanup
os.remove(tampered_file)
