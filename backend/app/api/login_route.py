from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from datetime import datetime, timedelta

from pwdlib import PasswordHash
from pwdlib.exceptions import VerificationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

import jwt

from backend.app.main import app
from backend.app.database.connection import get_db
from backend.app.database.models import User

load_dotenv()

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

pwd_hasher = PasswordHash.recommended()

SECRET_KEY = os.getenv("JWT_KEY")

@app.post("/api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(
        (User.email == request.username_or_email) | (User.username == request.username_or_email)
    )

    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail = "Invalid email or password")
    
    
    try:
        pwd_hasher.verify(request.password, user.hashed_password)
    except Exception as e:
        raise HTTPException(status_code=401, detail = "Invalid email or password")
    
    payload = {
        "sub": str(user.id),
        "exp": datetime.now(datetime.UTC) + timedelta(hours = 24)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    stmt = select(User).where((User.email == request.email) | (User.username == request.username))
    existing = db.execute(stmt).scalar_one_or_none()

    

    if existing:
        if existing.email:
            raise HTTPException(status_code=409, detail = "Email already in use")
    

        if existing.username:
            raise HTTPException(status_code=409, detail = "Username already in use")
    
    hashed_password = pwd_hasher.hash(request.password)

    new_user = User(
        username = request.username,
        email = request.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }