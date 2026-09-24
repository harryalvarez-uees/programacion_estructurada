# Catálogo de productos con interfaz gráfica

Aplicación en **Python** para administrar un catálogo de productos desde una ventana hecha con **Flet**. Permite agregar, buscar, listar, actualizar y eliminar productos.

## Objetivo

Practicar el uso de colecciones (`list`, `dict`, `set`), el manejo de excepciones y una primera interfaz gráfica con manejo de eventos. La interfaz se seguirá ampliando en las próximas semanas.

## Funcionalidades

- Agregar un producto con código, nombre, precio y stock.
- Buscar un producto por su código.
- Listar los productos registrados.
- Actualizar los datos de un producto.
- Eliminar un producto.
- Seleccionar un producto de la lista para cargar sus datos en el formulario.
- Mostrar mensajes de éxito o de error (datos inválidos, código repetido, producto inexistente).

## Organización del proyecto

```text
semana_5y6/
└── catalogo/
    ├── main.py          # Interfaz gráfica (Flet) y manejo de eventos
    ├── catalogo.py      # Catálogo con list, dict y set
    ├── producto.py      # Modelo Producto con validaciones
    ├── excepciones.py   # Excepciones propias del catálogo
    ├── pruebas.py       # Prueba rápida por consola
    ├── requirements.txt
```

## Requisitos

- **Python 3.10 o superior**.
- Librerías `pydantic` y `flet` (se instalan con `requirements.txt`).

## Cómo ejecutar el proyecto

Desde la raíz del repositorio:

```bash
cd programacion_estructurada
source venv/bin/activate
cd semana_5y6/catalogo
pip install -r requirements.txt
python main.py
```

En Windows, la activación del entorno virtual es:

```bash
venv\Scripts\activate
```

Para probar solo el catálogo por consola, sin abrir la ventana:

```bash
python pruebas.py
```

## Ejemplo de uso

1. Escribir código, nombre, precio y stock, y presionar **Agregar**.
2. Escribir un código y presionar **Buscar** (o hacer clic en un producto de la lista).
3. Cambiar los datos y presionar **Actualizar**.
4. Con un código en el formulario, presionar **Eliminar**.
5. Probar un precio negativo o un código repetido para ver los mensajes de error.

## Conceptos aplicados

- Colecciones: `list` (orden de registro), `dict` (búsqueda por código) y `set` (evitar duplicados).
- Excepciones personalizadas y bloques `try` / `except`.
- Validación de datos con Pydantic.
- Interfaz gráfica con Flet y manejo de eventos (`on_click`).
- Separación entre la lógica del catálogo y la interfaz.
