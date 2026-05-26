import pytest

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database.connection import get_db, SessionLocal, engine


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
    
@pytest.fixture(scope="function")
def db_session():

    connection = engine.connect()
    transaction = connection.begin()

    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()