from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from crud import crud_estudiante
from models.tables import EncuestaSatisfaccion
from paquetes import schemas
from autenticacion.seguridad import get_current_user
from typing import Any

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.EncuestaSatisfaccionSalida)
def guardar_encuesta(data_encuesta: schemas.EncuestaSatisfaccionCreate , db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    encuesta = crud_estudiante.guardar_encuesta(db, data_encuesta.estudiante_id, data_encuesta.calificacion, data_encuesta.sugerencia)
    return encuesta

@router.get("/verificar/{estudiante_id}")
def verificar_encuesta(estudiante_id: int, db: Session = Depends(get_db)):
    existe = db.query(EncuestaSatisfaccion).filter(EncuestaSatisfaccion.estudiante_id == estudiante_id).first()
    return {"completada": existe is not None}