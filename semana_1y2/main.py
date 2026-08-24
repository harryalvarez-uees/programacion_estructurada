"""
HARRY ALVAREZ GOMEZ
"""

from banco import ClienteNormal, ClienteVIP, CuentaAhorros, CuentaCorriente, Banco


# ======================================================================
# Entrada de datos
# ======================================================================
class Cancelado(Exception):
    """El usuario escribio 0 para volver al menu."""


def pedir_texto(mensaje):
    valor = input(mensaje).strip()
    if valor == "0":
        raise Cancelado()
    if not valor:
        raise ValueError("El dato no puede quedar vacio")
    return valor


def pedir_numero(mensaje, entero=False):
    valor = input(mensaje).strip()
    if valor == "0":
        raise Cancelado()
    try:
        return int(valor) if entero else float(valor)
    except ValueError:
        raise ValueError(f"'{valor}' no es un numero valido")


def pedir_opcion(mensaje, opciones):
    valor = input(mensaje).strip()
    if valor == "0":
        raise Cancelado()
    if valor not in opciones:
        raise ValueError(f"Opcion invalida: {valor}")
    return valor


def titulo(texto):
    print()
    print("=" * 60)
    print(f"  {texto}")
    print("=" * 60)


# ======================================================================
# Opciones del menu
# ======================================================================
def registrar_cliente(banco):
    titulo("REGISTRAR CLIENTE")
    print("  (escriba 0 para cancelar)\n")
    cedula = pedir_texto("  Cedula (10 digitos) : ")
    nombre = pedir_texto("  Nombre completo     : ")
    email = pedir_texto("  Email               : ")
    ingreso = pedir_numero("  Ingreso mensual     : ")

    print("\n  Tipo de cliente:")
    print("    1. Normal")
    print("    2. VIP")
    tipo = pedir_opcion("  Opcion              : ", ["1", "2"])

    if tipo == "1":
        cliente = ClienteNormal(cedula, nombre, email, ingreso)
    else:
        asesor = pedir_texto("  Asesor asignado     : ")
        cliente = ClienteVIP(cedula, nombre, email, ingreso, asesor)

    banco.registrar_cliente(cliente)
    print("\n  Cliente registrado.\n")
    cliente.mostrar_informacion()


def abrir_cuenta(banco):
    titulo("ABRIR CUENTA")
    if not banco.clientes:
        print("  Primero debe registrar un cliente.")
        return
    for c in banco.clientes:
        print(f"    {c.cedula} - {c.nombre} ({c.tipo_cliente})")
    print("\n  (escriba 0 para cancelar)\n")

    cedula = pedir_texto("  Cedula del titular  : ")
    titular = banco.buscar_cliente(cedula)
    if titular is None:
        raise ValueError(f"No existe un cliente con cedula {cedula}")

    numero = pedir_texto("  Numero de cuenta    : ")
    saldo = pedir_numero("  Deposito inicial    : ")

    print("\n  Tipo de cuenta:")
    print("    1. Ahorros")
    print("    2. Corriente")
    tipo = pedir_opcion("  Opcion              : ", ["1", "2"])

    if tipo == "1":
        cuenta = CuentaAhorros(numero, titular, saldo)
    else:
        cuenta = CuentaCorriente(numero, titular, saldo)

    banco.abrir_cuenta(cuenta)
    print(f"\n  Cuenta abierta: {cuenta}")


def mostrar_cuentas(banco):
    print("  Cuentas:")
    for c in banco.cuentas:
        print(f"    {c.numero:<12} {c.tipo_cuenta:<10} {c.titular.nombre:<20} "
              f"${c.saldo:>12,.2f}")
    print()


def depositar(banco):
    titulo("DEPOSITAR")
    if not banco.cuentas:
        print("  No hay cuentas abiertas.")
        return
    mostrar_cuentas(banco)
    print("  (escriba 0 para cancelar)\n")

    cuenta = obtener_cuenta(banco)
    monto = pedir_numero("  Monto a depositar   : ")
    cuenta.depositar(monto)
    print(f"\n  Deposito realizado. Nuevo saldo: ${cuenta.saldo:,.2f}")


