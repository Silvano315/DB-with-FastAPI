from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text

class DatabaseConfig:
    """Database configuration settings."""
    POSTGRES_USER: str = "silvanoquarto"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "healthcare_db"
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """Generate database URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

db_config = DatabaseConfig()

engine = create_async_engine(
    db_config.SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
    poolclass=NullPool
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    """
    Initialize database with all models.
    
    Sets timezone to UTC and creates all tables.
    """
    async with engine.begin() as conn:
        await conn.execute(text('SET TIME ZONE "UTC"'))
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session.
    
    Yields:
        AsyncSession: Database session for async operations
    """
    async with async_session() as session:
        try:
            await session.execute(text('SET TIME ZONE "UTC"'))
            yield session
        finally:
            await session.close()

async def cleanup_db() -> None:
    """
    Cleanup database by dropping all tables.
    
    Used primarily for testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)