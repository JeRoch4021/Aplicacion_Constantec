from sqladmin import ModelView

from models.tables import Trabajador


class TrabajadorAdmin(ModelView, model = Trabajador): # type: ignore
    name = "Trabajador"
    name_plural = "Trabajadores"

    column_list = [Trabajador.id, Trabajador.nombre, Trabajador.apellidos, Trabajador.correo_institucional]

    form_columns = [Trabajador.id, Trabajador.nombre, Trabajador.apellidos, Trabajador.correo_institucional]
