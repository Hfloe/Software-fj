"""Clase Reserva: integra cliente, servicio, duración y estado."""
from enum import Enum

from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioNoDisponibleError,
                         SoftwareFJError)
from registro import obtener_logger
from servicios import IVA, Servicio

logger = obtener_logger()


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"


class Reserva(EntidadBase):
    def __init__(self, identificador, cliente, servicio, horas, **opciones):
        super().__init__(identificador)
        # try/except con encadenamiento: se conserva el error original
        try:
            if not isinstance(cliente, Cliente):
                raise TypeError("El cliente no es válido.")
            if not isinstance(servicio, Servicio):
                raise TypeError("El servicio no es válido.")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible.")
            servicio.validar_parametros(horas, **opciones)
        except ServicioNoDisponibleError:
            raise
        except (TypeError, SoftwareFJError) as error:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva #{identificador}: {error}") from error

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._opciones = opciones
        self._estado = EstadoReserva.PENDIENTE
        logger.info("Reserva #%s creada (PENDIENTE).", identificador)

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    def confirmar(self):
        if self._estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self._estado.value}.")
        self._estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva #%s CONFIRMADA.", self.id)

    def cancelar(self):
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado.value}.")
        self._estado = EstadoReserva.CANCELADA
        logger.info("Reserva #%s CANCELADA.", self.id)

    def procesar(self):
        """Procesa la reserva y devuelve el costo total con IVA."""
        costo = None
        try:
            if self._estado is not EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (actual: "
                    f"{self._estado.value}).")
            costo = self._servicio.calcular_costo(
                self._horas, impuesto=IVA, **self._opciones)
            if costo <= 0:
                raise CalculoInconsistenteError("El costo debe ser positivo.")
        except SoftwareFJError as error:
            raise ReservaInvalidaError(
                f"Falló el procesamiento de la reserva #{self.id}.") from error
        else:
            self._estado = EstadoReserva.PROCESADA
            logger.info("Reserva #%s PROCESADA. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            logger.info("Fin del intento de procesamiento de la reserva #%s.", self.id)

    def describir(self):
        return (f"Reserva #{self.id} | {self._cliente.nombre} | "
                f"{self._servicio.nombre} | {self._horas}h | {self._estado.value}")
