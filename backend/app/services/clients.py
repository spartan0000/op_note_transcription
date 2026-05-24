from openai import OpenAI, AzureOpenAI, AsyncAzureOpenAI
import os
from pathlib import Path

from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")


chat_client = AsyncAzureOpenAI(
    api_version = os.getenv("AZURE_GPT_API_VERSION"),
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    
)

# hnz_client = AsyncAzureOpenAI(
#     api_version = os.getenv("HNZ_API_VERSION"),
#     api_key = os.getenv("HNZ_API_KEY"),
#     azure_endpoint = os.getenv("HNZ_ENDPOINT")
# )

transcribe_client = AsyncAzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_TRANSCRIBE_ENDPOINT"),
    api_version = os.getenv("AZURE_TRANSCRIBE_API_VERSION")
)

whisper_client = AsyncAzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_WHISPER_ENDPOINT"),
    api_version = os.getenv("AZURE_WHISPER_API_VERSION")
)

