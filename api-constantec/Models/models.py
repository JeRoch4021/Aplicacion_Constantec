from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Estudiantes(Base):
    __tablename__ = "estudiantes"
    
    no_control = Column(String(20), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    municipio = Column(String(100), nullable=False)
    correo_institucional = Column(String(150), unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    contrasena = Column(String(255), nullable=False)
    primer_ingreso = Column(Boolean, default=True)

    solicitudes = relationship("Solicitud", back_populates="estudiante")


class Constancia(Base):
    __tablename__ = "constancias"

    id_constancia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=False)
    requisitos = Column(String, nullable=False)

    solicitudes = relationship("Solicitud", back_populates="constancia")


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id_solicitud = Column(Integer, primary_key=True, index=True, autoincrement=True)
    no_control = Column(String(20), ForeignKey("estudiantes.no_control"), nullable=False)
    id_constancia = Column(Integer, ForeignKey("constancias.id_constancia"), nullable=False)
    fecha_solicitud = Column(Date, nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_entrega = Column(Date, nullable=True)
    id_trabajador = Column(String(30), ForeignKey("trabajadores.id_trabajador"), nullable=False)

    estudiante = relationship("Estudiantes", back_populates="solicitudes")
    constancia = relationship("Constancia", back_populates="solicitudes")
    trabajador = relationship("Trabajador", back_populates="solicitudes")
    historial = relationship("HistorialSolicitud", back_populates="solicitud")


class HistorialSolicitud(Base):
    __tablename__ = "historial_solicitudes"

    id_historial = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_solicitud = Column(Integer, ForeignKey("solicitudes.id_solicitud"), nullable=False)
    estado_anterior = Column(String(50), nullable=False)
    estado_actual = Column(String(50), nullable=False)
    fecha_cambio = Column(Date, nullable=False)

    solicitud = relationship("Solicitud", back_populates="historial")


class Trabajador(Base):
    __tablename__ = "trabajadores"

    id_trabajador = Column(String(30), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    cargo = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo_institucional = Column(String(150), unique=True, nullable=False)
    fecha_inicio = Column(Date, nullable=False)

    solicitudes = relationship("Solicitud", back_populates="trabajador")