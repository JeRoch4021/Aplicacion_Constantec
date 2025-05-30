from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from CRUD import crud_estudiante
from Schemas import schemas
from Models.models import Solicitudes
from sqlalchemy.orm import joinedload
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SolicitudRequestSchema)
def registrar_solicitud(data_constancia: schemas.CrearConstanciaRequest, db: Session = Depends(get_db)):

    if (getattr(data_constancia, "descripcion", None) is None or len(data_constancia.descripcion) == 0 ):
        raise HTTPException(status_code=400, detail="No se puede crear una solicitud sin descripcion")

    solicitud = crud_estudiante.crear_solicitud(db, data_constancia.id_estudiante, data_constancia.descripcion, data_constancia.otros, data_constancia.constancia_opciones)

    response = db.query(Solicitudes).options(
        joinedload(Solicitudes.estudiante),
        joinedload(Solicitudes.constancia),
        joinedload(Solicitudes.estatus),
    ).filter(Solicitudes.id == solicitud.id).first()

    return response

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

@router.get("/{id_estudiante}", response_model=list[schemas.SolicitudResponseSchema])
def historial_estudiante(id_estudiante: str, db: Session = Depends(get_db)):
    return crud_estudiante.obtener_solicitudes(db, id_estudiante)