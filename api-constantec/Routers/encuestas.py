from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from crud import crud_estudiante
from paquetes import schemas

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.EncuestaSatisfaccionSalida)
def guardar_encuesta(data_encuesta: schemas.EncuestaSatisfaccionCreate , db: Session = Depends(get_db)):
    encuesta = crud_estudiante.guardar_encuesta(db, data_encuesta.estudiante_id, data_encuesta.calificacion)
    return encuesta