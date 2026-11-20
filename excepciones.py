"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos."""


class ServicioInvalidoError(SoftwareFJError):
    """Datos o parámetros de servicio inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Intento de reserva incorrecto o procesamiento fallido."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no permitida para el estado actual."""


class CalculoInconsistenteError(SoftwareFJError):
    """Resultado de cálculo inconsistente (negativo, cero o no numérico)."""
