from openai import OpenAI, AzureOpenAI, AsyncAzureOpenAI
import os

from dotenv import load_dotenv
import asyncio
import json
import yaml

from app.services.clients import chat_client, whisper_client, transcribe_client

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_PATH / "prompts"
DATA_PATH = BASE_PATH / "data"

def load_prompt(prompt_path: str) -> str:
    prompt_file = PROMPT_PATH / prompt_path
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {e}")
        system_prompt = f"{config['prompt']['content']}"
        rules = config['prompt'].get('rules')
        if rules:
            rules_text = "\n Rules: \n" + "\n".join(f' - {rule}' for rule in rules)
            system_prompt = f'{system_prompt}\n{rules_text}'
        return system_prompt


#function to get transcription

async def transcribe_audio(file_path: str) -> str:
    prompt = load_prompt('transcription_prompt.yaml')
    with open(file_path, 'rb') as audio_file:
        transcription = await transcribe_client.audio.transcriptions.create(
            model = 'gpt-4o-transcribe',
            file = audio_file,
            response_format = 'text',
            prompt = prompt
        )
    return transcription

#function to get structured data from the transcription
async def extract_structured_data(transcript: str) -> dict:
    pass




async def cleanup():
    await transcribe_client.close()


###development and testing
async def main():
    data_path = DATA_PATH / "sample_op.mp3"
    result = await transcribe_audio(data_path)
    await cleanup()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())