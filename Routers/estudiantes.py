from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from CRUD import crud_estudiante
from Schemas import schemas

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=schemas.EstudiantesSalida)
def login(data: schemas.EstudiantesLogin, db: Session = Depends(get_db)):
    estudiante = crud_estudiante.obtener_estudiante_por_no_control(db, data.No_Control)
    if not estudiante or estudiante.Contrasena != data.Contrasena:
        raise HTTPException (detail="Credenciales invalidas", status_code=401)
    return estudiante

@router.put("/cambiar-contrasena", response_model=schemas.EstudiantesSalida)
def cambiar_contrasena(no_control: str, nueva_contrasena: str, db: Session = Depends(get_db)):
    estudiante_actualizado = crud_estudiante.actualizar_contrasena(db, no_control, nueva_contrasena)
    if not estudiante_actualizado:
        raise HTTPException (detail="Estudiante no encontrado", status_code=404)
    return estudiante_actualizado

@router.get("/perfil/{id_estudiante}", response_model=schemas.EstudiantesSalida)
def obtener_perfil(id_estudiante: str, db: Session = Depends(get_db)):
    estudiante = crud_estudiante.obtener_estudiante_por_id(db, id_estudiante)
    if not estudiante:
        raise HTTPException (detail="Estudiante no encontrado", status_code=404)
    return estudiante

