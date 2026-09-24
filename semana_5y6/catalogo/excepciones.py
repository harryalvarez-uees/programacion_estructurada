"""Excepciones propias del catálogo (errores del negocio)."""


class ProductoDuplicadoError(Exception):
    """Se intenta registrar un código que ya existe."""


class ProductoNoEncontradoError(Exception):
    """Se busca, actualiza o elimina un código que no existe."""
