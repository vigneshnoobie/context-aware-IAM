import sys
import os
import json
import time

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.auth.utils.issue_vc import issue_credential
from backend.auth.utils.verify_vc import verify_credential

print(" Benchmark 5: Credential Portability & Migration")

# Step 1: Issue VC
vc = issue_credential("did:example:user456", "user456@example.com", "user")

# Step 2: Export VC as JSON to a file
export_path = "sdk/exported_vc.json"
with open(export_path, "w") as f:
    json.dump(vc, f, indent=2)
print(f"✅ VC exported to: {export_path}")

# Step 3: Simulate transfer and re-import
with open(export_path, "r") as f:
    imported_vc = json.load(f)

# Step 4: Verify imported VC
start = time.time()
valid = verify_credential(imported_vc)
end = time.time()
latency_ms = round((end - start) * 1000, 2)

# Step 5: Structural Check
has_fields = all(k in imported_vc for k in ["@context", "credentialSubject", "issuer", "proof", "type"])

# Final Results
print(f" Structural Check: {'✅ Passed' if has_fields else '❌ Failed'}")
print(f"Signature Verification: {'✅ Passed' if valid else '❌ Failed'}")
print(f" Verification Latency: {latency_ms} ms")

# Clean up (optional)
# os.remove(export_path)


