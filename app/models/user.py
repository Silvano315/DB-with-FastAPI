from typing import TYPE_CHECKING, List, Optional
from enum import Enum
from sqlmodel import Field, Relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .patient import Patient  

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RESEARCHER = "researcher"

class User(BaseModel, table=True):
    """
    User model for authentication and authorization.
    
    Attributes:
        username: Unique username for the user
        email: Unique email address
        hashed_password: Securely hashed password
        full_name: User's full name
        role: User's role in the system
        department: Optional department affiliation
        is_active: Whether the user account is active
        patients: List of patients associated with this user (for doctors)
    """
    __tablename__ = "users"

    username: str = Field(
        unique=True, 
        index=True, 
        nullable=False,
        description="Unique username for the user"
    )
    email: str = Field(
        unique=True, 
        index=True, 
        nullable=False,
        description="Unique email address"
    )
    hashed_password: str = Field(
        nullable=False,
        description="Securely hashed password"
    )
    full_name: str = Field(
        nullable=False,
        description="User's full name"
    )
    role: UserRole = Field(
        nullable=False,
        description="User's role in the system"
    )
    department: Optional[str] = Field(
        default=None,
        description="Optional department affiliation"
    )
    is_active: bool = Field(
        default=True, 
        nullable=False,
        description="Whether the user account is active"
    )

    patients: List["Patient"] = Relationship(
        back_populates="primary_doctor",
        sa_relationship_kwargs={
            "lazy": "selectin", 
            "cascade": "all, delete-orphan"  
        }
    )

    def __repr__(self) -> str:
        """String representation of the user."""
        return f"User(id={self.id}, username={self.username}, role={self.role})"