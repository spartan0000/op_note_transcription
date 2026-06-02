import pytest
from unittest.mock import AsyncMock, patch

from types import SimpleNamespace

from backend.app.services.functions import _empty_report, extract_structured_data


###tests endpoint including openai api calls
@pytest.mark.integration
def test_create_note(client):
    response = client.post("/api/transcribe-text", json={"transcript": "This is a test transcript."})
    assert response.status_code == 200

    data = response.json()
    assert "note_id" in data

#mocked test
def test_extract_structured_data(client):
    fake = {
        "transcript": "This is a test transcript"
    }

    with patch("backend.app.services.functions.extract_structured_data", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = {"key": "value"}
        
        response = client.post("/api/transcribe-text", json = fake)
        assert response.status_code == 200
        data = response.json()

        from backend.app.api.transcription_route import note_cache
        assert "note_id" in data
        note_id= data['note_id']
        assert note_cache[note_id]['transcription'] == "This is a test transcript"
        assert mock_extract.called

def test_extraction_failure(client):
    fake = {
        "transcript": "This is a test transcript"
    }

    with patch("backend.app.services.functions.extract_structured_data", new_callable=AsyncMock) as mock_extract:
        mock_extract.side_effect = Exception("Extraction failed")

        response = client.post("/api/transcribe-text", json = fake)

        assert response.status_code == 502


def test_empty_transcript(client):
    

    response = client.post("/api/transcribe", json = {})

    assert response.status_code == 422

def test_wrong_field_name(client):
    fake = {
        'wrong_field': "this is a test"
    }

    response = client.post("/api/transcribe-text", json = fake)

    assert response.status_code == 422


#this works and is needed only because note_cache = {} is shared in-memory state
#if we move to a database we would need to query the database instead
def test_note_cache_populated(client):
    fake = {
        'transcript': "test"
    }
    with patch("backend.app.services.functions.extract_structured_data", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = {"key": "value"}
    response = client.post("/api/transcribe-text", json = fake)

    assert response.status_code == 200
    data = response.json()
    note_id = data['note_id']

    from backend.app.api.transcription_route import note_cache

    assert note_id in note_cache

    note_data = note_cache[note_id]

    assert note_data['transcription'] == "test"
    assert 'structured_data' in note_data
    assert 'created_at' in note_data
    assert 'expires_at' in note_data

