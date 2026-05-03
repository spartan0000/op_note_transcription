from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime, date

class Note(BaseModel):
    id: Optional[int] = Field(default = None, description = "Unique identifier for the note")
    preop_diagnosis: Optional[str] = Field(default = None, description = "Preoperative diagnosis")
    postop_diagnosis: Optional[str] = Field(default = None, description = "Postoperative diagnosis")
    anesthesia: Optional[str] = Field(default = None, description="Type of anesthesia")
    date_of_dicatation: Optional[date] = Field(default = date.today(), description="Date of dictation")
    date_of_procedure: Optional[date] = Field(default = None, description="Date of the procedure")
    procedures: List[Optional[str]] = Field(default = None, description="The name of the procedure")
    procedure_description: Optional[str] = Field(default = None, description="Description of the operative procedure")
    ebl: Optional[float] = Field(default = None, description="The estimated blood loss")
    specimens: Optional[str] = Field(default = None, description="Any specimens collected during the procedure")

