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

def test_multiple_reports(client, db_session, test_user):
    payload1 = {
        'preop_diagnosis': 'diagnosis 1',
        'user_id': test_user.id
    }

    payload2 = {
        'preop_diagnosis': 'diagnosis 2',
        'user_id': test_user.id
    }

    response1 = client.post("/api/reports", json = payload1)
    response2 = client.post("/api/reports", json = payload2)

    assert response1.status_code == 200
    assert response2.status_code == 200

    user_reports = db_session.query(Report).filter_by(user_id = test_user.id).all()

    assert len(user_reports) == 2
