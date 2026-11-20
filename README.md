# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso Programación (213023) – UNAD. Python 3.8+, sin bases de datos ni librerías externas.

## Ejecución
- Cuaderno: abrir `software_fj.ipynb` (Jupyter o Google Colab) y ejecutar todas las celdas.
- Módulos: `python main.py`.
El log queda en `logs/software_fj.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| excepciones.py | Excepciones personalizadas (jerarquía desde SoftwareFJError) |
| registro.py | Configuración del archivo de logs |
| entidades.py | EntidadBase (abstracta) y Cliente (encapsulación + validaciones) |
| servicios.py | Servicio (abstracta), ReservaSala, AlquilerEquipo, Asesoria |
| reserva.py | Reserva: confirmar, cancelar, procesar (try/except/else/finally) |
| gestor.py | Listas internas y ejecución segura de operaciones |
| main.py | Simulación de 12 operaciones válidas e inválidas |

## Conceptos aplicados
- Abstracción: EntidadBase y Servicio (ABC + @abstractmethod).
- Herencia y polimorfismo: calcular_costo_base, validar_parametros y describir sobrescritos.
- Encapsulación: atributos privados con properties y validación en setters.
- Sobrecarga (simulada con parámetros opcionales): calcular_costo(h), (h, impuesto), (h, impuesto, descuento).
- Excepciones: personalizadas, try/except, try/except/else/finally y encadenamiento (`raise ... from`).
- Logs: todos los eventos y errores quedan registrados en archivo.


## Validaciones reforzadas
- Rechaza booleanos en campos numéricos y cantidades.
- Rechaza tarifas, duraciones, impuestos y descuentos no finitos.
- La disponibilidad solo acepta True o False.

## Pruebas automáticas
Ejecutar: `python -m unittest discover -s tests -v`

## Nota sobre sobrecarga
Python no ofrece sobrecarga tradicional por firma. Este proyecto simula variantes del cálculo con parámetros opcionales (`impuesto` y `descuento`); explíquese así en la sustentación.
