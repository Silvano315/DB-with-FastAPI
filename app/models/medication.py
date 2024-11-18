from datetime import date
from typing import Optional
from sqlmodel import Field
from uuid import UUID
from .base import BaseModel

class Medication(BaseModel, table=True):
    patient_id: UUID = Field(foreign_key="patient.id")
    name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    prescribed_by_id: UUID = Field(foreign_key="user.id")
    is_active: bool = True
    notes: Optional[str] = None