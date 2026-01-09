from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from CRUD import crud_estudiante
from database.connection import SessionLocal
from models.common import Constancias
from Schemas import schemas

router = APIRouter()


# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/crear-constancia", response_model=schemas.ConstanciaSalida)
def registrar_constancia(data: schemas.ConstanciaBase, db: Session = Depends(get_db)):
    constancia = crud_estudiante.crear_constancia(
        db, data.Tipo, data.Descripcion, data.Requisitos
    )
    return constancia


@router.get("/", response_model=list[schemas.ConstanciaSalida])
def listar_constancias(db: Session = Depends(get_db)):
    return db.query(Constancias).all()


@router.get("/{id_constancia}", response_model=schemas.ConstanciaSalida)
def buscar_constancia(id_constancia: str, db: Session = Depends(get_db)):
    constancia = (
        db.query(Constancias).filter(Constancias.ID_Constancia == id_constancia).first()
    )
    if not constancia:
        raise HTTPException(detial="Constancia no encontrada", status_code=404)
    return constancia
