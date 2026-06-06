from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from datetime import datetime, timedelta

from pwdlib import PasswordHasher


import jwt

from backend.app.main import app



