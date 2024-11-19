import pytest
import asyncio
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import engine, async_session, init_db, cleanup_db
from app.core.security import SecurityConfig
from app.models.user import User, UserRole
from app.models.patient import Patient, Gender
from datetime import date
from sqlalchemy import text

@pytest.fixture
async def test_patient(db_session: AsyncSession, test_user: User) -> Patient:
    """
    Create a test patient.
    
    Args:
        db_session: Database session
        test_user: Test user (doctor) for the patient
        
    Returns:
        Patient: Created test patient
    """
    patient = Patient(
        fiscal_code="TEST123456",
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1950, 1, 1),
        gender=Gender.MALE,  
        primary_doctor_id=test_user.id
    )
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)
    return patient

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Setup and cleanup the database before and after each test.
    
    This fixture runs automatically for each test.
    """
    await cleanup_db()  
    await init_db()     
    yield
    await cleanup_db() 

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a test database session.
    
    Yields:
        AsyncSession: Clean database session for testing
    """
    async with async_session() as session:
        await session.execute(text('SET TIME ZONE "UTC"'))
        yield session

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """
    Create a test user.
    
    Args:
        db_session: Database session
        
    Returns:
        User: Created test user
    """
    user = User(
        username="testdoctor",
        email="doctor@test.com",
        hashed_password=SecurityConfig.get_password_hash("testpass123"),
        full_name="Test Doctor",
        role=UserRole.DOCTOR,
        department="Cardiology"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def verify_timezone(db_session: AsyncSession) -> None:
    """
    Verify that the timezone is set correctly.
    
    This is a utility fixture for debugging timezone issues.
    """
    result = await db_session.execute(text("SHOW TIME ZONE"))
    timezone = result.scalar()
    assert timezone == "UTC", f"Expected timezone to be UTC, got {timezone}"