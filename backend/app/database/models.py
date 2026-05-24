from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column


from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
