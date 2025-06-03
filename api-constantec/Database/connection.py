import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# from Models.models import Base

logger = logging.getLogger(__name__)

DB_DRIVER = "ODBC Driver 18 for SQL Server".replace(' ', '+')

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
    # Base.metadata.create_all(engine)
    # with engine.connect() as connexion:
    #     logger.info("Conexión exitosa a la base de datos")
except Exception as e:
    logger.warning("Error al conectar la base de datos: ", e)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session