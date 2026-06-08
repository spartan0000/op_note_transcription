from backend.app.main import app
from backend.app.database.connection import get_db, TestSessionLocal, test_engine
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from backend.app.database.models import Base

from backend.app.database.models import Report, User

from backend.app.api.login_route import RegisterRequest

def test_user_registration(client, db_session):
    registration = RegisterRequest(
        username = 'santa',
        email = 'santa@northpole.co',
        password = 'abcd1234' 
    )

    response = client.post("/api/register")

    assert response.status_code == 200

    data = response.json()

    user_id = data['user_id']

    assert user_id is not None