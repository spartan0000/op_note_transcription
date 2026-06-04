from backend.app.main import app
from backend.app.database.connection import get_db, TestSessionLocal, test_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.models import Base

from backend.app.database.models import Report

def test_create_report(client, db_session, test_user):
    payload = {
        'preop_diagnosis': 'test diagnosis',
        'user_id': test_user.id
    }

    response = client.post("/api/reports", json = payload)

    assert response.status_code == 200

    data = response.json()

    assert "id" in data

    report_id = data['id']

    report = db_session.query(Report).filter_by(id = report_id).first()

    assert report is not None
    assert report.preop_diagnosis == 'test diagnosis'
    assert report.user_id == test_user.id

def test_invalid_user_id(client, db_session):
    payload = {
        'preop_diagnosis': 'test',
        'user_id': 9999
    }

    response = client.post("/api/reports", json = payload)

    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == "User not found"

