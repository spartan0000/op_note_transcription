from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column


from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    preop_diagnosis: Mapped[str] = mapped_column(String, nullable=True)
    postop_diagnosis: Mapped[str] = mapped_column(String, nullable=True)
    anesthesia: Mapped[str] = mapped_column(String, nullable=True)
    date_of_dictation: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    date_of_procedure: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    procedures: Mapped[list[str]] = mapped_column(JSONB, nullable=True)
    procedure_description: Mapped[str] = mapped_column(String, nullable=True)
    ebl: Mapped[float] = mapped_column(Float, nullable=True)
    specimens: Mapped[str] = mapped_column(String, nullable=True)

