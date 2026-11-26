from django.db import IntegrityError, transaction

from .models import Habitacion


class NumeroDuplicadoError(Exception):
    """Ya existe una habitación no eliminada con el mismo número (RN15)."""


def numero_en_uso(numero):
    return Habitacion.objects.filter(numero=numero, eliminada=False).exists()


def listar_habitaciones():
    return Habitacion.objects.filter(eliminada=False).order_by('numero')


def registrar_habitacion(gerente, numero, capacidad, orientacion):
    """Crea una habitación vacante a nombre del gerente que la registra."""
    if numero_en_uso(numero):
        raise NumeroDuplicadoError
    try:
        with transaction.atomic():
            return Habitacion.objects.create(
                numero=numero,
                capacidad=capacidad,
                orientacion=orientacion,
                registrada_por=gerente,
            )
    except IntegrityError as exc:
        # Otro gerente pudo registrar el mismo número después de la consulta.
        if numero_en_uso(numero):
            raise NumeroDuplicadoError from exc
        raise
