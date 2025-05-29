from sqlalchemy.orm import Session
from sqlalchemy import update
#from Models.security import cifrar_contrasena
from Models.models import Estudiantes, Solicitudes, Constancias
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

def crear_constancia(db: Session, tipo: str, descripcion: str, requisitos: str):
    # 1. crear constancia y guardar el id
    # 2. insertar todos los constancia opciones por cada opcion q selecciono el usuario
    # 3. insertar en solicitudes
    nueva_constancia = Constancias(
        Tipo = tipo,
        Descripcion = descripcion,
        Requisitos = requisitos
    )
    db.add(nueva_constancia)
    db.commit()
    db.refresh(nueva_constancia)
    return nueva_constancia


# Metodos para endpoints de solicitudes

def crear_solicitud(db: Session, no_control: str, id_constancia: str, fecha_folicitud: date, estado: str, fecha_entrega: date, id_trabajador: str):
    try:
        nueva_solicitud = Solicitudes(
            No_Control = no_control,
            ID_Constancia = id_constancia,
            Fecha_Solicitud = fecha_folicitud,
            Estado = estado,
            Fecha_Entrega = fecha_entrega,
            ID_Trabajador = id_trabajador
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

    
