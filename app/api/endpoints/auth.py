from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import SecurityConfig, Token
from app.db.session import get_session
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login.
    
    Args:
        db: Database session
        form_data: OAuth2 form data with username and password
        
    Returns:
        Token: Access token if authentication successful
        
    Raises:
        HTTPException: If authentication fails
    """
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not SecurityConfig.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = SecurityConfig.create_access_token(
        data={"sub": user.username, "scopes": [user.role.value]},
        expires_delta=access_token_expires,
    )
    
    return Token(access_token=access_token, token_type="bearer")