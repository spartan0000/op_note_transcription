from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float, List
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="user")


class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    preop_diagnosis: Mapped[str] = mapped_column(String, nullable=True)
    postop_diagnosis: Mapped[str] = mapped_column(String, nullable=True)
    anesthesia: Mapped[str] = mapped_column(String, nullable=True)
    date_of_dictation: Mapped[DateTime] = mapped_column(datetime, nullable=True)
    date_of_procedure: Mapped[DateTime] = mapped_column(datetime, nullable=True)
    procedures: Mapped[list[str]] = mapped_column(JSONB, nullable=True)
    procedure_description: Mapped[str] = mapped_column(String, nullable=True)
    ebl: Mapped[float] = mapped_column(Float, nullable=True)
    specimens: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    user: Mapped["User"] = relationship("User", back_populates="reports")