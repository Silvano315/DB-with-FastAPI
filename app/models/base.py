from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from sqlalchemy import DateTime, func

class BaseModel(SQLModel):
    """
    Base model for all database models.
    
    Uses PostgreSQL TIMESTAMP WITH TIME ZONE for datetime fields.
    """
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    
    created_at: datetime = Field(
        sa_column=DateTime(timezone=True),
        default_factory=lambda: datetime.now()
    )
    
    updated_at: datetime = Field(
        sa_column=DateTime(timezone=True),
        default_factory=lambda: datetime.now()
    )
    
    is_active: bool = Field(default=True)

    class Config:
        """Model configuration."""
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda v: str(v)
        }
        
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()