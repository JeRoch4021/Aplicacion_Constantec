from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

server = 'localhost,1434'
database = 'Seguimiento_Constancias'
username = 'SA'
password = 'Jeshua21SQL'
driver = 'ODBC Driver 18 for SQL Server'

database_url = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}"
    f"?driver={driver.replace(' ', '+')}&TrustServerCertificate=yes&Encrypt=yes"
    )

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

try:
    with engine.connect() as connexion: 
        print("Conexión exitosa a la base de datos")

except Exception as ex:
    print("Error al conectar la base de datos: ", ex)


