from backend.auth.utils.policy_manager import upload_policy_to_ipfs

policy = {
    "did": "did:example:user1",
    "resource": "/admin/settings",
    "permissions": ["read", "write"],
    "conditions": {
        "role": "admin",
        "trust_score_min": 0.7
    }
}

ipfs_hash = upload_policy_to_ipfs(policy)
print("Policy IPFS hash:", ipfs_hash)
