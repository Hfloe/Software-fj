"""Entidad abstracta general y la clase Cliente."""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError, ParametroFaltanteError

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad del sistema."""

    def __init__(self, identificador):
        if not isinstance(identificador, int) or isinstance(identificador, bool) \
                or identificador <= 0:
            raise ValueError("El identificador debe ser un entero positivo.")
        self._id = identificador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible de la entidad."""

    def __str__(self):
        return self.describir()


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    def __init__(self, identificador, nombre=None, documento=None,
                 email=None, telefono=None):
        super().__init__(identificador)
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    @staticmethod
    def _requerido(valor, campo):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError(f"Falta el campo obligatorio: {campo}.")
        return str(valor).strip()

    # --- nombre ---
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._requerido(valor, "nombre")
        if len(valor) < 3 or not all(
            c.isalpha() or c.isspace() or c in "-'’" for c in valor
        ):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'.")
        self._nombre = valor.title()

    # --- documento ---
    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = self._requerido(valor, "documento")
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(
                f"Documento inválido (6-12 dígitos): '{valor}'.")
        self._documento = valor

    # --- email ---
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        valor = self._requerido(valor, "email")
        if not EMAIL_RE.match(valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self._email = valor.lower()

    # --- teléfono ---
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._requerido(valor, "teléfono")
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(
                f"Teléfono inválido (7-10 dígitos): '{valor}'.")
        self._telefono = valor

    def describir(self):
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.email} | Tel: {self.telefono}")
