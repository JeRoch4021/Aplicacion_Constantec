from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
#from Models.security import cifrar_contrasena
from Models.models import Estudiantes, Solicitudes, Constancias, ConstanciaOpciones, Trabajador, EncuestaSatisfaccion
from datetime import date, datetime
from Autenticacion.seguridad import get_password_hash
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)

from enum import Enum

class SolicitudEstatus(Enum):
    PENDIENTE = 1
    REVISION = 2  
    COMPLETO = 3


def obtener_estudiante_por_no_control(db: Session, no_control: str):
    return db.query(Estudiantes).filter(Estudiantes.no_control == no_control).first()

def actualizar_contrasena(db: Session, no_control: str, nueva_contrasena: str):
    estudiante = obtener_estudiante_por_no_control(db, no_control)
    
    if estudiante:
        estudiante.contrasena = get_password_hash(nueva_contrasena)
        estudiante.primer_ingreso = False

        db.commit()
        # db.refresh(estudiante)
        print(estudiante)
        return estudiante
    return None

def listar_estudiantes(db: Session):
    return db.query(Estudiantes).all()


# Métodos para el endpoint de constancias

def crear_solicitud(db: Session, id_estudiante: int, descripcion: str, otros: str, tipos_ids: list[int], folio: str):
    try:
        nueva_constancia = Constancias(
            descripcion = descripcion,
            otros = otros
        )
        
        db.add(nueva_constancia)
        db.flush()
        
        for tipo_id in tipos_ids:
            opcion = ConstanciaOpciones(
                constancia_id = nueva_constancia.id,
                constancias_tipo_id = tipo_id
            )
            db.add(opcion)

        nueva_solicitud = Solicitudes(
            estudiantes_id = id_estudiante,
            constancia_id = nueva_constancia.id,
            solicitud_estatus_id = SolicitudEstatus.PENDIENTE.value,
            trabajador_id = "TFR093",
            folio = folio
        )

        db.add(nueva_solicitud)
    except Exception as ex:
        logger.debug(ex)
        db.rollback()
        raise HTTPException(status_code=500, detail="Ocurrio un error al generar la solicitud de la constancia");
    finally:
        db.commit()

    return nueva_solicitud

def obtener_estado_constancia(db: Session, id_solicitud: int):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).order_by(Solicitudes.fecha_solicitud.desc()).first()
    if solicitud:
        return solicitud.estatus
    return None


def actualizar_estado_solicitud(db: Session, id_solicitud:int, nuevo_estado: int):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).first()
    if solicitud:
        solicitud.solicitud_estatus_id = nuevo_estado
        solicitud.notificacion = None
        solicitud.fecha_entrega = None
        if nuevo_estado in [SolicitudEstatus.REVISION.value]:
            solicitud.fecha_entrega = date.today()
        elif nuevo_estado in [SolicitudEstatus.COMPLETO.value]:
            solicitud.fecha_entrega = date.today()
            solicitud.notificacion = "Vaya a ventanilla a recoger su constancia"
        db.commit()
        db.refresh(solicitud)
        return solicitud
    return None


def obtener_solicitudes(db: Session, estudiante_id: int):
    solicitudes = db.query(Solicitudes).options(joinedload(Solicitudes.estatus)).filter(Solicitudes.estudiantes_id == estudiante_id).all()
    return solicitudes

    
def guardar_encuesta (db: Session, id_estudiante: int, calificacion: int):
    nueva_encuesta = EncuestaSatisfaccion(
        estudiante_id = id_estudiante,
        calificacion = calificacion
    )

    db.add(nueva_encuesta)
    db.commit()
    db.refresh(nueva_encuesta)
    return nueva_encuesta