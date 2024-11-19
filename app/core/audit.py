from typing import Any, Dict, Optional
from datetime import datetime, timezone
from sqlmodel import Session
from uuid import UUID
from app.schemas.audit import AuditEntry

class AuditLog:
    """
    Class for handling audit logging of system actions.
    
    This class provides methods to log and track all significant
    actions performed in the system for compliance and security purposes.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize audit logger.
        
        Args:
            db_session: SQLModel session for database operations
        """
        self.db_session = db_session

    async def log_action(
        self,
        user_id: UUID,
        action: str,
        resource_type: str,
        resource_id: Optional[UUID] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an action in the audit trail.
        
        Args:
            user_id: ID of the user performing the action
            action: Type of action performed (e.g., "CREATE", "READ", "UPDATE", "DELETE")
            resource_type: Type of resource being acted upon
            resource_id: Optional ID of the specific resource
            details: Optional additional details about the action
        """
        audit_entry = AuditEntry(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            timestamp=datetime.now(timezone.utc)
        )
        self.db_session.add(audit_entry)
        await self.db_session.commit()