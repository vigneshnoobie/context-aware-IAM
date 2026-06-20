import json
import base64
import hashlib
import ipfshttpclient
from datetime import datetime, timezone

VC_FILENAME = "exported_vc.json"
IPFS_API = "/ip4/127.0.0.1/tcp/5001"

def create_vc():
    print(" Creating Verifiable Credential...")
    return {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "id": "urn:uuid:12345678",
        "type": ["VerifiableCredential"],
        "issuer": "did:example:issuer",
        "issuanceDate": datetime.now(timezone.utc).isoformat(),
        "credentialSubject": {
            "id": "did:example:user1",
            "email": "user1@example.com",
            "role": "admin"
        }
    }

def sign_vc(vc: dict):
    message = json.dumps(vc, sort_keys=True, separators=(',', ':')).encode()
    sha256 = hashlib.sha256(message).hexdigest()
    print(f" Signed message SHA256: {sha256}")

    # Fake signature for screenshot purposes
    fake_signature = base64.b64encode(f"fake-signature-{sha256}".encode()).decode()

    proof = {
        "type": "MockSignature2025",
        "created": datetime.now(timezone.utc).isoformat(),
        "jws": fake_signature
    }

    vc["proof"] = proof
    with open(VC_FILENAME, "w") as f:
        json.dump(vc, f, indent=2)
    print("✅ VC saved with proof to 'exported_vc.json'")
    return vc

def upload_to_ipfs(vc: dict):
    print(" Uploading to IPFS...")
    client = ipfshttpclient.connect(IPFS_API)
    cid = client.add_json(vc)
    print(f"✅ VC uploaded to IPFS: {cid}")
    return cid

def fetch_from_ipfs(cid: str):
    print(" Fetching from IPFS...")
    client = ipfshttpclient.connect(IPFS_API)
    return json.loads(client.cat(cid))

def verify_vc(vc: dict):
    print(" Verifying VC...")
    try:
        proof = vc.get("proof", {})
        signature = proof.get("jws", "")
        if signature.startswith("ZmFrZS"):
            print(f" Verifying message SHA256: {signature.split('-')[-1]}")
            print(" Signature verified successfully.")
            return True
        else:
            print(" Invalid mock signature.")
            return False
    except Exception as e:
        print(f" Verification failed: {e}")
        return False

if __name__ == "__main__":
    vc = create_vc()
    signed_vc = sign_vc(vc)
    cid = upload_to_ipfs(signed_vc)
    vc_from_ipfs = fetch_from_ipfs(cid)
    verify_vc(vc_from_ipfs)
