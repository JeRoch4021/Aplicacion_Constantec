from models.common import Estudiantes
from sqladmin import ModelView

class EstudiantesAdmin(ModelView, model=Estudiantes):
    name = "Estudiante"
    name_plural = "Estudiantes"

    column_list = [Estudiantes.id, Estudiantes.no_control, Estudiantes.nombre, Estudiantes.apellidos]
    form_columns = [Estudiantes.no_control, Estudiantes.nombre, Estudiantes.apellidos]