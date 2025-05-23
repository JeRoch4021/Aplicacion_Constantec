from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Database.database import Base


class Estudiantes(Base):
    __tablename__ = "Estudiantes"
    
    No_Control = Column(String(20), primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Apellidos = Column(String(100), nullable=False)
    Fecha_Nacimiento = Column(Date, nullable=False)
    Edad = Column(Integer, nullable=False)
    Municipio = Column(String(100), nullable=False)
    Correo_Institucional = Column(String(150), unique=True, nullable=False)
    Fecha_Registro = Column(Date, nullable=False)
    Contrasena = Column(String(255), nullable=False)
    Primer_Ingreso = Column(Boolean, default=True)

    solicitudes = relationship("Solicitud", back_populates="estudiante")


class Constancia(Base):
    __tablename__ = "Constancias"

    ID_Constancia = Column(String(10), primary_key=True, index=True)
    Tipo = Column(String(100), nullable=False)
    Descripcion = Column(String, nullable=False)
    Requisitos = Column(String, nullable=False)

    solicitudes = relationship("Solicitud", back_populates="constancia")


class Solicitud(Base):
    __tablename__ = "Solicitudes"

    ID_Solicitud = Column(String(10), primary_key=True, index=True)
    No_Control = Column(String(10), ForeignKey("Estudiantes.No_Control"), nullable=False)
    ID_Constancia = Column(String(10), ForeignKey("Constancias.ID_Constancia"), nullable=False)
    Fecha_Solicitud = Column(Date, nullable=False)
    Estado = Column(String(50), nullable=False)
    Fecha_Entrega = Column(Date, nullable=True)
    ID_Trabajador = Column(String(10), ForeignKey("Trabajadores.ID_Trabajador"), nullable=False)

    estudiante = relationship("Estudiantes", back_populates="solicitudes")
    constancia = relationship("Constancia", back_populates="solicitudes")
    trabajador = relationship("Trabajador", back_populates="solicitudes")
    historial = relationship("HistorialSolicitud", back_populates="solicitud")


class HistorialSolicitud(Base):
    __tablename__ = "Historial_Solicitudes"

    ID_Historial = Column(String(10), primary_key=True, index=True)
    ID_Solicitud = Column(String(10), ForeignKey("Solicitudes.ID_Solicitud"), nullable=False)
    Estado_Anterior = Column(String(50), nullable=False)
    Estado_Actual = Column(String(50), nullable=False)
    Fecha_Cambio = Column(Date, nullable=False)

    solicitud = relationship("Solicitud", back_populates="historial")


class Trabajador(Base):
    __tablename__ = "Trabajadores"

    ID_Trabajador = Column(String(10), primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Apellidos = Column(String(100), nullable=False)
    Fecha_Nacimiento = Column(Date, nullable=False)
    Edad = Column(Integer, nullable=False)
    Cargo = Column(String(100), nullable=False)
    Telefono = Column(String(20), nullable=False)
    Correo_Institucional = Column(String(150), unique=True, nullable=False)
    Fecha_Inicio = Column(Date, nullable=False)

    solicitudes = relationship("Solicitud", back_populates="trabajador")