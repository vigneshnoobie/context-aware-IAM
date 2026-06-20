import ipfshttpclient

client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")
cid = client.add_str("Hello IPFS from VS Code!")
print("✅ Stored in IPFS with CID:", cid)

fetched = client.cat(cid)
print("📦 Retrieved from IPFS:", fetched.decode())
