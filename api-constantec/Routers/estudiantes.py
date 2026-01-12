from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.init_db import init_db
from crud import crud_estudiante
from paquetes import schemas
from autenticacion.seguridad import get_current_user
from typing import Any
from autenticacion.seguridad import verify_password, create_access_token
from comun.response import Response

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.put("/cambiar-contrasena", response_model=schemas.EstudiantesSalida)
# def cambiar_contrasena(data: schemas.EstudiantesContrasenaUpdate, db: Session = Depends(get_db)):
#     estudiante_actualizado = crud_estudiante.actualizar_contrasena(db, data.no_control, data.nuevo_password)
#     if not estudiante_actualizado:
#         raise HTTPException (detail="Estudiante no encontrado", status_code=404)
#     return estudiante_actualizado


@router.get("/{no_control}/", response_model=schemas.EstudiantesSalida)
def buscar_perfil(no_control: str, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estudiante = crud_estudiante.obtener_estudiante_por_no_control(db, no_control)
    if not estudiante:
        raise HTTPException (detail="Estudiante no encontrado", status_code=404)
    
    if estudiante.no_control != auth_user.get("sub"):
        raise HTTPException (detail="Numero de control no coincide con el estudiante", status_code=404)
    
    return estudiante


@router.get("/obtener-estudiantes", response_model=list[schemas.EstudiantesSalida])
def listar_estudiantes (db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estudiante = crud_estudiante.listar_estudiantes(db)

    if not estudiante:
        raise HTTPException (detail="Estudiantes no encontrados", status_code=404)
    
    if estudiante.no_control != auth_user.get("sub"):
        raise HTTPException (detail="Numero de control no coincide con el estudiante", status_code=404)
    
    return estudiante
    


