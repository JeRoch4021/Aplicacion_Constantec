from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
#from Models.security import cifrar_contrasena
from Models.models import Estudiantes, Solicitudes, Constancias, ConstanciaOpciones
from datetime import date, datetime
from Autenticacion.seguridad import get_password_hash
from sqlalchemy.orm import joinedload
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

from enum import Enum

class SolicitudEstatus(Enum):
    PENDIENTE = 1
    REVISION = 2  
    COMPLETO = 3


# def crear_estudiante(db: Session, estudiante: schemas.EstudianteBase):
#     estudiante_dict = estudiante.model_dump()
#     estudiante_dict['Contrasena'] = cifrar_contrasena(estudiante_dict['Contrasena'])  # Cifrar la contraseña
#     db_estudiante = models.Estudiantes(**estudiante_dict)

#     db.add(db_estudiante)
#     db.commit()
#     db.refresh(db_estudiante)
#     return db_estudiante


# Métodos para los endpoints de estudiantes

def obtener_estudiante_por_no_control(db: Session, no_control: str):
    return db.query(Estudiantes).filter(Estudiantes.no_control == no_control).first()

def actualizar_contrasena(db: Session, no_control: str, nueva_contrasena: str):
    estudiante = obtener_estudiante_por_no_control(db, no_control)
    
    if estudiante:
        estudiante.Contrasena = get_password_hash(nueva_contrasena)
        estudiante.Primer_Ingreso = False

        db.commit()
        # db.refresh(estudiante)
        print(estudiante)
        return estudiante
    return None

def listar_estudiantes(db: Session):
    return db.query(Estudiantes).all()


# Métodos para el endpoint de constancias

def crear_solicitud(db: Session, id_estudiante: int, descripcion: str, otros: str, tipos_ids: list[int]):
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
        )

        db.add(nueva_solicitud)
    except Exception as ex:
        logger.debug(ex)
        db.rollback()
        raise HTTPException(status_code=500, detail="Ocurrio un error al generar la solicitud de la constancia");
    finally:
        db.commit()

    return nueva_solicitud

def obtener_estado_constancia(db: Session, id_solicitud: str):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).order_by(Solicitudes.Fecha_Solicitud.desc()).first()
    if solicitud:
        return solicitud.Estado
    return None


def actualizar_estado_solicitud(db: Session, id_solicitud:str, nuevo_estado: str):
    solicitud = db.query(Solicitudes).filter(Solicitudes.id == id_solicitud).first()
    if solicitud:
        estado_anterior = solicitud.Estado
        solicitud.Estado = nuevo_estado

        # Registrar el cambio en el historial
        # historial = HistorialSolicitud(
        #     ID_Historial = f"HIST-{id_solicitud}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        #    .id = id_solicitud,
        #     Estado_Anterior = estado_anterior,
        #     Estado_Actual = nuevo_estado,
        #     Fecha_Cambio = date.today()
        # )
        # db.add(historial)
        db.commit()
        db.refresh(solicitud)
        # db.refresh(historial)
        return solicitud
    return None


def obtener_solicitudes(db: Session, estudiante_id: str):
    solicitudes = db.query(Solicitudes).options(joinedload(Solicitudes.estatus)).filter(Solicitudes.estudiantes_id == estudiante_id).all()
    return solicitudes

    
