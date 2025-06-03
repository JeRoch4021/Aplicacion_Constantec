from datetime import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from database.connection import Base
from fastapi_admin.models import AbstractAdmin as BaseAdminModel
from sqlalchemy import Column, Integer, String, Boolean

# Base = declarative_base()


class Estudiantes(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    no_control = Column(String(20), index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False)
    municipio = Column(String(100), nullable=False)
    correo_institucional = Column(String(150), unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    contrasena = Column(String(255), nullable=False)
    primer_ingreso = Column(Boolean, default=True)

    solicitudes = relationship(
        "Solicitudes", back_populates="estudiante", cascade="all, delete"
    )


class ConstanciaTipos(Base):
    __tablename__ = "constancia_tipos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=False)


class ConstanciaOpciones(Base):
    __tablename__ = "constancia_opciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    constancia_id = Column(Integer, ForeignKey("constancias.id"), nullable=False)
    constancias_tipo_id = Column(
        Integer, ForeignKey("constancia_tipos.id"), nullable=False
    )

    tipo = relationship("ConstanciaTipos", backref="opciones")


class Constancias(Base):
    __tablename__ = "constancias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String(100), nullable=True)
    otros = Column(String(100), nullable=True)

    solicitudes = relationship("Solicitudes", back_populates="constancia")
    opciones = relationship("ConstanciaOpciones", backref="constancia")


class SolicitudEstatus(Base):
    __tablename__ = "solicitud_estatus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=False)

    solicitudes = relationship("Solicitudes", back_populates="estatus")


class Solicitudes(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    estudiantes_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    constancia_id = Column(Integer, ForeignKey("constancias.id"), nullable=False)
    solicitud_estatus_id = Column(
        Integer, ForeignKey("solicitud_estatus.id"), nullable=False
    )
    fecha_solicitud = Column(
        Date, nullable=False, default=lambda: datetime.now().date()
    )
    fecha_entrega = Column(Date, nullable=True)
    # trabajador_id = Column(String(30), ForeignKey("trabajadores.id_trabajador"), nullable=False)

    estudiante = relationship("Estudiantes", back_populates="solicitudes")
    constancia = relationship("Constancias", back_populates="solicitudes")
    estatus = relationship("SolicitudEstatus", back_populates="solicitudes")
    # trabajador = relationship("Trabajador", back_populates="solicitudes")


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

    # solicitudes = relationship("Solicitud", back_populates="trabajador")


class AdminUser(Base, BaseAdminModel):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"{self.username}"