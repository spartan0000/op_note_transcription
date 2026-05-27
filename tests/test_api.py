def test_create_note(client):
    response = client.post("/transcribe-text", json={"transcript": "This is a test transcript."})
    assert response.status_code == 200

    data = response.json()
    assert "note_id" in data