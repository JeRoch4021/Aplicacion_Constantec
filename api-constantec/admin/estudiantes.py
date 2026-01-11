from wtforms import PasswordField
from autenticacion.seguridad import get_password_hash
from models.tables import Estudiantes
from sqladmin import ModelView

class EstudiantesAdmin(ModelView, model=Estudiantes):
    name = "Estudiante"
    name_plural = "Estudiantes"

    column_list = [Estudiantes.id, 
                   Estudiantes.no_control, 
                   Estudiantes.nombre, 
                   Estudiantes.apellidos,
                   Estudiantes.fecha_nacimiento, 
                   Estudiantes.edad, 
                   Estudiantes.municipio, 
                   Estudiantes.correo_institucional, 
                   Estudiantes.fecha_registro,
                   Estudiantes.contrasena]

    form_columns = [Estudiantes.no_control, 
                    Estudiantes.nombre, 
                    Estudiantes.apellidos, 
                    Estudiantes.fecha_nacimiento, 
                    Estudiantes.edad, 
                    Estudiantes.municipio, 
                    Estudiantes.correo_institucional, 
                    Estudiantes.fecha_registro,
                    Estudiantes.contrasena]

    form_overrides = {
        "contrasena": PasswordField,
    }

    column_labels = {Estudiantes.no_control : "No. Control", 
                     Estudiantes.nombre : "Nombre",
                     Estudiantes.apellidos: "Apellidos", 
                     Estudiantes.fecha_nacimiento: "Nacimiento", 
                     Estudiantes.edad : "Edad", 
                     Estudiantes.municipio : "Municipio", 
                     Estudiantes.correo_institucional : "Correo Institucional", 
                     Estudiantes.fecha_registro : "Fecha de Registro",
                     Estudiantes.contrasena : "Contraseña"}

    async def on_model_change(self, data, model, is_created, request):
        # Extraer la contraseña del diccionario de datos del formulario
        password_plana = data.get('contrasena')

        if password_plana:
            # Ciframos la contraseña
            password_cifrada = get_password_hash(password_plana)

            # Actualizamos el valor cifrado de la contraseña en el modelo y diccionario data
            model.contrasena = password_cifrada
            data['contrasena'] = password_cifrada
        elif is_created:
            # Si es un diccionario nuevo y no hay contraseña, 
            # lanzamos un error manual para evitar el IntegrityError
            # de SQL Server
            raise Exception("La contraseña es obligatoria para nuevos registros")

        return await super().on_model_change(data, model, is_created, request)