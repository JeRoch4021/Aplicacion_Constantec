from models.factories import EstudiantesFactory, AdminFactory
from database.connection import Base

def crear_estudiantes(numero_estudiantes: int):
    EstudiantesFactory.create_batch(5)

def crear_administradores(numero_administradores: int):
    AdminFactory.create_batch(5)