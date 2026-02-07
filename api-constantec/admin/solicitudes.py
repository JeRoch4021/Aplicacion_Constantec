from sqladmin import ModelView

from models.tables import Solicitudes, SolicitudEstatus


class SolicitudEstatusAdmin(ModelView, model = SolicitudEstatus): # type: ignore
    name = "Estatus de Solicitud"
    name_plural = "Estatus de Solicitudes"

    column_list = [SolicitudEstatus.id, SolicitudEstatus.tipo, SolicitudEstatus.descripcion]

    form_columns = [SolicitudEstatus.id, SolicitudEstatus.tipo, SolicitudEstatus.descripcion]


class SolicitudesAdmin(ModelView, model = Solicitudes): # type: ignore
    name = "Solicitudes"
    name_plural = "Solicitudes"

    column_list = [
        Solicitudes.id,
        Solicitudes.id_estudiantes,
        Solicitudes.id_constancia,
        Solicitudes.estatus,
        Solicitudes.fecha_solicitud,
        Solicitudes.fecha_entrega,
        Solicitudes.trabajador,
        Solicitudes.folio,
    ]

    form_columns = [
        Solicitudes.id_estudiantes,
        Solicitudes.id_constancia,
        Solicitudes.estatus,
        Solicitudes.fecha_solicitud,
        Solicitudes.fecha_entrega,
        Solicitudes.trabajador,
        Solicitudes.folio,
    ]
