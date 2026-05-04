from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services import functions

import uuid

from datetime import datetime, timedelta

note_cache = {}

router = APIRouter(tags=["transcription"])

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    output = await functions.transcribe_audio_endpoint(file)

    note_id = str(uuid.uuid4())

    note_cache[note_id] = {
        'transcription': output,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(hours=1)
    }

    return {
        'note_id': note_id,
        'url': f"/note/{note_id}"
    }

@router.get("/note/{note_id}")
async def get_note(note_id: str):
    if note_id not in note_cache:
        raise HTTPException(status_code = 404, detail = "Note not found")
    note = note_cache[note_id]

    if datetime.now() > note['expires_at']:
        del note_cache[note_id]
        raise HTTPException(status_code = 404, detail = "Note expired")
    return note['transcription']