'''

Decentralized Identity Storage Module
--------------------------------------
This module enables decentralized storage of user identities and authentication data
using IPFS or Distributed Hash Tables (DHT), ensuring privacy and providing resilient storage solutions.

'''

import json
import os
import ipfshttpclient

IPFS_ENABLED = os.getenv('ENABLE_IPFS', 'true').lower() == 'true'
IPFS_API_URL = os.getenv('IPFS_API_URL', '/dns/localhost/tcp/5001/http')


class DecentralizedIdentityStorage:
    def __init__(self):
        if IPFS_ENABLED:
            try:
                self.client = ipfshttpclient.connect(IPFS_API_URL)
                print("[✅] Connected to IPFS")
            except Exception as e:
                print(f"[❌] IPFS connection failed: {e}")
                self.client = None
        else:
            self.client = None

    def store_identity(self, user_id: str, identity_payload: dict) -> str:
        """
        Store user identity object in IPFS.
        Returns the IPFS hash (CID) for retrieval.
        """
        if not self.client:
            print("[⚠️] IPFS not enabled. Cannot store identity.")
            return ""

        try:
            identity_json = json.dumps(identity_payload)
            result = self.client.add_json(identity_json)
            print(f"[📦] Stored identity for {user_id} at CID: {result}")
            return result
        except Exception as e:
            print(f"[❌] Failed to store identity: {e}")
            return ""

    def retrieve_identity(self, cid: str) -> dict:
        """
        Retrieve user identity from IPFS using CID.
        """
        if not self.client:
            return {}
        try:
            identity_data = self.client.get_json(cid)
            return identity_data
        except Exception as e:
            print(f"[❌] Failed to retrieve identity: {e}")
            return {}

    def revoke_identity(self, cid: str) -> bool:
        """
        Placeholder for revocation mechanism (e.g., unpinning, blacklisting).
        """
        print(f" Identity revocation simulated for CID: {cid}")
        # IPFS is immutable; revocation typically managed off-chain (e.g., in DB or policy engine)
        return True


# Usage Example (for developers/testing only)
if __name__ == '__main__':
    storage = DecentralizedIdentityStorage()

    identity = {
        "user_id": "alice@example.com",
        "device": "Pixel_6",
        "trust_score": 0.85,
        "roles": ["user"],
        "context": {"ip": "192.168.1.2", "browser": "Firefox"}
    }

    cid = storage.store_identity("alice@example.com", identity)
    retrieved = storage.retrieve_identity(cid)
    print(" Retrieved from IPFS:", retrieved)
    storage.revoke_identity(cid)
