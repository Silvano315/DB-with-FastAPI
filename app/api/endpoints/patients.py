from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from app.api.deps import get_current_user, get_db
from app.models.patient import Patient
from app.models.user import User, UserRole
from app.core.audit import AuditLog

router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("/", response_model=List[Patient])
async def read_patients(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(
        get_current_user,
        scopes=["admin", "doctor", "nurse"]
    ),
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    search: Optional[str] = None
) -> List[Patient]:
    """
    Retrieve patients with pagination and optional search.
    
    Args:
        db: Database session
        current_user: Authenticated user
        skip: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search term for patient name
        
    Returns:
        List[Patient]: List of patient records
    """
    query = select(Patient)
    
    if current_user.role == UserRole.DOCTOR:
        query = query.where(Patient.primary_doctor_id == current_user.id)

    if search:
        query = query.where(
            (Patient.first_name.ilike(f"%{search}%")) |
            (Patient.last_name.ilike(f"%{search}%"))
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.exec(query)
    patients = result.scalars().all()

    audit = AuditLog(db)
    await audit.log_action(
        user_id=current_user.id,
        action="READ",
        resource_type="Patient",
        details={"search": search, "skip": skip, "limit": limit}
    )
    
    return patients

@router.post("/", response_model=Patient)
async def create_patient(
    *,
    db: AsyncSession = Depends(get_db),
    patient: Patient,
    current_user: User = Security(
        get_current_user,
        scopes=["admin", "doctor"]
    )
) -> Patient:
    """
    Create a new patient record.
    
    Args:
        db: Database session
        patient: Patient data
        current_user: Authenticated user
        
    Returns:
        Patient: Created patient record
    """
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    
    audit = AuditLog(db)
    await audit.log_action(
        user_id=current_user.id,
        action="CREATE",
        resource_type="Patient",
        resource_id=patient.id
    )
    
    return patient

@router.get("/{patient_id}", response_model=Patient)
async def read_patient(
    *,
    db: AsyncSession = Depends(get_db),
    patient_id: UUID,
    current_user: User = Security(
        get_current_user,
        scopes=["admin", "doctor", "nurse"]
    )
) -> Patient:
    """
    Retrieve a specific patient by ID.
    
    Args:
        db: Database session
        patient_id: UUID of the patient
        current_user: Authenticated user
        
    Returns:
        Patient: Patient record
        
    Raises:
        HTTPException: If patient not found or user lacks permission
    """
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    if (current_user.role == UserRole.DOCTOR and
        patient.primary_doctor_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this patient"
        )
    
    audit = AuditLog(db)
    await audit.log_action(
        user_id=current_user.id,
        action="READ",
        resource_type="Patient",
        resource_id=patient_id
    )
    
    return patient