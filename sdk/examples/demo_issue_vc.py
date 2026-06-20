from sdk.iam_client import IAMClient

client = IAMClient()

# Issue a sample credential
vc_response = client.issue_credential(
    did="did:example:user123",
    email="user123@example.com",
    role="admin"
)

print("Issued VC:")
print(vc_response["vc"])

# Verify the credential immediately
verify_result = client.verify_credential(vc_response["vc"])
print("Verification Result:", verify_result)