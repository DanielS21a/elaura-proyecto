from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Habitacion(models.Model):
    class Orientacion(models.TextChoices):
        PARQUE = 'PARQUE', 'Parque'
        PISCINA = 'PISCINA', 'Piscina'
        MAR = 'MAR', 'Mar'
        CERRO = 'CERRO', 'Cerro'

    class Disponibilidad(models.TextChoices):
        VACANTE = 'VACANTE', 'Vacante'
        OCUPADA = 'OCUPADA', 'Ocupada'

    numero = models.PositiveIntegerField('número', validators=[MinValueValidator(1)])
    capacidad = models.PositiveSmallIntegerField(
        'capacidad', validators=[MinValueValidator(1)]
    )
    orientacion = models.CharField('orientación', max_length=10, choices=Orientacion.choices)
    estado = models.CharField(
        'estado',
        max_length=10,
        choices=Disponibilidad.choices,
        default=Disponibilidad.VACANTE,
    )
    eliminada = models.BooleanField('eliminada', default=False)
    registrada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='habitaciones_registradas',
        verbose_name='registrada por',
    )

    class Meta:
        verbose_name = 'habitación'
        verbose_name_plural = 'habitaciones'
        constraints = [
            models.UniqueConstraint(
                fields=['numero'],
                condition=Q(eliminada=False),
                name='uq_habitacion_numero_activa',
            ),
            models.CheckConstraint(
                condition=Q(capacidad__gte=1), name='habitacion_capacidad_min'
            ),
        ]
        indexes = [models.Index(fields=['estado', 'capacidad'])]

    def __str__(self):
        return f'Habitación {self.numero}'

    def esta_vacante(self):
        return self.estado == self.Disponibilidad.VACANTE
