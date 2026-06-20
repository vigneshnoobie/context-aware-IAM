# verify_vc.py

import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def verify_credential(vc: dict) -> bool:
    try:
        # load issuer's public key
        with open("issuer_public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # extract and remove the proof section
        proof = vc.pop("proof", None)
        if not proof or "jws" not in proof:
            print("❌ Missing proof or JWS field.")
            return False

        # decode the JWS signature
        signature = base64.b64decode(proof["jws"])

        # serialize the VC content (excluding proof) for verification
        message = json.dumps(vc, sort_keys=True, separators=(',', ':')).encode()

        # verify the digital signature
        public_key.verify(
            signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # reattach the proof for completeness
        vc["proof"] = proof
        print("✅ Verified signature for credential.")
        return True

    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

# example usage
if __name__ == "__main__":
    try:
        with open("exported_vc.json", "r") as f:
            credential = json.load(f)
        verify_credential(credential)
    except FileNotFoundError:
        print("❌ exported_vc.json not found.")
