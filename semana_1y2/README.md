# Sistema de gestión bancaria

Aplicación de consola desarrollada en **Python** para simular operaciones básicas de un banco. El programa permite registrar clientes, abrir cuentas, mover dinero y administrar préstamos desde un menú sencillo.

## Objetivo

Practicar los fundamentos de programación y la programación orientada a objetos mediante un sistema que organiza clientes, cuentas y préstamos, aplicando validaciones y reglas diferentes para cada tipo de cliente o cuenta.

## Funcionalidades principales

- Registrar clientes normales o VIP.
- Validar cédula, nombre, correo e ingreso mensual.
- Abrir cuentas de ahorros o corrientes.
- Depositar y retirar dinero.
- Permitir un sobregiro controlado en las cuentas corrientes.
- Solicitar préstamos según el cupo de crédito del cliente.
- Calcular intereses, cuotas y saldo pendiente.
- Pagar cuotas de préstamos.
- Consultar clientes y ver un resumen general del banco.
- Cancelar una operación escribiendo `0` y mostrar mensajes cuando existe un dato inválido.

## Organización del proyecto

```text
semana_1y2/
├── main.py              # Menú y flujo principal de la aplicación
└── banco/
    ├── __init__.py      # Exporta las clases del paquete
    ├── banco.py         # Administra clientes, cuentas y préstamos
    ├── cliente.py       # Cliente, ClienteNormal y ClienteVIP
    ├── cuenta.py        # Cuenta, CuentaAhorros y CuentaCorriente
    └── prestamo.py      # Cálculos y pagos de préstamos
```

## Cómo ejecutar el proyecto

1. Tener instalado **Python 3**.
2. Abrir una terminal en la raíz del repositorio y entrar a la carpeta del proyecto:

   ```bash
   cd programacion_estructurada/semana_1y2
   ```

3. Ejecutar el programa:

   ```bash
   python main.py
   ```

   Si la terminal ya está ubicada dentro de `semana_1y2`, basta con ejecutar `python main.py`.

No se necesitan librerías externas. El sistema funciona directamente en la terminal.

## Ejemplo de uso

Una demostración sencilla puede seguir este orden:

1. Registrar un cliente.
2. Abrirle una cuenta de ahorros o corriente.
3. Depositar o retirar dinero.
4. Solicitar un préstamo.
5. Pagar una cuota.
6. Consultar el resumen del banco.

Para regresar o cancelar una operación, se puede escribir `0` cuando el programa lo indique.

## Conceptos aplicados

- Clases y objetos.
- Encapsulamiento mediante atributos privados, propiedades y validaciones.
- Herencia entre clientes y tipos de cuenta.
- Polimorfismo en las reglas de crédito y tasas de interés.
- Composición entre el banco, sus clientes, cuentas y préstamos.
- Funciones, estructuras condicionales, ciclos y manejo de excepciones.

## Autor

Harry Álvarez Gómez
