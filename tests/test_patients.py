from datetime import date, datetime, timezone
import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.models.patient import Patient, Gender
from app.models.user import User
from app.main import app

@pytest.mark.asyncio
async def test_create_patient(db_session: AsyncSession, test_user: User):
    """Test patient creation"""
    patient = Patient(
        fiscal_code="TEST123456",
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1950, 1, 1),
        gender=Gender.MALE.value,
        primary_doctor_id=test_user.id
    )
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)
    
    stmt = select(Patient).where(Patient.fiscal_code == "TEST123456")
    result = await db_session.execute(stmt)
    db_patient = result.scalar_one_or_none()
    
    assert db_patient is not None
    assert db_patient.first_name == "John"
    assert db_patient.last_name == "Doe"

@pytest.mark.asyncio
async def test_get_patient(db_session: AsyncSession, test_user: User, test_patient: Patient):
    """Test patient retrieval"""
    stmt = select(Patient).where(Patient.fiscal_code == "TEST123456")
    result = await db_session.execute(stmt)
    db_patient = result.scalar_one_or_none()
    
    assert db_patient is not None
    assert db_patient.first_name == "John"
    assert db_patient.last_name == "Doe"
    assert db_patient.primary_doctor_id == test_user.id