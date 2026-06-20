import os
import ipfshttpclient
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# connect to local IPFS daemon
client = ipfshttpclient.connect(os.getenv("IPFS_API_URL"))

# test: Add string to IPFS
cid = client.add_str("Hello from IPFS!")
print("✅ Stored in IPFS with CID:", cid)

# test: retrieve the content back
content = client.cat(cid)
print(" Retrieved content:", content.decode())
