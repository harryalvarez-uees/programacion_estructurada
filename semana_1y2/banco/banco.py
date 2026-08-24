TASA_BASE = 16.0   # tasa anual de referencia para los prestamos


class Banco:
    """Entidad que agrupa clientes, cuentas y prestamos."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.__clientes = []
        self.__cuentas = []
        self.__prestamos = []

    # ------------------------------------------------------------------
    # Getters y setters
    # ------------------------------------------------------------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ValueError("El nombre del banco debe tener al menos 3 caracteres")
        self.__nombre = valor

    @property
    def clientes(self):
        return tuple(self.__clientes)

    @property
    def cuentas(self):
        return tuple(self.__cuentas)

    @property
    def prestamos(self):
        return tuple(self.__prestamos)

    # ------------------------------------------------------------------
    # Busquedas
    # ------------------------------------------------------------------
    def buscar_cliente(self, cedula):
        for cliente in self.__clientes:
            if cliente.cedula == str(cedula).strip():
                return cliente
        return None

    def buscar_cuenta(self, numero):
        for cuenta in self.__cuentas:
            if cuenta.numero == str(numero).strip():
                return cuenta
        return None

    def buscar_prestamo(self, codigo):
        for prestamo in self.__prestamos:
            if prestamo.codigo == str(codigo).strip().upper():
                return prestamo
        return None

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def registrar_cliente(self, cliente):
        if self.buscar_cliente(cliente.cedula) is not None:
            raise ValueError(f"El cliente {cliente.cedula} ya esta registrado")
        self.__clientes.append(cliente)
        return cliente

    def abrir_cuenta(self, cuenta):
        """Registra la cuenta y la vincula con su titular."""
        if self.buscar_cuenta(cuenta.numero) is not None:
            raise ValueError(f"El numero de cuenta {cuenta.numero} ya existe")
        cuenta.titular.agregar_cuenta(cuenta)
        self.__cuentas.append(cuenta)
        return cuenta

    def deuda_de(self, cliente):
        """Total que el cliente aun debe al banco."""
        return round(sum(
            p.saldo_pendiente() for p in self.__prestamos
            if p.cuenta.titular is cliente
        ), 2)

    def generar_codigo_prestamo(self):
        return f"P-{len(self.__prestamos) + 1:03d}"

    def otorgar_prestamo(self, cuenta, monto, cuotas):
        """Aprueba el credito si el cliente tiene cupo, y lo desembolsa.

        La tasa la define el propio cliente segun su segmento.
        """
        from banco.prestamo import Prestamo

        titular = cuenta.titular
        monto = float(monto)
        deuda = self.deuda_de(titular)
        if deuda + monto > titular.limite_credito():
            raise ValueError(
                f"Prestamo rechazado: excede el cupo de {titular.nombre} "
                f"(cupo ${titular.limite_credito():,.2f}, "
                f"deuda actual ${deuda:,.2f})"
            )

        tasa = titular.tasa_preferencial(TASA_BASE)
        prestamo = Prestamo(self.generar_codigo_prestamo(), cuenta, monto, cuotas, tasa)
        self.__prestamos.append(prestamo)
        prestamo.desembolsar()
        return prestamo

    def total_depositos(self):
        return round(sum(c.saldo for c in self.__cuentas), 2)

    def total_prestado(self):
        return round(sum(p.saldo_pendiente() for p in self.__prestamos), 2)

    def resumen(self):
        print(f"  Banco                : {self.nombre}")
        print(f"  Clientes registrados : {len(self.__clientes)}")
        print(f"  Cuentas abiertas     : {len(self.__cuentas)}")
        print(f"  Prestamos otorgados  : {len(self.__prestamos)}")
        print(f"  Total en depositos   : ${self.total_depositos():,.2f}")
        print(f"  Por cobrar (creditos): ${self.total_prestado():,.2f}")
