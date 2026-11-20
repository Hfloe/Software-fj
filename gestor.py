"""Gestor integral: administra listas internas de clientes, servicios y reservas."""
from entidades import Cliente
from excepciones import SoftwareFJError
from registro import obtener_logger
from reserva import Reserva

logger = obtener_logger()


class GestorSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    def _ejecutar(self, descripcion, funcion):
        """Ejecuta una operación sin dejar que un error detenga el programa."""
        try:
            resultado = funcion()
        except SoftwareFJError as error:
            causa = f" | causa: {error.__cause__}" if error.__cause__ else ""
            logger.error("%s FALLÓ -> %s: %s%s", descripcion,
                         type(error).__name__, error, causa)
            print(f"  [ERROR CONTROLADO] {type(error).__name__}: {error}{causa}")
            return None
        except Exception as error:  # error inesperado: se registra y se continúa
            logger.exception("%s FALLÓ con error inesperado: %s", descripcion, error)
            print(f"  [ERROR INESPERADO CONTROLADO] {type(error).__name__}: {error}")
            return None
        else:
            logger.info("%s OK.", descripcion)
            print(f"  [OK] {resultado}")
            return resultado
        finally:
            logger.info("Operación finalizada: %s", descripcion)

    def registrar_cliente(self, **datos):
        def accion():
            cliente = Cliente(len(self._clientes) + 1, **datos)
            self._clientes.append(cliente)
            return cliente
        return self._ejecutar("Registro de cliente", accion)

    def agregar_servicio(self, clase, *args, **kwargs):
        def accion():
            servicio = clase(len(self._servicios) + 1, *args, **kwargs)
            self._servicios.append(servicio)
            return servicio
        return self._ejecutar(f"Creación de servicio {clase.__name__}", accion)

    def crear_reserva(self, cliente, servicio, horas, **opciones):
        def accion():
            reserva = Reserva(len(self._reservas) + 1, cliente, servicio,
                              horas, **opciones)
            self._reservas.append(reserva)
            return reserva
        return self._ejecutar("Creación de reserva", accion)

    def confirmar_reserva(self, reserva):
        return self._ejecutar(f"Confirmación reserva #{getattr(reserva, 'id', '?')}",
                              lambda: (reserva.confirmar(), reserva)[1])

    def cancelar_reserva(self, reserva):
        return self._ejecutar(f"Cancelación reserva #{getattr(reserva, 'id', '?')}",
                              lambda: (reserva.cancelar(), reserva)[1])

    def procesar_reserva(self, reserva):
        return self._ejecutar(
            f"Procesamiento reserva #{getattr(reserva, 'id', '?')}",
            lambda: f"Total con IVA: ${reserva.procesar():,.2f}")
