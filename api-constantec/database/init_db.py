import logging
import os

from sqlalchemy import create_engine

from models.tables import (
    Base,
)

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def init_db():
    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas sincronizadas exitosamente en PostgreSQL")
    except Exception as e:
        logger.warning(f"Error al inicializar la base de datos: {e}")
