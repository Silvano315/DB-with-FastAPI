from datetime import datetime
from typing import Optional
from sqlmodel import Field
from uuid import UUID
from .base import BaseModel

class VitalSigns(BaseModel, table=True):
    patient_id: UUID = Field(foreign_key="patient.id")
    measured_at: datetime
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    measured_by_id: UUID = Field(foreign_key="user.id")
    notes: Optional[str] = None