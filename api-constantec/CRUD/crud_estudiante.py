from sqlalchemy.orm import Session
from sqlalchemy import update
#from Models.security import cifrar_contrasena
from Models.models import Estudiantes, Solicitudes, Constancias, ConstanciaOpciones
from datetime import date, datetime
from Autenticacion.seguridad import get_password_hash
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)


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
    return db.query(Estudiantes).filter(Estudiantes.No_Control == no_control).first()

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

def crear_constancia(db: Session, id_estudiante: int, descripcion: str, otros: str, tipos_ids: list[int]):
    # 1. crear constancia y guardar el id
    # 2. insertar todos las constancia opciones por cada opcion q selecciono el usuario
    # 3. insertar en solicitudes
    nueva_constancia = Constancias(
        id_estudiante = id_estudiante,
        descripcion = descripcion,
        otros = otros
    )
    db.add(nueva_constancia)
    db.commit()
    db.refresh(nueva_constancia)

    for tipo_id in tipos_ids:
        opcion = ConstanciaOpciones(
            constancia_id = nueva_constancia.id,
            constancias_tipo_id = tipo_id

        )
        db.add(opcion)
    db.commit()

    return nueva_constancia.id


# Metodos para endpoints de solicitudes

def crear_solicitud(db: Session, estudiantes_id: int, constancia_id: int, solicitud_estatus_id: int, fecha_solicitud: date, fecha_entrega: date):
    try:
        nueva_solicitud = Solicitudes(
            estudiantes_id = estudiantes_id,
            constancia_id = constancia_id,
            solicitud_estatus_id = solicitud_estatus_id,
            fecha_solicitud = fecha_solicitud,
            fecha_entrega = fecha_entrega,
            #id_trabajador = id_trabajador
        )
        db.add(nueva_solicitud)
        db.commit()
        db.refresh(nueva_solicitud)

        return nueva_solicitud
    except Exception as ex:
        db.rollback()
        print(f"Error al crear la solicitud: {ex}")
        return None


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
    logging.debug(print(solicitudes))
    return solicitudes

    
