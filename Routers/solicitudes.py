from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from CRUD import crud_estudiante
from Schemas import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SolicitudSalida)
def registrar_solicitud(solicitud: schemas.CrearSolicitud, db: Session = Depends(get_db)):
    return crud_estudiante(db, solicitud)

@router.get("/estado")
def obtener_estado_constancia(id_estudiante: str, id_constancia: str, db: Session = Depends(get_db)):
    estado = crud_estudiante.obtener_estado_constancia(db, id_estudiante, id_constancia)
    if not estado:
        raise HTTPException(detail="Constancia no encontrada", status_code=404)
    return {"estado actual": estado}

@router.put("/actualizar-estado")
def actualizar_estado(id_solicitud: str, nuevo_estado: str, db: Session = Depends(get_db)):
    solicitud = crud_estudiante.actualizar_estado_constancia(db, id_solicitud, nuevo_estado)
    if not solicitud:
        raise HTTPException(detail="Solicitud no encontrada", status_code=404)
    return {"mensaje": f"Estado actualizado a {nuevo_estado}"}

@router.get("/historial/{id_estudiante}", response_model=list[schemas.HistorialSolicitudSalida])
def historial_estudiante(id_estudiante: str, db: Session = Depends(get_db)):
    return crud_estudiante.consultar_historial_solicitudes(db, id_estudiante)