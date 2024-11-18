from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema for access token response.
    
    Attributes:
        access_token: The JWT token string
        token_type: The type of token (usually "bearer")
    """
    access_token : str
    token_type : str

class TokenData(BaseModel):
    """
    Schema for decoded token data.
    
    Attributes:
        username: The username extracted from the token
        scopes: List of permission scopes for the user
    """
    username : Optional[str] = None
    scopes : list[str] = []

class SecurityConfig:
    """
    Configuration class for security settings.
    
    This class handles all security-related configurations including
    JWT settings, password hashing, and token generation.
    """
    SECRET_KEY: str = "your-secret-key-stored-in-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: The password in plain text
            hashed_password: The hashed password to compare against
            
        Returns:
            bool: True if passwords match, False otherwise
        """
        SecurityConfig.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: The plain text password to hash
            
        Returns:
            str: The hashed password
        """
        SecurityConfig.pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: The data to encode in the token
            expires_delta: Optional expiration time override
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp" : expire})
        encoded_jwt = jwt.encode(
            to_encode,
            SecurityConfig.SECRET_KEY,
            algorithm=SecurityConfig.ALGORITHM
        )
        return encoded_jwt