from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging

# server = 'localhost,1434'
# database = 'Seguimiento_Constancias'
# username = 'SA'
# password = 'Jeshua21SQL'
driver = 'ODBC Driver 18 for SQL Server'

DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', '')

logging.debug(f"""
    DB_HOST: {DB_HOST}
    DB_PORT: {DB_PORT}
    DB_USER: {DB_USER}
    DB_PASSWORD: {DB_PASSWORD}
    DB_NAME: {DB_NAME}
             """)

database_url = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    f"?driver={driver.replace(' ', '+')}&TrustServerCertificate=yes&Encrypt=yes"
    )
engine = None

try:
    engine = create_engine(database_url)
except Exception as e:
    logging.debug(e)

logging.debug(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

try:
    with engine.connect() as connexion: 
        print("Conexión exitosa a la base de datos")

except Exception as ex:
    print("Error al conectar la base de datos: ", ex)


