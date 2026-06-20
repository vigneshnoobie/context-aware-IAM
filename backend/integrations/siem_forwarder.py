'''
SIEM Forwarder Module
---------------------
This module forwards access logs and behavioral data to external SIEM solutions
such as Splunk, ELK, or Wazuh. The forwarding logic is invoked after each
access decision to maintain centralized log aggregation.


'''

import json
import requests
import os

# configuration from environment variables
SPLUNK_HEC_URL = os.getenv('SPLUNK_HEC_URL')
SPLUNK_HEC_TOKEN = os.getenv('SPLUNK_HEC_TOKEN')

ELK_ENDPOINT = os.getenv('ELK_LOGSTASH_URL')  
WAZUH_API = os.getenv('WAZUH_API_URL')        
WAZUH_TOKEN = os.getenv('WAZUH_API_TOKEN')    

def forward_to_splunk(event):
    """
    Forwards the given log event to Splunk using HEC (HTTP Event Collector).
    """
    if not SPLUNK_HEC_URL or not SPLUNK_HEC_TOKEN:
        print("[⚠️] Splunk HEC configuration missing.")
        return False

    headers = {
        'Authorization': f'Splunk {SPLUNK_HEC_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'event': event,
        'sourcetype': 'context-aware-iam',
    }
    try:
        response = requests.post(SPLUNK_HEC_URL, headers=headers, data=json.dumps(payload))
        return response.status_code == 200
    except Exception as e:
        print(f"[❌] Failed to send to Splunk: {e}")
        return False

def forward_to_elk(event):
    """
    Forwards logs to ELK endpoint (e.g., Logstash input endpoint).
    """
    if not ELK_ENDPOINT:
        return False
    try:
        headers = {'Content-Type': 'application/json'}
        res = requests.post(ELK_ENDPOINT, headers=headers, data=json.dumps(event))
        return res.status_code in [200, 201]
    except Exception as e:
        print(f"[❌] ELK forwarding failed: {e}")
        return False

def forward_to_wazuh(event):
    """
    Forwards logs to Wazuh API endpoint if configured.
    """
    if not WAZUH_API or not WAZUH_TOKEN:
        return False
    try:
        headers = {
            'Authorization': f'Bearer {WAZUH_TOKEN}',
            'Content-Type': 'application/json'
        }
        res = requests.post(WAZUH_API, headers=headers, data=json.dumps(event))
        return res.status_code in [200, 201]
    except Exception as e:
        print(f"[❌] Wazuh forwarding failed: {e}")
        return False

def forward_log_to_all_siems(log_data):
    """
    Forward a unified access log to all configured SIEMs.
    """
    success_splunk = forward_to_splunk(log_data)
    success_elk = forward_to_elk(log_data)
    success_wazuh = forward_to_wazuh(log_data)

    print("[✅] Log forwarded to:", {
        "Splunk": success_splunk,
        "ELK": success_elk,
        "Wazuh": success_wazuh
    })
