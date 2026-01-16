from models.tables import Trabajador
from sqladmin import ModelView

class TrabajadorAdmin(ModelView, model=Trabajador):
    name = "Trabajador"
    name_plural = "Trabajadores"

    column_list = [Trabajador.id,
                   Trabajador.nombre,
                   Trabajador.apellidos,
                   Trabajador.correo_institucional]
    
    form_columns = [Trabajador.id,
                    Trabajador.nombre,
                    Trabajador.apellidos,
                    Trabajador.correo_institucional]