import sys
import os
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

def fetch_logs(server_name: str, component: str) -> str:
    """
    In Real Azure environment, KQL queries run here.
    Currently reading from local file for testing. 
    """
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, "data", "incident_logs.txt")
    
    with open(log_file, "r", encoding="utf-8") as f:
        all_logs = f.read()
    
    # KQL simulate — filtering based on server name 
    relevant_lines = []
    for line in all_logs.split("\n"):
        if server_name.upper() in line.upper() or component.upper() in line.upper():
            relevant_lines.append(line)
    
    filtered_logs = "\n".join(relevant_lines)
    
    # Relevant logs లేకపోతే — all logs return చేయి
    if not filtered_logs.strip():
        return all_logs
        
    return filtered_logs

# Test
if __name__ == "__main__":
    logs = fetch_logs("APP-PROD-01", "Database")
    print("Fetched Logs:")
    print(logs)