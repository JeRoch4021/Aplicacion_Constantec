import logging
# import os

# import pyodbc
from sqlalchemy import text
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from database.connection import APPLICATION_DB_URL, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, engine, Base, DB_DRIVER, DB_USER


logger = logging.getLogger(__name__)

MASTER_DB_URL = f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/master?driver={DB_DRIVER}&Encrypt=no&TrustServerCertificate=yes"

# def create_database_if_not_exists():
#     database_url = (
#         f"mssql+pyodbc://SA:{DB_PASSWORD}@{DB_HOST}/master"
#         f"?driver={driver}&TrustServerCertificate=yes&Encrypt=yes"
#     )

#     with pyodbc.connect(database_url, autocommit=True) as conn:
#         cursor = conn.cursor()
#         cursor.execute(f"IF DB_ID(N'{DB_NAME}') IS NULL CREATE DATABASE [{DB_NAME}]")
#         cursor.close()
#         logger.info("Base de datos creada!!!!!")


# def init_db():
#     Base = declarative_base()
#     create_database_if_not_exists()
#     database_url = (
#         f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#         f"?driver={driver}&TrustServerCertificate=yes&Encrypt=yes"
#     )
#     engine = create_engine(database_url)
#     Base.metadata.create_all(bind=engine)


async def initialize_database():
    master_engine = create_async_engine(MASTER_DB_URL, isolation_level="AUTOCOMMIT")
    # Base = declarative_base()

    try:
        async with master_engine.connect() as connection:
            # Check if the database exists
            result = await connection.execute(
                text(f"SELECT name FROM sys.databases WHERE name = :db_name"),
                {"db_name": DB_NAME}
            )
            database_exists = result.scalar_one_or_none() is not None

            if not database_exists:
                logger.info(f"Database '{DB_NAME}' does not exist. Creating...")
                await connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
                logger.info(f"Database '{DB_NAME}' created successfully.")
            else:
                logger.info(f"Database '{DB_NAME}' already exists.")

    except sqlalchemy.exc.DBAPIError as e:
        print(f"Error while trying to ensure database '{DB_NAME}' exists: {e}")
        # Depending on the error, you might want to raise it or handle it differently
        # For example, if connection to master fails, the app likely can't start.
        raise
    finally:
        await master_engine.dispose() # Close the temporary engine

    
