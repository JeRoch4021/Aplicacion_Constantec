from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from consultas.consulta_estudiante import obtener_estudiante_por_no_control
from paquetes import schemas
from models.tables import Estudiantes
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

@router.get("/{no_control}", response_model=schemas.EstudiantesSalida)
def buscar_perfil(no_control: str, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estudiante = obtener_estudiante_por_no_control(db, no_control)
    if not estudiante:
        raise HTTPException (detail="Estudiante no encontrado", status_code=404)
    
    if estudiante.no_control != auth_user.get("sub"):
        raise HTTPException (detail="Numero de control no coincide con el estudiante", status_code=404)
    
    return estudiante

@router.get("/todos_estudiantes", response_model=list[schemas.EstudiantesSalida])
def listar_estudiantes (db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estudiante = db.query(Estudiantes).all()

    if not estudiante:
        raise HTTPException (detail="Estudiantes no encontrados", status_code=404)
    
    if estudiante.no_control != auth_user.get("sub"):
        raise HTTPException (detail="Numero de control no coincide con el estudiante", status_code=404)
    
    return estudiante
    


