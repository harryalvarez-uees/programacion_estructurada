class Cuenta:
    """Cuenta bancaria generica."""

    def __init__(self, numero, titular, saldo_inicial=0.0):
        self.__numero = self.__validar_numero(numero)
        self.__titular = titular
        self.__saldo = 0.0

        if saldo_inicial and saldo_inicial > 0:
            self.depositar(saldo_inicial)

    @staticmethod
    def __validar_numero(numero):
        numero = str(numero).strip()
        if len(numero) < 4:
            raise ValueError("El numero de cuenta debe tener al menos 4 caracteres")
        return numero

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    @property
    def numero(self):
        return self.__numero

    @property
    def titular(self):
        return self.__titular

    @property
    def saldo(self):
        # A proposito no existe un setter de saldo: el dinero solo se
        # mueve con depositar() y retirar().
        return round(self.__saldo, 2)

    @property
    def saldo_disponible(self):
        """Cuanto se puede retirar. Cada tipo de cuenta lo redefine."""
        return self.saldo

    @property
    def tipo_cuenta(self):
        return "GENERICA"

    # ------------------------------------------------------------------
    # Metodos internos, disponibles para las clases derivadas
    # ------------------------------------------------------------------
    def _abonar(self, monto):
        self.__saldo += monto

    def _debitar(self, monto):
        self.__saldo -= monto

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def depositar(self, monto):
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser mayor a cero")
        self._abonar(monto)
        return self.saldo

    def retirar(self, monto):
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor a cero")
        if monto > self.saldo_disponible:
            raise ValueError(
                f"Fondos insuficientes: disponible ${self.saldo_disponible:,.2f}, "
                f"solicitado ${monto:,.2f}"
            )
        self._debitar(monto)
        return self.saldo

    def __str__(self):
        return f"{self.tipo_cuenta} {self.__numero} - ${self.saldo:,.2f}"


class CuentaAhorros(Cuenta):
    """Cuenta de ahorros: no se puede retirar mas de lo que tiene."""

    @property
    def tipo_cuenta(self):
        return "AHORROS"


class CuentaCorriente(Cuenta):
    """Cuenta corriente: permite un sobregiro de hasta 500 dolares."""

    SOBREGIRO = 500.0

    @property
    def tipo_cuenta(self):
        return "CORRIENTE"

    @property
    def saldo_disponible(self):
        # Al saldo real se le suma el cupo de sobregiro.
        return round(self.saldo + CuentaCorriente.SOBREGIRO, 2)
