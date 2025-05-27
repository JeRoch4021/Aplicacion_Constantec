from pydantic import BaseModel
from typing import Optional
from datetime import date

# Estudiantes

class EstudianteBase(BaseModel):
    No_Control: str
    Nombre: str
    Apellidos: str
    Fecha_Nacimiento: date
    Edad: int
    Municipio: str
    Correo_Institucional: str
    Fecha_Registro: date
    Primer_Ingreso: Optional[bool] = True

class EstudiantesLogin(BaseModel):
    No_Control: str
    Contrasena: str

class EstudiantesContrasenaUpdate(BaseModel):
    No_Control: str
    Nueva_Contrasena: str

class EstudiantesSalida(EstudianteBase):
    class Config:
        orm_mode = True

# Constancias

class ConstanciaBase(BaseModel):
    ID_Constancia: str
    Tipo: str
    Descripcion: str
    Requisitos: str

class ConstanciaSalida(ConstanciaBase):
    class Config:
        orm_mode = True

# Solicitudes

class SolicitudBase(BaseModel):
    ID_Solicitud: str
    No_Control: str
    ID_Constancia: str
    Fecha_Solicitud: date
    Estado: str
    Fecha_Entrega: Optional[date] = None
    ID_Trabajador: str

class SolicitudEstado(BaseModel):
    ID_Solicitud: str

class SolicitudNuevoEstado(BaseModel):
    ID_Solicitud: str
    Nuevo_Estado: str

class SolicitudSalida(SolicitudBase):
    class Config:
        orm_mode = True

# Historial de solicitudes

class HistorialSolicitudBase(BaseModel):
    ID_Historial: str
    ID_Solicitud: str
    Estado_Anterior: str
    Estado_Actual: str
    Fecha_Cambio: date

class HistorialSolicitudSalida(HistorialSolicitudBase):
    class Config:
        orm_mode = True

# Trabajadores

class TrabajadorBase(BaseModel):
    ID_Trabajador: str
    Nombre: str
    Apellidos: str
    Fecha_Nacimiento: date
    Edad: int
    Cargo: str
    Telefono: str
    Correo_Institucional: str
    Fecha_Inicio: date

class TrabajadorSalida(TrabajadorBase):
    class Config:
        orm_mode = True
