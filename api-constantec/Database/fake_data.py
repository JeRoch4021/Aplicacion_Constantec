from models.factories import EstudiantesFactory
from database.connection import Base

def crear_estudiantes(numero_estudiantes: int):
    EstudiantesFactory.create_batch(5)