from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from urllib.parse import quote_plus
import pyodbc

# Funciona para comprobar el tipo de Driver que se tiene instalado
print(pyodbc.drivers())

server = 'localhost,1434'
database = 'Seguimiento_Constancias'
username = 'SA'
password = 'JeshuaSQL21'
driver = 'ODBC Driver 18 for SQL Server'


    # params = quote_plus(
    #         f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};"
    #         f"TrustServerCertificate=YES;Encrypt=YES"
    #     )

    # database_url = f'mssql+pyodbc:///?odbc_connect={params}'

database_url = f'mssql+pyodbc://SA:{password}@localhost,1434/{database}?driver{driver}'

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

try:
    with engine.connect() as connexion: 
        print("Conexión exitosa a la base de datos")

except Exception as ex:
    print("Error al conectar la base de datos: ", ex)


