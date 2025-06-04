import logging
import os
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

DB_DRIVER = "ODBC Driver 18 for SQL Server".replace(" ", "+")

DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")

APPLICATION_DB_URL = (
    f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    f"?driver={DB_DRIVER}&TrustServerCertificate=yes&Encrypt=no"
)


try:
    # engine = create_engine(database_url)
    engine = create_async_engine(APPLICATION_DB_URL)
    AsyncSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )
    Base = declarative_base()
except Exception as e:
    logger.warning("Error al conectar la base de datos: ", e)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_database_connection():
    # This is where you might dispose of the engine on shutdown
    print("Lifespan: Closing database connection (disposing engine)...")
    await engine.dispose()
    print("Lifespan: Database connection closed.")
