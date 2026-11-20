"""Clase abstracta Servicio y servicios especializados (polimorfismo)."""
import math
from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import CalculoInconsistenteError, ServicioInvalidoError

IVA = 0.19


class Servicio(EntidadBase, ABC):
    """Servicio genérico de Software FJ."""

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")
        if (isinstance(tarifa_hora, bool)
                or not isinstance(tarifa_hora, (int, float))
                or not math.isfinite(tarifa_hora) or tarifa_hora <= 0):
            raise ServicioInvalidoError(
                "La tarifa por hora debe ser un número finito mayor que cero.")
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self._disponible = valor

    # --- métodos abstractos (se sobrescriben en cada servicio) ---
    @abstractmethod
    def calcular_costo_base(self, horas, **opciones):
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, horas, **opciones):
        """Lanza ServicioInvalidoError si los parámetros no son válidos."""

    @abstractmethod
    def describir(self):
        """Descripción del servicio."""

    @staticmethod
    def _validar_horas(horas, minimo, maximo):
        if (isinstance(horas, bool) or not isinstance(horas, (int, float))
                or not math.isfinite(horas)):
            raise ServicioInvalidoError("La duración debe ser un número finito.")
        if not minimo <= horas <= maximo:
            raise ServicioInvalidoError(
                f"La duración debe estar entre {minimo} y {maximo} horas.")

    # --- sobrecarga simulada: varias variantes con parámetros opcionales ---
    def calcular_costo(self, horas, impuesto=None, descuento=None, **opciones):
        """Variantes de uso:
        calcular_costo(h)                       -> costo base
        calcular_costo(h, impuesto=0.19)        -> con impuesto
        calcular_costo(h, descuento=0.10)       -> con descuento
        calcular_costo(h, 0.19, 0.10)           -> con ambos
        """
        impuesto = 0.0 if impuesto is None else impuesto
        descuento = 0.0 if descuento is None else descuento
        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if (isinstance(valor, bool) or not isinstance(valor, (int, float))
                    or not math.isfinite(valor)):
                raise CalculoInconsistenteError(
                    f"El {nombre} debe ser un número finito.")
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):
            raise CalculoInconsistenteError(
                "Impuesto debe estar en [0,1] y descuento en [0,1).")
        base = self.calcular_costo_base(horas, **opciones)
        total = base * (1 - descuento) * (1 + impuesto)
        if not math.isfinite(total) or total <= 0:
            raise CalculoInconsistenteError(f"Costo inconsistente: {total}")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas por horas."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser un entero > 0.")
        self._capacidad = capacidad

    def validar_parametros(self, horas, **opciones):
        self._validar_horas(horas, 1, 8)
        asistentes = opciones.get("asistentes", 1)
        if (isinstance(asistentes, bool) or not isinstance(asistentes, int)
                or not 1 <= asistentes <= self._capacidad):
            raise ServicioInvalidoError(
                f"Asistentes fuera de capacidad (máx {self._capacidad}).")

    def calcular_costo_base(self, horas, **opciones):
        self.validar_parametros(horas, **opciones)
        return self._tarifa_hora * horas

    def describir(self):
        return (f"[Sala] {self.nombre} - capacidad {self._capacidad} - "
                f"${self.tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (el costo escala con la cantidad)."""

    def __init__(self, identificador, nombre, tarifa_hora, stock, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if isinstance(stock, bool) or not isinstance(stock, int) or stock <= 0:
            raise ServicioInvalidoError("El stock debe ser un entero > 0.")
        self._stock = stock

    def validar_parametros(self, horas, **opciones):
        self._validar_horas(horas, 1, 72)
        cantidad = opciones.get("cantidad", 1)
        if (isinstance(cantidad, bool) or not isinstance(cantidad, int)
                or not 1 <= cantidad <= self._stock):
            raise ServicioInvalidoError(
                f"Cantidad inválida (stock disponible: {self._stock}).")

    def calcular_costo_base(self, horas, **opciones):
        self.validar_parametros(horas, **opciones)
        return self._tarifa_hora * horas * opciones.get("cantidad", 1)

    def describir(self):
        return (f"[Equipo] {self.nombre} - stock {self._stock} - "
                f"${self.tarifa_hora:,.0f}/h por unidad")


class Asesoria(Servicio):
    """Asesoría especializada; el nivel senior cuesta 50% más."""

    NIVELES = {"junior": 1.0, "senior": 1.5}

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad es obligatoria.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, horas, **opciones):
        self._validar_horas(horas, 1, 6)
        if opciones.get("nivel", "junior") not in self.NIVELES:
            raise ServicioInvalidoError("Nivel debe ser 'junior' o 'senior'.")

    def calcular_costo_base(self, horas, **opciones):
        self.validar_parametros(horas, **opciones)
        factor = self.NIVELES[opciones.get("nivel", "junior")]
        return self._tarifa_hora * horas * factor

    def describir(self):
        return (f"[Asesoría] {self.nombre} - {self._especialidad} - "
                f"${self.tarifa_hora:,.0f}/h")
