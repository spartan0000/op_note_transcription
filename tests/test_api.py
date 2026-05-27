import pytest
from unittest.mock import AsyncMock, patch


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
        assert "note_id" in data
        assert mock_extract.called
