import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_connection():
    """Test the database connection."""
    try:
        DATABASE_URL = "postgresql+asyncpg://silvanoquarto:password@localhost:5432/healthcare_db"
        engine = create_async_engine(DATABASE_URL, echo=True)
        
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            await conn.commit()
            logger.info("✅ Database connection successful!")
            
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())