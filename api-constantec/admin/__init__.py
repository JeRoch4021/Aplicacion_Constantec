from .administradores import UserAdmin
from .estudiantes import EstudiantesAdmin
from .constancias import ConstanciaTiposAdmin, ConstanciaOpcionesAdmin, ConstanciasAdmin
from .solicitudes import SolicitudEstatusAdmin, SolicitudesAdmin
from .encuestas import EncuestasAdmin
from .trabajador import TrabajadorAdmin
from .comprobantes import ComprobantesAdmin

__all__ = ['UserAdmin',
           'EstudiantesAdmin',
           'ConstanciaTiposAdmin',
           'ConstanciaOpcionesAdmin',
           'ConstanciasAdmin',
           'SolicitudEstatusAdmin',
           'SolicitudesAdmin',
           'EncuestasAdmin',
           'ComprobantesAdmin',
           'TrabajadorAdmin']