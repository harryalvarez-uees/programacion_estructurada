class Prestamo:
    """Credito asociado a una cuenta."""

    def __init__(self, codigo, cuenta, monto, cuotas, tasa_anual):
        self.__codigo = str(codigo).strip().upper()
        self.__cuenta = cuenta
        self.monto = monto
        self.cuotas = cuotas
        self.tasa_anual = tasa_anual
        self.__cuotas_pagadas = 0

    # ------------------------------------------------------------------
    # Getters y setters
    # ------------------------------------------------------------------
    @property
    def codigo(self):
        return self.__codigo

    @property
    def cuenta(self):
        return self.__cuenta

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, valor):
        valor = float(valor)
        if valor <= 0:
            raise ValueError("El monto del prestamo debe ser mayor a cero")
        self.__monto = round(valor, 2)

    @property
    def cuotas(self):
        return self.__cuotas

    @cuotas.setter
    def cuotas(self, valor):
        valor = int(valor)
        if not 1 <= valor <= 60:
            raise ValueError("El numero de cuotas debe estar entre 1 y 60")
        self.__cuotas = valor

    @property
    def tasa_anual(self):
        return self.__tasa_anual

    @tasa_anual.setter
    def tasa_anual(self, valor):
        valor = float(valor)
        if not 0 < valor <= 60:
            raise ValueError("La tasa anual debe estar entre 0 y 60 %")
        self.__tasa_anual = round(valor, 2)

    @property
    def cuotas_pagadas(self):
        return self.__cuotas_pagadas

    @property
    def cuotas_pendientes(self):
        return self.__cuotas - self.__cuotas_pagadas

    # ------------------------------------------------------------------
    # Calculos
    # ------------------------------------------------------------------
    def interes_total(self):
        """Interes de todo el plazo, calculado como interes simple."""
        tasa_mensual = self.tasa_anual / 100 / 12
        return round(self.monto * tasa_mensual * self.cuotas, 2)

    def total_a_pagar(self):
        return round(self.monto + self.interes_total(), 2)

    def cuota_mensual(self):
        return round(self.total_a_pagar() / self.cuotas, 2)

    def saldo_pendiente(self):
        return round(self.cuota_mensual() * self.cuotas_pendientes, 2)

    def esta_cancelado(self):
        return self.cuotas_pendientes == 0

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def desembolsar(self):
        """Acredita el dinero del prestamo en la cuenta."""
        self.__cuenta.depositar(self.monto)
        return self.__cuenta.saldo

    def pagar_cuota(self):
        """Debita una cuota de la cuenta asociada."""
        if self.esta_cancelado():
            raise ValueError(f"El prestamo {self.__codigo} ya esta cancelado")
        cuota = self.cuota_mensual()
        self.__cuenta.retirar(cuota)
        self.__cuotas_pagadas += 1
        return cuota

    def mostrar_informacion(self):
        print(f"  Prestamo {self.__codigo} - cuenta {self.__cuenta.numero}")
        print(f"     Monto           : ${self.monto:,.2f}")
        print(f"     Tasa anual      : {self.tasa_anual} %")
        print(f"     Cuotas          : {self.cuotas} de ${self.cuota_mensual():,.2f}")
        print(f"     Total a pagar   : ${self.total_a_pagar():,.2f}")
        print(f"     Cuotas pagadas  : {self.cuotas_pagadas} de {self.cuotas}")
        print(f"     Falta por pagar : ${self.saldo_pendiente():,.2f}")

    def __str__(self):
        return (f"{self.__codigo} - cuenta {self.__cuenta.numero} - "
                f"pendiente ${self.saldo_pendiente():,.2f}")
