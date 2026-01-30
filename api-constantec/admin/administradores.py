
from sqladmin import ModelView

# TODO: ¿Por qué no puedo integrar los stubs de wtforms instaladors en mi ruta:
# /Users/jeroch/.asdf/installs/python/3.12.7/lib/python3.12/site-packages?
from wtforms import PasswordField  # type: ignore

from autenticacion.seguridad import get_password_hash
from models.admin import Administradores


class UserAdmin(ModelView):
    model = Administradores
    name = "Usuario"
    name_plural = "Usuarios"

    column_list = [
        Administradores.id,
        Administradores.username,
        Administradores.is_active,
        Administradores.fecha_creacion,
    ]

    form_overrides = {
        "password": PasswordField,
    }

    column_labels = {Administradores.password: "Contraseña"}

    async def on_model_change(self, data, model, is_created, request):
        # Extraer la contraseña del diccionario de datos del formulario
        password_plana = data.get("password")

        if password_plana:
            # Ciframos la contraseña
            password_cifrada = get_password_hash(password_plana)

            # Actualizamos el valor cifrado de la contraseña en el modelo
            # y diccionario data
            model.password = password_cifrada
            data["password"] = password_cifrada
        elif is_created:
            # Si es un diccionario nuevo y no hay contraseña,
            # lanzamos un error manual para evitar el IntegrityError
            # de SQL Server
            raise Exception("La contraseña es obligatoria para nuevos registros")

        return await super().on_model_change(data, model, is_created, request)
