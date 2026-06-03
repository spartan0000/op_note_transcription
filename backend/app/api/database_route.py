from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from backend.app.services import functions

from sqlalchemy.orm import Session


import uuid

from datetime import datetime, timedelta

from backend.app.database.connection import get_db
from backend.app.database.models import Report
from backend.app.pydantic.note import ReportCreate, Note


router = APIRouter(tags=['database'])

@router.post("/reports")
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    report = Report(**payload.model_dump())
    db.add(report)

    db.commit()
    db.refresh(report)

    return {
        "id": report.id
    }