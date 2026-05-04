import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.database.models import Base

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:",
    f"{os.getenv('DB_PASS')}@",
    f"{os.getenv('DB_HOST')}:5432/",
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bine=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()