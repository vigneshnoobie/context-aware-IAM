# issue_and_upload_vc.py

import json, base64
from datetime import datetime
import ipfshttpclient
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


with open("issuer_private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)


vc = {
    "issuer": "did:example:issuer123",
    "holder": "did:example:user123",
    "issued": str(datetime.utcnow()),
    "credentialSubject": {
        "id": "did:example:user123",
        "role": "admin"
    }
}


message = json.dumps(vc, sort_keys=True, separators=(',', ':')).encode()
signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
jws = base64.b64encode(signature).decode()


vc["proof"] = {
    "type": "RsaSignature2018",
    "created": str(datetime.utcnow()),
    "jws": jws
}


with open("exported_vc.json", "w") as f:
    json.dump(vc, f, indent=2)
print("✅ VC saved to 'exported_vc.json'.")


client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")
cid = client.add_json(vc)
print("✅ VC uploaded to IPFS.")
print(f"🆔 IPFS CID: {cid}")
