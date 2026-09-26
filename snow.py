import sys
import os
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

def get_oauth_token():
    """OAuth token తీసుకుంటుంది"""
    
    instance = os.getenv("SNOW_INSTANCE")
    
    token_url = f"{instance}/oauth_token.do"
    
    data = {
        "grant_type": "password",
        "client_id": os.getenv("SNOW_CLIENT_ID"),
        "client_secret": os.getenv("SNOW_CLIENT_SECRET"),
        "username": os.getenv("SNOW_USERNAME"),
        "password": os.getenv("SNOW_PASSWORD")
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Token obtained successfully!")
        return token
    else:
        print(f"Token error: {response.status_code}")
        print(response.text)
        return None

def fetch_latest_incident():
    """ServiceNow నుండి latest incident fetch చేస్తుంది"""
    
    token = get_oauth_token()
    if not token:
        return None
    
    instance = os.getenv("SNOW_INSTANCE")
    url = f"{instance}/api/now/table/incident"
    
    params = {
        "sysparm_limit": 1,
        "sysparm_query": "active=true^priority=1",
        "sysparm_fields": "number,short_description,description,priority,state,sys_created_on"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        incidents = response.json().get("result", [])
        if incidents:
            incident = incidents[0]
            print(f"\nTicket: {incident['number']}")
            print(f"Description: {incident['short_description']}")
            print(f"Priority: {incident['priority']}")
            return incident
        else:
            print("No active incidents found!")
            return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    fetch_latest_incident()