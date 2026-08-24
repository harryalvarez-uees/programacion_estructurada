class Cliente:
    """Titular de las cuentas y los prestamos."""

    def __init__(self, cedula, nombre, email, ingreso_mensual):
        # Se asigna con los setters para que la validacion se aplique
        # siempre, venga el dato de aqui o de un cambio posterior.
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.ingreso_mensual = ingreso_mensual
        self.__cuentas = []

    # ------------------------------------------------------------------
    # Getters y setters
    # ------------------------------------------------------------------
    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ValueError("La cedula debe tener exactamente 10 digitos numericos")
        self.__cedula = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        self.__nombre = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = str(valor).strip().lower()
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError(f"Email invalido: {valor}")
        self.__email = valor

    @property
    def ingreso_mensual(self):
        return self.__ingreso_mensual

    @ingreso_mensual.setter
    def ingreso_mensual(self, valor):
        valor = float(valor)
        if valor <= 0:
            raise ValueError("El ingreso mensual debe ser mayor a cero")
        self.__ingreso_mensual = round(valor, 2)

    @property
    def cuentas(self):
        # Se devuelve una copia para que nadie agregue cuentas por fuera
        # saltandose la validacion de agregar_cuenta().
        return tuple(self.__cuentas)

    # ------------------------------------------------------------------
    # Comportamiento
    # ------------------------------------------------------------------
    def agregar_cuenta(self, cuenta):
        """Vincula una cuenta al cliente."""
        if cuenta in self.__cuentas:
            raise ValueError("La cuenta ya esta asociada a este cliente")
        self.__cuentas.append(cuenta)
        return cuenta

    def patrimonio(self):
        """Suma de los saldos de todas sus cuentas."""
        return round(sum(c.saldo for c in self.__cuentas), 2)

    # Politicas comerciales. Cada segmento las redefine a su manera.
    @property
    def tipo_cliente(self):
        return "GENERAL"

    def limite_credito(self):
        """Cuanto puede deber como maximo este cliente."""
        return round(self.ingreso_mensual * 3, 2)

    def tasa_preferencial(self, tasa_base):
        """Tasa de interes que se le aplica a un prestamo."""
        return tasa_base

    def mostrar_informacion(self):
        print(f"  [{self.tipo_cliente}] {self.nombre} - CI {self.cedula}")
        print(f"     Email           : {self.email}")
        print(f"     Ingreso mensual : ${self.ingreso_mensual:,.2f}")
        print(f"     Cupo de credito : ${self.limite_credito():,.2f}")
        if self.cuentas:
            for cuenta in self.cuentas:
                print(f"     Cuenta {cuenta.numero} ({cuenta.tipo_cuenta}): "
                      f"${cuenta.saldo:,.2f}")
        else:
            print("     Sin cuentas abiertas")

    def __str__(self):
        return f"{self.nombre} ({self.tipo_cliente})"


class ClienteNormal(Cliente):
    """Cliente de banca masiva."""

    @property
    def tipo_cliente(self):
        return "NORMAL"

    def limite_credito(self):
        return round(self.ingreso_mensual * 5, 2)


class ClienteVIP(Cliente):
    """Cliente premium: tiene asesor asignado y mejores condiciones."""

    def __init__(self, cedula, nombre, email, ingreso_mensual, asesor):
        super().__init__(cedula, nombre, email, ingreso_mensual)
        self.asesor = asesor

    @property
    def asesor(self):
        return self.__asesor

    @asesor.setter
    def asesor(self, valor):
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ValueError("El asesor asignado debe tener un nombre valido")
        self.__asesor = valor.title()

    @property
    def tipo_cliente(self):
        return "VIP"

    def limite_credito(self):
        return round(self.ingreso_mensual * 10, 2)

    def tasa_preferencial(self, tasa_base):
        # El cliente VIP recibe dos puntos menos de tasa.
        return round(max(tasa_base - 2, 1), 2)

    def mostrar_informacion(self):
        super().mostrar_informacion()      # reutiliza lo del padre
        print(f"     Asesor asignado : {self.asesor}")
