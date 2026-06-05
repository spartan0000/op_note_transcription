from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from backend.app.services import functions

from sqlalchemy.orm import Session
from sqlalchemy import select


import uuid

from datetime import datetime, timedelta

from backend.app.database.connection import get_db
from backend.app.database.models import Report, User
from backend.app.pydantic.note import ReportCreate, Note


router = APIRouter(tags=['database'])

@router.post("/reports")
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    report = Report(**payload.model_dump())
    db.add(report)

    db.commit()
    db.refresh(report)

    return {
        "id": report.id
    }