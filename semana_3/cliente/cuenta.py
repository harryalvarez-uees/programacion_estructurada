"""
Composición: una Cuenta TIENE un Cliente (no "es un" Cliente).

cobrar_servicio() no pregunta de qué tipo es el cliente: solo le pide
que calcule su descuento. Eso es polimorfismo (cero if/else por tipo).
"""

from pydantic import BaseModel, Field

from cliente import Cliente


class Cuenta(BaseModel):
    numero: str = Field(min_length=4)
    cliente: Cliente  # <- composición
    saldo: float = Field(default=0.0, ge=0)

    def cobrar_servicio(self, monto: float) -> float:
        """Cobra un servicio aplicando el descuento propio del cliente."""
        total = self.cliente.calcular_total(monto)
        self.saldo = round(self.saldo - total, 2)
        return total
