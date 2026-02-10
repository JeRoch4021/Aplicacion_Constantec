from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Tabla de estudiantes del ITL
class Estudiantes(Base):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    no_control: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)
    carrera: Mapped[str] = mapped_column(String(100), nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False)
    correo_institucional: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    fecha_registro: Mapped[date] = mapped_column(Date, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    solicitudes: Mapped[List["Solicitudes"]] = relationship("Solicitudes", back_populates="estudiante", cascade="all, delete")


# Tabla de tipos de constancia
class ConstanciaTipos(Base):
    __tablename__ = "constancia_tipos"

    # Definición de columnas con Mapped
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship as a List
    opciones: Mapped[List["ConstanciaOpciones"]] = relationship("ConstanciaOpciones", back_populates="tipo")


# Tabla de opciones de constancia
class ConstanciaOpciones(Base):
    __tablename__ = "constancia_opciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    # Claves foráneas tipadas
    id_constancia: Mapped[int] = mapped_column(ForeignKey("constancias.id"), nullable=False)
    id_constancias_tipo: Mapped[int] = mapped_column(ForeignKey("constancia_tipos.id"), nullable=False)

    tipo: Mapped["ConstanciaTipos"] = relationship("ConstanciaTipos", back_populates="opciones")

    constancia: Mapped["Constancias"] = relationship("Constancias", back_populates="opciones")


# Tabla de constancias
class Constancias(Base):
    __tablename__ = "constancias"

    # Columnas tipadas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    # "otros" es nullable=True, por lo que usamos Optional en el tipado
    otros: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    solicitudes: Mapped[List["Solicitudes"]] = relationship("Solicitudes", back_populates="constancia")

    opciones: Mapped[List["ConstanciaOpciones"]] = relationship("ConstanciaOpciones", back_populates="constancia")


# Tabla de estatus de solicitudes
class SolicitudEstatus(Base):
    __tablename__ = "solicitud_estatus"

    # Columnas tipadas para MyPy
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relación inversa: Un estatus puede estar en muchas solicitudes
    # Usamos List["Solicitudes"] para que MyPy sepa que es una colección
    solicitudes: Mapped[List["Solicitudes"]] = relationship("Solicitudes", back_populates="estatus")

    def __str__(self) -> str:
        # El type hint -> str ayuda a MyPy a validar vistas de admin
        return f"{self.tipo} - {self.descripcion}"


# Tabla de solicitudes
class Solicitudes(Base):
    __tablename__ = "solicitudes"

    # Columnas con Mapped
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    # Claves foráneas
    id_estudiantes: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"), nullable=False)
    id_constancia: Mapped[int] = mapped_column(ForeignKey("constancias.id"), nullable=False)
    id_solicitud_estatus: Mapped[int] = mapped_column(ForeignKey("solicitud_estatus.id"), nullable=False)

    # Usamos default de Python directamente en mapped_column
    fecha_solicitud: Mapped[date] = mapped_column(Date, nullable=False, default=lambda: datetime.now().date())

    # Campos opcionales (pueden ser None en la DB)
    fecha_entrega: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    id_trabajador: Mapped[Optional[int]] = mapped_column(ForeignKey("trabajadores.id"), nullable=True)

    folio: Mapped[str] = mapped_column(String(100), nullable=False)

    estudiante: Mapped["Estudiantes"] = relationship("Estudiantes", back_populates="solicitudes")
    constancia: Mapped["Constancias"] = relationship("Constancias", back_populates="solicitudes")
    estatus: Mapped["SolicitudEstatus"] = relationship("SolicitudEstatus", back_populates="solicitudes")
    trabajador: Mapped["Trabajador"] = relationship("Trabajador", back_populates="solicitudes")


# Tabla de trabajador
class Trabajador(Base):
    __tablename__ = "trabajadores"

    # Mapped[tipo] define el tipo para Python/MyPy
    # mapped_column define la configuración de la base de datos
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    cargo: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    correo_institucional: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)

    # Para las relaciones, usamos Mapped[List["Clase"]]
    solicitudes: Mapped[List["Solicitudes"]] = relationship("Solicitudes", back_populates="trabajador")

    def __str__(self) -> str:
        return f"{self.id} - {self.nombre} {self.apellidos}"


# Tabla de encuestas
class EncuestaSatisfaccion(Base):
    __tablename__ = "encuesta_satisfaccion"

    # Definición de columnas con Mapped
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    calificacion: Mapped[int] = mapped_column(Integer, nullable=False)
    sugerencia: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Claves foráneas
    id_estudiante: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"), nullable=True)

    # Relación Many-to-One
    # Usamos Optional porque un estudiante puede ser nulo (encuesta anónima)
    estudiante: Mapped["Estudiantes"] = relationship("Estudiantes")


# Tabla de comprobantes
class ComprobantesPago(Base):
    __tablename__ = "comprobantes_pago"

    # Columnas con Mapped
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    factura: Mapped[str] = mapped_column(String(255), nullable=False)

    # Claves foráneas
    id_estado_comprobante: Mapped[int] = mapped_column(ForeignKey("estado_comprobante.id"), nullable=False)
    id_estudiante: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"), nullable=False)
    motivo_rechazo: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relaciones Many-to-One
    # MyPy ahora sabe que 'estudiante' siempre devolverá un objeto Estudiantes
    estudiante: Mapped["Estudiantes"] = relationship("Estudiantes")

    # Relación con EstadoComprobante
    estado: Mapped["EstadoComprobante"] = relationship("EstadoComprobante", back_populates="comprobante")


class EstadoComprobante(Base):
    __tablename__ = "estado_comprobante"

    # Columnas tipadas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relación inversa (Uno a Muchos)
    # Un estado puede estar presente en muchos comprobantes
    comprobante: Mapped[List["ComprobantesPago"]] = relationship("ComprobantesPago", back_populates="estado")

    def __str__(self) -> str:
        # Definir el retorno como str ayuda a los plugins de Admin
        return f"{self.tipo} - {self.descripcion}"
