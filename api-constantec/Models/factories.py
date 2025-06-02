import datetime
import random
import string

import factory
from Autenticacion.seguridad import get_password_hash
from database.connection import SessionLocal
from factory.alchemy import SQLAlchemyModelFactory
from Models.models import Estudiantes
from sqlalchemy import create_engine

session = SessionLocal()

class EstudiantesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Estudiantes
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    no_control = factory.Faker("bothify", text="########")
    nombre = factory.Faker("name")
    apellidos = factory.Faker("last_name")
    fecha_nacimiento = factory.Faker("date_of_birth")
    edad = factory.Faker("random_int", min=18, max=25)
    municipio = factory.Faker("city")
    correo_institucional = factory.LazyAttribute(lambda obj: f"{obj.no_control.lower().replace(" ", "_")}@leon.tecnm.mx")
    fecha_registro = factory.LazyFunction(datetime.date.today)
    contrasena = get_password_hash('test')
    primer_ingreso = False
