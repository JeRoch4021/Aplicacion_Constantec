from Models.factories import EstudiantesFactory
from Database.database import Base

def crear_estudiantes(numero_estudiantes: int):
    EstudiantesFactory.create_batch(5)