def retirar(banco):
    titulo("RETIRAR")
    if not banco.cuentas:
        print("  No hay cuentas abiertas.")
        return
    mostrar_cuentas(banco)
    print("  (escriba 0 para cancelar)\n")

    cuenta = obtener_cuenta(banco)
    print(f"  Disponible          : ${cuenta.saldo_disponible:,.2f}")
    monto = pedir_numero("  Monto a retirar     : ")
    cuenta.retirar(monto)
    print(f"\n  Retiro realizado. Nuevo saldo: ${cuenta.saldo:,.2f}")


def obtener_cuenta(banco):
    numero = pedir_texto("  Numero de cuenta    : ")
    cuenta = banco.buscar_cuenta(numero)
    if cuenta is None:
        raise ValueError(f"No existe la cuenta {numero}")
    return cuenta


def solicitar_prestamo(banco):
    titulo("SOLICITAR PRESTAMO")
    if not banco.cuentas:
        print("  Primero debe abrir una cuenta.")
        return
    mostrar_cuentas(banco)
    print("  (escriba 0 para cancelar)\n")

    cuenta = obtener_cuenta(banco)
    monto = pedir_numero("  Monto solicitado    : ")
    cuotas = pedir_numero("  Numero de cuotas    : ", entero=True)

    prestamo = banco.otorgar_prestamo(cuenta, monto, cuotas)
    print("\n  Prestamo aprobado y acreditado en la cuenta.\n")
    prestamo.mostrar_informacion()
    print(f"\n  Saldo de la cuenta {cuenta.numero}: ${cuenta.saldo:,.2f}")


def pagar_cuota(banco):
    titulo("PAGAR CUOTA")
    if not banco.prestamos:
        print("  No hay prestamos registrados.")
        return
    print("  Prestamos:")
    for p in banco.prestamos:
        estado = "CANCELADO" if p.esta_cancelado() else f"faltan {p.cuotas_pendientes}"
        print(f"    {p.codigo:<8} cuenta {p.cuenta.numero:<12} "
              f"cuota ${p.cuota_mensual():>10,.2f}   {estado}")
    print("\n  (escriba 0 para cancelar)\n")

    codigo = pedir_texto("  Codigo del prestamo : ")
    prestamo = banco.buscar_prestamo(codigo)
    if prestamo is None:
        raise ValueError(f"No existe el prestamo {codigo}")

    cuota = prestamo.pagar_cuota()
    print(f"\n  Cuota pagada: ${cuota:,.2f}")
    print(f"  Cuotas pagadas   : {prestamo.cuotas_pagadas} de {prestamo.cuotas}")
    print(f"  Falta por pagar  : ${prestamo.saldo_pendiente():,.2f}")
    print(f"  Saldo de la cuenta {prestamo.cuenta.numero}: ${prestamo.cuenta.saldo:,.2f}")
    if prestamo.esta_cancelado():
        print("\n  El prestamo quedo cancelado.")


def ver_clientes(banco):
    titulo("CLIENTES")
    if not banco.clientes:
        print("  No hay clientes registrados.")
        return
    for cliente in banco.clientes:
        cliente.mostrar_informacion()
        deuda = banco.deuda_de(cliente)
        if deuda:
            print(f"     Deuda vigente   : ${deuda:,.2f}")
        print()


def ver_resumen(banco):
    titulo("RESUMEN DEL BANCO")
    banco.resumen()


# ======================================================================
# Menu principal
# ======================================================================
MENU = """
  1. Registrar cliente
  2. Abrir cuenta
  3. Depositar
  4. Retirar
  5. Solicitar prestamo
  6. Pagar cuota de prestamo
  7. Ver clientes
  8. Resumen del banco
  0. Salir
"""


def main():
    banco = Banco("Banco de Guayaquil")

    acciones = {
        "1": registrar_cliente,
        "2": abrir_cuenta,
        "3": depositar,
        "4": retirar,
        "5": solicitar_prestamo,
        "6": pagar_cuota,
        "7": ver_clientes,
        "8": ver_resumen,
    }

    while True:
        print("\n" + "-" * 60)
        print(f"  {banco.nombre}")
        print(MENU)
        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "0":
            print("\n  Hasta luego.\n")
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("\n  Opcion no valida.")
            continue

        try:
            accion(banco)
        except Cancelado:
            print("\n  Operacion cancelada.")
        except ValueError as error:
            # Aqui llegan las validaciones que lanzan las clases.
            print(f"\n  No se pudo completar: {error}")

        input("\nPresione ENTER para continuar...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Programa interrumpido.\n")
