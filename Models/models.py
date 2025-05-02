from sqlalchemy import Column, String, Integer, Date, Boolean
from Database.database import Base

class Estudiantes(Base):
    __tablename__ = 'Estudiantes'
    ID_Estudiante = Column(String(10), primary_key=True, index=True)
    No_Control = Column(String(20), unique=True, index=True)
    Nombre = Column(String(100))
    Apellidos = Column(String(100))
    Fecha_Nacimiento = Column(Date)
    Edad = Column(Integer)
    Municipio = Column(String(100))
    Correo_Institucional = Column(String(150))
    Fecha_Registro = Column(Date)
    Contrasena = Column(String(255))
    Primer_Ingreso = Column(Boolean, default=True)

