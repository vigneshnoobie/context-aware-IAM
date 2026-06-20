# backend/auth/utils/policy_manager.py

import ipfshttpclient

# explicitly connect to IPFS Desktop's API endpoint
IPFS_API_ADDRESS = "/ip4/127.0.0.1/tcp/5001"

def upload_policy_to_ipfs(policy_dict):
    client = ipfshttpclient.connect(IPFS_API_ADDRESS)
    return client.add_json(policy_dict)

def get_policy_from_ipfs(ipfs_hash):
    client = ipfshttpclient.connect(IPFS_API_ADDRESS)
    return client.get_json(ipfs_hash)
