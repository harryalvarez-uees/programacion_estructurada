"""
Interfaz gráfica del catálogo con Flet.

La ventana solo captura datos y muestra resultados. Las reglas de
negocio siguen en Producto (validación) y Catalogo (colecciones).
"""

import flet as ft
from pydantic import ValidationError

from catalogo import Catalogo
from excepciones import ProductoDuplicadoError, ProductoNoEncontradoError
from producto import Producto


def main(page: ft.Page):
    page.title = "Catálogo de productos"
    page.window.width = 520
    page.window.height = 680
    page.padding = 20

    catalogo = Catalogo()

    # ---------- controles ----------
    campo_codigo = ft.TextField(label="Código", width=150)
    campo_nombre = ft.TextField(label="Nombre", expand=True)
    campo_precio = ft.TextField(label="Precio", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    campo_stock = ft.TextField(label="Stock", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    mensaje = ft.Text("")
    lista_visual = ft.ListView(expand=True, spacing=2)
    total = ft.Text("0 productos", italic=True)

    # ---------- funciones de apoyo ----------
    def mostrar_mensaje(texto, error=False):
        mensaje.value = texto
        mensaje.color = ft.Colors.RED if error else ft.Colors.GREEN
        page.update()

    def limpiar_campos():
        for campo in (campo_codigo, campo_nombre, campo_precio, campo_stock):
            campo.value = ""

    def refrescar_lista():
        lista_visual.controls.clear()
        for p in catalogo.listar():
            lista_visual.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{p.codigo} - {p.nombre}"),
                    subtitle=ft.Text(f"${p.precio:.2f}  |  Stock: {p.stock}"),
                    data=p.codigo,
                    on_click=seleccionar_producto,
                )
            )
        total.value = f"{len(catalogo)} productos"
        page.update()

    def leer_formulario() -> Producto:
        """Convierte lo escrito en los campos a un Producto (valida el modelo)."""
        try:
            precio = float(campo_precio.value)
        except ValueError:
            raise ValueError("El precio debe ser un número")
        try:
            stock = int(campo_stock.value or 0)
        except ValueError:
            raise ValueError("El stock debe ser un número entero")
        return Producto(
            codigo=campo_codigo.value,
            nombre=campo_nombre.value,
            precio=precio,
            stock=stock,
        )

    def ejecutar(operacion):
        """Ejecuta una operación y muestra el error que corresponda."""
        try:
            operacion()
        except ValidationError as e:
            mostrar_mensaje(e.errors()[0]["msg"].replace("Value error, ", ""), error=True)
        except (ProductoDuplicadoError, ProductoNoEncontradoError, ValueError) as e:
            mostrar_mensaje(str(e), error=True)

    # ---------- manejadores de eventos ----------
    def agregar_producto(evento):
        def operacion():
            producto = leer_formulario()
            catalogo.agregar(producto)
            limpiar_campos()
            refrescar_lista()
            mostrar_mensaje(f"Producto {producto.codigo} agregado")
        ejecutar(operacion)

    def buscar_producto(evento):
        def operacion():
            p = catalogo.buscar(campo_codigo.value)
            campo_codigo.value = p.codigo
            campo_nombre.value = p.nombre
            campo_precio.value = str(p.precio)
            campo_stock.value = str(p.stock)
            mostrar_mensaje(f"Producto {p.codigo} encontrado")
        ejecutar(operacion)

    def actualizar_producto(evento):
        def operacion():
            producto = leer_formulario()
            catalogo.actualizar(producto)
            limpiar_campos()
            refrescar_lista()
            mostrar_mensaje(f"Producto {producto.codigo} actualizado")
        ejecutar(operacion)

    def eliminar_producto(evento):
        def operacion():
            p = catalogo.eliminar(campo_codigo.value)
            limpiar_campos()
            refrescar_lista()
            mostrar_mensaje(f"Producto {p.codigo} eliminado")
        ejecutar(operacion)

    def seleccionar_producto(evento):
        # La fuente del evento es el elemento de la lista; su data es el código
        campo_codigo.value = evento.control.data
        buscar_producto(evento)

    def limpiar(evento):
        limpiar_campos()
        mostrar_mensaje("")

    # ---------- armado de la ventana ----------
    page.add(
        ft.Text("Catálogo de productos", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([campo_codigo, campo_nombre]),
        ft.Row([campo_precio, campo_stock]),
        ft.Row(
            [
                ft.ElevatedButton(text="Agregar", icon=ft.Icons.ADD, on_click=agregar_producto),
                ft.ElevatedButton(text="Buscar", icon=ft.Icons.SEARCH, on_click=buscar_producto),
                ft.ElevatedButton(text="Actualizar", icon=ft.Icons.EDIT, on_click=actualizar_producto),
                ft.ElevatedButton(text="Eliminar", icon=ft.Icons.DELETE, on_click=eliminar_producto),
            ],
            wrap=True,
        ),
        ft.Row([mensaje, ft.TextButton(text="Limpiar", on_click=limpiar)],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        ft.Row([ft.Text("Productos", weight=ft.FontWeight.BOLD), total],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        lista_visual,
    )


if __name__ == "__main__":
    ft.app(target=main)
