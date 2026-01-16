from models.tables import ConstanciaTipos, ConstanciaOpciones, Constancias
from sqladmin import ModelView

class ConstanciaTiposAdmin(ModelView, model=ConstanciaTipos):
    name = "Tipo de Constancia"
    name_plural = "Tipos de Constancias"

    column_list = [ConstanciaTipos.id,
                   ConstanciaTipos.tipo,
                   ConstanciaTipos.descripcion]
    
    form_columns = [ConstanciaTipos.id,
                    ConstanciaTipos.tipo,
                    ConstanciaTipos.descripcion]
    
class ConstanciaOpcionesAdmin(ModelView, model=ConstanciaOpciones):
    name = "Opciones de Constancia"
    name_plural = "Opciones de Constancias"

    column_list = [ConstanciaOpciones.id,
                   ConstanciaOpciones.id_constancia,
                   ConstanciaOpciones.id_constancias_tipo]
    
    form_columns = [ConstanciaOpciones.id,
                    ConstanciaOpciones.id_constancia,
                    ConstanciaOpciones.id_constancias_tipo]

class ConstanciasAdmin(ModelView, model=Constancias):
    name = "Constancias"
    name_plural = "Constancias"

    column_list = [Constancias.id,
                   Constancias.descripcion,
                   Constancias.otros]
    
    form_columns = [Constancias.id,
                    Constancias.descripcion,
                    Constancias.otros]