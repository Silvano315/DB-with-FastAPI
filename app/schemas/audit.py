from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

class AuditEntry(BaseModel):
    """
    Schema for audit log entries.
    
    Attributes:
        id: Unique identifier for the audit entry
        user_id: ID of the user who performed the action
        action: Type of action performed
        resource_type: Type of resource affected
        resource_id: ID of the specific resource affected
        details: Additional details about the action
        timestamp: When the action occurred
    """
    id: UUID
    user_id: UUID
    action: str
    resource_type: str
    resource_id: Optional[UUID] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime