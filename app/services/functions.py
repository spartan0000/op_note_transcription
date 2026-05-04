from openai import OpenAI, AzureOpenAI, AsyncAzureOpenAI
import os

from fastapi import UploadFile

from dotenv import load_dotenv
import asyncio
import json
import yaml

from app.services.clients import chat_client, whisper_client, transcribe_client
from app.pydantic.note import Note

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


async def transcribe_audio_endpoint(file: UploadFile) -> str:
    prompt = load_prompt('transcription_prompt.yaml')
    
    transcription = await transcribe_client.audio.transcriptions.create(
        model = 'gpt-4o-transcribe',
        file = (file.filename, file.file, file.content_type),
        response_format = 'text',
        prompt = prompt
    )
    return transcription

def _empty_report() -> dict:
    return {
        'id': None,
        'preop_diagnosis': None,
        'postop_diagnosis': None,
        'anesthesia': None,
        'date_of_dictation': None,
        'date_of_procedure': None,
        'procedures': [],
        'procedure_description': None,
        'ebl': None,
        'specimens': None
    }

#function to get structured data from the transcription
async def extract_structured_data(transcript: str) -> dict:
    prompt = load_prompt('extraction_prompt.yaml')

    try:
        response = await chat_client.responses.parse(
            model = 'gpt-5-mini',
            input = [
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': transcript}
            ],
            text_format = Note
        )

        if type(response.output_parsed) is str or response.output_parsed is None:
            return _empty_report()
        print(response.text)
    except Exception as e:
        print(f'Error extracting structured data: {e}')
        return _empty_report()
    return response.output_parsed



async def cleanup():
    await transcribe_client.close()
    await chat_client.close()


###development and testing
async def main():
    data_path = DATA_PATH / "sample_op.mp3"
    result = await transcribe_audio(data_path)
    output = await extract_structured_data(result)
    await cleanup()
    #print(result)
    print(output)
if __name__ == "__main__":
    asyncio.run(main())