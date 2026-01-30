from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.tables import Base


class Administradores(Base):
    __tablename__ = "usuarios_administradores"

    # Definición de columnas con Mapped para soporte total de MyPy
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[date] = mapped_column(Date, nullable=False)
