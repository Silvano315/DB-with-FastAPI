from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class BaseModel(SQLModel):
    id : UUID = Field(default_factory=uuid4, primary_key=True)
    created_at : datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=datetime.now(timezone.utc))
    is_active : bool = Field(default=True)