import logging
from datetime import date
from enum import Enum

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from autenticacion.seguridad import get_password_hash
from models.tables import (
    ConstanciaOpciones,
    Constancias,
    EncuestaSatisfaccion,
    Estudiantes,
    Solicitudes,
)

logger = logging.getLogger(__name__)


class SolicitudEstatus(Enum):
    PENDIENTE = 1
    REVISION = 2
    COMPLETO = 3


# Métodos para los endpoints de estudiantes


def obtener_estudiante_por_no_control(db: Session, no_control: str):
    return db.query(Estudiantes).filter(Estudiantes.no_control == no_control).first()


def actualizar_contrasena(db: Session, no_control: str, nueva_contrasena: str):
    estudiante = obtener_estudiante_por_no_control(db, no_control)

    if estudiante:
        estudiante.contrasena = get_password_hash(nueva_contrasena)
        estudiante.primer_ingreso = False

        db.commit()
        print(estudiante)
        return estudiante
    return None


# Métodos para el endpoint de constancias


def crear_solicitud(db: Session, id_estudiante: int, descripcion: str, otros: str, tipos: list[int], folio: int):
    try:
        nueva_constancia = Constancias(descripcion=descripcion, otros=otros)

        db.add(nueva_constancia)
        db.flush()

        for id_tipo in tipos:
            opcion = ConstanciaOpciones(id_constancia=nueva_constancia.id, id_constancias_tipo=id_tipo)
            db.add(opcion)

        nueva_solicitud = Solicitudes(
            id_estudiantes=id_estudiante, id_constancia=nueva_constancia.id, id_solicitud_estatus=SolicitudEstatus.PENDIENTE.value, id_trabajador=1, folio=folio
        )

        db.add(nueva_solicitud)
    except Exception as ex:
        logger.debug(ex)
        db.rollback()
        raise HTTPException(status_code=500, detail="Ocurrio un error al generar la solicitud de la constancia")
    finally:
        db.commit()

    return nueva_solicitud


def estado_solicitud(db: Session, id_solicitud: int):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).order_by(Solicitudes.fecha_solicitud.desc()).first()
    if solicitud:
        return solicitud.estatus
    return None


def actualizar_estado_solicitud(db: Session, id_solicitud: int, nuevo_estado: int):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).first()
    if solicitud:
        solicitud.id_solicitud_estatus = nuevo_estado
        solicitud.fecha_entrega = None
        if nuevo_estado in [SolicitudEstatus.REVISION.value]:
            solicitud.fecha_entrega = date.today()
        elif nuevo_estado in [SolicitudEstatus.COMPLETO.value]:
            solicitud.fecha_entrega = date.today()
        db.commit()
        db.refresh(solicitud)
        return solicitud
    return None


def historial_solicitudes(db: Session, id_estudiante: int):
    solicitudes = db.query(Solicitudes).options(joinedload(Solicitudes.estatus)).filter(Solicitudes.id_estudiantes == id_estudiante).all()
    return solicitudes


def guardar_encuesta_estudiante(db: Session, id_estudiante: int, calificacion: int, sugerencia: str):
    nueva_encuesta = EncuestaSatisfaccion(id_estudiante=id_estudiante, calificacion=calificacion, sugerencia=sugerencia)

    db.add(nueva_encuesta)
    db.commit()
    db.refresh(nueva_encuesta)
    return nueva_encuesta
