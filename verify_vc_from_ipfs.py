import os
import json
import base64
import ipfshttpclient
import traceback
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Connect to IPFS Desktop explicitly
IPFS_API = "/ip4/127.0.0.1/tcp/5001"

def verify_signature(vc: dict) -> bool:
    try:
        # Resolve key path
        script_dir = os.path.dirname(__file__)
        key_path = os.path.join(script_dir, "issuer_public_key.pem")

        with open(key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # Extract and remove proof
        proof = vc.get("proof", {})
        if not proof or "jws" not in proof:
            print("❌ Missing proof or JWS.")
            return False

        signature = base64.b64decode(proof["jws"])

        # Remove proof and re-serialize payload exactly as during signing
        vc_payload = {k: v for k, v in vc.items() if k != "proof"}
        message = json.dumps(vc_payload, sort_keys=True, separators=(',', ':')).encode()

        # Verify signature
        public_key.verify(signature, message, padding.PKCS1v15(), hashes.SHA256())

        print("✅ Signature verified successfully.")
        return True

    except Exception as e:
        print("❌ Verification error:")
        traceback.print_exc()
        return False

def fetch_vc_from_ipfs(cid: str) -> dict:
    try:
        client = ipfshttpclient.connect(IPFS_API)
        data = client.cat(cid)
        return json.loads(data)
    except Exception as e:
        print(f"❌ Failed to fetch from IPFS: {e}")
        return {}

if __name__ == "__main__":
    cid = input("🔍 Enter IPFS CID of the Verifiable Credential: ").strip()
    vc_data = fetch_vc_from_ipfs(cid)

    if vc_data:
        verify_signature(vc_data)
