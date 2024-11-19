import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.core.security import SecurityConfig
from app.models.user import User, UserRole
from app.main import app

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Test user creation"""
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
    
    stmt = select(User).where(User.username == "testdoctor")
    result = await db_session.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    assert db_user is not None
    assert db_user.username == "testdoctor"
    assert db_user.role == UserRole.DOCTOR

@pytest.mark.asyncio
async def test_user_authentication(db_session: AsyncSession):  
    """Test user authentication endpoint"""
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

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/token", 
            data={
                "username": "testdoctor",
                "password": "testpass123",
                "grant_type": "password" 
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"