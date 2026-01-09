from wtforms import PasswordField
from autenticacion.seguridad import get_password_hash
from models.common import Estudiantes
from sqladmin import ModelView

class EstudiantesAdmin(ModelView, model=Estudiantes):
    name = "Estudiante"
    name_plural = "Estudiantes"

    column_list = [Estudiantes.id, Estudiantes.no_control, Estudiantes.nombre, Estudiantes.apellidos]
    form_columns = [Estudiantes.no_control, Estudiantes.nombre, Estudiantes.apellidos, Estudiantes.contrasena]

    form_overrides = {
        "contrasena": PasswordField,
    }

    async def on_model_change(self, data, model, is_created, request):
        # Cifrar la contraseña antes de guardar el estudiante
        if 'contrasena' in data:
            model.contrasena = get_password_hash(data['contrasena'])   

        return await super().on_model_change(data, model, is_created, request)