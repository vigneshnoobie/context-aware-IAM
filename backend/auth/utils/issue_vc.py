import json, datetime, base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import ipfshttpclient

# generate issuer keys (run only once)
def generate_issuer_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open("issuer_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("issuer_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# issue and sign a credential
def issue_credential(user_did, email, role):
    with open("issuer_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    credential = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential"],
        "issuer": "did:example:issuer123",
        "issuanceDate": datetime.datetime.utcnow().isoformat() + "Z",
        "credentialSubject": {
            "id": user_did,
            "email": email,
            "role": role
        }
    }

    # sign the credential
    message = json.dumps(credential, sort_keys=True).encode()
    signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
    jws = base64.b64encode(signature).decode()

    credential["proof"] = {
        "type": "RsaSignature2018",
        "created": datetime.datetime.utcnow().isoformat() + "Z",
        "proofPurpose": "assertionMethod",
        "verificationMethod": "https://example.com/issuer123#keys-1",
        "jws": jws
    }

    return credential

# upload VC to IPFS
def upload_to_ipfs(vc_dict):
    client = ipfshttpclient.connect()
    ipfs_hash = client.add_json(vc_dict)
    return ipfs_hash
