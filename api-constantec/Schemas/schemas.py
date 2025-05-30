from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ConstanciaTiposSchema(BaseModel):
    id: int
    tipo: str
    descripcion: str

    class Config:
        orm_mode = True

class ConstanciaOpcionesSchema(BaseModel):
    id: int
    tipo: ConstanciaTiposSchema 

    class Config:
        orm_mode = True

class ConstanciaSchema(BaseModel):
    descripcion: Optional[str] = None
    otros: Optional[str] = None
    opciones: List[ConstanciaOpcionesSchema] = []

class EstudianteSchema(BaseModel):
    no_control: str
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    edad: int
    municipio: str
    correo_institucional: str

class SolicitudEstatusSchema(BaseModel):
    id: int
    tipo: str
    descripcion: str

    class Config:
        orm_mode = True

class SolicitudRequestSchema(BaseModel):
    fecha_solicitud: date
    estatus: SolicitudEstatusSchema
    estudiante: EstudianteSchema
    constancia: ConstanciaSchema

    class Config:
        orm_mode = True

class SolicitudResponseSchema(BaseModel):
    fecha_entrega: Optional[date] = None
    fecha_solicitud: date
    estatus: SolicitudEstatusSchema
    estudiante: EstudianteSchema
    constancia: ConstanciaSchema

    class Config:
        orm_mode = True

class EstudianteBase(BaseModel):
    no_control: str
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    edad: int
    municipio: str
    correo_institucional: str
    fecha_registro: date
    primer_ingreso: Optional[bool] = True

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

class CrearConstanciaRequest(BaseModel):
    descripcion: str
    otros: str
    id_estudiante: int
    constancia_opciones: list[int]

class ConstanciaBase(BaseModel):
    Tipo: str
    Descripcion: str
    Requisitos: str

class ConstanciaSalida(ConstanciaBase):
    class Config:
        orm_mode = True

# Solicitudes

class SolicitudPost(BaseModel):
    No_Control: str
    ID_Constancia: int
    Fecha_Solicitud: date
    Estado: str
    Fecha_Entrega: Optional[date] = None
    ID_Trabajador: str

class SolicitudBase(BaseModel):
    estudiantes_id: int
    solicitud_estatus_id: int
    fecha_solicitud: date
    fecha_entrega: Optional[date] = None
    # id_trabajador: str

class SolicitudEstado(BaseModel):
    ID_Solicitud: int

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
