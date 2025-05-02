#import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# Funciona para comprobar el tipo de Driver que se tiene instalado
#print(pyodbc.drivers())

server = 'localhost,1434'
database = 'Seguimiento_Constancias'
username = 'SA'
password = 'JeshuaSQL21'
driver = 'ODBC Driver 18 for SQL Server'

try:

    params = quote_plus(
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};"
        f"TrustServerCertificate=YES;Encrypt=YES"
    )

    DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

    print("Conexión exitosa")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
except Exception as ex:
    print(ex)



