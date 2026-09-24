"""
Catálogo de productos.

Cada colección tiene un propósito:
- list  -> guarda los productos en el orden en que se registran.
- dict  -> busca un producto por su código sin recorrer la lista.
- set   -> guarda los códigos usados para no permitir duplicados.
"""

from excepciones import ProductoDuplicadoError, ProductoNoEncontradoError
from producto import Producto


class Catalogo:
    def __init__(self):
        self.productos: list[Producto] = []
        self.indice: dict[str, Producto] = {}
        self.codigos: set[str] = set()

    def agregar(self, producto: Producto) -> None:
        if producto.codigo in self.codigos:
            raise ProductoDuplicadoError(f"Ya existe un producto con código {producto.codigo}")
        self.productos.append(producto)
        self.indice[producto.codigo] = producto
        self.codigos.add(producto.codigo)

    def buscar(self, codigo: str) -> Producto:
        producto = self.indice.get(codigo.strip().upper())
        if producto is None:
            raise ProductoNoEncontradoError(f"No existe el producto {codigo}")
        return producto

    def listar(self) -> list[Producto]:
        return list(self.productos)

    def actualizar(self, nuevo: Producto) -> None:
        anterior = self.buscar(nuevo.codigo)
        posicion = self.productos.index(anterior)
        self.productos[posicion] = nuevo
        self.indice[nuevo.codigo] = nuevo

    def eliminar(self, codigo: str) -> Producto:
        producto = self.buscar(codigo)
        self.productos.remove(producto)
        del self.indice[producto.codigo]
        self.codigos.discard(producto.codigo)
        return producto

    def __len__(self) -> int:
        return len(self.productos)
