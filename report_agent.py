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

llm=get_llm()

report_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IT incident report specialist.
Generate a clear, professional incident report based on the technical analysis provided.

The report should have:
1. Executive Summary (2-3 lines, non-technical, for management)
2. Impact Assessment (who was affected, how long)
3. Root Cause (simple explanation)
4. Immediate Actions Taken
5. Preventive Measures (top 3 recommendations)

Keep it concise and professional. Avoid excessive technical jargon."""),
    ("human", """
Original Ticket:
{ticket}

Technical Analysis:
{analysis}

Generate a professional incident report.
""")
])

def generate_report(ticket: str, analysis: str) -> str:
    """Professional incident report generate చేస్తుంది"""
    
    chain = report_prompt | llm
    response = chain.invoke({
        "ticket": ticket,
        "analysis": analysis
    })
    
    return response.content

# Test
if __name__ == "__main__":
    test_ticket = """
    Production server APP-PROD-01 is down since 2:30 AM. 
    Users are getting error 503. Database connection is failing.
    """
    
    test_analysis = """
    Root cause: Connection pool exhaustion cascaded into deadlock 
    and JVM OutOfMemoryError bringing server down.
    Timeline: 02:25 pool pressure, 02:30 full outage.
    """
    
    result = generate_report(test_ticket, test_analysis)
    print("Incident Report:")
    print(result)