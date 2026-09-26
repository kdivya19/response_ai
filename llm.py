import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

def get_llm():
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_version="2024-06-01"
    )