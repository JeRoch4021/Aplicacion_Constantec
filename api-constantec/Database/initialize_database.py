import logging

import sqlalchemy
from fastapi import Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from autenticacion.seguridad import get_password_hash
from database.connection import (
    DB_DRIVER,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    Base,
    engine,
    get_async_db,
)
from database.decorators import with_async_session
from models.admin import AdminUser
from models.common import *

logger = logging.getLogger(__name__)

MASTER_DB_URL = f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/master?driver={DB_DRIVER}&Encrypt=no&TrustServerCertificate=yes"


@with_async_session
async def create_admin_user(db: AsyncSession):
    try:
        AdminUserQuery = select(AdminUser).where(AdminUser.username == "admin")
        result = await db.execute(AdminUserQuery)

        admin_exists = result.scalar_one_or_none()

        if admin_exists is None:
            hashed_pwd = get_password_hash("test")
            new_admin = AdminUser(
                username="admin", password=hashed_pwd, is_superuser=True
            )
            db.add(new_admin)
            logger.info("Admin user created.")
        else:
            logger.info("Admin user already exists.")
    except sqlalchemy.exc.DBAPIError as e:
        logger.error(f"Error while trying to create admin user '{DB_NAME}': {e}")
        raise


async def create_tables_in_database():
    try:
        async with engine.begin() as connection:
            logger.info(f"Checking and creating tables for database '{DB_NAME}'...")
            # await connection.run_sync(Base.metadata.create_all)
            await connection.run_sync(
                lambda sync_conn: Base.metadata.create_all(
                    bind=sync_conn, checkfirst=True
                )
            )
            logger.info(f"Tables for database '{DB_NAME}' are ensured to exist.")
    except sqlalchemy.exc.DBAPIError as e:
        logger.error(
            f"Error while trying to create tables in database '{DB_NAME}': {e}"
        )
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error while trying to ensure tables in database '{DB_NAME}': {e}"
        )
        raise
    finally:
        await engine.dispose()


async def create_database():
    master_engine = create_async_engine(MASTER_DB_URL, isolation_level="AUTOCOMMIT")

    try:
        async with master_engine.connect() as connection:

            query_result = await connection.execute(
                text(f"SELECT name FROM sys.databases WHERE name = :db_name"),
                {"db_name": DB_NAME},
            )

            database_exists = query_result.scalar_one_or_none() is not None

            if not database_exists:
                logger.info(f"Database '{DB_NAME}' does not exist. Creating...")
                await connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
                logger.info(f"Database '{DB_NAME}' created successfully.")
            else:
                logger.info(f"Database '{DB_NAME}' already exists.")

    except sqlalchemy.exc.DBAPIError as e:
        logger.error(f"Error while trying to ensure database '{DB_NAME}' exists: {e}")
        raise
    finally:
        await master_engine.dispose()
