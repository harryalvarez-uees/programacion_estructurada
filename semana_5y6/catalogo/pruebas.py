"""Prueba rápida del catálogo por consola (sin interfaz gráfica)."""

from pydantic import ValidationError

from catalogo import Catalogo
from excepciones import ProductoDuplicadoError, ProductoNoEncontradoError
from producto import Producto

catalogo = Catalogo()

# Agregar
catalogo.agregar(Producto(codigo="P001", nombre="Mouse inalámbrico", precio=15.5, stock=10))
catalogo.agregar(Producto(codigo="P002", nombre="Teclado mecánico", precio=45, stock=5))
catalogo.agregar(Producto(codigo="P003", nombre="Monitor 24 pulgadas", precio=180, stock=2))
print("Productos registrados:")
for p in catalogo.listar():
    print(" ", p)

# Buscar
print("\nBuscar P002:", catalogo.buscar("p002"))

# Actualizar
catalogo.actualizar(Producto(codigo="P002", nombre="Teclado mecánico RGB", precio=49.9, stock=8))
print("Actualizado:", catalogo.buscar("P002"))

# Eliminar
catalogo.eliminar("P001")
print("Eliminado P001. Quedan", len(catalogo), "productos")

# Casos de error
print("\nCasos de error:")
try:
    catalogo.agregar(Producto(codigo="P002", nombre="Otro teclado", precio=20))
except ProductoDuplicadoError as e:
    print("  Duplicado:", e)

try:
    catalogo.buscar("P999")
except ProductoNoEncontradoError as e:
    print("  No encontrado:", e)

try:
    Producto(codigo="P010", nombre="Silla", precio=-5)
except ValidationError as e:
    print("  Dato inválido:", e.errors()[0]["msg"].replace("Value error, ", ""))
