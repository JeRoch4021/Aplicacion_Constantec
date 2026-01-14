from models.tables import ConstanciaTipos, SolicitudEstatus, Solicitudes
from sqladmin import ModelView

class SolicitudEstatusAdmin(ModelView, model=SolicitudEstatus):
    name = "Estatus de Solicitud"
    name_plural = "Estatus de Solicitudes"

    column_list = [SolicitudEstatus.id,
                   SolicitudEstatus.tipo,
                   SolicitudEstatus.descripcion]
    
    form_columns = [SolicitudEstatus.id,
                    SolicitudEstatus.tipo,
                    SolicitudEstatus.descripcion]

class SolicitudesAdmin(ModelView, model=Solicitudes):
    name = "Solicitudes"
    name_plural = "Solicitudes"

    column_list = [Solicitudes.id,
                   Solicitudes.estudiantes_id,
                   Solicitudes.constancia_id,
                   Solicitudes.estatus,
                   Solicitudes.fecha_solicitud,
                   Solicitudes.fecha_entrega,
                   Solicitudes.trabajador,
                   Solicitudes.folio]
    
    form_columns = [Solicitudes.estudiantes_id,
                    Solicitudes.constancia_id,
                    Solicitudes.estatus,
                    Solicitudes.fecha_solicitud,
                    Solicitudes.fecha_entrega,
                    Solicitudes.trabajador,
                    Solicitudes.folio]