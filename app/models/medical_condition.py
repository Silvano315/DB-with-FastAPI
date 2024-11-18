from enum import Enum
from datetime import date
from typing import Optional
from sqlmodel import Field
from uuid import UUID
from .base import BaseModel

class ConditionCategory(str, Enum):
    CARDIOVASCULAR = "cardiovascular"
    NEURODEGENERATIVE = "neurodegenerative"
    FRAILTY = "frailty"

class Severity(str, Enum):
    FIT = 'fit'
    MILDLY = "mildly"
    MODERATELY = "moderately"
    SEVERELY = "severely"

class MedicalCondition(BaseModel, table = True):
    patient_id: UUID = Field(foreign_key="patient.id")
    category: ConditionCategory
    name: str
    diagnosis_date: date
    severity: Severity
    diagnosing_doctor_id: UUID = Field(foreign_key="user.id")
    notes: Optional[str] = None
    treatment_plan: Optional[str] = None