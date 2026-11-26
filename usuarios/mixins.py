from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Usuario


class RolRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Exige sesión y uno de los roles declarados (por defecto, ninguno).

    Sin sesión redirige al login; con un rol no autorizado responde 403.
    """

    roles_permitidos = ()

    def test_func(self):
        return self.request.user.rol in self.roles_permitidos


class GerenteRequeridoMixin(RolRequeridoMixin):
    roles_permitidos = (Usuario.Rol.GERENTE,)


class PersonalRequeridoMixin(RolRequeridoMixin):
    roles_permitidos = (Usuario.Rol.GERENTE, Usuario.Rol.RECEPCIONISTA)
