from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager

from .config import settings

# Create database URL for SQLAlchemy
# Convert standard postgres:// URL to postgresql+asyncpg:// for async operation
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create base class for declarative models
Base = declarative_base()

@asynccontextmanager
async def get_db():
    """
    Get a database session as an async context manager.
    This function provides a database session and ensures it is closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Database initialization function
async def init_db():
    """
    Initialize the database by creating all tables.
    This is called during application startup.
    """
    async with engine.begin() as conn:
        # Drop all tables (only in development mode)
        if settings.DEBUG:
            # await conn.run_sync(Base.metadata.drop_all)
            pass
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
