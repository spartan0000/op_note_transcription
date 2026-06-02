from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from backend.app.services import functions

import uuid

from datetime import datetime, timedelta

from backend.app.database.connection import get_db


router = APIRouter(tags=['database'])

