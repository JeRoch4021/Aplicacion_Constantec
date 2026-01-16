from sqlalchemy.orm import Session
from models.admin import Administradores

# Métodos para los endpoints de estudiantes

def obtener_administrador_por_id(db: Session, username: str):
    return db.query(Administradores).filter(Administradores.username == username).first()
