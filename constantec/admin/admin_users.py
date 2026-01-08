from models.admin import AdminUser
from sqladmin import ModelView

class UserAdmin(ModelView, model=AdminUser):
    name = "Usuario"
    name_plural = "Usuarios"

    column_list = [AdminUser.id, AdminUser.username]