# Context-Aware IAM SDK

This SDK allows developers to integrate with the Decentralized Passwordless IAM System.

## Setup

```bash
pip install requests
```

## Usage

### 1. Initialize the client
```python
from sdk.iam_client import IAMClient
client = IAMClient(base_url="http://localhost:5000")
```

### 2. Issue Verifiable Credential
```python
vc = client.issue_credential("did:example:xyz", "user@example.com", "user")
```

### 3. Verify Credential
```python
result = client.verify_credential(vc["vc"])
```

### Run the demo
```bash
python sdk/examples/demo_issue_vc.py
```