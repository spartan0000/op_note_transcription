import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from backend.app.database.models import Base

import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST_TEST'),
    port=5432,
    database=os.getenv('DB_NAME_TEST'),
)

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST_PROD'),
    port=5432,
    database=os.getenv('DB_NAME'),
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()