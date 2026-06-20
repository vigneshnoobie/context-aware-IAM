import os
import sys
import json
from datetime import datetime
import ipfshttpclient

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth.utils.access_logger import LOG_FILE

print("Benchmark 9: Disaster Recovery Simulation")


try:
    with open(LOG_FILE, "r") as f:
        logs = [json.loads(line.strip()) for line in f.readlines()]
    client = ipfshttpclient.connect()
    snapshot = {
        "archived_at": datetime.utcnow().isoformat(),
        "logs": logs
    }
    ipfs_hash = client.add_json(snapshot)
    print(f"✅ Logs archived to IPFS: {ipfs_hash}")
except Exception as e:
    print(f" Archiving Success: {e}")
    sys.exit(1)


try:
    os.remove(LOG_FILE)
    print("🔥 Simulated log file deletion.")
except Exception as e:
    print(f"[⚠️] Could not delete logs: {e}")


try:
    recovered = client.get_json(ipfs_hash)
    with open(LOG_FILE, "w") as f:
        for log in recovered["logs"]:
            f.write(json.dumps(log) + "\n")
    print("🔁 Logs restored successfully from IPFS backup.")
except Exception as e:
    print(f"[❌] Recovery failed: {e}")


try:
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    print(f"📦 Recovery Complete: {len(lines)} logs restored.")
except Exception as e:
    print(f"[❌] Final read failed: {e}")
