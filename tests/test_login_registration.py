from backend.app.main import app
from backend.app.database.connection import get_db, TestSessionLocal, test_engine
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from backend.app.database.models import Base

from backend.app.database.models import Report, User

from backend.app.api.login_route import RegisterRequest, pwd_hasher

def test_user_registration(client, db_session):
    registration = RegisterRequest(
        username = 'santa',
        email = 'santa@northpole.co',
        password = 'abcd1234' 
    )

    response = client.post("/api/register", json = registration.model_dump())

    assert response.status_code == 200

    data = response.json()

    user_id = data['user_id']

    assert isinstance(user_id, int)

    user = db_session.get(User, user_id)

    assert user is not None
    assert user.username == registration.username
    assert user.email == registration.email
    assert user.hashed_password != registration.password
    assert pwd_hasher.verify(registration.password, user.hashed_password)

def test_duplicate_email_registration(client, db_session):
    registration = RegisterRequest(
        username = 'santaclause',
        email = 'santa@northpole.co',
        password = 'abcd1234'
    )

    client.post("/api/register", json = registration.model_dump())

    response = client.post("/api/register", json = registration.model_dump())

    assert response.status_code == 409

    data = response.json()

    assert data['detail'] == "Email already in use"

def test_duplicate_username_registration(client, db_session):
    registration1 = RegisterRequest(
        username = 'santa',
        email = 'santa@northpole.co',
        password = 'abcd1234'
    )

    registration2 = RegisterRequest(
        username = 'santa',
        email = 'santa2@northpole.co',
        password = 'abcd1234'
    )

    client.post("/api/register", json = registration1.model_dump())

    response = client.post("/api/register", json = registration2.model_dump())

    assert response.status_code == 409
    data = response.json()

    assert data['detail'] == "Username already in use"

def test_missing_registration_data(client):

    response = client.post("/api/register", json = {})

    assert response.status_code == 422

def test_invalid_email_registration(client):
    
    response = client.post("/api/register", json = {'username': 'santa', 'email': 'not-email', 'password': 'pass'})

    assert response.status_code == 422