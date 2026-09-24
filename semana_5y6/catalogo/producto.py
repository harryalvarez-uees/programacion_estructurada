"""
Producto del catálogo.

La validación vive en el modelo: venga el dato de la interfaz o de
cualquier otro lado, siempre pasa por las mismas reglas.
"""

from pydantic import BaseModel, field_validator


class Producto(BaseModel):
    codigo: str
    nombre: str
    precio: float
    stock: int = 0

    @field_validator("codigo")
    @classmethod
    def validar_codigo(cls, valor: str) -> str:
        valor = valor.strip().upper()
        if not valor:
            raise ValueError("El código es obligatorio")
        return valor

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        valor = valor.strip()
        if len(valor) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return valor

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor: float) -> float:
        if valor <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return round(valor, 2)

    @field_validator("stock")
    @classmethod
    def validar_stock(cls, valor: int) -> int:
        if valor < 0:
            raise ValueError("El stock no puede ser negativo")
        return valor

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} | ${self.precio:.2f} | Stock: {self.stock}"
