from models.tables import ComprobantesPago
from sqladmin import ModelView

class ComprobantesAdmin(ModelView, model=ComprobantesPago):
    name = "Comprobantes de Pago"
    name_plural = "Comprobantes de Pago"

    column_list = [ComprobantesPago.id,
                   ComprobantesPago.estudiante_id,
                   ComprobantesPago.factura,
                   ComprobantesPago.estado_validacion,
                   ComprobantesPago.motivo_rechazo]
    
    form_columns = [ComprobantesPago.id,
                    ComprobantesPago.estudiante_id,
                    ComprobantesPago.factura,
                    ComprobantesPago.estado_validacion,
                    ComprobantesPago.motivo_rechazo]