import sys
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from extraction_agent import extract_entities
from log_ingestion import fetch_logs
from analysis_agent import analyze_incident
from report_agent import generate_report

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Home route"""
    return jsonify({
        "status": "online",
        "message": "Welcome to Response AI Incident Escalation API",
        "endpoints": {
            "health": "GET /health",
            "analyze": "POST /analyze (Requires JSON body: {\"ticket\": \"...\"})"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """API health check"""
    return jsonify({"status": "ok", "message": "Response AI is running!"})

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    """
    Analyzes incident ticket and generated response
    """
    if request.method == "GET":
        return jsonify({
            "message": "The /analyze endpoint requires a POST request with JSON body.",
            "example_request_body": {
                "ticket": "Production server APP-PROD-01 is down since 2:30 AM. Users are getting error 503."
            }
        }), 200

    data = request.get_json()
    
    if not data or "ticket" not in data:
        return jsonify({"error": "ticket field required"}), 400
    
    ticket = data["ticket"]
    
    try:
        # Step 1: Extract entities
        entities = extract_entities(ticket)
        
        # Step 2: Fetch logs
        logs = fetch_logs(entities.server_name, entities.component)
        
        # Step 3: Analyze
        analysis = analyze_incident(ticket, logs)
        
        # Step 4: Generate report
        report = generate_report(ticket, analysis)
        
        return jsonify({
            "status": "success",
            "entities": {
                "server_name": entities.server_name,
                "error_code": str(entities.error_code),
                "component": entities.component,
                "incident_time": entities.incident_time,
                "reporter": entities.reporter
            },
            "analysis": analysis,
            "report": report
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)