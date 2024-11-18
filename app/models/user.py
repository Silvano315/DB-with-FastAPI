from enum import Enum
from typing import Optional
from sqlmodel import Field
from .base import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RESEARCHER = "researcher"
    # Enter new roles (e.g. PhD, neuropsychiatrist, ...)

class User(BaseModel, table = True):
    username : str = Field(unique=True, index=True)
    email : str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role : UserRole
    department : Optional[str] = None
    is_active : bool = True