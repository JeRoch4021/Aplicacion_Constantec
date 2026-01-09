from database.connection import Base
from models.factories import EstudiantesFactory


def crear_estudiantes(numero_estudiantes: int):
    EstudiantesFactory.create_batch(5)
