from pydantic import BaseModel
from datetime import date

class EstudianteBase(BaseModel):
    ID_Estudiante: str
    Nombre: str
    Apellidos: str
    Fecha_Nacimiento: date
    Edad: int
    Municipio: str
    Correo_Institucional: str
    Fecha_Registro: date

class EstudiantesLogin(BaseModel):
    No_Control: str
    Contrasena: str

class EstudiantesSalida(BaseModel):
    class Config:
        orm_mode = True