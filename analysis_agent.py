import sys
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model_name="groq/compound-mini"
# )

llm = get_llm()

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior IT operations engineer.
You will be given:
1. An incident ticket raised by a user
2. Related system logs

Your job is to analyze and find:
- What exactly went wrong
- Root cause of the issue
- Which components were affected
- Timeline of events

Be specific and technical. Use the log evidence to support your analysis."""),
    ("human", """
Incident Ticket:
{ticket}

System Logs:
{logs}

Provide a detailed technical analysis.
""")
])

def analyze_incident(ticket: str, logs: str) -> str:
    """finds root cause from the logs + ticket"""
    
    chain = analysis_prompt | llm
    response = chain.invoke({
        "ticket": ticket,
        "logs": logs
    })
    
    return response.content

# Test
if __name__ == "__main__":
    test_ticket = """
    Production server APP-PROD-01 is down since 2:30 AM. 
    Users are getting error 503. Database connection is failing.
    """
    
    test_logs = """
    2024-01-15 02:25:33 INFO - Connection pool metrics: Active=45, Idle=5, Pending=89
    2024-01-15 02:30:01 ERROR - Failed to acquire connection from pool. Active=50, Idle=0
    2024-01-15 02:30:05 FATAL - Deadlock detected! Rolled back 3 transactions
    2024-01-15 02:30:15 FATAL - OutOfMemoryError: Java heap space. Usage=98.7%
    """
    
    result = analyze_incident(test_ticket, test_logs)
    print("Analysis Result:")
    print(result)