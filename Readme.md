# Response AI — Agentic Escalation Analysis

An intelligent multi-agent system that automates IT incident analysis using Azure AI Foundry and LangChain.

## Architecture

ServiceNow Ticket (Input)
↓
Extraction Agent → Entity extraction + KQL generation
↓
Log Ingestion → Azure Monitor logs fetch
↓
Analysis Agent → Root cause analysis
↓
Report Agent → Professional incident report
↓
Flask REST API (Output)


## 🛠️ Tech Stack

- **LLM:** Azure OpenAI (GPT-5.4-mini) via Azure AI Foundry
- **Agent Framework:** LangChain
- **Log Storage:** Azure Log Analytics (KQL)
- **API:** Flask
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Ticketing:** ServiceNow REST API

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Azure subscription
- Azure AI Foundry deployment

### Installation

```bash
git clone https://github.com/kdivya19/response_ai.git
cd response_ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create `.env` file:


### Run

```bash
# Run pipeline directly
python main.py

# Run Flask API
python agents/app.py
```

### API Usage

```bash
POST /analyze
Content-Type: application/json

{
  "ticket": "Production server APP-PROD-01 is down since 2:30 AM. Users getting error 503."
}
```

### Response

```json
{
  "status": "success",
  "entities": {
    "server_name": "APP-PROD-01",
    "error_code": "503",
    "component": "Database",
    "incident_time": "2:30 AM",
    "reporter": "John Smith"
  },
  "analysis": "...",
  "report": "..."
}
```

##  Agents

| Agent | Responsibility |

| Extraction Agent | Extracts server, error code, component from ticket |
| Log Ingestion | Fetches relevant logs from Azure Monitor |
| Analysis Agent | Identifies root cause from logs |
| Report Agent | Generates professional incident report |

## 📁 Project Structure

response_ai/
├── agents/
│ ├── extraction_agent.py
│ ├── analysis_agent.py
│ ├── report_agent.py
│ ├── log_ingestion.py
│ ├── servicenow_agent.py
│ ├── llm.py
│ └── app.py
├── data/
│ ├── incident_logs.txt
│ └── sample_log.json
├── main.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md 


## 🔮 Future Enhancements

- Email notifications via Azure Logic Apps
- Dashboard UI