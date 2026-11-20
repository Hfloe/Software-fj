"""Software FJ - Simulación de 12 operaciones (válidas e inválidas)."""
from gestor import GestorSoftwareFJ
from registro import ARCHIVO_LOG, obtener_logger
from servicios import Asesoria, AlquilerEquipo, ReservaSala

logger = obtener_logger()


def titulo(n, texto):
    print(f"\n--- Operación {n}: {texto} ---")


def main():
    logger.info("===== INICIO DE LA SIMULACIÓN =====")
    g = GestorSoftwareFJ()

    titulo(1, "Cliente válido")
    ana = g.registrar_cliente(nombre="ana maría pérez", documento="1012345678",
                              email="ana@correo.com", telefono="3101234567")

    titulo(2, "Cliente inválido (correo mal formado)")
    g.registrar_cliente(nombre="Luis Gómez", documento="987654321",
                        email="luis@@correo", telefono="3009876543")

    titulo(3, "Cliente inválido (falta el teléfono)")
    g.registrar_cliente(nombre="Carlos Ruiz", documento="55443322",
                        email="carlos@correo.com")

    titulo(4, "Cliente válido")
    luis = g.registrar_cliente(nombre="Luis Gómez", documento="987654321",
                               email="luis@correo.com", telefono="3009876543")

    titulo(5, "Servicio válido: sala")
    sala = g.agregar_servicio(ReservaSala, "Sala Innovación", 50000, 10)

    titulo(6, "Servicio inválido: tarifa negativa")
    g.agregar_servicio(AlquilerEquipo, "Proyector 4K", -20000, 5)

    titulo(7, "Servicios válidos: equipo y asesoría")
    equipo = g.agregar_servicio(AlquilerEquipo, "Portátil Gamer", 15000, 5)
    asesoria = g.agregar_servicio(Asesoria, "Asesoría Cloud", 80000, "Cloud")
    fuera = g.agregar_servicio(Asesoria, "Asesoría Legal", 90000, "Legal",
                               disponible=False)

    titulo(8, "Reserva exitosa: confirmar y procesar (sala, 3h, 8 personas)")
    r1 = g.crear_reserva(ana, sala, 3, asistentes=8)
    g.confirmar_reserva(r1)
    g.procesar_reserva(r1)

    titulo(9, "Reserva fallida: sala con más asistentes que la capacidad")
    g.crear_reserva(luis, sala, 2, asistentes=25)

    titulo(10, "Reserva fallida: servicio no disponible")
    g.crear_reserva(luis, fuera, 2, nivel="senior")

    titulo(11, "Reserva de equipo y cancelación; luego procesar (no permitido)")
    r2 = g.crear_reserva(luis, equipo, 24, cantidad=2)
    g.cancelar_reserva(r2)
    g.procesar_reserva(r2)

    titulo(12, "Asesoría senior + cálculo con descuento (sobrecarga) + cliente None")
    r3 = g.crear_reserva(ana, asesoria, 2, nivel="senior")
    g.confirmar_reserva(r3)
    g.procesar_reserva(r3)
    print("  Costo base:             ", asesoria.calcular_costo(2, nivel="senior"))
    print("  Con IVA:                ", asesoria.calcular_costo(2, 0.19, nivel="senior"))
    print("  Con IVA y 10% dcto:     ",
          asesoria.calcular_costo(2, 0.19, 0.10, nivel="senior"))
    g.crear_reserva(None, asesoria, 2)

    print("\n=== RESUMEN ===")
    for lista in (g.clientes, g.servicios, g.reservas):
        for item in lista:
            print(" ", item)
    print(f"\nEl programa terminó sin interrupciones. Log: {ARCHIVO_LOG}")
    logger.info("===== FIN DE LA SIMULACIÓN =====")


if __name__ == "__main__":
    main()
