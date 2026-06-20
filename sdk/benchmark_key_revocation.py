import os
import sys
import time
from datetime import datetime

# add root path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.auth.utils.issue_vc import issue_credential
from backend.auth.utils.verify_vc import verify_credential

# file paths
KEY_DIR = "."  
OLD_KEY = "issuer_private_key.pem"
OLD_PUB = "issuer_public_key.pem"
NEW_KEY = "issuer_private_key_new.pem"
NEW_PUB = "issuer_public_key_new.pem"

def generate_keys(new_key=NEW_KEY, new_pub=NEW_PUB):
    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)

    with open(new_key, "wb") as f:
        f.write(key.export_key())

    with open(new_pub, "wb") as f:
        f.write(key.publickey().export_key())

    print(" New RSA keypair generated.")

def swap_keys(use_new=True):
    if use_new:
        os.replace(OLD_KEY, OLD_KEY + ".bak")
        os.replace(NEW_KEY, OLD_KEY)
        os.replace(NEW_PUB, OLD_PUB)
    else:
        os.replace(OLD_KEY, NEW_KEY)
        os.replace(OLD_KEY + ".bak", OLD_KEY)
        os.replace(OLD_PUB, NEW_PUB)

if __name__ == "__main__":
    print(" Benchmark 7: Key Revocation & Reissuance")

    # Step 1: Generate new keys
    generate_keys()

    # Step 2: Revoke old key by swapping
    swap_keys(use_new=True)
    print("🔄 Switched to new keys (simulated revocation)")

    # Step 3: Issue VC with new key
    did = "did:example:user789"
    email = "user789@example.com"
    role = "user"

    start_issue = time.time()
    vc = issue_credential(did, email, role)
    issue_duration = round((time.time() - start_issue) * 1000, 2)

    # Step 4: Verify the VC
    start_verify = time.time()
    result = verify_credential(vc)
    verify_duration = round((time.time() - start_verify) * 1000, 2)

    print(f"🧾 VC Reissued in: {issue_duration} ms")
    print(f"🔍 Verification Time: {verify_duration} ms")
    print(f"🔐 Verification Result: {result}")

    # Step 5: Restore old key
    swap_keys(use_new=False)
    print("🧹 Original key restored (test cleanup done)")
