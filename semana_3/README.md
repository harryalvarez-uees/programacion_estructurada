# Sistema de clientes y cobro de servicios

Aplicación de consola desarrollada en **Python** para registrar clientes, crear sus cuentas y cobrar servicios aplicando automáticamente el descuento que corresponde a cada tipo de cliente.

## Objetivo

Practicar la abstracción, la herencia, el polimorfismo y la composición en un programa pequeño y fácil de usar. El sistema demuestra que cada cliente puede aplicar una regla de descuento diferente sin que el menú tenga que conocer los detalles de cada tipo.

## Funcionalidades principales

- Registrar clientes mayoristas o minoristas.
- Validar los datos básicos del cliente.
- Abrir una cuenta con un saldo inicial.
- Cobrar un servicio desde una cuenta.
- Calcular automáticamente el descuento según el cliente.
- Mostrar el total cobrado y el saldo restante.
- Consultar un resumen de los clientes y sus cuentas.
- Informar errores cuando faltan datos o se selecciona una opción inválida.

## Reglas de descuento

- **Cliente mayorista:** aplica 15 % de descuento y 20 % cuando el servicio cuesta desde $1.000.
- **Cliente minorista:** aplica 5 % de descuento, con un descuento máximo de $50.

## Organización del proyecto

```text
semana_3/
└── cliente/
    ├── main.py       # Menú, entradas y flujo de la aplicación
    ├── cliente.py    # Clase abstracta y tipos de cliente
    └── cuenta.py     # Cuenta y cobro de servicios
```

## Requisitos

- **Python 3.10 o superior**.
- Librería `pydantic` para validar los datos de los modelos.

## Cómo ejecutar el proyecto

Desde la raíz del repositorio, activar el entorno virtual y ejecutar:

```bash
cd programacion_estructurada
source venv/bin/activate
pip install pydantic
cd semana_3/cliente
python main.py
```

En Windows, la activación del entorno virtual puede hacerse con:

```bash
venv\Scripts\activate
```

También es posible ejecutar el programa usando directamente el Python del entorno virtual:

```bash
../../venv/bin/python main.py
```

## Ejemplo de uso

1. Registrar un cliente mayorista o minorista.
2. Abrir una cuenta y asignarle un saldo inicial.
3. Seleccionar la cuenta para cobrar un servicio.
4. Ingresar el valor del servicio y observar el descuento, el total y el nuevo saldo.
5. Consultar el resumen para revisar la información registrada.

## Conceptos aplicados

- Clases y objetos.
- Clase abstracta e interfaces mediante `ABC` y `abstractmethod`.
- Herencia entre clientes.
- Polimorfismo en el cálculo del descuento.
- Composición: una cuenta tiene un cliente.
- Validación de datos con modelos de Pydantic.
- Funciones, listas, diccionarios, ciclos y manejo de excepciones.

## Autor

Harry Álvarez Gómez
