# backend/utils/si_em.py

def forward_logs_to_siem(request, response):
    """
    Simulate forwarding logs to a SIEM.
    In production, this could send to Splunk, QRadar, ELK, etc.
    """
    log_data = {
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "user_agent": request.headers.get('User-Agent'),
        "ip": request.remote_addr,
    }

    
    print(f"[SIEM LOG] {log_data}")
