from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field, Relationship
from sqlalchemy import DateTime
from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    
class Gender(str, Enum):
    """Patient gender enumeration."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class BloodType(str, Enum):
    """Blood type enumeration."""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class Patient(BaseModel, table=True):
    """Patient model with complete medical information."""
    __tablename__ = "patients"

    fiscal_code: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    
    last_visit_date: Optional[datetime] = Field(
        default=None,
        sa_column=DateTime(timezone=True)
    )
    
    primary_doctor_id: Optional[UUID] = Field(
        default=None,
        foreign_key="users.id"
    )
    primary_doctor: Optional["User"] = Relationship(
        back_populates="patients",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        """String representation of the patient."""
        return f"Patient(id={self.id}, name={self.first_name} {self.last_name})"

    @property
    def full_name(self) -> str:
        """Get patient's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Calculate patient's current age."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < 
            (self.date_of_birth.month, self.date_of_birth.day)
        )