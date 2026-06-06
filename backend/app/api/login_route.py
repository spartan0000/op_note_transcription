from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from datetime import datetime, timedelta

from pwdlib import PasswordHasher
from sqlalchemy import select
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

import jwt

from backend.app.main import app
from backend.app.database import get_db
from backend.app.database.models import User

load_dotenv()

class LoginRequest(BaseModel):
    email: str
    password: str

pwd_hasher = PasswordHasher()
SECRET_KEY = os.getenv("JWT_KEY")

@app.post("/api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == request.email)

    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail = "Invalid email or password")
    
    
    try:
        pwd_hasher.verify(request.password, user.hashed_password)
    except:
        raise HTTPException(status_code=401, detail = "Invalid email or password")
    
    payload = {
        "sub": str(user.id),
        "exp": datetime.now(datetime.UTC) + timedelta(hours = 24)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}