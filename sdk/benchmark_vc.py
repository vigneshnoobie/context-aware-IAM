import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.auth.utils.issue_vc import issue_credential
from backend.auth.utils.verify_vc import verify_credential

import time

# Sample input
did = "did:example:user123"
email = "user123@example.com"
role = "admin"

# --- Measure VC Issuance Time ---
start_issue = time.time()
vc = issue_credential(did, email, role)
end_issue = time.time()
issue_time_ms = round((end_issue - start_issue) * 1000, 2)

# --- Measure VC Verification Time ---
start_verify = time.time()
result = verify_credential(vc)
end_verify = time.time()
verify_time_ms = round((end_verify - start_verify) * 1000, 2)

# --- Output Results ---
print(f"✅ VC Issuance Time: {issue_time_ms} ms")
print(f"✅ VC Verification Time: {verify_time_ms} ms")
print(f"Verification Result: {result}")
