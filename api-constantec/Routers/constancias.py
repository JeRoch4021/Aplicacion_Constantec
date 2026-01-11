from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models import tables
from paquetes import schemas

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/obtener-constancias", response_model=list[schemas.ConstanciaSalida])
def listar_constancias(db: Session = Depends(get_db)):
    return db.query(tables.Constancias).all()

@router.get("/{id_constancia}", response_model=schemas.ConstanciaSalida)
def buscar_constancia(id_constancia: str, db: Session = Depends(get_db)):
    constancia = db.query(tables.Constancia).filter(tables.Constancia.ID_Constancia == id_constancia).first()
    if not constancia:
        raise HTTPException(detial="Constancia no encontrada", status_code=404)
    return constancia

