from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager

from .config import settings

# Create database URL for SQLAlchemy (asyncpg)
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
    """Provide a transactional scope around a series of operations."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Note: commit is typically handled within the service layer
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Database initialization function
async def init_db():
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        # In a real app, consider using Alembic for migrations instead of create_all
        # await conn.run_sync(Base.metadata.drop_all) # Use with caution
        await conn.run_sync(Base.metadata.create_all)
