from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import Field
from uuid import UUID
from .base import BaseModel

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class BloodType(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class Patient(BaseModel, table = True):
    # Personal Data
    fiscal_code : str = Field(unique=True, index=True)
    first_name : str
    last_name : str
    date_of_birth : date
    gender : Gender

    # Contacts
    phone : Optional[str] = None
    email : Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    
    # Medical Data Base
    blood_type: Optional[BloodType] = None
    height: Optional[float] = None  # in cm
    weight: Optional[float] = None  # in kg
    allergies: Optional[str] = None

    # Risk Indicators
    smoking: bool = False
    alcohol_consumption: bool = False
    physical_activity_level: Optional[str] = None

    # Metadata
    primary_doctor_id: Optional[UUID] = None
    last_visit_date: Optional[datetime] = None