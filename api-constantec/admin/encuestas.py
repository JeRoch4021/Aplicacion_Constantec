from sqladmin import ModelView

from models.tables import EncuestaSatisfaccion


class EncuestasAdmin(ModelView):
    model = EncuestaSatisfaccion
    name = "Encuestas de Estudiantes"
    name_plural = "Encuestas de Estudiantes"

    column_list = [EncuestaSatisfaccion.id, EncuestaSatisfaccion.id_estudiante, EncuestaSatisfaccion.calificacion, EncuestaSatisfaccion.sugerencia]

    form_columns = [EncuestaSatisfaccion.id, EncuestaSatisfaccion.id_estudiante, EncuestaSatisfaccion.calificacion, EncuestaSatisfaccion.sugerencia]
