import requests

class IAMClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def issue_credential(self, did, email, role):
        payload = {
            "did": did,
            "email": email,
            "role": role
        }
        response = requests.post(f"{self.base_url}/auth/issue_credential", json=payload)
        return response.json()

    def verify_credential(self, vc_json):
        response = requests.post(f"{self.base_url}/auth/verify_credential", json=vc_json)
        return response.json()