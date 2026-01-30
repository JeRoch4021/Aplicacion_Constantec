from .administradores import UserAdmin
from .comprobantes import ComprobantesAdmin, EstadoComprobantesAdmin
from .constancias import ConstanciaOpcionesAdmin, ConstanciasAdmin, ConstanciaTiposAdmin
from .encuestas import EncuestasAdmin
from .estudiantes import EstudiantesAdmin
from .solicitudes import SolicitudesAdmin, SolicitudEstatusAdmin
from .trabajador import TrabajadorAdmin

__all__ = [
    "UserAdmin",
    "EstudiantesAdmin",
    "ConstanciaTiposAdmin",
    "ConstanciaOpcionesAdmin",
    "ConstanciasAdmin",
    "SolicitudEstatusAdmin",
    "SolicitudesAdmin",
    "EncuestasAdmin",
    "ComprobantesAdmin",
    "EstadoComprobantesAdmin",
    "TrabajadorAdmin",
]
