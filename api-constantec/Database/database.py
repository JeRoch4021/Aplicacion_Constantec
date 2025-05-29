from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging
from .init_db import init_db
from Models.models import Base

logger = logging.getLogger(__name__)

driver = 'ODBC Driver 18 for SQL Server'

DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', '')

database_url = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    f"?driver={driver.replace(' ', '+')}&TrustServerCertificate=yes&Encrypt=yes"
    )


try:
    engine = create_engine(database_url)    
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)
    with engine.connect() as connexion: 
        logger.info("Conexión exitosa a la base de datos")
except Exception as e:
    logger.warning("Error al conectar la base de datos: ", e)

