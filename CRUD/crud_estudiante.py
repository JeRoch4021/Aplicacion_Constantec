from sqlalchemy.orm import Session
import Models.models, Schemas.schemas

def crear_estudiante(db: Session, estudiante: Schemas.schemas.EstudianteBase):
    db_estudiante = Models.models.Estudiantes(**estudiante.dict())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

def obtener_estudiante_por_no_control(db: Session, no_control: str):
    return db.query(Models.models.Estudiantes).filter(Models.models.Estudiantes.No_Control == no_control).first()

def obtener_estudiante_por_id(db: Session, id_estudiante: str):
    return db.query(Models.models.Estudiantes).filter(Models.models.Estudiantes.ID_Estudiante == id_estudiante).first()

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
    return db.query(Models.models.Estudiantes).all()
