from sqladmin import ModelView

from models.tables import ComprobantesPago, EstadoComprobante


class ComprobantesAdmin(ModelView, model=ComprobantesPago):  # type: ignore
    name = "Comprobantes de Pago"
    name_plural = "Comprobantes de Pago"

    column_list = [ComprobantesPago.id, ComprobantesPago.id_estudiante, ComprobantesPago.factura, ComprobantesPago.estado, ComprobantesPago.motivo_rechazo]

    form_columns = [ComprobantesPago.id, ComprobantesPago.id_estudiante, ComprobantesPago.factura, ComprobantesPago.estado, ComprobantesPago.motivo_rechazo]


class EstadoComprobantesAdmin(ModelView, model=EstadoComprobante):  # type: ignore
    name = "Estado de Comprobantes"
    name_plural = "Estado de Comprobantes"

    column_list = [EstadoComprobante.id, EstadoComprobante.tipo, EstadoComprobante.descripcion]

    form_columns = [EstadoComprobante.id, EstadoComprobante.tipo, EstadoComprobante.descripcion]
