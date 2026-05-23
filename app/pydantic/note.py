from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Literal
from datetime import datetime, date


class Note(BaseModel):
    id: Optional[int] = Field(default = None, description = "Unique identifier for the note")
    preop_diagnosis: Optional[str] = Field(default = None, description = "Preoperative diagnosis")
    postop_diagnosis: Optional[str] = Field(default = None, description = "Postoperative diagnosis")
    anesthesia: Optional[str] = Field(default = None, description="Type of anesthesia")
    date_of_dictation: Optional[date] = Field(default = date.today(), description="Date of dictation")
    date_of_procedure: Optional[date] = Field(default = None, description="Date of the procedure")

    @field_validator('date_of_dictation', 'date_of_procedure')
    @classmethod
    def validate_dates(cls, v):
        if v is None:
            return None
        if v and v > date.today():
            raise ValueError("Dates cannot be in the future")
        if v and v < date(2000, 1, 1):
            raise ValueError("Dates cannot be before January 1, 2000")
        return v
    @model_validator(mode = 'after')
    def validate_date_order(self):
        if (
            self.date_of_dictation and self.date_of_procedure and self.date_of_dictation < self.date_of_procedure
        ):
            self.date_of_dictation = None
            self.date_of_procedure = None
        return self

        
    procedures: List[Optional[str]] = Field(default = None, description="The name of the procedure")
    procedure_description: Optional[str] = Field(default = None, description="Description of the operative procedure")
    ebl: Optional[float] = Field(default = None, description="The estimated blood loss")
    specimens: Optional[str] = Field(default = None, description="Any specimens collected during the procedure")

