from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q


class UsuarioManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # El superusuario inicial opera como gerente del hotel.
        extra_fields.setdefault('rol', Usuario.Rol.GERENTE)
        return super().create_superuser(username, email, password, **extra_fields)


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        GERENTE = 'GERENTE', 'Gerente'
        RECEPCIONISTA = 'RECEPCIONISTA', 'Recepcionista'

    nombre = models.CharField('nombre', max_length=120)
    rol = models.CharField('rol', max_length=15, choices=Rol.choices)

    REQUIRED_FIELDS = ['nombre']

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        constraints = [
            models.CheckConstraint(
                condition=Q(rol__in=['GERENTE', 'RECEPCIONISTA']),
                name='usuario_rol_valido',
            )
        ]

    @property
    def es_gerente(self):
        return self.rol == self.Rol.GERENTE
