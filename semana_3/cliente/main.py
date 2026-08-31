"""Aplicación interactiva para clientes y cuentas."""

from pydantic import ValidationError

from cliente import Cliente, ClienteMayorista, ClienteMinorista
from cuenta import Cuenta


def pedir_texto(mensaje: str) -> str:
    valor = input(mensaje).strip()
    if not valor:
        raise ValueError("El dato no puede quedar vacío")
    return valor


def pedir_monto(mensaje: str) -> float:
    try:
        monto = float(input(mensaje).strip())
    except ValueError as error:
        raise ValueError("Debe ingresar un número válido") from error
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a cero")
    return monto


def mostrar_clientes(clientes: list[Cliente]) -> None:
    if not clientes:
        print("\nNo hay clientes registrados.")
        return
    print("\nClientes registrados:")
    for indice, cliente in enumerate(clientes, start=1):
        print(f"  {indice}. {cliente.identificacion} - {cliente.nombre} ({cliente.tipo})")


def seleccionar_cliente(clientes: list[Cliente]) -> Cliente:
    mostrar_clientes(clientes)
    if not clientes:
        raise ValueError("Primero debe registrar un cliente")
    try:
        indice = int(input("Seleccione el número de cliente: ")) - 1
        return clientes[indice]
    except (ValueError, IndexError) as error:
        raise ValueError("Cliente inválido") from error


def registrar_cliente(clientes: list[Cliente]) -> None:
    print("\n--- Registrar cliente ---")
    nombre = pedir_texto("Nombre: ")
    identificacion = pedir_texto("Identificación: ")
    print("1. Mayorista\n2. Minorista")
    tipo = input("Tipo de cliente: ").strip()

    tipos = {
        "1": ClienteMayorista,
        "2": ClienteMinorista,
    }
    clase_cliente = tipos.get(tipo)
    if clase_cliente is None:
        raise ValueError("Tipo de cliente inválido")

    cliente = clase_cliente(nombre=nombre, identificacion=identificacion)
    clientes.append(cliente)
    print(f"Cliente {cliente.nombre} registrado como {cliente.tipo}.")


def abrir_cuenta(clientes: list[Cliente], cuentas: list[Cuenta]) -> None:
    print("\n--- Abrir cuenta ---")
    cliente = seleccionar_cliente(clientes)
    numero = pedir_texto("Número de cuenta: ")
    saldo = pedir_monto("Saldo inicial: ")
    cuenta = Cuenta(numero=numero, cliente=cliente, saldo=saldo)
    cuentas.append(cuenta)
    print(f"Cuenta creada para {cliente.nombre} con saldo ${cuenta.saldo:.2f}.")


def cobrar_servicio(cuentas: list[Cuenta]) -> None:
    print("\n--- Cobrar servicio ---")
    if not cuentas:
        raise ValueError("Primero debe abrir una cuenta")
    for indice, cuenta in enumerate(cuentas, start=1):
        print(f"  {indice}. {cuenta.numero} - {cuenta.cliente.nombre} ({cuenta.cliente.tipo})")
    try:
        indice = int(input("Seleccione el número de cuenta: ")) - 1
        cuenta = cuentas[indice]
    except (ValueError, IndexError) as error:
        raise ValueError("Cuenta inválida") from error

    monto = pedir_monto("Monto del servicio: ")
    descuento = cuenta.cliente.calcularDescuento(monto)
    total = cuenta.cobrar_servicio(monto)
    print(f"Descuento aplicado: ${descuento:.2f}")
    print(f"Total cobrado: ${total:.2f}")
    print(f"Saldo restante: ${cuenta.saldo:.2f}")


def mostrar_resumen(clientes: list[Cliente], cuentas: list[Cuenta]) -> None:
    print("\n--- Resumen ---")
    mostrar_clientes(clientes)
    print("\nCuentas:")
    if not cuentas:
        print("  No hay cuentas abiertas.")
    for cuenta in cuentas:
        print(f"  {cuenta.numero} - {cuenta.cliente.nombre}: ${cuenta.saldo:.2f}")


def main() -> None:
    clientes: list[Cliente] = []
    cuentas: list[Cuenta] = []
    acciones = {
        "1": lambda: registrar_cliente(clientes),
        "2": lambda: abrir_cuenta(clientes, cuentas),
        "3": lambda: cobrar_servicio(cuentas),
        "4": lambda: mostrar_resumen(clientes, cuentas),
    }

    while True:
        print("\n=== SISTEMA DE CLIENTES ===")
        print("1. Registrar cliente")
        print("2. Abrir cuenta")
        print("3. Cobrar servicio")
        print("4. Ver resumen")
        print("0. Salir")
        try:
            opcion = input("Seleccione una opción: ").strip()
        except EOFError:
            print("\nEntrada finalizada. Programa finalizado.")
            break
        if opcion == "0":
            print("Programa finalizado.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida.")
            continue
        try:
            accion()
        except (ValueError, ValidationError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
