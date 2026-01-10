import pyodbc
import os
import logging
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

driver = 'ODBC Driver 18 for SQL Server'.replace(' ', '+')

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def create_database_if_not_exists():
    database_url = (
    f"mssql+pyodbc://SA:{DB_PASSWORD}@{DB_HOST}/master"
    f"?driver={driver}&TrustServerCertificate=yes&Encrypt=yes"
    )

    with pyodbc.connect(database_url, autocommit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(f"IF DB_ID(N'{DB_NAME}') IS NULL CREATE DATABASE [{DB_NAME}]")
        cursor.close()
        logger.info("Base de datos creada!!!!!")

def init_db():
    Base = declarative_base()
    create_database_if_not_exists()
    database_url = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        f"?driver={driver}&TrustServerCertificate=yes&Encrypt=yes"
    )
    engine = create_engine(database_url)    
    Base.metadata.create_all(bind=engine)
