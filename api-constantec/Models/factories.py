import datetime
import factory
from factory.alchemy import SQLAlchemyModelFactory
#from sqlalchemy import create_engine
from models.tables import Estudiantes
from models.admin import Administradores
from database.connection import SessionLocal
from autenticacion.seguridad import get_password_hash

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
    semestre = factory.Faker("random_int", min=1, max=9)
    carrera = factory.Faker("word")
    municipio = factory.Faker("city")
    correo_institucional = factory.LazyAttribute(lambda obj: f"{obj.no_control.lower().replace(" ", "_")}@leon.tecnm.mx")
    fecha_registro = factory.LazyFunction(datetime.date.today)
    password = get_password_hash('test')
    is_active = True

class AdminFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Administradores
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    username = factory.Faker("name")
    password = get_password_hash('test')
    is_active = True
    fecha_creacion = factory.LazyFunction(datetime.date.today)
