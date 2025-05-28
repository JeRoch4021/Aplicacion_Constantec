import datetime
import random
import string
import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import create_engine
from Models.models import Estudiantes
from Database.database import SessionLocal
from Autenticacion.seguridad import get_password_hash

session = SessionLocal()

def random_upper_alphanumeric(length=10):
    chars = string.ascii_uppercase + string.digits  # A-Z and 0-9
    return ''.join(random.choices(chars, k=length))

# Define the factory
class EstudiantesFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Estudiantes
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    no_control = factory.LazyFunction(random_upper_alphanumeric)
    nombre = factory.Faker("name")
    apellidos = factory.Faker("last_name")
    fecha_nacimiento = factory.Faker("date_of_birth")
    edad = factory.Faker("random_int", min=18, max=25)
    municipio = factory.Faker("city")
    correo_institucional = factory.LazyAttribute(lambda obj: f"{obj.nombre.lower().replace(" ", "_")}@leon.tecnm.mx")
    fecha_registro = factory.LazyFunction(datetime.date.today)
    contrasena = get_password_hash('test')
    primer_ingreso = False
