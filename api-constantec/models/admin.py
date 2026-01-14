from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from models.tables import Base

# Base ya importado de models.tables

class Administradores(Base):
    __tablename__ = "usuarios_administradores"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    fecha_creacion = Column(Date, nullable=False)