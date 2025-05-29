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
def registrar_solicitud(data: schemas.SolicitudBase, db: Session = Depends(get_db)):
    solicitutd = crud_estudiante.crear_solicitud(db, data.ID_Solicitud, data.No_Control, data.ID_Constancia, data.Fecha_Solicitud, data.Estado, data.Fecha_Entrega, data.ID_Trabajador)
    return solicitutd

@router.post("/estado")
def obtener_estado_constancia(data: schemas.SolicitudEstado, db: Session = Depends(get_db)):
    estado = crud_estudiante.obtener_estado_constancia(db, data.ID_Solicitud)
    if not estado:
        raise HTTPException(detail="Constancia no encontrada", status_code=404)
    return {"Estado: ": estado}

@router.put("/actualizar-estado")
def actualizar_estado(data: schemas.SolicitudNuevoEstado, db: Session = Depends(get_db)):
    solicitud = crud_estudiante.actualizar_estado_solicitud(db, data.ID_Solicitud, data.Nuevo_Estado)
    if not solicitud:
        raise HTTPException(detail="Solicitud no encontrada", status_code=404)
    return {"mensaje": f"Estado actualizado a {data.Nuevo_Estado}"}

@router.get("/{id_estudiante}", response_model=list[schemas.SolicitudSchema])
def historial_estudiante(id_estudiante: str, db: Session = Depends(get_db)):
    return crud_estudiante.obtener_solicitudes(db, id_estudiante)