from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Models.security import cifrar_contrasena
from Models.models import Solicitud, Constancia, HistorialSolicitud
from Models import models
from Schemas import schemas
from datetime import date


def crear_estudiante(db: Session, estudiante: schemas.EstudianteBase):
    estudiante_dict = estudiante.model_dump()
    estudiante_dict['Contrasena'] = cifrar_contrasena(estudiante_dict['Contrasena'])  # Cifrar la contraseña
    db_estudiante = models.Estudiantes(**estudiante_dict)

    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

def obtener_estudiante_por_no_control(db: Session, no_control: str):
    return db.query(models.Estudiantes).filter(models.Estudiantes.No_Control == no_control).first()

def obtener_estudiante_por_id(db: Session, id_estudiante: str):
    return db.query(models.Estudiantes).filter(models.Estudiantes.ID_Estudiante == id_estudiante).first()

def actualizar_contrasena(db: Session, no_control: str, nueva_contrasena: str):
    estudiante = obtener_estudiante_por_no_control(db, no_control)
    if estudiante:
        estudiante.Contrasena = nueva_contrasena
        estudiante.Primer_Ingreso = False
        db.commit()
        db.refresh(estudiante)
        return estudiante
    return None

def listar_estudiantes(db: Session):
    return db.query(models.Estudiantes).all()

def registrar_solicitud(db: Session, id_estudiante: str, id_constancia: str, id_trabajador: str):
    nueva_solicitud = Solicitud(
        ID_Solicitud = f"SQL-{id_estudiante}-{id_constancia}-{int(date.today().strftime('%Y%m%d'))}",
        ID_Esdiante = id_estudiante,
        ID_Constancia = id_constancia,
        Fecha_Solicitud = date.today(),
        Estado = "Pendiente",
        ID_Trabajador = id_trabajador
    )
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud

def obtener_estado_constancia(db: Session, id_constancia: str):
    solicitud = db.query(Solicitud).filter(Solicitud.ID_Constancia == id_constancia).order_by(Solicitud.Fecha_Solicitud.desc()).first()
    if solicitud:
        return solicitud.Estado
    return None

def actualizar_estado_constancia(db: Session, id_solicitud:str, nuevo_estado: str):
    solicitud = db.query(Solicitud).filter(Solicitud.ID_Solicitud == id_solicitud).first()
    if solicitud:
        estado_anterior = solicitud.Estado
        solicitud.Estado = nuevo_estado
        db.commit()
        db.refresh(solicitud)

        # Registrar el cambio en el historial
        historial = HistorialSolicitud(
            ID_Historial = f"HIST-{id_solicitud}-{int(date.today().strftime('%Y%m%d%H%M%S'))}",
            ID_Solicitud = id_solicitud,
            Estado_Anterior = estado_anterior,
            Estado_Actual = nuevo_estado,
            Fecha_Cambio = date.today()
        )
        db.add(historial)
        db.commit()
        db.refresh(historial)
        return solicitud
    return None

def consultar_historial_solicitudes(db: Session, id_estudiante: str):
    solicitudes = db.query(Solicitud).filter(Solicitud.ID_Estudiante == id_estudiante).all()
    return solicitudes

    
