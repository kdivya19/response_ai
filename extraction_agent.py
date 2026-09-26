import sys
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="groq/compound-mini" 
# )
llm=get_llm()


# Pydantic Model — defining Output structure 
class ExtractedEntities(BaseModel):
    server_name: str = Field(description="Name of the affected server")
    error_code: int = Field(description="Error code mentioned in ticket")
    component: str = Field(description="Affected component eg Database, API")
    incident_time: str = Field(description="Time when incident occurred")
    reporter: str = Field(description="Person who reported the incident")

# Binding LLM with pydantic model
structured_llm = llm.with_structured_output(ExtractedEntities, method="json_mode")

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IT incident analyst. 
Extract the following details from the incident ticket in json format:
- server_name
- error_code  
- component
- incident_time
- reporter

If any field is not found, use unknown."""),
    ("human", "{ticket}")
])

def extract_entities(ticket: str) -> ExtractedEntities:
    chain = extraction_prompt | structured_llm
    result = chain.invoke({"ticket": ticket})
    return result

# Test
if __name__ == "__main__":
    test_ticket = """
    Production server APP-PROD-01 is down since 2:30 AM. 
    Users are getting error 503. Database connection is failing. 
    Reported by John Smith.
    """
    
    result = extract_entities(test_ticket)
    print(result)
    print(f"\nServer: {result.server_name}")
    print(f"Error: {result.error_code}")