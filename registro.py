"""Configuración del archivo de logs (eventos y errores)."""
import logging
import os

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger(nombre="software_fj"):
    """Devuelve un logger que escribe en logs/software_fj.log."""
    logger = logging.getLogger(nombre)
    if not logger.handlers:
        os.makedirs(RUTA_LOGS, exist_ok=True)
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        manejador.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s"))
        logger.addHandler(manejador)
        logger.propagate = False
    return logger
