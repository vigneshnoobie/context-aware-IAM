from backend.auth.utils.access_logger import archive_logs_to_ipfs

ipfs_hash = archive_logs_to_ipfs()
if ipfs_hash:
    print(f"✅ Logs archived to IPFS: {ipfs_hash}")
else:
    print("⚠️ No logs to archive.")
