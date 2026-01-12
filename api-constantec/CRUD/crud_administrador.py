from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
#from Models.security import cifrar_contrasena
from models.admin import Administradores
from datetime import date, datetime
from autenticacion.seguridad import get_password_hash
from sqlalchemy.orm import joinedload
import logging

# Métodos para los endpoints de estudiantes

def obtener_administrador_por_id(db: Session, username: str):
    return db.query(Administradores).filter(Administradores.username == username).first()
