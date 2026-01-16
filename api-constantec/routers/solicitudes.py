from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from consultas.consulta_estudiante import crear_solicitud, estado_solicitud, actualizar_estado_solicitud, historial_solicitudes
from paquetes import schemas
from models.tables import Solicitudes, Constancias, ConstanciaOpciones
from sqlalchemy.orm import joinedload
import logging
from autenticacion.seguridad import get_current_user
from typing import Any

logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SolicitudRequestSchema)
def registrar_solicitud(data_constancia: schemas.CrearConstanciaRequest, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):

    if (getattr(data_constancia, "descripcion", None) is None or len(data_constancia.descripcion) == 0 ):
        raise HTTPException(status_code=400, detail="No se puede crear una solicitud sin descripcion")

    solicitud = crear_solicitud(
        db, data_constancia.id_estudiante, 
        data_constancia.descripcion, 
        data_constancia.otros, 
        data_constancia.constancia_opciones, 
        data_constancia.folio
        )

    response = db.query(Solicitudes).options(
        joinedload(Solicitudes.estudiante),
        joinedload(Solicitudes.constancia)
            .joinedload(Constancias.opciones)
            .joinedload(ConstanciaOpciones.tipo),
        joinedload(Solicitudes.estatus),
    ).filter(Solicitudes.id == solicitud.id).first()

    return response

@router.post("/estado")
def estado (data: schemas.SolicitudEstado, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estado = estado_solicitud(db, data.id_solicitud)
    if not estado:
        raise HTTPException(detail="Constancia no encontrada", status_code=404)
    return {"Estado: ": estado}

@router.put("/nuevo_estado")
def actualizar_estado(data: schemas.SolicitudNuevoEstado, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    solicitud = actualizar_estado_solicitud(db, data.id_solicitud, data.nuevo_estado)
    if not solicitud:
        raise HTTPException(detail="Solicitud no encontrada", status_code=404)
    return {"mensaje": f"Estado actualizado a {data.nuevo_estado}"}

@router.get("/{id_estudiante}", response_model=list[schemas.SolicitudResponseSchema])
def historial (id_estudiante: int, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    return historial_solicitudes(db, id_estudiante)

@router.get("/datos_solicitud", response_model=list[schemas.SolicitudResponseSchema])
def listar_solicitudes(db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    return db.query(Solicitudes).options(
        joinedload(Solicitudes.estatus),
        joinedload(Solicitudes.estudiante),
        joinedload(Solicitudes.constancia)
            .joinedload(Constancias.opciones)
            .joinedload(ConstanciaOpciones.tipo),
        joinedload(Solicitudes.trabajador)
    ).all()

@router.delete("/{id_solicitud}", status_code=status.HTTP_200_OK)
def eliminar_solicitud(id_solicitud: int, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).first()

    if not solicitud:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La solicitud con ID {id_solicitud} no existe."
        )

    db.delete(solicitud)
    db.commit()
    return {"Solicitud borrada correctamente"}