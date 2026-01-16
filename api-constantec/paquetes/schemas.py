from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Constancias

class CrearConstanciaRequest(BaseModel):
    descripcion: str
    otros: str
    id_estudiante: int
    constancia_opciones: list[int]
    folio: int

class ConstanciaBase(BaseModel):
    id: int
    descripcion: str
    otros: Optional[str] = None

class ConstanciaSalida(ConstanciaBase):
    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True

# Estudiantes

class EstudianteSchema(BaseModel):
    no_control: str
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    edad: int
    municipio: str
    correo_institucional: str

    class Config:
        orm_mode = True

class EstudianteBase(BaseModel):
    no_control: str
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    edad: int
    semestre: int
    carrera: str
    municipio: str
    correo_institucional: str
    fecha_registro: date
    is_active: Optional[bool] = True

class EstudiantesContrasenaUpdate(BaseModel):
    no_control: str
    nueva_password: str

class LoginRequest(BaseModel):
    usuario: str
    password: str

class EstudiantesSalida(EstudianteBase):
    class Config:
        orm_mode = True

# Trabajadores

class TrabajadorSchema(BaseModel):
    id: int
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    edad: int
    cargo: str
    telefono: str
    correo_institucional: str
    fecha_inicio: date

class TrabajadorSalida(TrabajadorSchema):
    class Config:
        orm_mode = True

# Solicitudes

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
    trabajador: TrabajadorSchema
    folio: str

    class Config:
        orm_mode = True

class SolicitudBase(BaseModel):
    id_estudiantes: int
    id_solicitud_estatus: int
    fecha_solicitud: date
    fecha_entrega: Optional[date] = None

class SolicitudEstado(BaseModel):
    id_solicitud: int

class SolicitudNuevoEstado(BaseModel):
    id_solicitud: int
    nuevo_estado: int

class SolicitudSalida(SolicitudBase):
    class Config:
        orm_mode = True

# Encuesta de Satisfaccion

class EncuestaSatisfaccionCreate(BaseModel):
    id_estudiante: int
    calificacion: int
    sugerencia: str

class EncuestaSatisfaccionSalida(BaseModel):
    id: int
    id_estudiante: int
    calificacion: int
    sugerencia: str
    
    class Config:
        orm_mode = True

# Comprobante de pago con factura

class ComprobanteSalida(BaseModel):
    id: str
    id_estudiante: str
    id_estado_comprobante: int
    motivo_rechazo: Optional[str] = None

    class Config:
        from_attributes = True  