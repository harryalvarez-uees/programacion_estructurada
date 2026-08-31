"""
Clientes: clase abstracta + subclases concretas.

Cliente define el CONTRATO (calcularDescuento). No se puede instanciar.
Cada subclase decide CÓMO calcula su descuento -> polimorfismo.
"""

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class Cliente(BaseModel, ABC):
    """Clase abstracta: comparte estado (nombre, identificacion) y un método concreto."""

    nombre: str = Field(min_length=3)
    identificacion: str = Field(min_length=10, max_length=13)

    @abstractmethod
    def calcularDescuento(self, monto: float) -> float:
        """Cada subclase debe implementar su propia regla de descuento."""

    def calcular_descuento(self, monto: float) -> float:
        """Alias con la convención de nombres de Python."""
        return self.calcularDescuento(monto)

    # Método concreto: lo heredan todas las subclases sin reescribirlo.
    def calcular_total(self, monto: float) -> float:
        return round(monto - self.calcularDescuento(monto), 2)

    @property
    def tipo(self) -> str:
        return type(self).__name__


class ClienteMayorista(Cliente):
    """15% de descuento, y 20% en compras desde $1000."""

    porcentaje: float = Field(default=0.15, ge=0, le=1)

    def calcularDescuento(self, monto: float) -> float:
        porcentaje = 0.20 if monto >= 1000 else self.porcentaje
        return round(monto * porcentaje, 2)


class ClienteMinorista(Cliente):
    """5% de descuento, con un tope máximo de $50."""

    porcentaje: float = Field(default=0.05, ge=0, le=1)
    tope: float = Field(default=50.0, gt=0)

    def calcularDescuento(self, monto: float) -> float:
        return round(min(monto * self.porcentaje, self.tope), 2)
