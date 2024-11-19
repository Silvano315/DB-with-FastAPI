from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import JWTError, jwt
from uuid import UUID
from app.core.security import SecurityConfig, TokenData
from app.db.session import async_session
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "admin": "Full access to all resources",
        "doctor": "Access to assigned patients",
        "nurse": "Limited access to patient data",
        "researcher": "Anonymized data access"
    }
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for database session.
    
    Yields:
        AsyncSession: Database session for async operations
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Validate token and return current user.
    
    Args:
        security_scopes: Required permission scopes
        token: JWT token
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token,
            SecurityConfig.SECRET_KEY,
            algorithms=[SecurityConfig.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception
    
    user = await db.get(User, username=token_data.username)
    if user is None:
        raise credentials_exception
        
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
            
    return user