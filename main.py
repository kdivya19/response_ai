import sys
import os
from dotenv import load_dotenv
from extraction_agent import extract_entities
from log_ingestion import fetch_logs
from analysis import analyze_incident
from report_agent import generate_report

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

def run_pipeline(ticket: str):
    
    print("=" * 60)
    print("RESPONSE AI — AGENTIC ESCALATION ANALYSIS")
    print("=" * 60)
    
    # Step 1: Extract entities
    print("\n[STEP 1] Extracting entities from ticket...")
    entities = extract_entities(ticket)
    print(f"Server: {entities.server_name}")
    print(f"Component: {entities.component}")
    print(f"Error Code: {entities.error_code}")
    
    # Step 2: Fetch logs
    print("\n[STEP 2] Fetching relevant logs...")
    logs = fetch_logs(entities.server_name, entities.component)
    print(f"Fetched {len(logs.splitlines())} log lines")
    
    # Step 3: Analyze
    print("\n[STEP 3] Analyzing incident...")
    analysis = analyze_incident(ticket, logs)
    print(analysis)
    
    # Step 4: Generate report
    print("\n[STEP 4] Generating incident report...")
    report = generate_report(ticket, analysis)
    print(report)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    test_ticket = """
    Production server APP-PROD-01 is down since 2:30 AM. 
    Users are getting error 503. Database connection is failing. 
    Reported by John Smith.
    """
    
    run_pipeline(test_ticket)