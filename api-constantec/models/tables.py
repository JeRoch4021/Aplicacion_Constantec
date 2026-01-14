from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# Tabla de estudiantes del ITL
class Estudiantes(Base):
    __tablename__ = "estudiantes"
    
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    no_control = Column(String(20), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    semestre = Column(Integer, nullable=False)
    carrera = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    correo_institucional = Column(String(150), unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    solicitudes = relationship("Solicitudes", back_populates="estudiante", cascade="all, delete")

# Tabla de tipos de constancia
class ConstanciaTipos(Base):
    __tablename__ = "constancia_tipos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=False)

# Tabla de opciones de constancia
class ConstanciaOpciones(Base):
    __tablename__ = "constancia_opciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    constancia_id = Column(Integer, ForeignKey("constancias.id"), nullable=False)
    constancias_tipo_id = Column(Integer, ForeignKey("constancia_tipos.id"), nullable=False)

    tipo = relationship("ConstanciaTipos", backref="opciones")

# Tabla de constancias
class Constancias(Base):
    __tablename__ = "constancias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String(100), nullable=True)
    otros = Column(String(100), nullable=True)

    solicitudes = relationship("Solicitudes", back_populates="constancia")
    opciones = relationship("ConstanciaOpciones", backref="constancia")

# Tabla de estatus de solicitudes 
class SolicitudEstatus(Base):
    __tablename__ = "solicitud_estatus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=False)

    solicitudes = relationship("Solicitudes", back_populates="estatus")

    def __str__(self):
        return f"{self.tipo} - {self.descripcion}"

# Tabla de solicitudes
class Solicitudes(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    estudiantes_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    constancia_id = Column(Integer, ForeignKey("constancias.id"), nullable=False)
    solicitud_estatus_id = Column(Integer, ForeignKey("solicitud_estatus.id"), nullable=False)
    fecha_solicitud = Column(Date, nullable=False, default= lambda: datetime.now().date())
    fecha_entrega = Column(Date, nullable=True)
    trabajador_id = Column(String(30), ForeignKey("trabajadores.id_trabajador"), nullable=True)
    folio = Column(String(100), nullable=False)

    estudiante = relationship("Estudiantes", back_populates="solicitudes")
    constancia = relationship("Constancias", back_populates="solicitudes")
    estatus = relationship("SolicitudEstatus", back_populates="solicitudes")
    trabajador = relationship("Trabajador", back_populates="solicitudes")
 
# Tabla de trabajador
class Trabajador(Base):
    __tablename__ = "trabajadores"

    id_trabajador = Column(String(30), primary_key=True, index=True, unique=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    cargo = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo_institucional = Column(String(150), unique=True, nullable=False)
    fecha_inicio = Column(Date, nullable=False)

    solicitudes = relationship("Solicitudes", back_populates="trabajador")

    def __str__(self):
        return f"{self.id_trabajador}"

# Tabla de encuestas
class EncuestaSatisfaccion(Base):
    __tablename__ = "encuesta_satisfaccion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    calificacion = Column(Integer, nullable=False)
    sugerencia = Column(String(500), nullable=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), unique=True, nullable=True)

    estudiante = relationship("Estudiantes")

class ComprobantesPago(Base):
    __tablename__ = "comprobantes_pago"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    factura = Column(String(255), nullable=False)
    estado_validacion = Column(String(50), nullable=False) #default="SIN_COMPROBANTE")
    motivo_rechazo = Column(String(255), nullable=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    
    estudiante = relationship("Estudiantes")